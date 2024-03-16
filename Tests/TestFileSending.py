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
        self.sent_filename = "employee_dataset.txt"
        self.received_filename = "received_file.txt"
        self.sent_file_content = ''


    def test_FileSending(self):
        """
        Test if the server writes the sent data in a file
        """         
        encryption = False 
        self.sent_file_content = self.client.readFile(self.sent_filename,encryption)
        
        if self.sent_file_content != False:  # file exists
            write_file = True
            print_message = False
            dictionary_format = False
            self.client.sendData(self.sent_file_content, write_file, print_message, dictionary_format, encryption)

            time.sleep(2.0)
            self.assertTrue(os.path.exists(self.received_filename))


    def test_FileContent(self):
        """
        Test if the data sent by the client is identical with the data written in the file by the server
        """
        received_file_content = ''

        time.sleep(2.0)
        try:
            with open(self.received_filename, 'r', encoding="utf-8") as file:
                received_file_content = file.read()
            file.close()
   
        except FileNotFoundError:
            print(f"Error found in the comparison of the file contents.")
        

        if self.sent_file_content != '' and  received_file_content != '':
            self.assertEqual(self.sent_file_content, received_file_content)

    
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestDataTransfer('test_FileSending'))       # Add test case for file sending
    suite.addTest(TestDataTransfer('test_FileContent'))       # Add test case for file content
    result = unittest.TestResult()                            # Create a test result object
    suite.run(result)                                         # Run the test suite

    # Print the test results
    print("Number of tests run:", result.testsRun)
    print("Number of failures:", len(result.failures))
    print("Number of errors:", len(result.errors))