

import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
from tkinter import filedialog
import time

window = tk.Tk()
window.title("Add Election Details")
window.geometry('1000x600')


lb1 = tk.Label(window, text="Election Id", width=10, font=("arial",12))  
lb1.place(x=20, y=120)  
en1 = tk.Entry(window)  
en1.place(x=200, y=120) 


lb2 = tk.Label(window, text="Elections Name", width=10, font=("arial",12))  
lb2.place(x=20, y=160)  
en2 = tk.Entry(window)  
en2.place(x=200, y=160) 


lb3 = tk.Label(window, text="Select candidates", width=10, font=("arial",12))  
lb3.place(x=20, y=200)    




def getCandidatesData():
	file = open('database/candidateData/candidateData.txt', 'r')
		
	a = file.read().split('\n')
	a.pop(-1)
	options = [i.split(',')[0] for i in a]


	print(options)
	file.close()
	
	return options


options =  getCandidatesData()

clicked = tk.StringVar()


clicked.set("")
  

drop = tk.OptionMenu(window, clicked, *options)
drop.place(x=200, y=200) 


bt2 = tk.Button( window , text = "Add" , command = lambda:show())
bt2.place(x = 220, y = 240)
 


bt21 = tk.Button(window, text = "Add Election", width = 10, command = lambda:create())
bt21.place(x = 900, y = 360)


listbox = tk.Listbox(window, height = 10,
                  width = 15,
                  bg = "grey",
                  activestyle = 'dotbox',
                  font = "Helvetica",
                  fg = "white")
listbox.place(x=500, y = 100)

added = []

def show():
	global clicked , added
	
	val = clicked.get()
	if val not in added and val != '':
		added.append(val)
		listbox.insert(len(added) + 1, val)




def readElectionData():
	file = open('database/electionData/electionData.txt', 'r')
	a = file.read()
	
	b = a.split('\n')
	if(b[-1] == ""):
		b.pop(-1)
	# b.pop(-1)
	data = []
	
	for i in b:
		c = i.split(',')
		if(len(c)<3):
			continue
		di = {}
		di['id'] = c[0]
		di['name'] = c[1]
		di['status'] = c[2]
		di['candidates'] = []
		file2 = open('database/electionData/'+di['id']+'.txt', 'r')
		d = file2.read()
		d = d.split('\n')
		if(d[-1] == ""):
			d.pop(-1)
		
		for k in d:
			e = k.split(',')
			f = []
			for h in e:
				f.append(h.replace('\n', ''))
			f[1]  = int(f[1])
			di['candidates'].append(f)
		data.append(di)
		file2.close()
	file.close()
	return data
	
			

data = readElectionData()


def create():
	global added
	
	
	
	a = en1.get()
	
	
	error = False
	for i in data:
		if(i['id'] == a):
			error  = True
			break
	
	
	if(error):
		print("election id already in use")
		
		tk.messagebox.showerror('Error', 'Election Id already in use')
		return
	
	file1 = open('database/electionData/electionData.txt', 'a')
	file1.write(en1.get() + ',' +  en2.get() + ",0" + '\n')
	
	# file1.write(','.join(added))
	
	
	# file1.write('\n,\n')
	
	file1.close()
	
	
	
	file1 = open(f'database/electionData/{en1.get()}.txt', 'w')

	
	for i in added:
		file1.write(i + ",0" + '\n')
	

	file1.close()
	
	tk.messagebox.showinfo('showinfo', 'Successfull Registered')
	
	en1.delete(0, tk.END)
	en2.delete(0, tk.END)
	listbox.delete(0, tk.END)
	added = []
	clicked.set("")

# def showFrame1():
# 	frame1.pack(fill ='both', expand = 1)
# 	frame2.pack_forget()

# def showFrame2():
# 	frame2.pack(fill ='both', expand = 1)
# 	frame1.pack_forget()
	
	
# showFrame1()

window.mainloop()