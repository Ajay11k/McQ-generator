from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from utils import generate_mcq, write_mcq

class MCQGenerator:
    def __init__(self):
        self.main_window = Tk()
        self.main_window.title('MCQ Generator')
        self.main_window.geometry("550x550+100+100")
        self.main_window.configure(bg="#15c2ed")

        self.top_frame = Frame(self.main_window, bg="#032429", width=550, height=120)
        self.top_frame.place(x=0, y=0)

        image = Image.open("mcq-generator/Image/MCq.png")
        image = image.resize((64, 64))
        logo = ImageTk.PhotoImage(image)
        Label(self.top_frame, image=logo, bg="#032429").place(x=10, y=20)
        Label(self.top_frame, text="MCQ Generator from text", font="Helvetica 20 bold italic",
              fg="#0bdb27", bg="#032429").place(x=130, y=35)

        Label(self.main_window, text="Experience learning like never before!\n Convert plain text into captivating\n Multiple Choice Questions and master the subject.", font="Helvetica 15 bold",
              fg="#333333", bg="#15c2ed").place(x=30, y=140)

        image1 = Image.open("mcq-generator/Image/txt-open-file-format.png")
        image1 = image1.resize((128, 128))
        logo1 = ImageTk.PhotoImage(image1)
        Label(self.main_window, image=logo1, bg="#15c2ed").place(x=200, y=240)

        browse_button_img = PhotoImage(file='mcq-generator/Image/upload-file (1).png')
        self.button_browse = Button(self.main_window,
                                    text="  Choose a file", compound=LEFT, image=browse_button_img, width=150, font="arial 10 bold", bg="black", fg="white",
                                    command=self.browse_files)

        self.button_browse.place(x=190, y=380)

        exit_button_img = PhotoImage(file='mcq-generator/Image/exit (1).png')
        self.button_exit = Button(self.main_window,
                                  text="Exit", compound=LEFT, image=exit_button_img, width=150, font="arial 10 bold", bg="black", fg="white",
                                  command=self.exit_app)
        self.button_exit.place(x=190, y=430)
        self.main_window.resizable(False, False)
        self.main_window.mainloop()

    def browse_files(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                              filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
        if file_path:
            with open(file_path, encoding='utf-8') as file:
                content = file.read()
                self.generate_mcqs(content)

    def save_text(self):
        text = self.text_widget.get("1.0", END)
        file_path = filedialog.asksaveasfilename(filetypes=[('text file', '*.txt')], defaultextension='.txt',
                                                 initialdir="/")
        if file_path:
            with open(file_path, mode='w') as file:
                file.write(text)
            self.text_widget.delete('1.0', END)

            if self.mcq_window:
                self.mcq_window.destroy()
            if self.save_button:
                self.save_button.destroy()

    def generate_mcqs(self, content):
        distractor, sentence = generate_mcq(content)
        self.mcq_window = Tk()
        self.mcq_window.title("MCQ Questions")
        self.mcq_window.geometry("1100x1100+600+100")
        v_scrollbar = Scrollbar(self.mcq_window, orient='vertical')
        v_scrollbar.pack(side=RIGHT, fill='y')
        self.text_widget = Text(self.mcq_window, height=200, width=200, bg="#C1C1CD", font="arial 15 bold",
                                yscrollcommand=v_scrollbar.set)
        v_scrollbar.config(command=self.text_widget.yview)
        self.text_widget.pack()
        self.text_widget.insert(END, "**************************************        Multiple Choice Questions        *******************************")
        self.text_widget.insert(END, "\n")
        write_mcq(distractor, sentence, self.text_widget, END)

        save_button_img = PhotoImage(file='mcq-generator/Image/download.png')
        self.save_button = Button(self.main_window,
                                  text="Save", compound=LEFT, image=save_button_img, width=150, font="arial 10 bold",
                                  bg="black", fg="white",
                                  command=self.save_text)
        self.save_button.place(x=190, y=480)
        self.mcq_window.resizable(False, False)
        self.mcq_window.mainloop()

    def exit_app(self):
        self.main_window.destroy()

if __name__ == "__main__":
    app = MCQGenerator()
