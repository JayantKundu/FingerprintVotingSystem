




import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
from tkinter import filedialog

window = tk.Tk()
window.title("Show Election Details")
window.geometry('1000x600')



# drawing table



lb11 = tk.Label(window, text="Election Id", font=("arial",12))  
lb11.place(x=20, y=120) 

lb12 = tk.Label(window, text="", font=("arial",12))  
lb12.place(x=150, y=120) 

lb21 = tk.Label(window, text="Election Name", font=("arial",12))  
lb21.place(x=20, y=160)

lb22 = tk.Label(window, text="", font=("arial",12))  
lb22.place(x=150, y=160)


lb31 = tk.Label(window, text="Election Status", font=("arial",12))
lb31.place(x=20, y=200)

lb32 = tk.Label(window, text="", font=("arial",12))
lb32.place(x=150, y=200)




options = []

def readElectionData():
	file = open('database/electionData/electionData.txt', 'r')
	a = file.read()
	
	b = a.split('\n')
	if(b[-1] == ""):
		b.pop(-1)
	
	data = []
	
	for i in b:
		c = i.split(',')
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

for i in data:
	options.append(i['id'])


clicked = tk.StringVar()


clicked.set("")
  
lb5 = tk.Label(window, text="Choose Election", font=("arial",10))  
lb5.place(x=20, y=20) 

drop = tk.OptionMenu(window, clicked, *options)
drop.place(x=20, y=40) 


bt2 = tk.Button( window , text = "Show" , command = lambda:show())
bt2.place(x = 90, y = 40)
 


# bt21 = tk.Button(window, text = "Add Election", width = 10, command = lambda:create())
# bt21.place(x = 900, y = 360)

bt3 = tk.Button(window, text = "", width = 10, command = lambda:changeState())
bt3.place(x = 900, y = 360)


lb4 = tk.Label(window, text="Candidate Name", font=("arial",10))  
lb4.place(x=500, y=80) 

listbox = tk.Listbox(window, height = 10,
                  width = 15,
                  bg = "grey",
                  activestyle = 'dotbox',
                  font = "Helvetica",
                  fg = "white")
listbox.place(x=500, y = 100)



lb5 = tk.Label(window, text="Number of votes", font=("arial",10))  
lb5.place(x=650, y=80) 

listbox2 = tk.Listbox(window, height = 10,
                  width = 15,
                  bg = "grey",
                  activestyle = 'dotbox',
                  font = "Helvetica",
                  fg = "white")
listbox2.place(x=650, y = 100)




election = []
val = ""

def show():
	global election, val
	val = clicked.get()
	
	if(val == ""):
		return
	
	for i in data:
		if(i['id'] == val):
			election = i
	
	
	lb12.config(text = election['id'])
	lb22.config(text = election['name'])
	
	status = ''
	if(election['status'] == '0'):
		status = "Not Started"
		bt3.config(text = 'Start')
	elif(election['status'] == '1'):
		status = "Ongoing"
		bt3.config(text = 'Stop')
	else:
		status = "Completed"
		bt3.config(text = 'Annonunce')
		
	lb32.config(text = status)
	
	
	listbox.delete(0, tk.END)
	listbox2.delete(0, tk.END)
	for i in range(len(election['candidates'])):
		listbox.insert(i+1, election['candidates'][i][0])
		listbox2.insert(i+1, election['candidates'][i][1])

	
	

def changeState():
	global election, val
	index = -1
	for num, i in enumerate(data):
		if(i['id'] == val):
			index = num
		
		
	if(election['status'] == '2'):
		
		isDraw = False
		x = sorted(data[index]['candidates'], key=lambda x: x[1], reverse = True)
		print('x sorted')
		print(x)
		names = []
		maxVotes = x[0][1]
		for i in range(len(x)):
			if(x[i][1] == maxVotes):
				names.append(x[i][0])
		
		
		if(len(names) == 1):
			tk.messagebox.showinfo('Result', name[0] + " Won!!")
				
		else:
			tk.messagebox.showinfo('Result', 'Draw between ' + ', '.join(names))
			
		return
		
		
	elif(election['status'] == '0'):
		data[index]['status'] = '1'
	else:
		data[index]['status'] = '2'
	
	
	
	
	file = open('database/electionData/electionData.txt', 'r')
	a = file.read()
	file.close()
	
	b = a.find(election['id'])
	
	while(True):
		if(a[b+1] == '\n'):
			break
		b+=1
	
	# a[b] = data[index]['status']
	
	c = a[:b] + data[index]['status']+a[b+1:]
	file = open('database/electionData/electionData.txt', 'w')
	file.write(c)
	file.close()
	
	
	election = data[index]
	show()
	
	

# def create():
# 	global added
	
	
	
# 	a = en1.get()
	
	
# 	error = False
# 	for i in data:
# 		if(i['id'] == a):
# 			error  = True
# 			break
	
	
# 	if(error):
# 		print("election id already in use")
		
# 		tk.messagebox.showerror('Error', 'Election Id already in use')
# 		return
	
# 	file1 = open('database/electionData/electionData.txt', 'a')
# 	file1.write(en1.get() + ',' +  en2.get() + ",0" + '\n')
	
# 	# file1.write(','.join(added))
	
	
# 	# file1.write('\n,\n')
	
# 	file1.close()
	
	
	
# 	file1 = open(f'database/electionData/{en1.get()}.txt', 'w')

	
# 	for i in added:
# 		file1.write(i + ",0" + '\n')
	

# 	file1.close()
	
# 	tk.messagebox.showinfo('showinfo', 'Successfull Registered')
	
# 	en1.delete(0, tk.END)
# 	en2.delete(0, tk.END)
# 	listbox.delete(0, tk.END)
# 	added = []
# 	clicked.set("")

# def showFrame1():
# 	frame1.pack(fill ='both', expand = 1)
# 	frame2.pack_forget()

# def showFrame2():
# 	frame2.pack(fill ='both', expand = 1)
# 	frame1.pack_forget()
	
	
# showFrame1()

window.mainloop()