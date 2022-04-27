#/usr/bin/python3
# import all the modules

from importlib.metadata import files
import time
from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join


# define the class
class AESCipher:
    def __init__(self, key): # used to encrypt and decrypt the data
        self.key = key
    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size) # pad the data

    def encrypt(self, message, key, key_size = 256): # a function to encrypt the data
        message = self.pad(message)  # pad the data
        iv = Random.new().read(AES.block_size) # generate a random iv
        cipher = AES.new(key, AES.MODE_CBC, iv) # encrypt the data
        return iv + cipher.encrypt(message) # return the encrypted data

    # function that opens the file and reads the data of the file, then encrypts the data
    # and creates a new file with the encrypted data with an extension of .enc and deletes the original file
    def encrypt_file(self, file_name): 
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    # function that opens the file and reads the data of the file, then decrypts the data
    # and creates a new file with the decrypted data with an extension of .dec and deletes the original file
    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4],'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    # function getAllFiles that returns a list of all the files in the current directory
    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'cipher.py' and fname != 'data.txt.enc'):
                    files.append(dirName + "\\" + fname)
        return files
    
    def encryptAllFiles(self):
        files = self.getAllFiles()
        for file in files:
            self.encrypt_file(file)
    
    def decryptAllFiles(self):
        files = self.getAllFiles()
        for file in files:
            self.decrypt_file(file)

key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = AESCipher(key)
clear = lambda: os.system('cls')



if os.path.isfile('data.txt.enc'):
    while True:
        password = str(input("Enter password: "))
        enc.decrypt_file("data.txt.enc")
        p = ''
        with open("data.txt", "r") as f:
            p = f.readlines()
        if p[0] == password:
            enc.encrypt_file("data.txt")
            break

    while True:
        clear()
        choice = int(input(
            "1. Press '1' to encrypt file.\n2. Press '2' to decrypt file.\n3. Press '3' to Encrypt all files in the directory.\n4. Press '4' to decrypt all files in the directory.\n5. Press '5' to exit.\n"))
        clear()
        if choice == 1:
            enc.encrypt_file(str(input("Enter name of file to encrypt: ")))
        elif choice == 2:
            enc.decrypt_file(str(input("Enter name of file to decrypt: ")))
        elif choice == 3:
            enc.encrypt_all_files()
        elif choice == 4:
            enc.decrypt_all_files()
        elif choice == 5:
            exit()
        else:
            print("Please select a valid option!")

else:
    while True:
        clear()
        password = str(input("Setting up stuff. Enter a password that will be used for decryption: "))
        repassword = str(input("Confirm password: "))
        if password == repassword:
            break
        else:
            print("Passwords Mismatched!")
    f = open("data.txt", "w+")
    f.write(password)
    f.close()
    enc.encrypt_file("data.txt")
    print("Please restart the program to complete the setup")
    time.sleep(15)





    
            

    
