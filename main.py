#!/usr/bin/env python3

import os
import sys
import tkinter as tk
from tkinter import messagebox

from scripts import decryptor, encryptor, rpg

# ********************************* GLOBALS ***********************************
PATH = sys.path[0]

PASSWD = os.path.join(PATH, ".pw")
if not os.path.isfile(PASSWD):
    print("WELCOME!")
    try:
        new_pas = input("Enter new root password: ")
        encryptor.encrypt_to_file(PASSWD, new_pas, "somesaltyjuicer")
    except KeyboardInterrupt:
        print("\nBye.")
        sys.exit(0)

DB_PATH = os.path.join(PATH, ".db")
if not os.path.exists(DB_PATH):
    os.mkdir(DB_PATH)

# TODO: "somesaltyjuicer" could/should be changed/decided somehow
access = decryptor.decrypt_from_file(PASSWD, "somesaltyjuicer")

# Customizing root
main_font = ("Arial", 14)  # 10 fonts
button_font = ("Arial", 14)  # font of 3 Buttons on main window
listbox_item_font = ("Arial", 14)  # font of listbox items

MAIN_COLOR = "#ACC0D5"  # status, infolabel and  midframe color

DEL_BTN_COLOR = "#800000"
SHOW_BTN_COLOR = "#364B61"
ADD_BTN_COLOR = "#F5F5F5"
GENERATE_BTN_COLOR = "#56A656"
HIGHLIGHT_COLOR = "#A1B0BC"

pW_width, pW_height, pW_x, pW_y = (215, 117, 550, 200)  # popupWindow geometry
mr_width, mr_height, mr_x, mr_y = (400, 570, 500, 30)  # Main Root geometry
aW_width, aW_height, aW_x, aW_y = (420, 187, 500, 200)  # addWindows geometry
npcw_width, npcw_height, npcw_x, npcw_y = (
    215, 100, 550, 200)  # NameOrPasChangeWindow geometry


# ********************************* CLASSES ***********************************
class PopupWindow:

    attempts = 0

    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        top.title("")
        top.geometry("{}x{}+{}+{}".format(pW_width, pW_height, pW_x, pW_y))
        top.resizable(width=False, height=False)
        icon1 = tk.PhotoImage(
            file=os.path.join(PATH, "img", "icon3.png")
        )
        top.tk.call("wm", "iconphoto", top._w, icon1)
        top.focus_force()
        self.popup_window_label = tk.Label(
            top, text=" Password: ",
            font=("Bitstream Vera Serif", 15),
            justify=tk.CENTER
        )
        self.popup_window_label.pack(pady=3)
        self.popup_window_entry = tk.Entry(top, show="*", width=25, bd=3)
        self.popup_window_entry.pack(pady=7)
        self.popup_window_entry.bind("<Return>", self.cleanup)
        self.b = tk.Button(
            top, text="Submit", command=self.cleanup, font=main_font, bd=2
        )
        self.b.pack(pady=3)
        self.popup_window_entry.focus()
        # do after close button pressed
        top.protocol("WM_DELETE_WINDOW", self.on_closing)

    def cleanup(self, event=None):
        self.value = self.popup_window_entry.get()
        if self.value:
            if self.value == access:
                self.top.destroy()
                root.deiconify()
            else:
                self.attempts += 1
                if self.attempts == 3:
                    root.quit()
                self.popup_window_entry .delete(0, "end")
                messagebox.showerror(
                    "Incorrect Password", "Wrong password!\nRemaining attempts: "
                    + str(3 - self.attempts)
                )
                self.top.focus_force()
                self.popup_window_entry.focus()

    def on_closing(self):
        self.top.destroy()
        root.destroy()


