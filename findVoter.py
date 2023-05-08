



import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
from tkinter import filedialog
import time

window = tk.Tk()
window.title("Find voter")
window.geometry('1000x600')


data1 = ['', '', '']

frame2 = tk.Frame(window, width = 1000, height = 600)
lb11 = tk.Label(frame2, text="Voter Id" + ":\t" + data1[0], font=("arial",12))  
lb11.place(x=20, y=120)  

lb21 = tk.Label(frame2, text="Name" + ':\t' + data1[1], font=("arial",12))  
lb21.place(x=20, y=160)  



lb31 = tk.Label(frame2, text="Address" + ':\t' + data1[2], font=("arial",12))  
lb31.place(x=20, y=200)  


bt21 = tk.Button(window, text = "Go Back", width = 10, command = lambda:showFrame1())
bt21.place(x = 10, y = 10)



# listbox1= tk.Listbox(window, height = 10,
#                   width = 15,
#                   bg = "grey",
#                   activestyle = 'dotbox',
#                   font = "Helvetica",
#                   fg = "white")
# listbox.place(x=500, y = 100)


# listbox1= tk.Listbox(window, height = 10,
#                   width = 15,
#                   bg = "grey",
#                   activestyle = 'dotbox',
#                   font = "Helvetica",
#                   fg = "white")
# listbox.place(x=500, y = 100)



Image2 = None


imageLabel11 = tk.Label(frame2, borderwidth = 1, relief = "solid")
imageLabel11.place(x = 300, y = 120)
img=Image.open('not selected.png')
img=ImageTk.PhotoImage(img)
imageLabel11.image = img
imageLabel11['image'] = img





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
	
			
options = [""]
data = readElectionData()
print(data)
for i in data:
	if(i['status'] == '1'):
		options.append(i['id'])

print(options)
clicked = tk.StringVar()

clicked.set("")
  
lb5 = tk.Label(frame2, text="Choose Election", font=("arial",10))  
lb5.place(x=500, y=120) 

drop1 = tk.OptionMenu(frame2, clicked, *options)
drop1.place(x=500, y=140)

bt2 = tk.Button(frame2, text = "Select" , command = lambda:selectElection())
bt2.place(x = 600, y = 140)



options2 = [""]
clicked2 = tk.StringVar()

clicked2.set("")
	  
lb52 = tk.Label(frame2, text="Choose Candidate", font=("arial",10))  
lb52.place(x=700, y=120) 

drop2 = tk.OptionMenu(frame2, clicked2 , *options2)
drop2.place(x=700, y=140)

bt22 = tk.Button(frame2, text = "Give Vote" , command = lambda:giveVote())
bt22.place(x = 800, y = 140)


index = -1
def selectElection():
	global index
	val = clicked.get()
	if(val == ""):
		return
	
	
	#checking if already voted
	file = open('database/votingData/votingData.txt', 'r')
	a = file.read()
	
	a = a.split('\n')
	
	if(a[-1] == ""):
		a.pop(-1)
	
	for i in a:
		b = i.split(',')
		if(b[2].replace('\n', '') == data1[0] and b[0] == val):
			tk.messagebox.showinfo('Info', 'Already Voted')
			return

	for i in range(len(data)):
		if(data[i]['id'] == val):
			index = i
			break
			
	options2 = [""]

	for i in data[index]['candidates']:
		options2.append(i[0])


	

	clicked2.set("")
	  
	lb52 = tk.Label(frame2, text="Choose Candidate", font=("arial",10))  
	lb52.place(x=700, y=120) 

	drop2 = tk.OptionMenu(frame2, clicked2 , *options2)
	drop2.place(x=700, y=140)

	bt22 = tk.Button(frame2, text = "Give Vote" , command = lambda:giveVote())
	bt22.place(x = 800, y = 140)
	
	



