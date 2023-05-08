





import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np




window = tk.Tk()
window.title("Add Candidate")
window.geometry('1000x600')

lb1 = tk.Label(window, text="Candidate Id", width=10, font=("arial",12))  
lb1.place(x=20, y=120)  
en1 = tk.Entry(window)  
en1.place(x=200, y=120) 


lb2 = tk.Label(window, text="Name", width=10, font=("arial",12))  
lb2.place(x=20, y=160)  
en2 = tk.Entry(window)  
en2.place(x=200, y=160) 


lb3 = tk.Label(window, text="Address", width=10, font=("arial",12))  
lb3.place(x=20, y=200)  
en3 = tk.Entry(window)  
en3.place(x=200, y=200) 

bt1 = tk.Button(window, text = "Select Image", width = 10, command = lambda:uploadPPImage())
bt1.place(x = 900, y = 120)


bt2 = tk.Button(window, text = "Select Image", width = 10, command = lambda:uploadFPImage())
bt2.place(x = 900, y = 320)


bt3 = tk.Button(window, text = "Submit", width = 10, command = lambda:submitData())
bt3.place(x = 500, y = 520)
Image1 = Image2 = None


imageLabel1 = tk.Label(window, borderwidth = 1, relief = "solid")
imageLabel1.place(x = 600, y = 100)
img=Image.open('not selected.png')
img=ImageTk.PhotoImage(img)
imageLabel1.image = img
imageLabel1['image'] = img

imageLabel2 = tk.Label(window, borderwidth = 1, relief = "solid")
imageLabel2.place(x = 600, y = 350)
imageLabel2.image = img
imageLabel2['image'] = img

def uploadPPImage():
	global Image1
	f_types = [('PNG Files','*.png'), ('Jpg Files', '*.jpg')]  
	filename = tk.filedialog.askopenfilename(multiple=False)

	img=Image.open(filename)
	img=img.resize((96,103))
	Image1 = np.asarray(img)
	Image1 = cv2.cvtColor(Image1, cv2.COLOR_RGB2BGR)
	img=ImageTk.PhotoImage(img)
	imageLabel1.image = img
	imageLabel1['image'] = img



def uploadFPImage():
	global Image2
	f_types = [('PNG Files','*.png'), ('Jpg Files', '*.jpg')]  
	filename = tk.filedialog.askopenfilename(multiple=False)

	img=Image.open(filename)
	img=img.resize((96,103))
	Image2 = np.asarray(img)
	Image2 = cv2.cvtColor(Image2, cv2.COLOR_RGB2BGR)
	img=ImageTk.PhotoImage(img)
	imageLabel2.image = img
	imageLabel2['image'] = img  
    



def submitData():
	global Image1, Image2
	voterId = en1.get()
	name = en2.get()
	address = en3.get()
	
	if(voterId == ''):
		print("enter voter id")
		return
	if(name == ''):
		print("enter name")
		return
	if(address == ''):
		print("enter address")
		return
	if(Image1 is None):
		print("select photo")
		return
	if(Image2 is None):
		print("select fingerprint image")
		return
	
	
	file = open('database/candidateData/candidateData.txt', 'a')
	
	file.write(voterId+','+name+',' +address+'\n')
	file.close()
	
	cv2.imwrite('database/candidateData/photos/'+voterId+'.png', Image1)
	cv2.imwrite('database/candidateData/fingerprints/'+voterId+'.png', Image2)
	
	
	tk.messagebox.showinfo('showinfo', 'Successfull Registered')
	
	en1.delete(0, tk.END)
	en2.delete(0, tk.END)
	en3.delete(0, tk.END)
	
	imageLabel1.image = None
	imageLabel2.image = None
	
	Image1 = None
	Image2 = None
	
	
	print('function done')

window.mainloop()