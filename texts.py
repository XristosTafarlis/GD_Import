import re
import os
import DB
import info
import pandas

def output_file_nameMaker(input_file):
	# Extract the number from the input filename and creating the output .csv
	base_number = int(re.search(r'\d+', os.path.basename(input_file)).group())
	output_number = base_number + 3800
	output_file = f"{info.name}-{output_number}.csv"
	return output_file

def data_row_per_row(input_file):
	# Load data from Excel
	dataframe = pandas.read_excel(input_file)
	data = dataframe.apply(lambda row: ";".join(row.astype(str)), axis=1)
	dataPerRow = [row for row in data] # All rows with MSISDN;Stars;SMS format
	return dataPerRow

def process_msisdn_rows(data):
	# Function to process each MSISDN and its row data
	active_rows = [] # List to store active rows with MSISDN;Stars;SMS
	inactive_msisdns = [] # List to store inactive or missing MSISDNs

	for row in data:
		parts = row.split(';')	# Split the row by semicolon
		msisdn = parts[0]		# MSISDN is always present
		
		# Assign default values using unpacking and defaults
		stars = parts[1] if len(parts) > 1 and parts[1] else 0
		sms = parts[2] if len(parts) > 2 and parts[2] else 'YES'
		
		if DB.check_status_in_db(msisdn):
			# Only add active rows in the desired format
			active_rows.append(f"{msisdn.split('.', 1)[0]};{stars.split('.', 1)[0]};{sms}")
		else:
			inactive_msisdns.append(msisdn)
	
	return active_rows, inactive_msisdns