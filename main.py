from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledFrame
import customtkinter as ctk
import json

contact_list = dict()
contact_Book = []


def update_dict():
    global contact_list
    try:
        contact_file = open("contacts.json", 'r')
    except:
        contact_file = open("contacts.json", 'w')
        contact_file.close()
    else:
        contact_list = json.load(contact_file)
        contact_file.close()


def update_json():
    contact_file = open("contacts.json", 'w')
    json.dump(contact_list, contact_file, indent=1)
    contact_file.close()


update_dict()


class Contact:
    def __init__(self, master, name, number, email, address):
        self.top_frame = Frame(root, height=760, width=520)
        self.master = master
        self.name = StringVar(value=name.title())
        try:
            self.f_name = StringVar(value=self.name.get().split(" ")[0])
            self.l_name = StringVar(value=self.name.get().split(" ")[1])
        except:
            self.f_name = StringVar(value=self.name.get())
            self.l_name = StringVar(value="")
        self.number = StringVar(value=number)
        self.email = StringVar(value=email)
        self.address = StringVar(value=address)

        self.main_frame = Button(self.master, text="\n"*2, width=80, style="light", command=self.view,)
        self.main_frame.pack()

        Label(self.main_frame, textvariable=self.name, font=("Dubai medium", 14, "bold"), style="warning", justify="left").place(x=20, y=0)
        Label(self.main_frame, textvariable=self.number, font=("dubai", 10), style="info").place(x=45, y=27)
        Frame(self.main_frame, width=445, height=0, style="secondary").place(y=50, anchor="center", x=243)
        self.delete_btn = Button(self.main_frame, text="🗑", command=self.delete, style="danger-outline")
        self.delete_btn.place(x=430, y=10)

    def view(self, new=0):
        self.top_frame = Frame(root, height=750, width=520)
        self.top_frame.place(x=0, y=0)

        entries = []
        temps = []
        labels = {
            "First Name": self.f_name,
            "Last Name": self.l_name,
            "Phone Number": self.number,
            "Email Address": self.email,
            "Home Address": self.address
        }

        def back():
            if back_btn.cget("text") == "❎":
                if new and self.f_name.get() == "" and self.l_name.get() == "":
                    contact_list.pop(self.name.get())
                    contact_Book.remove(self)
                    update_json()
                    self.top_frame.destroy()
                    return 0

                for entry in entries:
                    entry.configure(text_color="gray", state="disabled", border_color="gray",)

                edit_btn.configure(text="🖋️", text_color="black", fg_color="#F8F9FA", hover_color="#F8F9FA")
                back_btn.configure(text="🔙", text_color="black", fg_color="#F8F9FA", hover_color="#F8F9FA")

                for i, var in enumerate(labels.values()):
                    var.set(temps[i])

            else:
                self.top_frame.destroy()
                reload()

        def edit():
            if edit_btn.cget("text") == "✅":
                if new and self.f_name.get() == "" and self.l_name.get() == "":
                    contact_list.pop(self.name.get())
                    contact_Book.remove(self)
                    update_json()
                    self.top_frame.destroy()
                    return 0

                temp = self.name.get()
                self.name.set(value=f"{self.f_name.get()} {self.l_name.get()}".title())
                contact_list.pop(temp)
                contact_list[self.name.get()] = [self.number.get(), self.email.get(), self.address.get()]

                for entry in entries:
                    entry.configure(text_color="gray", state="disabled", border_color="gray")

                edit_btn.configure(text="🖋️", text_color="black", fg_color="#F8F9FA", hover_color="#F8F9FA")
                back_btn.configure(text="🔙", text_color="black", fg_color="#F8F9FA", hover_color="#F8F9FA")
                update_json()

            else:
                for entry in entries:
                    temps.append(entry.get())
                    entry.configure(state="normal", text_color="black", border_color="#02b875")

                edit_btn.configure(text="✅", text_color="#02b875")
                back_btn.configure(text="❎", text_color="red", fg_color="#F8F9FA", hover_color="#F8F9FA")

        back_btn = ctk.CTkButton(self.top_frame, text="🔙", command=back, height=50, width=50, font=("dubai", 20), text_color="black", fg_color="#F8F9FA", hover_color="#F8F9FA")
        back_btn.place(x=10, y=10)
        edit_btn = ctk.CTkButton(self.top_frame, text="🖋️️", command=edit, height=50, width=50, font=("dubai", 20), text_color="black", fg_color="#F8F9FA", hover_color="#F8F9FA")
        edit_btn.place(x=450, y=10)

        y = 150

        for label, variable in labels.items():
            ctk.CTkLabel(self.top_frame, text=label, font=("dubai", 20, "bold"), text_color="#f0ad4e").place(x=50, y=y)
            entries.append(ctk.CTkEntry(self.top_frame, textvariable=variable, fg_color="#F8F9FA", font=("dubai", 20), width=250, text_color="gray", state="disabled", border_color="gray"))
            entries[-1].place(x=200, y=y)
            y += 100

        if new:
            for entry in entries:
                temps.append(entry.get())
                entry.configure(state="normal", text_color="black", border_color="#02b875")

            edit_btn.configure(text="✅", text_color="#02b875")
            back_btn.configure(text="❎", text_color="red", fg_color="#F8F9FA", hover_color="#F8F9FA")

    def delete(self):
        self.delete_btn.config(state="disabled")
        temp = Frame(self.main_frame, width=200, height=100)
        temp.place(x=200)
        Label(temp, text="Delete this Contact?").pack()

        def undo():
            temp.destroy()
            self.delete_btn.config(state="normal")

        def do():
            contact_list.pop(self.name.get())
            update_json()
            self.main_frame.destroy()
            reload()

        Button(temp, text="No", style="success", command=undo).pack(side=LEFT)
        Button(temp, text="Yes", style="danger", command=do).pack(side=RIGHT)


