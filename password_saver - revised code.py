from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_letters = [choice(letters) for char in range(nr_letters)]
    password_symbols = [choice(symbols) for char in range(nr_symbols)]
    password_numbers = [choice(numbers) for char in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers #type: list
    shuffle(password_list)

    # password = ""
    # for char in password_list:
    #   password += char

    password = "".join(password_list) #join all item in a list/tuple/dictionary into a string

    password_entry.insert(0,password) #insert the password automatically every time I entered into this program

    pyperclip.copy(password)#copy the password in my clipboard

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
        "email": email,
        "password":password,
        }
    }

    # data validation: if the website/password is empty, we do not save the data and show the pop-up box
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json","r") as data_file:
                # read old data which will convert into python dictionary
                data = json.load(data_file)
        except FileNotFoundError: #if this is the first time we create this data.json
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else: #if the data.json exist
                #update the data file with new data(it's going to append existing file)
            data.update(new_data)

            with open("data.json","w") as data_file:
                #saving the updated data and wipe all previously saved data
                json.dump(data, data_file, indent=4)#indent all json data
        finally:
                # #clean everything out with delete function
                website_entry.delete(0,END)
                password_entry.delete(0,END)
# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()#data type: string
    try:
        with open("data.json") as data_file:
            data = json.load(data_file) #type: dictionary
    except FileNotFoundError:
        messagebox.showinfo(message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            #show a message with website's name and password
            messagebox.showinfo(title = website, message=f"email:{email}"
                                            f"\nPassword : {password}")
        else:
            messagebox.showinfo(message=f"No details for the {website} exists.")



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)

canvas = Canvas(width=200,height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo_img) #tuple/position: 100,100
canvas.grid(column=1,row=0)

#create a textbox and entries:
website_label = Label(text="Website:")
website_label.grid(column=0,row=1)
email_label= Label(text="Email/Username:")
email_label.grid(column=0,row=2)
password_label = Label(text="Password:")
password_label.grid(column=0,row=3)

website_entry = Entry(width=21)
website_entry.grid(column=1,row=1)
website_entry.focus() #when you launch this app, the cursor will be focused on the first website entry

email_entry = Entry(width=38)
email_entry.grid(column=1,row=2,columnspan=2)
email_entry.insert(0,"my_email") #we want this to be pre-populated, so we insert at index=0(beginning) with my_email
password_entry = Entry(width=21)
password_entry.grid(column=1,row=3)

#buttons
search_button= Button(text="Search",width=13,command=find_password)
search_button.grid(row=1,column=2)
generate_password_button = Button(text="Generate Password",command=generate_password)
generate_password_button.grid(row=3,column=2)
add_button = Button(text="Add",width=36,command=save)
add_button.grid(row=4,column=1,columnspan=2)


window.mainloop()

