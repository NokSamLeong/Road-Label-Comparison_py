import tkinter as tk
import tkinter.messagebox as mb
import Backend
import ctypes

user = ctypes.windll.user32
screenW = user.GetSystemMetrics(0)
screenH = user.GetSystemMetrics(1)
be = Backend.Backend()
current = be.get_next()


def next_action():
    global current
    if not be.is_stop_record():
        if not be.is_any_checked():     # if not checkbox including none is checked
            mb.showerror(title="fail attempt",
                         message="Please select none or at least one image")
        else:
            # save to excel
            try:
                comment = text_field_var.get()
                be.write_in(comment)
            except IOError:
                mb.showerror(title="Error", message="Unable to write in result")
            # reset checkbox
            for checkbox in checkbox_list:
                checkbox.deselect()
            none.deselect()
            current = be.get_next()
            change_status()
            change_label()
            check_none.set(be.isNone)
            if len(current) == 0:
                label_text.set("Finish")
                for checkbox in checkbox_list:
                    checkbox.text = ""
                text_field_var.set("Finish")
            else:
                label_text.set(be.get_key())
                text_field_var.set(be.get_key())
    else:
        mb.showerror(title="Finish", message="finished all data")


def click_event():  # load in data
    for i in range(len(be.checkboxBoo)):
        be.checkboxBoo[i] = bool(checkbox_status[i].get())


def change_status():  # restore data
    for i in range(len(be.checkboxBoo)):
        checkbox_status[i].set(be.checkboxBoo[i])


def change_label():
    for cb in range(len(checkbox_list)):
        if cb < len(current):
            checkbox_string[cb].set(current[cb][0:-4])
        else:
            checkbox_string[cb].set("")


def close():
    if mb.askyesno("Delete file", "Do you want to delete the images you already judged?"):
        be.delete_image()
        window.destroy()
    else:
        window.destroy()


def pre_action():
    global current
    if be.is_any_checked():
        try:
            be.write_in(text_field_var.get())
        except IOError:
            mb.showerror(title="Error", message="Unable to write in result")
    #try:
    current = be.get_pre()
    #except TypeError as e:
       # print(e)
    #mb.showerror(title="fail attempt", message="type error Unable to access the previous set")
    if not current:
        mb.showerror(title="fail attempt", message="Unable to access the previous set or no previous set")
    else:
        check_none.set(be.isNone)
        change_label()
        change_status()
        label_text.set(be.get_key())
        if not be.get_commend() == "":
            text_field_var.set(be.get_commend())
        else:
            text_field_var.set(be.get_key())


window = tk.Tk()
window.protocol("WM_DELETE_WINDOW", close)
frame = tk.Frame(window, height=screenH/2, width=screenW/2)
frame.pack()
checkbox_string = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
checkbox_status = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
checkbox_list = [tk.Checkbutton(window, textvariable=checkbox_string[0], command=click_event, variable=checkbox_status[0]),
                 tk.Checkbutton(window, textvariable=checkbox_string[1], command=click_event, variable=checkbox_status[1]),
                 tk.Checkbutton(window, textvariable=checkbox_string[2], command=click_event, variable=checkbox_status[2]),
                 tk.Checkbutton(window, textvariable=checkbox_string[3], command=click_event, variable=checkbox_status[3])]
check_none = tk.IntVar()
none = tk.Checkbutton(window, text="none", variable=check_none, command=be.change_none)
change_label()
for num in range(len(checkbox_list)):
    checkbox_list[num].pack()
    checkbox_list[num].place(relx=0.1, rely=num*0.09 + 0.3)
none.pack()
none.place(relx=0.1, rely=len(checkbox_list)*0.09 + 0.3)

# label
label_text = tk.StringVar()
label_text.set(be.get_key())
keyLabel = tk.Label(textvariable=label_text, width=19, font=('arial', 10), anchor='center')
keyLabel.pack()
keyLabel.place(relx=0.4, rely=0.03)
label_comment = tk.StringVar()
label_comment.set("Comment")
commentLabel = tk.Label(textvariable=label_comment, width=10, font=('arial', 10), anchor='w')
commentLabel.pack()
commentLabel.place(relx=0.1, rely=0.75)
# key text
text_field_var = tk.StringVar()
txt = tk.Entry(window, textvariable=text_field_var, width=100)
text_field_var.set(be.get_key())
txt.pack()
txt.place(relx=0.1, rely=0.83)

# button
gobackButton = tk.Button(width=20, height=3, text="<<", command=pre_action)
gobackButton.pack()
gobackButton.place(relx=0.2, rely=0.1)

openButton = tk.Button(width=20, height=3, text="Open", command=be.open_image)
openButton.pack()
openButton.place(relx=0.4, rely=0.1)

nextButton = tk.Button(width=20, height=3, text=">>", command=next_action)
nextButton.pack()
nextButton.place(relx=0.6, rely=0.1)

window.mainloop()
