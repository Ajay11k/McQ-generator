# Python program to create
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *
from tkinter import ttk,messagebox
# import filedialog module
from tkinter import filedialog
from PIL import Image,ImageTk

# Function for opening the
# file explorer window
def browseFiles():
	

	filename = filedialog.askopenfilename(initialdir = "/",
										title = "Select a File",
										filetypes = (("Text files",
														"*.txt*"),
													("all files",
														"*.*")))

	file = open(filename,encoding='utf-8')
	read = file.read()
	print(read)
	window1 = Tk()
	window1.title("MCQ Questions")
	window1.geometry("500x500+600+100")
	v = Scrollbar(window1,orient='vertical')
	v.pack(side=RIGHT,fill='y')
	t = Text(window1,height=100,width=100,bg="#C1C1CD",font="arial 15 bold",yscrollcommand=v.set)
	v.config(command=t.yview)
	t.pack()
	
	

	favt = 'ajay is good boy.\n'
	das = 'ajay is grat person'
	t.insert(END,f"hello,{favt}")
	t.insert(END,das)
	def save_text():
		s = t.get("1.0",END)
		fob = filedialog.asksaveasfile(filetypes=[('text file','*.txt')],defaultextension ='.txt',initialdir = "/",mode= 'w')
		fob.write(s)
	   
		fob.close()
		t.delete('1.0',END)
		t.update()

	#save_text()
	bimg2 = PhotoImage(file='download.png')	
	button_save = Button(window,
					text = "Save",compound=LEFT,image=bimg2,width=150,font="arial 10 bold",bg="black",fg="white",
					command = save_text)
	button_save.place(x=190,y=450)	
	#b1.place(x=200,y=200)				
    
    
	file.close()
	window1.resizable(False,False)
	window1.pack()
    
	window1.mainloop()

	# Change label contents
	label_file_explorer.configure(text="File Opened: "+filename)
	
	
																								
# Create the root window
window = Tk()

# Set window title
window.title('MCQ Generator')

# Set window size
window.geometry("500x500+100+100")
window.configure(bg="#305065")

image_icon = PhotoImage(file='base.png')
window.iconphoto(FALSE,image_icon)

#Set window background color

#window.config(background = "white")
'''bg = PhotoImage(file='base.png')
canvas1 = Canvas(window,width=500,height=500)
canvas1.pack(fill="both",expand=True)
canvas1.create_image(0,0,image=bg,anchor="nw")'''
# Create a File Explorer label

top_frame=Frame(window,bg="#00EEEE",width=500,height=100)
top_frame.place(x=0,y=0)
image = Image.open("MCq.png")
image = image.resize((64,64))
logo = ImageTk.PhotoImage(image)
Label(top_frame,image=logo,bg="#00EEEE").place(x=10,y=11)
Label(top_frame,text = "MCQ Generator from text",font="Helvetica 20 bold italic",
							fg = "#4B4B00",bg="#F0F080").place(x=100,y=30)
Label(window,text = "Upload any text file and \n see the magic.",font="Helvetica 15 bold",
							fg = "#FAFAF0",bg="#305065").place(x=155,y=130)

image1 = Image.open("kindpng_333606.png")
image1 = image1.resize((128,128))
logo1 = ImageTk.PhotoImage(image1)
Label(window,image=logo1,bg="#305065").place(x=200,y=200)
#label_canvas=canvas1.create_window(1,10,anchor ="nw",window=label_file_explorer)
bimg = PhotoImage(file='upload-file (1).png')	
button_explore = Button(window,
						text = "  Choose a file",compound=LEFT,image=bimg,width=150,font="arial 10 bold",bg="black",fg="white",
						command = browseFiles)
button_explore.place(x=190,y=350)						
#explore_canvas=canvas1.create_window(100,100,anchor ="nw",window=button_explore)						
bimg1 = PhotoImage(file='exit (1).png')	
button_exit = Button(window,
					text = "Exit",compound=LEFT,image=bimg1,width=150,font="arial 10 bold",bg="black",fg="white",
					command = exit)
button_exit.place(x=190,y=400)					
#exit_canvas=canvas1.create_window(100,140,anchor ="nw",window=button_exit)					

# Grid method is chosen for placingimage
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
#label_file_explorer.grid(column = 1, row = 1)

#button_explore.grid(column = 1, row = 2)

#button_exit.grid(column = 1,row = 3)

# Let the window wait for any events
window.resizable(False,False)
window.mainloop()
