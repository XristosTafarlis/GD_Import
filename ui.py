import DB
import sys
import main
import info
import winsound
import tkinter
import tkinter.filedialog

def main_widnow():
	# Create a new Tk instance
	background_color = "gray9"
	root = tkinter.Tk()
	root.configure(bg = background_color)
	
	# Get the screen width and height
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	
	# Set the size of the window
	window_width = 770
	window_height = 410
	
	# Set the initial position of the popup window
	position_x = (screen_width - window_width) // 2
	position_y = (screen_height - window_height) // 2
	
	# Make the window not resizable by setting its resizable attribute to False
	root.resizable(False, False)
	
	# Set the title of the popup window
	root.title(info.title)
	
	# Set the window geometry
	root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
	
	# Setting up the text parameters
	font_name = "Microsoft JhengHei"
	font_color = "gray70"
	font_size = 14
	
	# Printing the Title
	label1 = tkinter.Label(root, text="How to use the script:", fg = "gray80", bg = background_color)
	label1.config(font=("Impact", 30, "underline"))
	label1.pack(pady=15)
	
	# Printing the text
	label2 = tkinter.Label(root, text = info.label, fg = font_color, bg = background_color, justify = "left")
	label2.config(font=(font_name, font_size))
	label2.pack(padx=40, pady=(20, 20), anchor='w')
	
	# Make the "Open file" button
	button = tkinter.Button(
		text = "Choose file",
		width = 20,
		bd = 0,
		bg = "gray50",
		font = ("Microsoft JhengHei", 12),
		relief= "solid",
		activebackground = "gray30",
		activeforeground = "gray80",
		command = lambda: open_file(root))
	
	button.bind('<Enter>', on_hover)
	button.bind('<Leave>', on_default)
	
	button.pack(pady = (0, 10))
	
	# Bind the ESC key to close the window
	root.bind('<Escape>', lambda _: root.destroy())
	
	# Make the popup window visible (this will block execution until it's closed)
	root.mainloop()

def query_window():
	place_holder_text = "No data retrived from the Database..." # The text displayed on the text_box before the script gets and displays the data from the DB.
	
	# Call the DB to get the final results
	def call_db():
		print("Checking DB")
		data = DB.check_results_in_db()
		if data:
			text_box.config(state = 'normal')
			text_box.delete("1.0", tkinter.END)
			
			headers = f"|{'MSISDN'.center(info.msisdn)}|{'STARS'.center(info.star)}|\n"
			separator = "|------------+--------|" + "\n"
			text_box.insert(tkinter.END, headers)
			text_box.insert(tkinter.END, separator)
			
			for msisdn, stars in data:
				row = f"|{msisdn.center(info.msisdn)}|{stars.center(info.star)}|\n"
				text_box.insert(tkinter.END, row)
			
			text_box.config(state = "disabled")
			
			root.lift()
			root.attributes('-topmost', True)  # Temporarily make the window topmost
			root.attributes('-topmost', False) # Allow it to behave normally again
			winsound.MessageBeep(winsound.MB_ICONASTERISK)
		
		root.after(60000, call_db)
	
	# Creating a new Tkinter window, similar to the 1st
	root = tkinter.Tk()
	root.configure(bg = "gray9")
	root.title(info.title)
	
	# Center the window on the screen
	window_width = 600
	window_height = 400
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x_position = (screen_width // 2) - (window_width // 2)
	y_position = (screen_height // 2) - (window_height // 2)
	root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
	
	# Make the window not resizable by setting its resizable attribute to False
	root.resizable(False, False)
	
	# Set the on_close callback
	root.protocol("WM_DELETE_WINDOW", on_close)
	
	# Bind the ESC key to close the window
	root.bind('<Escape>', lambda _: on_close())
	
	# Add a text box for input
	text_box = tkinter.Text(
		root,
		width = 46,
		height = 15,
		bd = 0,
		fg = "gray80",
		bg = "gray20",
		font = ("Courier New", 16))
	
	text_box.pack(pady = 5)
	text_box.insert(tkinter.END, place_holder_text)
	text_box.config(state = "disabled")
	
	# Add a Copy button
	exit_button = tkinter.Button(
		root,
		text = "Exit",
		width = 20,
		bd = 0,
		bg = "gray50",
		font = ("Courier New", 14),
		relief= "solid",
		activebackground = "gray30",
		activeforeground = "gray80",
		command = lambda : on_close()
		)
	
	exit_button.bind('<Enter>', on_hover)
	exit_button.bind('<Leave>', on_default)
	
	exit_button.pack(padx = 30, pady = 5)
	
	call_db() # Start the first DB query immediately
	root.mainloop()

def on_hover(event):
	event.widget.configure(bg = "gray70")

def on_default(event):
	event.widget.configure(bg = "gray50")

def open_file(root):
	file_path = tkinter.filedialog.askopenfilename(title = "Select a file", filetypes = [("Excel Files", "*.xlsx")])
	if file_path:
		main.main(file_path)
		root.destroy()
	else:
		print("No file selected")

def on_close():
		print("Exiting...")
		sys.exit() # Exit the script
