import os
import json
import getpass
import hashlib
from cryptography.fernet import Fernet
from securedrop import SecureDrop

def login(toParse):
	email = input('Enter e-mail address: ').lower()

	print('Enter password: ')
	password = getpass.getpass()

	# Password Salting: Adding salt to the password before hashing password using SHA-256
	salt = "somesalt"
	salted_password = password+salt

	# Decrypting password
	decrypted_password = ""
	for user in toParse:
		if user['email'] == email:
			filename = os.path.join(os.getcwd(), "users", email, "key.bin")
			decrypted_password = SecureDrop.decrypt_text(filename, user['password'])

	while decrypted_password != salted_password:
		print('Email and password combinations invalid! Re-enter password.')
		# print(f"decrypted_password {decrypted_password}, salted_password {salted_password}")
		email = input('Enter e-mail address: ').lower()
		print('Enter password: ')
		password = getpass.getpass()
		salted_password = password+salt
	return email

def register():
	name = input('Enter full name: ').title()
	email = input('Enter e-mail address: ').lower()
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

	# Password Salting: Adding salt to the password before hashing password using SHA-256
	salt = "somesalt"

	filename = os.path.join(os.getcwd(), "users")

	os.makedirs(filename, exist_ok=True)

	filename = os.path.join(filename, email)
	os.makedirs(filename, exist_ok=True)
	filename = os.path.join(filename, "key.bin")
	SecureDrop.generate_key(filename)

	# Encrypting password
	encrypted_password = SecureDrop.encrypt_text(password+salt, filename)

	#build user object to be sent to json file
	user = {
		'name': name,
		'email': email,
		'password': encrypted_password
	}

	filename = os.path.join(os.getcwd(), "users", "users.json")
	try:
		with open(filename, 'r') as file:
			data = json.load(file)
	except FileNotFoundError or ValueError:
		data = []

	users_data = [user]
	data.extend(users_data)
	updated_data = json.dumps(data, indent=2)
	with open(filename, 'w') as file:
		file.write(updated_data)
		#send object to json, write to file