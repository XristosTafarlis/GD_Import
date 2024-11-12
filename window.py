import main
import info
import tkinter
import tkinter.filedialog

def show_popup():
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
	
	# Show the texts
	popup_text(root, background_color)
	
	# Show the button
	open_file_button(root)
	
	# Bind the ESC key to close the window
	root.bind('<Escape>', lambda _: root.destroy())
	
	# Make the popup window visible (this will block execution until it's closed)
	root.mainloop()

def popup_text(root, background_color):
	# Setting up the text parameters
	font_name = "Microsoft JhengHei"
	font_color = "gray70"
	font_size = 14
	
	# Printing the Title
	label1 = tkinter.Label(root, text="How to use the script:", fg = "gray80", bg = background_color)
	label1.config(font=("Impact", 30, "underline"))
	label1.pack(pady=15)
	
	# Printing the text
	label2 = tkinter.Label(root, text = info.label, fg=font_color, bg=background_color, justify="left")
	label2.config(font=(font_name, font_size))
	label2.pack(padx=40, pady=(20, 20), anchor='w')

def open_file_button(root):
	# Make the "Open file" button
	button = tkinter.Button(
		text = "Choose file(s)",
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

def on_hover(event):
	event.widget.configure(bg = "gray70")

def on_default(event):
	event.widget.configure(bg = "gray50")

def open_file(root):
	file_paths = tkinter.filedialog.askopenfilenames(title = "Select a file", filetypes = [("Excel Files", "*.xlsx")])
	if file_paths:
		for file_path in file_paths:
			main.main(file_path)
		root.destroy()
	else:
		print("No file selected")
