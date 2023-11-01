import os
import json

#specify path to user information
path = '/home/student/milestone1/users.txt'

#Check if the path exists
isExist = os.path.exists(path)

#Open file and check if any users registered
if isExist == True:
	o = open('users.txt', "r")
	toParse = o.read()

	#if file only has 2 charcters it is 'empty' just a placeholder
	if len(toParse) == 2:
		print('No users are registered with this client.'
		      'Do you want to register a new user (y/n)?')
		s = input(' ')

#if do not want to register a user, quit
		if s == 'n':
			quit()

		#elif want to register a user, prompt the different info and take in user input
		elif s == 'y':
			print('Enter full name: ')
			name = input(' ')
			print('Enter e-mail address: ')
			email = input(' ')
			print('Enter password: ')
			password = input(' ')
			print('Re-enter password: ')
			repassword = input(' ')

			#check to see if password and password re-entry match
			if password == repassword:
				print('Passwords match.')

			#build user object to be sent to json file
			user = {
				'name': name,
				'email': email,
				'password': password
			}

			#send object to json, write to file
			info = json.dumps(user)
			f = open('users.txt', "w")
			f.write(info)
			f.close
		#end elif
