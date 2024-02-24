from tkinter.simpledialog import *  # also imports all basic tkinter classes
from ctypes import windll
from PIL import Image, ImageTk  # i chose not to use tkinter's PhotoImage class, as it only accepts certain image extensions
from json import load

# a lesser known ctypes trick to increase the clarity of the tkinter window
windll.shcore.SetProcessDpiAwareness(1)

# basic json stuff
name_of_json_file = "quiz_data_eddie_mabo.json"
JSONFILE = load(open(name_of_json_file))

# variable that holds the user's name.
USER_NAME = ""


def _from_rgb(rgb):
    """turns a tuple of r, g, b values into a color code understandable by tkinter."""
    return "#%02x%02x%02x" % rgb


class externals:
    def __init__(self, window):
        self.two_second_label = None
        self.tkWindow = window
        self.tkWindow.iconbitmap("EddieMabo.ico")
        self.starting_screen()

    def starting_screen(self):
        """provides the starting screen for my quiz application"""

        def validateLogin(name, year):
            """checks to see if all login details are valid, and then move on to the next xtep"""
            try:
                try:
                    if year.get() != "":
                        int(year.get())
                except:
                    raise ValueError("Invalid input", "Year must be a number.")
                if name.get() == "" or year.get() == "":
                    raise ValueError("Invalid input", "Entries cannot be empty.")
                if (type(name.get()) == str) is False or (type(int(year.get())) == int) is False:
                    raise ValueError("Invalid input",
                                     "Input is considered invalid... please enter a string for your name and an integer for your age.")
                if int(year.get()) < 0:
                    raise ValueError("Invalid input", "Your age cannot be negative.")
                if int(year.get()) == 10:
                    for widget in self.tkWindow.winfo_children():
                        widget.destroy()
                    self.two_second_label = Label(self.tkWindow, text="Year accepted!", font=("consolas", 30))
                    self.two_second_label.grid(row=0, column=1)

                    # simple delay
                    self.tkWindow.after(500, lambda: self.three_pages_of_information(name.get()))
                else:
                    raise ValueError("Invalid age", "You have to be in Year 10 to participate in this quiz...")
            except ValueError as error:
                messagebox.showwarning(error.args[0], error.args[1])

        self.tkWindow.geometry('750x180')
        self.tkWindow.title('Eddie Mabo: A Quiz')

        # basic label + entry + button gridding
        self.name = StringVar(self.tkWindow, None)
        self.name_label = Label(self.tkWindow, text="Name: ", font=("consolas", 15))
        self.name_label.grid(row=0, column=0)
        self.name_entry = Entry(self.tkWindow, textvariable=self.name, font=("consolas", 15))
        self.name_entry.grid(row=0, column=1, padx=20, pady=10)

        self.year_label = Label(self.tkWindow, text="Year: ", font=("consolas", 15))
        self.year_label.grid(row=1, column=0)
        self.year = StringVar(self.tkWindow, value=None)
        self.year_entry = Entry(self.tkWindow, textvariable=self.year, font=("consolas", 15))
        self.year_entry.grid(row=1, column=1, padx=20, pady=10)
        self.name_entry.focus_set()

        # login button
        self.login_button = Button(self.tkWindow, text="Login", command=lambda: validateLogin(self.name, self.year),
                                   font=("consolas", 15))
        self.login_button.grid(row=4, column=1)

        # inputting an image using pillow
        self.img = ImageTk.PhotoImage(Image.open("mabo.jpg").resize((300, 168), Image.Resampling.LANCZOS))
        self.image_label = Label(self.tkWindow, image=self.img)
        self.image_label.grid(row=0, column=2, rowspan=5, pady=5)

        # setting simple shortcuts for the tkinter window.
        self.tkWindow.bind('<Down>', lambda x: self.year_entry.focus_set())
        self.tkWindow.bind('<Up>', lambda x: self.name_entry.focus_set())
        self.tkWindow.bind('<Return>', lambda x: validateLogin(self.name, self.year))

        # due to the nature of the __main__ loop at the end of the file, this statement needs to be made to SPECIFICALLY exit on window exit.
        self.tkWindow.protocol("WM_DELETE_WINDOW", lambda: exit(0))
        self.tkWindow.mainloop()

    def _next(self):
        """moves to the next page"""
        # simple yet somewhat analogue method to disable/enable button based off current page.
        if self.previous_button['state'] == "disabled":
            self.previous_button['state'] = "normal"

        self.current_info_page += 1
        self.three_pages_of_information_frame.delete("1.0", "end")
        self.three_pages_of_information_frame.insert("1.0", self.list_of_info_pages[self.current_info_page])

        # disables button if you are on the last page
        if self.current_info_page == len(self.list_of_info_pages) - 1:
            self.next_button['state'] = "disabled"

    def _previous(self):
        """moves to the previous page"""
        # simple yet somewhat analogue method to disable/enable button based off current page.
        if self.next_button['state'] == "disabled":
            self.next_button['state'] = "normal"

        self.current_info_page -= 1
        self.three_pages_of_information_frame.delete("1.0", "end")
        self.three_pages_of_information_frame.insert("1.0", self.list_of_info_pages[self.current_info_page])

        # disables button if you are on the first page
        if self.current_info_page == 0:
            self.previous_button['state'] = "disabled"

    def _done_reading(self):
        """messagebox that asks if you wish to continue, and then destroys window."""
        if messagebox.askyesno("Done reading?",
                               "Are you sure you are done reading? You will NOT be able to see this information again during the quiz."):
            self.tkWindow.destroy()
            return Tk

    def three_pages_of_information(self, name):
        """all three content slides"""
        global USER_NAME
        self.tkWindow.geometry('765x280')

        # removing the binding placed earlier, as they will cause errors if bound keys are pressed again
        self.tkWindow.unbind("<Down>")
        self.tkWindow.unbind("<Return>")
        self.tkWindow.unbind("<Up>")

        # creating a content frame, which is by far the easiest way to position an image next to it
        self.content_frame = Frame(self.tkWindow)
        self.content_frame.grid(row=1, column=0)

        self.two_second_label.destroy()
        self.greeting_label = Label(self.tkWindow, text=f"Hello, {name}!")

        # inserting an image
        self.img = ImageTk.PhotoImage(Image.open("mabo3.jpg").resize((276, 238), Image.Resampling.LANCZOS))
        self.image_label = Label(self.tkWindow, image=self.img)
        self.image_label.grid(row=1, column=1, sticky=S)

        # setting the username, which is the only shared variable between class externals and main_application.
        USER_NAME = name
        self.greeting_label.grid(row=0, column=0, sticky=W)

        # creating the textbox and the buttons, and placing them directly next to each other.
        self.three_pages_of_information_frame = Text(self.content_frame, width=50, height=10, wrap=WORD)
        self.three_pages_of_information_frame.grid(row=1, column=0, columnspan=3)

        self.next_button = Button(self.content_frame, text="Next", command=self._next, width=20)
        self.next_button.grid(row=3, column=0, sticky=W)

        self.previous_button = Button(self.content_frame, text="Previous", command=self._previous, width=20)
        self.previous_button.grid(row=3, column=1, sticky=W)

        self.done_reading_button = Button(self.content_frame, text="Done reading", command=self._done_reading, width=20)
        self.done_reading_button.grid(row=3, column=2, sticky=W)

        # setting the first content slide to 0
        self.current_info_page = 0

        # getting content slide info from the json file.
        info = JSONFILE['information']
        self.list_of_info_pages = []
        for i in range(len(info)):
            self.list_of_info_pages.append(info[i]['info'] if info[i]['pageNum'] == str(i + 1) else None)
        self.three_pages_of_information_frame.insert("1.0", self.list_of_info_pages[0])

        # setting the previous button to a disabled state, as the app starts on page 1.
        self.previous_button["state"] = "disabled"


