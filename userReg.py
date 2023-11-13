import os
import json
import getpass
import hashlib 
from cryptography.fernet import Fernet
from registration import getInfo

#specify path to user information
path = '/home/student/milestone1/users.json'

#Check if the path exists
isExist = os.path.exists(path)

#Open file and check if any users registered
if isExist == True:
	o = open('users.json', "r")
	toParse = o.read()
	o.close
	#if file only has 2 charcters it is 'empty' just a placeholder
	if len(toParse) <= 2:
		print('No users are registered with this client.'
		      'Do you want to register a new user (y/n)?')
		s = input(' ')

#if do not want to register a user, quit
		if s == 'n':
			quit()

		#elif want to register a user, prompt the different info and take in user input
		elif s == 'y':
			#print('Enter full name: ')
			#name = input(' ')
			#print('Enter e-mail address: ')
			#email = input(' ')
			#print('Enter password: ')
			#password = getpass.getpass()
			#print('Re-enter password: ')
			#repassword = getpass.getpass()

			#while password != repassword:
				#print('Passwords do not match. Re-enter password.')
				#print('Enter password: ')
				#password = getpass.getpass()
				#print('Re-enter password')
				#repassword = getpass.getpass()
			name, email, password = getInfo()			

			# Password Salting: Adding salt to the password for added security
			salt = "somesalt"
			#writing out the salt to a file for later use
			with open("salt.txt", "w") as salt_file:
				salt_file.write(salt)
 			#passowrd plus the salt for the password
			salted_password = password + salt 

			# Password Encryption: Encrypting and decrypting password using Fernet symmetric encryption 
			key = Fernet.generate_key()
			#write the password out to a bin file
			with open("password_key.bin", "wb") as key_file:
				key_file.write(key)
			#create a key
			cipher_suite = Fernet(key) 

			# Encrypting password 
			encrypted_password = cipher_suite.encrypt(salted_password.encode())
			#writing the password out to a file that is encrypted for later comparison
			with open("password_file.bin", "wb") as password_file:
				password_file.write(encrypted_password)

			#build user object to be sent to json file
			user = {
				'name': name,
				'email': email,
				'password': encrypted_password.decode()
			}

			#send object to json, write to file
			info = json.dumps(user)
			f = open('users.json', "w")
			f.write(info)
			f.close
		#end elif
