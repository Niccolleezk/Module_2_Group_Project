"""
Import unittest, os, time and Client.
"""
import unittest
import os
import time
from Client import Client

class TestDataTransfer(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.received_dict_name = "received_dict.txt"
        self.sending_dictionary = ''
      

    def test_DictionarySending(self):
        """
        Test if the server writes the sent data in a file.
        """ 
        encryption = False
        write_file = True
        print_message = True
        dictionary_format = True
        self.sending_dictionary = self.client.createDictionary(encryption)
        self.client.sendData(self.sending_dictionary, write_file, print_message, dictionary_format, encryption)

        time.sleep(2.0)
        self.assertTrue(os.path.exists(self.received_dict_name))
    
    def test_DictFileContent(self):
        """
        Test if the data sent by the client is identical
        with the data written in the file by the server.
        """
        received_dict_content = ''

        time.sleep(2.0)
        try:
            with open(self.received_dict_name, 'r', encoding="utf-8") as file:
                received_dict_content = file.read()
            file.close()

        except FileNotFoundError:
            print(f"Error found in the comparison of the file contents.")


        if self.sending_dictionary != '' and  received_dict_content != '':
            self.assertEqual(self.sending_dictionary, received_dict_content)
        

    
if __name__ == '__main__':
    """
    Create a test suite. 
    """
    suite = unittest.TestSuite()    
    suite.addTest(TestDataTransfer('test_DictionarySending'))  # Add test case for dictionary sending
    suite.addTest(TestDataTransfer('test_DictFileContent'))    # Add test case for dictionary file content
    result = unittest.TestResult()                             # Create a test result object
    suite.run(result)                                          # Run the test suite

    # Print the test results
    print("Number of tests run:", result.testsRun)
    print("Number of failures:", len(result.failures))
    print("Number of errors:", len(result.errors))
   
