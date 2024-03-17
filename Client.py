"""
Import pickle, socket and cryptography.fernet.
"""
import pickle
import socket
from cryptography.fernet import Fernet

class Client:
    """
    This class represents a client that can connect to the server
    and transfer dictionary and file to the server.
    """
    def __init__(self):
        self.s = socket.socket()                  # Create a socket object
        self.host = socket.gethostname()          # Get local machine nam
        self.port = 60000                         # Reserve a port for your service
        self.connected = False                    # Connection to the server
        try:
            # Connect to the server
            self.s.connect((self.host, self.port))  
            self.connected = True
        except ConnectionRefusedError:            # If client unable to connect to the server
            print('Connection failed. Please make sure there is a server / running on Port: %d' % (self.port))

        # Generate enryption key and create fernet object
        self.key = Fernet.generate_key()  
        self.fernet = Fernet(self.key)


    def readFile(self, filename, encryption):
        """
        Open and read the file.
        """
        try:
            f = open(filename, "r", encoding="utf-8")
            file_content = f.read()
            f.close()

            if encryption == True:     
                enc_message = self.fernet.encrypt(file_content.encode())   # Enrypt file content
                return enc_message
            return file_content
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except IOError:
            print("Error: An IOError occurred while performing file operation.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return False

    def createDictionary(self,encryption):
        """
        Create a dictionary for sending.
        """
        employee = {'id':1, 'Name' :'John Smith', 'Age':35, 'Gender' :'male','designation' :'Software Developer','department' :'IT'}
        if encryption == True:
            enc_employee = {}
            # Encrypt each key : value pair in the dictionary
            for key, value in employee.items():
                value = str(value)
                enc_key = self.fernet.encrypt(key.encode())
                enc_value = self.fernet.encrypt(value.encode())
                enc_employee[enc_key] = enc_value

            return enc_employee

        return employee
    
    def sendData(self, message, write_file, print_message, dictionary_format, encryption):
        """
        Create a dictionary with the configuration.
        """
        client_message = {
            'key' : self.key,                               # Encryption key  
            'message' : message,                            # Sending message (file content / dictionary)
            'write_file' : write_file,                      # Either write in a file
            'print_message' : print_message,                # Or print on the screen                    
            'encryption' : encryption,                      # Is the message enrypted ot not
            'dictionary_format' : dictionary_format         # Is the data in dictionary format or not
        }

        serialised_data = pickle.dumps(client_message)      # Serialise data
        self.s.sendall(serialised_data)                     # Send data to the server
        print('Done sending')

    def chooseDataType(self):
        """
        The user can choose which data type to send (dictionary or file)
        """
        dictionary_format = None

        while dictionary_format == None:
            data_type = input("1.) Do you send a dictionary (command 1) or a text file (command 2): ")
            if data_type == '1':  # DICTIONARY ENTRY
                dictionary_format = True
            elif data_type == '2':
                dictionary_format = False
            else:
                print("Wrong command")

        return dictionary_format

    def chooseOutputFormat(self):
        """
        The user can choose whether the server should write the content in a file.
        """
        write_file = None
        while write_file == None:
            write_file_answ = input("2.) Do you want to write the content to a file (True / False): ")

            if write_file_answ == 'True':
                write_file = True
            elif write_file_answ == 'False':
                write_file = False
            else:
                print("Wrong answer")

        return write_file
 
    def printMessage(self):
        """
        The user can choose whether the server should print the content to the screen.
        """
        print_message = None
        # Ask the user to input correct instruction
        while print_message == None:
            print_message_answ = input("3.) Do you want to print the content on the screen (True / False): ")
            if print_message_answ == 'True':
                print_message = True
            elif print_message_answ == 'False':
                print_message = False
            else:
                print("Wrong answer")
        return print_message
    
    def printSelectedOptions(self,write_file, print_message):
        """
        Print the options that the user selected.
        """
        if write_file == True and print_message == True:
            print("The content is written in a file and printed on the screen....")
        elif write_file == True and print_message == False:
            print("The content is written in a file....")
        elif write_file == False and print_message == True:
            print("The content is printed on the screen....")
      

    def chooseEncryption(self):
        """
        The user can choose to send encrypted content. 
        """
        select_enc = None
        while select_enc == None:
            select_enc_answ = input("4.) Do you want to encrypt the content (True / False): ")
            if select_enc_answ == 'True':
                select_enc = True
            elif select_enc_answ == 'False':
                select_enc = False
            else:
                print("Wrong answer")
        return select_enc

    def closeConnection(self):
        """
        Close connection.
        """
        self.s.close()
        print('Connection closed')


if __name__ == "__main__":
    file_content = False
    write_file = False
    print_message = False
    client = Client()                                        # Initialise the client object
    if client.connected == True:                             # Connection established
        
        dictionary_format = client.chooseDataType()          # Dictionary or text file

        while (write_file == False and print_message == False):
            write_file = client.chooseOutputFormat()         # Write in a file
            print_message = client.printMessage()            # Print on the screen

            if write_file == False and print_message == False:
                print("Please select at least one output option (write file or print message)....")
            
        select_enc = client.chooseEncryption()               # Encryption


        if dictionary_format == True:                        # Dictionary format will be sent
            print("Sending dictionary to server....")
            sending_dictionary = client.createDictionary(select_enc)
            client.sendData(sending_dictionary, write_file, print_message, dictionary_format, select_enc)
            client.printSelectedOptions(write_file, print_message)


        elif dictionary_format == False:                     # File will be sent
            filename = input("Please enter the filename: ")
            file_content = client.readFile(filename,select_enc)
        
            if file_content != False:                        # File exists
                client.sendData(file_content, write_file, print_message, dictionary_format, select_enc)
                client.printSelectedOptions(write_file, print_message)

        client.closeConnection()