class AddWindow:

    def __init__(self, master):
        root.withdraw()
        window = self.window = tk.Toplevel(master)
        window.title("Account List")
        window.geometry("{}x{}+{}+{}".format(aW_width, aW_height, aW_x, aW_y))
        window.resizable(width=False, height=False)
        icon2 = tk.PhotoImage(
            file=os.path.join(PATH, "img", "icon3.png")
        )
        window.tk.call("wm", "iconphoto", window._w, icon2)
        window.focus_force()

        self.head_label = tk.Label(
            window, text="New Account", font=("Bitstream Vera Serif", 18))
        self.accname_label = tk.Label(window, text="Name: ", font=main_font)
        self.login_label = tk.Label(window, text="Login: ", font=main_font)
        self.passw_label = tk.Label(window, text="Password: ", font=main_font)
        self.accname = tk.Entry(window, font=main_font, bd=2, width=30)
        self.login = tk.Entry(window, font=main_font, bd=2, width=30)
        self.password = tk.Entry(window, font=main_font, bd=2, width=30)
        # Binding Enter to do same as add button
        self.password.bind("<Return>", self.addacc_command)
        self.generate_b = tk.Button(window, text="Generate", command=self.generate_command,
                                    font=main_font, bg=GENERATE_BTN_COLOR, bd=3, padx=10, pady=8)
        self.generate_b.config(highlightbackground=HIGHLIGHT_COLOR)
        self.submit_b = tk.Button(window, text="Add", command=self.addacc_command,
                                  font=main_font, bg="white", bd=3, padx=40, pady=8)
        self.submit_b.config(highlightbackground=HIGHLIGHT_COLOR)

        self.head_label.grid(columnspan=2, row=0)
        self.accname_label.grid(row=1, sticky=tk.E, padx=5)
        self.login_label.grid(row=2, sticky=tk.E, padx=5)
        self.passw_label.grid(row=3, sticky=tk.E, padx=5)

        self.accname.grid(row=1, column=1, padx=5, pady=2)
        self.login.grid(row=2, column=1, padx=5, pady=2)
        self.password.grid(row=3, column=1, padx=5, pady=2)

        self.submit_b.grid(row=4, column=1, sticky=tk.E, padx=5, pady=4)
        self.generate_b.grid(row=4, column=1, sticky=tk.W, padx=5, pady=4)

        self.accname.focus()

        # do after close button pressed
        window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def addacc_command(self, event=None):
        name = self.accname.get()
        log = self.login.get()
        pas = self.password.get()
        if name and log and pas:
            self.accname.delete(0, "end")
            self.login.delete(0, tk.END)
            self.password.delete(0, "end")
            line1 = "Login: " + log
            line2 = "Password: " + pas
            txtfile = os.path.join(DB_PATH, name + "Acc.txt")
            with open(txtfile, "w") as file:
                file.write(f"{line1}\n{line2}")
            encryptor.encrypt_file(txtfile, access)
            messagebox.showinfo(
                "Success", "{} was successfuly added!".format(name))
            self.window.focus_force()
            self.accname.focus()

    def generate_command(self):
        newpw = rpg.generate_password()
        self.password.delete(0, "end")
        self.password.insert(0, newpw)

    def on_closing(self):
        self.window.destroy()
        root.deiconify()
        update_listbox()
        status_bar.config(text="")


class NameOrPasChangeWindow:

    def __init__(self, master, oldname=""):
        root.withdraw()
        if oldname:
            self.oldname = oldname
            self.oldpather = oldname + "Acc.txt"
        popWin = self.popWin = tk.Toplevel(root)
        if oldname:
            popWin.title("Rename")
        else:
            popWin.title("New Password")
        popWin.geometry("{}x{}+{}+{}".format(npcw_width,
                        npcw_height, npcw_x, npcw_y))
        popWin.resizable(width=False, height=False)
        icon3 = tk.PhotoImage(file=os.path.join(
            PATH, "img", "icon3.png"))  # Icon
        popWin.tk.call("wm", "iconphoto", popWin._w, icon3)
        popWin.focus_force()
        if oldname:
            what = "Account Name"
        else:
            what = "Password"

        self.h_label = tk.Label(
            popWin, text=f"Enter new {what}", font=main_font)
        self.h_label.pack()
        self.en_box = tk.Entry(popWin, width=25, bd=3, font=main_font)
        if oldname:
            self.en_box.insert(0, oldname)
        self.en_box.pack(padx=5)
        # binding Enter to same Button function
        self.en_box.bind("<Return>", self.adname)
        self.en_box.focus()
        self.btn = tk.Button(popWin, text="Submit", font=main_font, bd=2)
        if oldname:
            self.btn.config(command=self.adname)
        else:
            self.btn.config(command=self.changepass)
        self.btn.pack(side="right")

        # do after close button pressed
        popWin.protocol("WM_DELETE_WINDOW", self.on_closing)

    def adname(self, event=None):
        enteredname = self.en_box.get()
        if enteredname:
            self.en_box.delete(0, "end")
            pather2file = os.path.join(DB_PATH, self.oldpather)
            os.rename(pather2file, os.path.join(
                DB_PATH, enteredname + "Acc.txt"))
            ok = messagebox.showinfo(
                "Success", f"{self.oldname} was successfuly changed to {enteredname}")
            if ok == "ok":
                self.on_closing()

    def changepass(self):
        enteredpass = self.en_box.get()
        if enteredpass:
            self.en_box.delete(0, "end")
            with open(os.path.join(PATH, ".pw.txt"), "w") as f:
                f.write(enteredpass)
            encryptor.encrypt_file(os.path.join(
                PATH, ".pw.txt"), "somesaltyjuicer")
            ok = messagebox.showinfo("Success", "Password updated successfuly")
            if ok == "ok":
                self.on_closing()

    def on_closing(self):
        self.popWin.destroy()
        root.deiconify()
        update_listbox()
        status_bar.config(text="")


# ******************************** FUNCTIONS **********************************
def update_listbox():
    listbox.delete(0, "end")
    accs = os.listdir(DB_PATH)
    accs.sort()  # making alphabetic order
    if accs:
        menubar.entryconfig("Password", state="disabled")
        for a in accs:
            a = a.split(".")[0][:-3]
            listbox.insert(tk.END, a)
            del_button["state"] = "normal"
            show_button["state"] = "normal"

    else:
        del_button.config(state=tk.DISABLED)
        show_button.config(state=tk.DISABLED)
        menubar.entryconfig("Password", state=tk.NORMAL)


