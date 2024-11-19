import re
import os
import time
import info
import pandas
import pyperclip

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

def copy_email():
	# Copy the email template on clipboard
	pyperclip.copy(info.email)

def copy_queries():
	# Copy the queries to clipboard
	pyperclip.copy(info.query2)
	time.sleep(1)
