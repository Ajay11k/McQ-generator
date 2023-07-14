
# Python program to create 
# a file explorer in Tkinter

  
# import all components
# from the tkinter library

from tkinter import *

  
# import filedialog module

from tkinter import filedialog
filename="articles/fiverules.txt"
# Function for opening the 
# file explorer window

def browseFiles():

    filename = filedialog.askopenfilename(initialdir = "/",

                                          title = "Select a File",

                                          filetypes = (("Text files",

                                                        "*.txt*"),

                                                       ("all files",

                                                        "*.*")))

      

    # Change label contents
   
   # print(content)

    label_file_explorer.configure(text="File Opened: "+filename)

      

      

                                                                                                  
# Create the root window

window = Tk()

  
# Set window title

window.title('Extract Questions')

  
# Set window size

window.geometry("500x500")

  
#Set window background color

window.config(background = "white")

  
# Create a File Explorer label

label_file_explorer = Label(window, 

                            text = "Extract Questions by Passage",

                            width = 100, height = 4, 

                            fg = "red")

  

      

button_explore = Button(window, 

                        text = "Browse Files",

                        command = browseFiles) 

content=open(filename,"r", encoding="utf-8")
read=content.read()
print(read) 

button_exit = Button(window, 

                     text = "Exit",

                     command = exit) 

  
# Grid method is chosen for placing
# the widgets at respective positions 
# in a table like structure by
# specifying rows and columns

label_file_explorer.grid(column = 1, row = 1)

  

button_explore.grid(column = 1, row = 2)

  

button_exit.grid(column = 1,row = 3)

  
# Let the window wait for any events
window.mainloop()
print(filename)
 