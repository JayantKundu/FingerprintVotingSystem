


import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import time
import os



window = tk.Tk()
window.title("Add voter")
window.geometry('1000x600')

lb1 = tk.Label(window, text="Voter Id", width=10, font=("arial",12))  
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
	
	if(findImage()):
		tk.messagebox.showerror('Error', "Fingerprint already registered.")
		Image2 = None
		imageLabel2.image = None
		return
		
	
	file = open('database/votersData/votersData.txt', 'a')
	
	file.write(voterId+','+name+',' +address+'\n')
	file.close()
	
	cv2.imwrite('database/votersData/photos/'+voterId+'.png', Image1)
	cv2.imwrite('database/votersData/fingerprints/'+voterId+'.png', Image2)
	
	
	tk.messagebox.showinfo('showinfo', 'Successfull Registered')
	
	en1.delete(0, tk.END)
	en2.delete(0, tk.END)
	en3.delete(0, tk.END)
	
	imageLabel1.image = None
	imageLabel2.image = None
	
	Image1 = None
	Image2 = None
	
	
	print('function done')


def findImage():
	# global Image1, filenameFound, data1
	t1 = time.time()
	sample = Image2.copy()

	best_score = counter = 0
	filename = image = kp1 = kp2 = mp = None
	for file in os.listdir(
	    r"D:\Programming\pythonCodes\fingerprintVotingSystem\database\votersData\fingerprints"
	):
	
	    counter += 1

	    fingerprint_img = cv2.imread(
	        os.path.join(r"D:\Programming\pythonCodes\fingerprintVotingSystem\database\votersData\fingerprints", file)
	    )
	    sift = cv2.SIFT_create()
	    keypoints_1, des1 = sift.detectAndCompute(sample, None)
	    keypoints_2, des2 = sift.detectAndCompute(fingerprint_img, None)

	    # fast library for approx best match KNN
	    matches = cv2.FlannBasedMatcher({"algorithm": 1, "trees": 10}, {}).knnMatch(
	        des1, des2, k=2
	    )

	    match_points = []
	    for p, q in matches:
	        if p.distance < 0.1 * q.distance:
	            match_points.append(p)

	    keypoints = 0
	    if len(keypoints_1) <= len(keypoints_2):
	        keypoints = len(keypoints_1)
	    else:
	        keypoints = len(keypoints_2)
	    if len(match_points) / keypoints * 95 > best_score:
	        best_score = len(match_points) / keypoints * 95
	        filename = file
	        image = fingerprint_img
	        kp1, kp2, mp = keypoints_1, keypoints_2, match_points
	        print('new match')
	        print(filename)
	        print(best_score)
	        print()
	
	if(filename):
		print("Best match:  " + filename)
		print("Best score:  " + str(best_score))
	
	
	if(filename == None):
		return False
	else:
		return True
		
	# filenameFound = filename
	# if(filenameFound):
	# 	filenameFound = filenameFound.split('.')[0]
	   
	   
	# print('time taken is', time.time() - t1)
	
	# if(filenameFound):
		
	# 	file = open('database/votersData/votersData.txt')
	# 	database = file.read()
	# 	database = database.split('\n')
	# 	database = [i.split(',') for i in database]
	# 	print(database)
	# 	for i in database:
	# 		if(i[0] == filenameFound):
	# 			data1 = i.copy()
	# 			break
		
	# 	print(data1)	
	# 	lb11.config(text="Voter Id" + ":\t" + data1[0])  
		 
	# 	lb21.config(text="Name" + ':\t' + data1[1])  


	# 	lb31.config(text="Address" + ':\t' + data1[2])
		
	# 	Image1 = None

	# 	img=Image.open('database/votersData/photos/' + filename)
	# 	img=ImageTk.PhotoImage(img)
	# 	imageLabel11.image = img
	# 	imageLabel11['image'] = img
		
	# 	showFrame2()
	# 	tk.messagebox.showinfo('showinfo', 'Found '+filenameFound)	
		
	# else:
	# 	tk.messagebox.showerror('Error', 'fingerprint not found')
	
	
	# filenameFound = None
	# Image1 = None
	# img=Image.open('not selected.png')
	# img=ImageTk.PhotoImage(img)
	# imageLabel1.image = img
	# imageLabel1['image'] = img



window.mainloop()