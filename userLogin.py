import os
import json
import getpass
import hashlib 
from cryptography.fernet import Fernet

def login():
	print('Enter e-mail address: ')
	email = input(' ')
	print('Enter password: ')
	password = getpass.getpass()

        # Password Salting: Adding salt to the password
	with open("salt.txt", "r") as salt_file:
		salt = salt_file.read()
	#password + salt for added security
	salted_password = password + salt 
 	
	#reading the key from the key file
	with open("password_key.bin", "rb") as key_file:
		key = key_file.read()
	#reading the encrypted password from password file
	with open("password_file.bin", "rb") as password_to_match:
		pass_match = password_to_match.read()
	
	#generating the key using the key read in
	cipher_suite = Fernet(key)
        # Decrypting password 
	decrypted_password = cipher_suite.decrypt(pass_match).decode() 
	
	#checking if the decrypted password matches the password input with salt
	#if they do not match keeping doing it an checking
	while decrypted_password != salted_password:
		print('Email and password combinations invalid! Re-enter password.')
		print('Enter e-mail address: ')
		email = input(' ')
		print('Enter password: ')
		password = getpass.getpass()
		with open("salt.txt", "r") as salt_file:
			salt = salt_file.read()
		salted_password = password + salt

		with open("password_key.bin", "rb") as key_file:
			key = key_file.read()
		with open("password_file.bin", "rb") as password_to_match:
			pass_match = password_to_match.read()

		cipher_suite = Fernet(key)
        	# Decrypting password
		decrypted_password = cipher_suite.decrypt(pass_match).decode()

	print('Welcome to SecureDrop.')
	print('Type "help" For Commands.')
	request = input(' ')
	while(request != 'exit'):
		request = input(' secure_drop> ')
		if request == 'help':
			print('"add" -> Add a new contact')
			print('"list" -> List all online contacts')
			print('"send" -> Transfer file to contact')
			print('"exit" -> Exit SecureDrop')
		elif request == 'add':
			print('Enter full name: ')
			name = input(' ')
			print('Enter e-mail address: ')
			email = input(' ')
                        #build user object to be sent to json file
			contact = {
				'name': name,
				'email': email
			}
                
                        #send object to json, write to file
			info = json.dumps(contact)
			f = open('contacts.txt', "w")
			f.write(info)
			f.close
		elif request == 'list':
			print('will implement next')
		elif request == 'send':
			print('will implement after list')
	return

def register():
	print('Enter full name: ')
	name = input(' ')
	print('Enter e-mail address: ')
	email = input(' ')
	print('Enter password: ')
	password = getpass.getpass()
	print('Re-enter password: ')
	repassword = getpass.getpass()

	while password != repassword:
		print('Passwords do not match. Re-enter password.')
		print('Enter password: ')
		password = getpass.getpass()
		print('Re-enter password')
		repassword = getpass.getpass()


        #check to see if password and password re-entry match
	if password == repassword:
		print('Passwords match.')
		print('User registered.')
		print('Exiting SecureDrop.')

        # Password Salting: Adding salt to the password before hashing password using SHA-256
	salt = "somesalt"

	with open("salt.txt", "w") as salt_file:
		salt_file.write(salt)
 
	salted_password = hashlib.sha256((password + salt).encode()).hexdigest() 

        # Password Encryption: Encrypting and decrypting password using Fernet symmetric encryption 
	key = Fernet.generate_key()
	
	with open("password_key.key", "wb") as key_file:
		key_file.write(key)
 
	cipher_suite = Fernet(key) 

        # Encrypting password 
	encrypted_password = cipher_suite.encrypt(salted_password.encode()).decode()

        #build user object to be sent to json file
	user = {
		'name': name,
		'email': email,
		'password': encrypted_password
	}

        #send object to json, write to file
	info = json.dumps(user)
	f = open('users.txt', "w")
	f.write(info)
	f.close
	return

#specify path to user information
path = '/home/student/milestone1/users.json'

#Check if the path exists
isExist = os.path.exists(path)

#Open file and check if any users registered
if isExist == True:
        o = open('users.json', "r")
        toParse = o.read()

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
                        register()
                #end elif
        login()
