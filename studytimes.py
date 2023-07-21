#/bin/python3
import tkinter as tk
from tkinter import ttk,Menu,messagebox
from tkinter.filedialog import asksaveasfile,askopenfilename
import datetime
import os

root = tk.Tk()
root.title("Study Times")

time_entry = tk.Entry(root, state="disabled", justify="center")
time_entry.grid(row=0, column=0, columnspan=2, sticky="nsew")

def get_time():
    time_entry.configure(state="normal")
    time_entry.delete(0, tk.END)
    time_entry.insert(0,datetime.datetime.now().strftime('%y/%m/%d %a'))
    time_entry.configure(state="disabled")
get_time()

goal=8

def setting():
	def save_changes():
		global goal
		goal=int(goal_entry.get())
		popup.destroy()
		update_total()
	popup=tk.Tk()
	popup.title("Setting")
	tk.Label(popup,text="your goal(hours):").grid(row=0,column=0)
	goal_entry=tk.Entry(popup)
	goal_entry.grid(row=0,column=1)
	goal_entry.insert(0,goal)
	submit_button=tk.Button(popup, text="Save changes",command=save_changes,bg="red")
	submit_button.grid(row=10,column=1,pady=(20,0))
	
columns = ("Time(minutes)","Subject")
table = ttk.Treeview(root, columns=columns, show="headings", height=10)
vsb = ttk.Scrollbar(orient="vertical",command=table.yview)
table.column("Time(minutes)", anchor="center")
table.column("Subject", anchor="center")
table.heading("Time(minutes)", text="Time(minutes) ")
table.heading("Subject", text="Subject")
table.grid(row=1, column=0, columnspan=2)
vsb.grid(row=1, column=2, sticky="nsew")
table.configure(yscrollcommand=vsb.set)

goal_chart = ttk.Progressbar(root,length=100)
goal_chart.grid(row=2, column=0, columnspan=2, sticky="nsew")

def get_total():
    total = 0
    for child in table.get_children():
        total += int(table.item(child)["values"][0])
    return total
total_label = tk.Label(root, text="Total(minutes): 0")
total_label.grid(row=3, column=1)
total_hour = tk.Label(root, text="Total(hours): 0:0")
total_hour.grid(row=4, column=1)
def update_total():
    total_label.config(text=f"Total(minutes): {get_total()}")
    total_hour.config(text=f'Total(hours): {get_total()//60}:{get_total()%60}')
    goal_chart["value"]=0
    goal_chart.step((get_total()/60/goal*99.99))


def add_item():
    minutes_v = int(minutes_entry.get())
    subject_v = subject_entry.get()
    table.insert("", tk.END, values=(minutes_v,subject_v))
    minutes_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    update_total()
root.bind('<Return>', lambda e: add_item())

def clear_all():
    box_stat = tk.messagebox.askquestion(title="Warning", message='Are you sure you want to clear all?')
    if box_stat == 'yes':
        minutes_entry.delete(0, tk.END)
        subject_entry.delete(0, tk.END)
        for item in table.get_children():
            table.delete(item)
        update_total()
def clear_all_direct():
	minutes_entry.delete(0, tk.END)
	subject_entry.delete(0, tk.END)
	for item in table.get_children():
		table.delete(item)
	update_total()
    
def exit_app():
    box_stat = tk.messagebox.askquestion(title="Warning", message='Are you sure you want to exit the application?')
    if box_stat == 'yes':
        exit()
        
def delete_item():
    box_stat = tk.messagebox.askquestion(title="Warning", message='Are you sure you want to delete this?')
    if box_stat == 'yes':
    	selected_item = table.selection()[0]
    	table.delete(selected_item)
    	update_total()

