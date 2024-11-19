import os
import DB
import sys
import texts
import window
import message
import file_writer

def main(input_file):
	# Get the path to Desktop
	desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
	
	# Make the output file name
	output_file_name = texts.output_file_nameMaker(input_file)
	
	active_csv = os.path.join(desktop_path, output_file_name)
	inactive_txt = os.path.join(desktop_path, "inactive_msisdns.txt")
	
	# Take the .xlsx file and extract the data
	data_rows = texts.data_row_per_row(input_file)
	
	# Process each row of the data, to filter STATUS "ACTIVE" or "INACTIVE"
	active_rows, inactive_rows = DB.process_msisdn_rows(data_rows) # Goes to the Data Base and checks all MSISDNs
	
	# Make 2 files, one .csv for "ACTIVE" and one .txt for "INACTIVE"
	file_writer.write_files(active_rows, inactive_rows, active_csv, inactive_txt)
	
	# Copy Queries that are used to check if all stars have been assigned on clipboard 
	texts.copy_queries()
	
	# Copy Email template on clipboard
	# texts.copy_email()
	message.send_message(active_csv)

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