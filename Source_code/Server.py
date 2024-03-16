"""
Import pickle, socket and cryptography.fernet.
"""
import pickle
import socket
from cryptography.fernet import Fernet


class Server:
    """
    This class represents a server that can receive data from the client.
    """
    def __init__(self, filename, dictionary_name):
        port = 60000                            # Reserve a port for your service
        self.conn = False                       
        self.s = socket.socket()                # Create a socket object
        host = socket.gethostname()             # Get local machine name
        self.s.bind((host, port))               # Bind to the port
        self.s.listen(5)                        # Now wait for client connection
        self.filename = filename
        self.dictionary_name = dictionary_name

        print ('Server listening....')

    def decDictionary(self, enc_dictionary, fernet):
        """
        Decode the encrypted dictionary that the server receives.
        """
        decDictionary = {}
        for key, value in enc_dictionary.items():
            dec_key = fernet.decrypt(key).decode()
            dec_value = fernet.decrypt(value).decode()
            decDictionary[dec_key] = dec_value

        return decDictionary

    def printDictionary(self, dec_dictionary):
        """
        Print the received dictionary.
        """
        print("Received dictionary content: ")
        for key, value in dec_dictionary.items():
            print("key: " , key, " " , "value: ", value)

    def writeDictionaryToFile(self, dec_dictionary):
        """
        Write the dictionary into a file.
        """
        write_file = open(self.dictionary_name, 'w', encoding="utf-8")
        count = 0

        for key, value in dec_dictionary.items():
            count +=1
            if count < len(dec_dictionary):
                write_file.write(f"{key}: {value}, ")
            else:
                write_file.write(f"{key}: {value}")
        write_file.close()

    def writeMsgToFile(self, dec_message):
        """
        Write the received file content to a file.
        """
        write_file =  open(self.filename, 'w', encoding="utf-8")
        write_file.write(dec_message)
        write_file.close()

    def receiveData(self):
        """
        Establish connection and receive data from the client. 
        """
        listening = True
        while listening:
            self.conn, addr = self.s.accept()
            print('Got connection from', addr)
            data = self.conn.recv(4096)
           
            if not data:
                listening = False
            else:
                # Deserialise data
                data = pickle.loads(data)
                key = data['key']
                message = data['message']
                write_file = data['write_file']
                print_message = data['print_message']
                encryption = data['encryption']
                dictionary_format = data['dictionary_format']
                # Initialise fernet object with encryption 
                fernet = Fernet(key)

                if dictionary_format == True:                               # If data is in dictionary format
                    received_dictionary = message

                    if encryption == True:
                        print("Coded Dictionary:" , received_dictionary)
                        received_dictionary = self.decDictionary(received_dictionary, fernet)    # Decoding dictionary

                    if print_message == True:
                        self.printDictionary(received_dictionary)            # Print dictionary
 
                    if write_file == True :
                        self.writeDictionaryToFile(received_dictionary)      # Write dictionary content in a file

                else:  # If the received data is not in dictionary format
                    if encryption == True:                                   # Decrypt file content
                        print("Coded message: ", message)
                        message = fernet.decrypt(message).decode()
                        print("Decoded message: ", message)
 
                    if print_message == True:                                # Print file content
                        print("Message: ",  message)

                    if write_file == True:                                   # Write file content in a file
                        self.writeMsgToFile(message)

                print('Successfully received') 


    def closeConnection(self):
        """
        Close connection.
        """
        print ("Connection closed.")
        self.conn.close()



if __name__ == "__main__":
    # Initialise the server  and defiine the files where we write the received data
    server = Server('received_file.txt', 'received_dict.txt')  
    server.receiveData()                                     # Start listening for client connection and receiving data                                                 
    server.closeConnection()                                 # Close connection
