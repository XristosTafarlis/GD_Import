import info
import oracledb
from pathlib import Path

home = str(Path.home())
oracledb.init_oracle_client(home + "\\instantclient")

def check_status_in_db(msisdn):
# Function to check MSISDN status
	try:
		# Use "with" to ensure the connection is closed after the block
		with oracledb.connect(
			user = info.user,
			password = info.password,
			host = info.host,
			service_name = info.service
		) as connection:
			# Use "with" to ensure the cursor is closed after the block
			with connection.cursor() as cursor:
				# Query to check if the MSISDN has status = "ACTIVE"
				query = info.query1
				cursor.execute(query, input = msisdn)
				result = cursor.fetchone()
				
				# Check if the MSISDN has a row and return True if status is ACTIVE
				return result and result[0] == 'ACTIVE'
		
		# Even though using "with" for both connection and cursor closes them, I will close them also manualy just in case.
		cursor.close()
		connection.close()
	
	except oracledb.Error as e:
		print(f"{info.error}: {e}")
		exit(1) # Close the application.
		return False

def process_msisdn_rows(data):
# Function to process each MSISDN and its row data
	active_rows = []  # List to store active rows with MSISDN;Stars;SMS
	inactive_msisdns = []  # List to store inactive or missing MSISDNs

	for row in data:
		parts = row.split(';')	# Split the row by semicolon
		msisdn = parts[0]		# MSISDN is always present
		
		# Assign default values using unpacking and defaults
		stars = parts[1] if len(parts) > 1 and parts[1] else 0
		sms = parts[2] if len(parts) > 2 and parts[2] else 'YES'
		
		if check_status_in_db(msisdn):
			# Only add active rows in the desired format
			active_rows.append(f"{msisdn.split('.', 1)[0]};{stars.split('.', 1)[0]};{sms}")
		else:
			inactive_msisdns.append(msisdn)

	return active_rows, inactive_msisdns
