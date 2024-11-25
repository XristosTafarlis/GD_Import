import info
import winsound
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
				return (result and result[0] == 'ACTIVE')
	
	except oracledb.Error as e:
		print(f"{info.error}: {e}")
		exit(1) # Close the application.
		return False

def check_results_in_db():
	try:
		# Using "with" to ensure the connection is closed after the block
		with oracledb.connect(
			user = info.user,
			password = info.password,
			host = info.host,
			service_name = info.service
		) as connection:
			# Using "with" to ensure the cursor is closed after the block
			with connection.cursor() as cursor:
				# Query to check if the procedure is done
				cursor.execute(info.query2)
				result = cursor.fetchone()
				
				if (result and result[0] == 'SUCCESS'):
					print("Procedure executed successfully.")
					
					# Query to get the results of the procedure
					cursor.execute(info.query3)
					
					result = cursor.fetchall()
					
					if result:
						print("DB accessed, data returned.")
						return result
				else:
					print("Procedure not executed, returning...")
					return None
	
	except oracledb.Error as e:
		winsound.MessageBeep(winsound.MB_ICONASTERISK)
		print(f"{info.error}: {e}")
		exit(1) # Close the application.
		return False