def giveVote():
	global index
	val = clicked2.get()
	print(val)
	if(val == ""):
		return
	
	
	newScore = 0
	for i in data[index]['candidates']:
		if(i[0] == val):
			i[1]+=1
			newScore = i[1]
			break
			
	file = open('database/electionData/' + data[index]['id'] + '.txt', 'r')
	a = file.read()
	file.close()
	
	b = a.find(val)
	
	while True:
		if(a[b+1] == '\n'):
			break
		
		b+=1
	
	
	
	c = a[:b] + str(newScore) + a[b+1:]
	
	
	file = open('database/electionData/' + data[index]['id'] + '.txt', 'w')
	file.write(c)
	file.close()
	
	
	file = open('database/votingdata/votingData.txt', 'a')
	file.write(data[index]['id'] + ',' + val + ',' + data1[0]+'\n')
	file.close()
	
	
	tk.messagebox.showinfo('Success', 'Vote successfull casted.')
	showFrame1()
	clicked.set("")
	clciked2.set("")
	

frame1 = tk.Frame(window, width = 1000, height = 600)

lb1 = tk.Label(frame1, text="Upload Fingerprint Image", font=("arial",10))
lb1.place(x=80, y=120)

bt1 = tk.Button(frame1, text = "Select Image", width = 10, command = lambda:uploadFPImage())
bt1.place(x = 500, y = 120)

bt3 = tk.Button(frame1, text = "Find", width = 10, command = lambda:findImage())
bt3.place(x = 500, y = 520)


Image1 = None

imageLabel1 = tk.Label(frame1, borderwidth = 1, relief = "solid")
imageLabel1.place(x = 250, y = 100)
img=Image.open('not selected.png')
img=ImageTk.PhotoImage(img)
imageLabel1.image = img
imageLabel1['image'] = img



def uploadFPImage():
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
    
filenameFound = None

def findImage():
	global Image1, filenameFound, data1
	t1 = time.time()
	sample = Image1.copy()

	best_score = counter = 0
	filename = image = kp1 = kp2 = mp = None
	for file in os.listdir(
	    r"D:\Programming\pythonCodes\fingerprintVotingSystem\database\votersData\fingerprints"
	):
	    # if counter % 10 == 0:
	    #     print(counter)
	    #     print(file)
	    counter += 1

	    fingerprint_img = cv2.imread(
	        os.path.join(r"D:\Programming\pythonCodes\fingerprintVotingSystem\database\votersData\fingerprints", file)
	    )
	    sift = cv2.SIFT_create()
	    keypoints_1, des1 = sift.detectAndCompute(sample, None)
	    keypoints_2, des2 = sift.detectAndCompute(fingerprint_img, None)
	    # print(kp1, des1)
	    # print(kp2, des2)
	    # print(len(kp1), len(kp2))
	    # print(len(des1), len(des2))
	    # print(des1[0], des2[0])\
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
	filenameFound = filename
	if(filenameFound):
		filenameFound = filenameFound.split('.')[0]
	# if len(match_points) > 0:
	#     result = cv2.drawMatches(sample, kp1, image, kp2, mp, None)
	#     result = cv2.resize(result, None, fx=5, fy=5)
	#     cv2.imshow("Result", result)
	#     cv2.waitKey(0)
	#     cv2.destroyAllWindows()
	   
	   
	print('time taken is', time.time() - t1)
	
	if(filenameFound):
		
		file = open('database/votersData/votersData.txt')
		database = file.read()
		database = database.split('\n')
		database = [i.split(',') for i in database]
		print(database)
		for i in database:
			if(i[0] == filenameFound):
				data1 = i.copy()
				break
		
		print(data1)	
		lb11.config(text="Voter Id" + ":\t" + data1[0])  
		 
		lb21.config(text="Name" + ':\t' + data1[1])  


		lb31.config(text="Address" + ':\t' + data1[2])
		
		Image1 = None

		img=Image.open('database/votersData/photos/' + filename)
		img=ImageTk.PhotoImage(img)
		imageLabel11.image = img
		imageLabel11['image'] = img
		
		showFrame2()
		tk.messagebox.showinfo('showinfo', 'Found '+filenameFound)	
		
	else:
		tk.messagebox.showerror('Error', 'fingerprint not found')
	
	
	filenameFound = None
	Image1 = None
	img=Image.open('not selected.png')
	img=ImageTk.PhotoImage(img)
	imageLabel1.image = img
	imageLabel1['image'] = img




def showFrame1():
	frame1.pack(fill ='both', expand = 1)
	frame2.pack_forget()

def showFrame2():
	frame2.pack(fill ='both', expand = 1)
	frame1.pack_forget()
	
	
showFrame1()

window.mainloop()