class tkinter_page_manager:
    def __init__(self, frame: Frame, text: str, answers: dict, correct_answer: str, img=None):
        # didn't really use this function all that much, as it felt too crammed to include images for each fo the ten questions
        self.img = img

        self.frame = frame
        self.text = text
        self.answers = answers
        self.correct_answer = correct_answer

        # couldn't figure out how to correctly set the radiobutton value to un-select it, the easiest way was to set it to an index that didn't exist.
        self.currently_active = "5"
        self.list_of_radiobuttons = []
        self.answered = StringVar(self.frame, self.currently_active)
        i = 1

        # looping through creating four radiobuttons.
        for (text, value) in self.answers.items():
            current_radiobutton = Radiobutton(self.frame, text=value, variable=self.answered, value=value,
                                              command=self.save_current_activated, bg="white", wraplength=500)
            self.list_of_radiobuttons.append(current_radiobutton)
            i = i + 1

    def init_gui(self):
        """initialises the GUI of the actual text + radiobutton slide.
        for no apparent and logical reason, I decided that the text box and radiobutton would be created separately for each instance :rolling_eyes:
        would have been significantly easier to just change the text, as the widget itself does not change."""

        # removing everythin within parent frame
        for widgets in self.frame.winfo_children():
            widgets.grid_forget()
        self.correct_answer = self.correct_answer

        self.textbox = Text(self.frame, height=5, wrap=WORD, width=70)
        self.textbox.grid(row=0, column=0, columnspan=4)
        if self.img is not None:
            self.textbox.image_create(END, image=self.img)
        self.textbox.insert("1.0", self.text)

        self.textbox.config(state="disabled")

        for i in self.list_of_radiobuttons:
            i.grid(row=self.list_of_radiobuttons.index(i) + 1, column=0)

    def save_current_activated(self):
        # saving the last activated radiobutton state
        self.currently_active = self.answered.get()
        return self.currently_active

    def get_is_correct(self):
        # return whether selected answer is correct when compared to the answer which will be provided from the json file.
        if str(list(self.answers.values()).index(self.answered.get()) + 1) == self.correct_answer:
            return True
        else:
            return False

    def get_is_answered(self):
        # checks if radiobuttons have been touched at all
        if self.currently_active == "5":
            return False
        else:
            return True

    def highlight_answers(self):
        # highlights the correct answer as green, and incorrect ones as red if any exist.
        ind = list(self.answers.values()).index(self.answered.get())
        print(f"index: {ind}")

        print(self.get_is_correct())
        if self.get_is_correct():
            self.list_of_radiobuttons[ind].configure(bg=_from_rgb((173, 235, 173)))
        else:
            self.list_of_radiobuttons[ind].configure(bg=_from_rgb((255, 102, 102)))
            self.list_of_radiobuttons[int(self.correct_answer) - 1].configure(bg=_from_rgb((173, 235, 173)))

    def disable(self):
        # disabling all the radiobuttons.
        for i in self.list_of_radiobuttons:
            i["state"] = "disabled"