def edit_item():
    def save_changes():
        selected_item = table.selection()[0]
        table.item(selected_item, values=(min_entry.get(), sub_entry.get()))
        popup.destroy()

    popup = tk.Tk()
    popup.title("Edit")
    selected_item = table.item(table.selection())["values"]
    tk.Label(popup, text="Time(minutes): ").grid(row=0, column=0)
    tk.Label(popup, text="Subject: ").grid(row=1, column=0)
    min_entry = tk.Entry(popup)
    min_entry.grid(row=0, column=1)
    sub_entry = tk.Entry(popup)
    sub_entry.grid(row=1, column=1)
    min_entry.insert(0, selected_item[0])
    sub_entry.insert(0, selected_item[1])
    submit_button = tk.Button(popup, text="Save changes", command=save_changes, bg="green")
    submit_button.grid(row=3, column=1, pady=(20, 0))
    
#set the entries, add & delete & quit button
table2 = ttk.Treeview(root, columns=("Time(minutes)","Subject"), show="headings", height=0)
table2.column("Time(minutes)", anchor="center")
table2.column("Subject", anchor="center")
table2.heading("Time(minutes)", text="Time(minutes)")
table2.heading("Subject", text="Subject")
table2.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=(40,0))
#tk.Label(root).grid(row=3,pady=20)
minutes_entry = tk.Entry(root)
minutes_entry.grid(row=6, column=0)
subject_entry = tk.Entry(root)
subject_entry.grid(row=6, column=1)
add_button = tk.Button(root, text="Add", command=add_item, background="green")
add_button.grid(row=7, column=0, columnspan=2, sticky="nsew") 
delete_button = tk.Button(root, text="Delete", command=delete_item, background="black", foreground="white")
delete_button.grid(row=8, column=0, columnspan=2, sticky="nsew")

def get_save():
    file = open(f'database/{datetime.datetime.now().strftime("%y%m%d")}.txt',mode='w')
    file.write(time_entry.get()+'\n')
    for child in table.get_children():
        for i in table.item(child)["values"]:
            file.write(str(i)+'\t\t')
        file.write('\n')
    file.write(str(f'{get_total()}'))
    file.close()

