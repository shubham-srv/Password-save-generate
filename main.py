from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def create_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password_created = "".join(password_list)
    print(f"Your password is: {password_created}")
    password_entry.delete(0, END)
    password_entry.insert(index=0, string=f"{password_created}")
    pyperclip.copy(password_created)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def password_save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    data = {website:
            {
                "email": email,
                "password": password,
            },
            }
    if len(email) == 0 or len(password) == 0 or len(website) == 0:
        messagebox.showerror(title="error", message="one or more empty field")
    else:
        try:
            with open(file="data.json", mode="r") as password_file:
                new_data = json.load(password_file)
                new_data.update(data)

        except FileNotFoundError:
            with open(file="data.json", mode="w") as file:
                json.dump(data, file, indent=4)
        else:
            with open(file="data.json", mode="w") as password_file:
                json.dump(new_data, password_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def search_password():
    website_search = website_entry.get()
    if len(website_search) == 0:
        messagebox.showerror(title="error", message="website field empty")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                my_data = json.load(data_file)
            get_email = my_data[website_search]["email"]
            get_password = my_data[website_search]["password"]
            messagebox.showinfo(title="search result", message=f"email: {get_email}\npassword: {get_password}"
                                                               f"\n\npassword copied ")
            pyperclip.copy(get_password)

        except KeyError as website_entered:
            messagebox.showerror(title="error", message=f"no email/password saved for {website_entered}")

        except FileNotFoundError:
            messagebox.showerror(title="error", message="datafile has not been created.\n create data file first.")
        else:
            pass

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password manager")
window.config(padx=50, pady=50)
canvas = Canvas(height=200, width=200)
password_image = PhotoImage(file="images/logo.png")
my_image = canvas.create_image(100, 100, image=password_image)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

website_entry = Entry(width=25)
website_entry.grid(row=1, column=1)

email_username = Label(text="Email/Username:")
email_username.grid(row=2, column=0)

email_entry = Entry(width=25)
email_entry.insert(0, string="shubham@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)

password_user = Label(text="Password:")
password_user.grid(row=3, column=0)

password_entry = Entry(width=25)
password_entry.grid(row=3, column=1)

password_generate = Button(text="Generate", command=create_password)
password_generate.grid(row=3, column=3)

add_password = Button(text="add", command=password_save)
add_password.grid(row=4, column=1)

search = Button(text="Search", command=search_password)
search.grid(row=1, column=3)

window.mainloop()
