# Module_2_Group_Project

This repository contains the requirements for the group project in the CSCK541 Software Development in Practice January 2024 A.
This project was prepared by group D (Tsz Fung Cheung, Zhi Kang Niccol Lee, Zsuzsanna Sándor and Shorouq Telfah). Python programming language was used to implement a simple client-server network that can receive a dictionary and a text file from the user, this architecture will help to share resources, data and services across a network. 

 All codes were conducted based on PEP-8 standards to improve the reliability and readability of the code. 
 The directory tree will provide the map for the repository.
 
•	Installation to use this project, you must install Python on your system. Clone the repository to your local machine:
-	git clone https://github.com/Niccolleezk/Module_2_Group_Project.git

• Ensure that the necessary packages in requirements.txt are installed.

General rules for running the codes:

- Always run the server code first before running any of the other codes and wait until it establishes the connection (server starts listening...).
- Always run the other codes (client and any of the unit tests) in dedicated terminal.
- Input requested data when the code requests the user to do so (e.g., Client will request to populate dictionary and select configuration options; TestDictionary and TestEncDictionary will request to populate dictionary before the unit test can be performed).

The following documents have been placed under the project:

1. Server code
2. Client code
3. TestDictionary (unit test) - These unit tests control whether the server successfully writes the received dictionary in a file (test_DictionarySending), and the content is identical with the sent data (test_DictFileContent).
4. TestEncDictionary(unit test) - This will perform tests similar to TestDictionary for dictionary data sent with encryption.
5. TestFileSending (unit test) - Unit tests written to confirm if the the server successfully writes the received string in a file (test_FileSending), and the content is identical with the sent data (test_FileContent).
6. TestEncFileSending (unit test) - Similar tests to TestFileSending for string sent with encryption.
7. Employee_dataset.txt - This text file with string will be sent by the client. Can be replaced with any other text file.
