import tkinter      # provides UI
import json     # important for saved data structure
import random   # allows choosing random data


class WHATEVER:
    def __init__(self):
        self.title = None
        self.loaded_data = {}
        self.root = tkinter.Tk()
        self.root.title("Generator Aligator RPG Tool")
        self.color = '#4473eb'
        self.root.config(padx=20,pady=20, bg=self.color)
        self.boot()
        self.loading_file()

    def boot(self):  # boot all the bacis UI items such as canva, buttons and widgets
        self.canvas = tkinter.Canvas(width=800, height=560, bg="#6f94f2", highlightthickness=0)
        self.canvas.grid(column=0, row=0, columnspan=16, rowspan=11)
        # Buttons
        self.button1 = tkinter.Button(text="ADD", highlightthickness=1, bg='#12a63e', command=self.get)
        self.button1.grid(column=3, row=2)
        self.button2 = tkinter.Button(text="DELETE", highlightthickness=0, bg='#12a63e', command=self.erase)
        self.button2.grid(column=4, row=2)
        self.button3 = tkinter.Button(text="SAVE", highlightthickness=0, bg='#12a63e', command=self.save)
        self.button3.grid(column=5, row=2)

        # Entry widget
        # Item entry
        self.canvas.create_text(50, 70, text=f"Item:", font=("Helvetica", 16), fill="blue")
        self.entry = tkinter.Entry(self.root, width=30)
        self.entry.grid(column=3, row=1, columnspan=3)
        self.entry.bind('<Return>', self.get)  # catch enter i input data

        ## Category title entry
        self.canvas.create_text(50, 20, text=f"Category:", font=("Helvetica", 16), fill="blue")
        self.title_entry = tkinter.Entry(self.root, width=30)
        self.title_entry.grid(column=3, row=0, columnspan=3)

        # Listbox data
        self.canvas.create_text(300, 180, text=f"Items in category:", font=("Helvetica", 16), fill="blue")
        self.input_values = tkinter.Listbox(self.root)
        self.input_values.grid(column=5, row=4, columnspan=4)
        self.chosen_list = []
        self.list_counter = 1
        self.text_label = tkinter.Label(self.root, text="", background="#6f94f2")
        self.text_label.grid(column=5, row=5, columnspan=5)

    def get(self,*args):  # adds input into listbox and list + *args allows to add as much args as we can
        # when button "add" is clicked, we pass just 1 parameter (input), when enter is clicked, 2 params are passed (input, event)
        input_text = self.entry.get()
        if input_text == '':
            pass
        else:
            self.text_label.config(text="")
            self.chosen_list.append(input_text)
            self.input_values.insert(self.list_counter, input_text)
            self.list_counter += 1
            self.entry.delete(0, 'end')

    def erase(self):  # erase chosen parameter from listbox
        try:
            self.text_label.config(text="")
            self.selection = self.input_values.curselection()        # define selected element in listbox
            self.chosen_list.remove(f"{self.input_values.get(self.selection[0])}")   # remove element from list
            self.input_values.delete(self.selection[0])      # remove element from listbox
            self.text_label.config(text="")
        except IndexError: # when no items were chosen
            self.text_label.config(text="Please choose item from the listbox first.")

    def loading_file(self):  # loads item from the json file that were saved earlier
        try:
            with open('generator_data.json', "r") as json_file:
                self.loaded_data = json.load(json_file)
            self.dynamic_buttons()
        except FileNotFoundError:  # when file was not created yet, or were deleted
            with open('generator_data.json', "w") as json_file:
                json.dump(self.loaded_data, json_file)
            with open('generator_data.json', "r") as json_file:
                self.loaded_data = json.load(json_file)

    def save(self):  # saved data into json file
        try:
            if self.title == '' or len(self.chosen_list) < 1:
                self.text_label.config(text="Please fill required fields.")
            else:
                self.title = self.title_entry.get()
                self.loaded_data[f'{self.title}'] = self.chosen_list

                with open('generator_data.json', "w") as json_file:
                    json.dump(self.loaded_data, json_file)
                self.chosen_list.clear()
                self.input_values.delete(0, 'end')
                self.title_entry.delete(0, 'end')
                self.reload()
                self.text_label.config(text="File saved successfully.")

        except SyntaxError:
            pass

# why lambda was used below?
# we need to use lambda statement to avoid triggering function white defining one of its parameters
    def create_button(self, name, number): # creates new buttons for saved keyitems
        button = tkinter.Button(text=f"{name}", highlightthickness=1, bg='#12a63e', command=lambda: self.read_file(name))
        button.grid(column=10, row=number)


    def dynamic_buttons(self): # reads json file and loop thorough keyitems
        counter2 = 1
        for key, value in self.loaded_data.items():
            self.create_button(key, counter2)
            counter2 += 1

    def randomizing(self, list, text_place):   # provides random item from list
        choice = random.choice(list)
        return self.canvas2.itemconfig(text_place, text=f"{choice}", fill="blue")


    def read_file(self, name):  # new window that allows you to read saved category and choose random item from that
        libr = self.loaded_data[name]
        self.canvas2 = tkinter.Canvas(width=800, height=560, bg="#DE9572", highlightthickness=0)
        self.canvas2.grid(column=0, row=0, columnspan=16, rowspan=11)
        text_place = self.canvas2.create_text(200, 150, text=f"", font=("Helvetica", 16), fill="blue")
        self.canvas2.create_text(100, 50, text=f"Category: {name}", font=("Helvetica", 16), fill="blue")
        self.random = tkinter.Button(text="Random", highlightthickness=1, bg='#12a63e', command=lambda: self.randomizing(libr, text_place))
        self.random.grid(column=3, row=2)
        self.button_go_back = tkinter.Button(text="Return", highlightthickness=1, bg='#12a63e', command= lambda: self.reload() )
        self.button_go_back.grid(column=5, row=1)

    def reload(self):  # reloads main menu
        self.boot()
        self.loading_file()