def get_open():
    file = open(askopenfilename(initialfile = f'database/{datetime.datetime.now().strftime("%y%m%d")}.txt', defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")]), mode='r')
    clear_all()
    time_entry.configure(state="normal")
    time_entry.delete(0, tk.END)
    time_entry.insert(0,file.readline().replace('\n',''))
    time_entry.configure(state="disabled")
    for i in file.readlines():
        if True:
            new_item_list=[]
            item_list = i.split("\t\t")
            for x in item_list:
                new_item_list.append(x.replace('\n',''))
            if len(new_item_list)>1:
                table.insert("", tk.END, values=(new_item_list))
    file.close()
    update_total()

def create_new():
    box_stat = tk.messagebox.askquestion(title="Warning", message='Do you want to save this receipt?')
    if box_stat == 'yes':
        get_save()
        minutes_entry.delete(0, tk.END)
        subject_entry.delete(0, tk.END)
        for item in table.get_children():
            table.delete(item)
        get_time()
    else:
        clear_all()
        get_time()

def per_day():
	if int(datetime.datetime.now().strftime("%d"))>1:
		fn=str(int(time_entry.get()[0:8].replace('/',''))-1)
		try:
			file=open(f'database/{fn}.txt',mode='r')
			clear_all_direct()
			time_entry.configure(state="normal")
			time_entry.delete(0, tk.END)
			time_entry.insert(0,file.readline().replace('\n',''))
			time_entry.configure(state="disabled")
			for i in file.readlines():
				new_item_list=[]
				item_list = i.split("\t\t")
				for x in item_list:
				          new_item_list.append(x.replace('\n',''))
				if len(new_item_list)>1:
					table.insert("", tk.END, values=(new_item_list))
				file.close()
				update_total()
		except:
			error=True

def nex_day():
	if int(datetime.datetime.now().strftime("%d"))<31:
		fn=str(int(time_entry.get()[0:8].replace('/',''))+1)
		try:
			file=open(f'database/{fn}.txt',mode='r')
			clear_all_direct()
			time_entry.configure(state="normal")
			time_entry.delete(0, tk.END)
			time_entry.insert(0,file.readline().replace('\n',''))
			time_entry.configure(state="disabled")
			for i in file.readlines():
				new_item_list=[]
				item_list = i.split("\t\t")
				for x in item_list:
				          new_item_list.append(x.replace('\n',''))
				if len(new_item_list)>1:
					table.insert("", tk.END, values=(new_item_list))
				file.close()
				update_total()
		except:
			error=True


# Create the "<" and ">" buttons
prev_day_button = tk.Button(root, text="<", command=per_day)
prev_day_button.grid(row=11, column=0, sticky="nsew")
root.bind('<Control-k>', lambda e: per_day())
next_day_button = tk.Button(root, text=">", command=nex_day)
next_day_button.grid(row=11, column=1, sticky="nsew")
root.bind('<Control-l>', lambda e: nex_day())
quit_button = tk.Button(root, text="Quit", command=exit_app, background='red')
quit_button.grid(row=12, column=0, columnspan=2, sticky="nsew")

def about_page():
    import webbrowser
    message = "This program was created by Mobin Babaee using Python and the Tkinter library.\n\nThank you for using this program!\n\nPlease check out the GitHub repository for the latest updates and to report issues:\n\n"
    link = "https://github.com/mobinbabaee/sales-receipt"
    result = messagebox.askquestion("About", message+"Would you like to go to the GitHub repository?", icon="info")
    if result == "yes":
        webbrowser.open_new(link)

#set the menu bar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=create_new)
root.bind('<Control-n>', lambda e: create_new())
filemenu.add_command(label="Open", command=get_open)
root.bind('<Control-o>', lambda e: get_open())
filemenu.add_command(label="Save", command=get_save)
root.bind('<Control-s>', lambda e: get_save())
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_app)
root.bind("<Escape>", lambda e: exit_app())
root.bind("<Alt-x>", lambda e: exit_app())
root.bind("<Control-q>", lambda e: exit_app())
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Clear all", command=clear_all)
editmenu.add_command(label="Update Time", command=get_time)
editmenu.add_command(label="Update Total",command=update_total)
root.bind('<Control-r>', lambda e: get_time())
editmenu.add_command(label="Edit",command=edit_item)
root.bind('<Control-e>', lambda e: edit_item())
editmenu.add_command(label="Delete", command=delete_item)
root.bind('<Delete>', lambda e: delete_item())
menubar.add_cascade(label="Edit", menu=editmenu)

setmenu = Menu(menubar, tearoff=0)
setmenu.add_command(label="Setting", command=setting)
setmenu.add_command(label="About...", command=about_page)
menubar.add_cascade(label="Options", menu=setmenu)

root.config(menu=menubar)

#start with today's time
if not os.path.exists("database"):
    os.makedirs("database")
try:
	file=open(f'database/{datetime.datetime.now().strftime("%y%m%d")}.txt',mode='r')
	time_entry.configure(state="normal")
	time_entry.delete(0, tk.END)
	time_entry.insert(0,file.readline().replace('\n',''))
	time_entry.configure(state="disabled")
	for i in file.readlines():
	           if True:
	           	new_item_list=[]
	           	item_list = i.split("\t\t")
	           	for x in item_list:
	           		new_item_list.append(x.replace('\n',''))
	           	if len(new_item_list)>1:
	           		table.insert("", tk.END, values=(new_item_list))
	file.close()
	update_total()
except:
	file=open(f'database/{datetime.datetime.now().strftime("%y%m%d")}.txt',mode='w')
	file.write(time_entry.get()+'\n')
	for child in table.get_children():
	           for i in table.item(child)["values"]:
	           	file.write(str(i)+'\t\t')
	           file.write('\n')
	file.write(str(f'{get_total()}'))
	file.close()

# Start the Tkinter event loop
root.mainloop()
