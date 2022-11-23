---Database

shadow.db  
	-> tables
		-> users
			-> each record contain name and password for login.
			-> tableschema: name|password
account.db  
	-> tables
		-> account
			-> for saving accounts and their passwords from users who are login.
			-> tableschema: name|account|password
