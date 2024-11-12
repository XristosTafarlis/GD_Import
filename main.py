import re
import os
import sys
import pandas
import window
import info # Contains data that is sensitive to share.
from DB import process_msisdn_rows
from texts import *

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
	dataPerRow = [row for row in data]  # All rows with MSISDN;Stars;SMS format
	return dataPerRow

def write_files(active, inactive, output):
	# Write active MSISDNs to CSV
	if (len(active) > 0):
		with open(output, 'w') as output_file:
			output_file.write("\n")  # Add a single blank line at the top
			for i, row in enumerate(active):
				if i == len(active) - 1:  # Check if it's the last row
					output_file.write(row)
				else:
					output_file.write(row + "\n")
	
	# Write inactive MSISDNs to TXT if there are any
	if (len(inactive) > 0):
		with open('inactive_msisdns.txt', 'w') as inactive_MSISDNs_file:
			# Construct the SQL query
			formatted_msisdns = ',\n'.join([f"		'{msisdn}'" for msisdn in inactive])
			
			# Write the query to the file
			query = (f"SELECT\n	*\nFROM\n	{info.schema}.{info.table1}\nWHERE\n	{info.column1} IN (\n{formatted_msisdns}\n	)\n	OR {info.column2} IN (\n{formatted_msisdns}\n	);")
			inactive_MSISDNs_file.write(query)

def main(input_file):
	# Make the output file name
	output_file_name = output_file_nameMaker(input_file)
	
	# Take the .xlsx file and extract the data
	data_rows = data_row_per_row(input_file)
	
	# Process each row of the data, to filter STATUS "ACTIVE" or "INACTIVE"
	active_rows, inactive_rows = process_msisdn_rows(data_rows) # Goes to the Data Base and checks all MSISDNs
	
	# Make 2 files, one .csv for "ACTIVE" and one .txt for "INACTIVE"
	write_files(active_rows, inactive_rows, output_file_name)
	
	# Copy Queries that are used to check if all stars have been assigned on clipboard 
	copy_queries()
	
	# Copy Email template on clipboard
	copy_email()

# Run the main function
if __name__ == "__main__":
	# Check if a file was dropped and if it has the .xlsx extension
	if len(sys.argv) > 1:
		for input_file in sys.argv[1:]:  # Loop through each file dropped
			if input_file.lower().endswith(".xlsx"):
				main(input_file)
			else:
				print(f"Skipping unsupported file: {input_file}")
	else:
		# If not, open the popup window
		window.show_popup()