root = Window(size=(520, 770), title="My Contact",)
root.iconbitmap("./logo.ico")


def load(name="", number=""):
    global contact_frame
    contact_frame.destroy()
    contact_frame = Frame(mid, height=550, width=500)
    contact_frame.pack()
    temp = dict()
    if name:
        for nm, contact in contact_list.items():
            if nm.lower() in name.lower() or name.lower() in nm.lower():
                temp[nm] = contact

    if number:
        for nm, contact in contact_list.items():
            if number in contact[0] or contact[0] in number:
                temp[nm] = contact

    if not name and not number:
        temp = contact_list

    if temp:
        sortedNames = sorted(temp.keys())
        for name in sortedNames:
            contact_Book.append(Contact(contact_frame, name, contact_list[name][0], contact_list[name][1], contact_list[name][2]))

    else:
        Label(contact_frame, text="No contact found ", style="dark").pack()

    count.set(f"{len(temp)} contacts found ")


search_value = StringVar(root)


top = Frame(root, width=500, height=100)
top.pack(pady=5)
Label(top, text="MY CONTACT", style="warning", font=("Arial black", 42)).pack()

count = StringVar(value="0 contacts found ")
bar = Frame(root)
bar.pack()
Label(bar, textvariable=count, style="dark").pack(side=LEFT)
Frame(bar, width=350, height=1, style="secondary").pack(pady=20)

mid = ScrolledFrame(root, height=550, width=500)
mid.pack()

contact_frame = Frame(mid, height=550, width=500)
contact_frame.pack()

footer = Frame(root, width=550, style="dark",)
footer.pack(side=BOTTOM)
Label(footer, text="©2024 Seiyaf Ahmed ", style="inverse-dark", justify="right",).pack(padx=201)


def reload(a=None):
    global contact_frame
    contact_frame.destroy()
    contact_frame = Frame(root, height=600, style="success")
    contact_frame.pack()
    try:
        temp = int(search_value.get())
    except:
        load(search_value.get())
    else:
        load("", search_value.get())


Button(top, text="🔍", style="success", command=reload,).pack(side=LEFT)
search = Entry(top, width=60, style="success", textvariable=search_value)
search.bind("<KeyRelease>", reload)
search.pack()


def add():
    contact_Book.append(Contact(contact_frame, "", "", "", ""))
    contact_list[""] = ["-", "-", "-"]
    update_json()
    contact_Book[-1].view(1)


ctk.CTkButton(root, text="➕", width=30, height=50, corner_radius=500, fg_color="#02b875", hover_color="#02a875", command=add).place(x=425, y=690)

load()

root.mainloop()