def update_status(event=None):
    tup = listbox.curselection()
    if tup:
        len_accs = len(os.listdir(DB_PATH))
        texnum = tup[0] + 1
        status_bar.config(text=f"{texnum} of {len_accs}")
        info_label.config(text="")


def show_info():
    accs = os.listdir(DB_PATH)
    accs.sort()
    tup = listbox.curselection()
    if tup:
        accname = listbox.get(tup[0])
        txtfile = os.path.join(DB_PATH, accname + "Acc.txt")
        data = decryptor.decrypt_from_file(txtfile, access)
        info_label["text"] = data


def delete_acc():
    tup = listbox.curselection()
    if tup:
        answer = messagebox.askquestion(
            "Delete", "Are you sure you want to delete this account?")
        if answer == "yes":
            currentselection = tup[0]
            filepth = os.path.join(DB_PATH, listbox.get(
                currentselection) + "Acc.txt")
            os.remove(filepth)
            update_listbox()
            status_bar.config(text="")


def rename_entry():
    tup = listbox.curselection()
    if tup:
        currentselection = tup[0]
        oldname = listbox.get(currentselection)
        NameOrPasChangeWindow(root, oldname=oldname)
    else:
        messagebox.showinfo("Choose Item", "You need to select an Account.")


def change_main_pass():
    NameOrPasChangeWindow(root)


# *********************************** DRAW ************************************
# Defining root
root = tk.Tk()
root.title("Password Manager")  # Title
icon = tk.PhotoImage(file=os.path.join(PATH, "img", "icon3.png"))  # Icon
root.tk.call("wm", "iconphoto", root._w, icon)
root.geometry("{}x{}+{}+{}".format(400, 570, 500, 30))
root.resizable(width=False, height=False)  # not resizable
root.withdraw()


pW = PopupWindow(root)  # the main passw windows

root.focus_force()


# ------------------
# Menu Bar

menubar = tk.Menu(root)
root.config(menu=menubar)

# File item
file_menu = tk.Menu(menubar)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Rename", command=rename_entry)
file_menu.add_command(label="Edit")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Option item
option_menu = tk.Menu(menubar)
menubar.add_cascade(label="Options", menu=option_menu, state="disabled")
# changes whole status, infolabel and midframe colors
option_menu.add_command(label="Change Font")
option_menu.add_command(label="Change Background Color")
option_menu.add_command(label="Change Add Account Button Color")
option_menu.add_command(label="Change Show Button Color")
option_menu.add_command(label="Change Delete Button Color")


# TODO: fix this
# Change Password item
change_pass_menu = tk.Menu(menubar)
menubar.add_cascade(label="Password", menu=change_pass_menu)
change_pass_menu.add_command(label="EDIT", command=change_main_pass)


# ------------------
# Frames
top_frame = tk.LabelFrame(root)
top_frame.pack()
mid_frame = tk.LabelFrame(root, bg=MAIN_COLOR)
mid_frame.pack()
bot_frame = tk.LabelFrame(root)
bot_frame.pack()

# Top Frame
scrollbar = tk.Scrollbar(top_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox = tk.Listbox(top_frame, width=40, height=15,
                     font=listbox_item_font, yscrollcommand=scrollbar.set)
# listbox.config(selectmode=tk.SINGLE) for single choice in lisstbox
listbox.bind("<<ListboxSelect>>", update_status)
listbox.pack()
scrollbar.config(command=listbox.yview)

# Middle Frame
del_button = tk.Button(mid_frame, text="Delete", font=button_font,
                       bg=DEL_BTN_COLOR, fg="white", bd=3, command=delete_acc)
del_button.pack(side="left", ipadx=15, ipady=7, padx=(1, 4))
show_button = tk.Button(mid_frame, text="Show", font=button_font,
                        bd=3, bg=SHOW_BTN_COLOR, fg="white", command=show_info)
show_button.pack(side="left", ipadx=15, ipady=7)
add_button = tk.Button(mid_frame, text="Add Account", font=button_font,
                       bg=ADD_BTN_COLOR, bd=3, command=lambda: AddWindow(root))
add_button.config(highlightbackground=HIGHLIGHT_COLOR)
add_button.pack(side="left", ipadx=15, ipady=7, padx=(31, 1))

# Bottom Frame
info_label = tk.Label(bot_frame, width=50, height=6,
                      justify=tk.LEFT, bg=MAIN_COLOR, font=("Arial", 16))
info_label.pack()

status_bar = tk.Label(root, bd=1, relief=tk.SUNKEN, anchor=tk.E, bg=MAIN_COLOR)
status_bar.pack(fill=tk.BOTH)

update_listbox()


# Looping the root
root.mainloop()
