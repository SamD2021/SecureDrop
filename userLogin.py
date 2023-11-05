import os
import json
import getpass
import hashlib 
from cryptography.fernet import Fernet

#specify path to user information
path = '/home/student/milestone1/users.txt'

#Check if the path exists
isExist = os.path.exists(path)

#Open file and check if any users registered
if isExist == True:
	o = open('users.txt', "r")
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
		end elif
	login()

def login():
	print('Enter e-mail address: ')
	email = input(' ')
	print('Enter password: ')
	password = getpass.getpass()

	# Password Salting: Adding salt to the password before hashing password using SHA-256
	salt = "somesalt" 
	salted_password = hashlib.sha256((password + salt).encode()).hexdigest() 
 
	# Decrypting password 
	decrypted_password = cipher_suite.decrypt(toParse[password].encode()).decode() 

	while decrypted_password != salted_password:
		print('Email and password combinations invalid! Re-enter password.')
		print('Enter e-mail address: ')
		email = input(' ')
		print('Enter password: ')
		password = getpass.getpass()

		# Password Salting: Adding salt to the password before hashing password using SHA-256
		salt = "somesalt" 
		salted_password = hashlib.sha256((password + salt).encode()).hexdigest()

	print('Welcome to SecureDrop.')
	print('Type "help" For Commands.')
	while(request != 'exit'):
		request = input(' secure_drop> ')
		if request == 'help':
			print('"add" -> Add a new contact')
			print("list" -> List all online contacts)
			print("send" -> Transfer file to contact)
			print("exit" -> Exit SecureDrop)
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
	salted_password = hashlib.sha256((password + salt).encode()).hexdigest() 

	# Password Encryption: Encrypting and decrypting password using Fernet symmetric encryption 
	key = Fernet.generate_key() 
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