class main_application:
    def __init__(self, window):
        # all of the usual function calling and what not. instead of using the Tk object provided, decided to use a frame named 'root'.
        self.master = window
        self.master.iconbitmap("EddieMabo.ico")
        self.master.protocol("WM_DELETE_WINDOW", lambda: exit(0))
        self.master.geometry("1200x720")
        self.master.title("Eddie Mabo: A Quiz")
        self.master.resizable(False, False)
        self.root = Frame(self.master, width=1000, height=600, bg="white")
        self.root.pack()

        # setting the frame that the title widgets will be placed in
        self.title_frame = Frame(self.root)
        self.title_frame.grid(row=0, column=0, columnspan=2, rowspan=2)

        # the image
        self.img = ImageTk.PhotoImage(Image.open("mabo2.jpg").resize((400, 192), Image.Resampling.LANCZOS))

        # placing the image within a label
        self.image_label = Label(self.title_frame, image=self.img)
        self.image_label.grid(row=0, column=1, sticky=E, rowspan=2)

        # the title
        self.title_label = Label(self.title_frame, text="Eddie Mabo - The Man Who Changed Australia ",
                                 font=("Consolas", 20))
        self.name_label = Label(self.title_frame, text="By Aniketh Kopalle", font=("Consolas", 10))
        self.title_label.grid(row=0, column=0)
        self.name_label.grid(row=1, column=0)

        # the frame that will contain all the text and radiobuttons.
        self.info_frame = Frame(self.root, bg="white", height=450, width=700)
        self.info_frame.grid(row=2, column=1, sticky=NE)
        self.info_frame.grid_propagate(0)
        self.info_frame.grid_rowconfigure(4)
        self.info_frame.grid_columnconfigure(3)

        # label that shows the user's name and eventually their score.
        self.score_and_name_label = Label(self.root, bg="white", text=f"Hello, {USER_NAME}!", font=("Consolas", 20))
        self.score_and_name_label.grid(row=3, column=1)

        # frame with all the control buttons
        self.controls_frame = Frame(self.root, bg="white", width=484, height=500)
        self.controls_frame.grid(row=2, column=0, rowspan=2)
        self.controls_frame.pack_propagate(0)

        # all the control buttons
        self.next_button = Button(self.controls_frame, text="Next", relief=FLAT, width=15, height=3,
                                  command=self.next_page)
        self.next_button.pack(pady=20)
        self.previous_button = Button(self.controls_frame, text="Previous", relief=FLAT, width=15, height=3,
                                      command=self.previous_page)
        self.previous_button.pack(pady=20)
        self.finish_button = Button(self.controls_frame, text="Finish", relief=FLAT, width=15, height=3,
                                    command=self.finish)
        self.finish_button.pack(pady=20)

        self.restart_button = Button(self.controls_frame, text="Restart Quiz", relief=FLAT, width=15, height=3,
                                     command=self.restart)
        self.restart_button.pack(pady=20)

        # calling the restart function at the start will initialise the first page of content, and will act as a restart regardless of the time initiated.
        self.restart()

        # basic menubar with basic functions.
        self.menubar = Menu(self.master)

        self.file_bar = Menu(self.menubar, tearoff=0)
        self.file_bar.add_command(label="About", command=lambda: messagebox.showinfo("About",
                                                                                     "Created by Aniketh Kopalle for his Year 10 IT Assessment."))
        self.file_bar.add_command(label="Exit", command=lambda: exit(0))
        self.file_bar.add_command(label="Restart Application", command=self.reset_application)

        self.menubar.add_cascade(label="File", menu=self.file_bar)

        # binding arrow keys to move between pages
        self.master.bind("<Right>", self.next_page)
        self.master.bind("<Left>", self.previous_page)

        self.master.config(menu=self.menubar)
        self.master.mainloop()

    @staticmethod
    def _pass():
        """my favourite function of them all"""
        pass

    def reset_application(self):
        """resetting the entire application"""
        if messagebox.askyesno("Do you want to delete all progress?",
                               "Do you want to restart the entire application?"):
            self.master.destroy()

    def restart(self):
        """restarts the quiz, not the app"""
        self.previous_button["state"] = "disabled"
        self.restart_button["state"] = "disabled"

        self.list_of_pages = []
        self.current_page_number = 0
        self.pages()
        self.list_of_pages[0].init_gui()

    def pages(self):
        # loops through the json file and initialises class for each of the pages
        page = JSONFILE['pages']
        for i in range(0, 10):
            self.list_of_pages.append(tkinter_page_manager(self.info_frame,
                                                           text=page[i]['text'] if page[i]['pageNum'] == str(
                                                               i + 1) else None,
                                                           correct_answer=page[i]['correctAns'] if page[i][
                                                                                                       'pageNum'] == str(
                                                               i + 1) else None,
                                                           answers=dict(page[i]['options'] if page[i]['pageNum'] == str(
                                                               i + 1) else None)))

    def next_page(self, event=None):
        # goes to the next page
        if self.previous_button['state'] == "disabled":
            # enables the hotkey and the next button
            self.previous_button['state'] = "normal"
            self.master.bind("<Left>", self.previous_page)

        # initialises the next page's GUI
        self.current_page_number = self.current_page_number + 1
        self.list_of_pages[self.current_page_number].init_gui()

        if self.current_page_number == len(self.list_of_pages) - 1:  # a tribute to pythons counterintuitive list :/
            # disables the hotkey and the next button
            self.next_button['state'] = "disabled"
            self.master.unbind("<Right>")

    def previous_page(self, event=None):
        # goes to the previous page
        if self.next_button['state'] == "disabled":
            # enables the hotkey and the next button
            self.next_button['state'] = "normal"
            self.master.bind("<Right>", self.next_page)

        # initialises the previous page's GUI
        self.current_page_number = self.current_page_number - 1
        self.list_of_pages[self.current_page_number].init_gui()

        if self.current_page_number == 0:
            # disables the hotkey and the next button
            self.previous_button['state'] = "disabled"
            self.master.unbind("<Left>")

    def finish(self):
        """finish function"""
        list_of_answered_questions = 0
        if messagebox.askyesno("Are you sure?",
                               "Are you sure you want to finish the quiz? You will not be able to change your answers again."):
            count = 0
            # checks if all questions have been answered
            for i in range(0, len(self.list_of_pages)):
                if self.list_of_pages[i].get_is_answered():
                    list_of_answered_questions += 1
            if list_of_answered_questions == len(self.list_of_pages):
                for i in range(0, len(self.list_of_pages)):
                    self.list_of_pages[i].highlight_answers()
                    self.list_of_pages[i].disable()
                    self.restart_button["state"] = "normal"
                    if self.list_of_pages[i].get_is_correct():
                        count += 1
                messagebox.showinfo("Score", f"You've gotten {count}/10, or {count * 10}% on your quiz!")
                self.score_and_name_label.config(text=self.score_and_name_label.cget("text") + f" - Score: {count}")
                self.finish_button["state"] = "disabled"
            else:
                messagebox.showinfo("You have not finished the quiz yet...", "Please finish the quiz to continue.")

    def change_info_content(self):
        pass


if __name__ == '__main__':
    # main loop, when externals dies, main application runs on new Tk object. this is purely for simplicity, and is only possible due to one shared variable.
    while True:
        if externals(Tk()):
            main_application(Tk())
