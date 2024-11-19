import info

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
			query = (info.query0_p1 + formatted_msisdns + info.query0_p2 + formatted_msisdns + info.query0_p3)
			inactive_MSISDNs_file.write(query)