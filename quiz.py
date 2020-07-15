import tkinter as tk
import json
import sqlite3

LARGE_FONT = ("Verdana",25)
MEDIUM_FONT = ("Verdana",15)
SMALL_FONT =("Verdana",10)

class RadioButton:
	def __init__(self,root,_id=None,callback=None):
		self.root = root
		self.checked = tk.PhotoImage(file="resources/radiochecked.png")
		self.unchecked = tk.PhotoImage(file="resources/radiounchecked.png")
		self.state = False
		self._id = _id
		self.button = tk.Button(self.root,image=self.unchecked,command=self.Toggle)
		self.callback = callback

	def Toggle(self):
		if self.state is True:
			self.state = False
			if self.callback is not None:
				self.callback(-1)
			self.button.configure(image=self.unchecked)
		else:
			self.state = True
			self.button.configure(image=self.checked)
			if self.callback is not None:
				self.callback(self._id)

	def GetId(self):
		return self._id

	def GetState(self):
		return self.state

	def SetState(self,state=None):
		if state is not None:
			self.state = state
			if state is False:
				self.button.configure(image=self.unchecked)
			else:
				self.button.configure(image=self.checked)

	def Grid(self,row=None,column=None):
		if row and column is not None:
			self.button.grid(row=row,column=column)
		else:
			self.button.grid(row=0,column=0)

	def Pack(self):
		self.button.pack()

class Question:
	def __init__(self,root,data=None):
		self.root = root
		self.frame = tk.Frame(self.root)
		self.questiontxt = tk.Text(self.frame,font=MEDIUM_FONT,height=2,width=50)
		self.optionstxt = []
		self.optionsradiobtn = []
		self.var = -1
		if data is not None:
			self.questiontxt.insert(tk.INSERT,data["question"])
			self.questiontxt.configure(state="disabled")
			self.questiontxt.grid(row=0,column=1)
			for i in range(0,len(data["options"])):
				self.optionsradiobtn.append(RadioButton(self.frame,i+1,self.CallBack))
				self.optionsradiobtn[i].Grid(i+1,0)

				self.optionstxt.append(tk.Text(self.frame,font=MEDIUM_FONT,height=2,width=50))
				self.optionstxt[i].insert(tk.INSERT,data["options"][i]["option"])
				self.optionstxt[i].configure(state="disabled")
				self.optionstxt[i].grid(row=i+1,column=1)

	def CallBack(self,_id=None):
		if _id is not None:
			self.var = _id
			print(_id,self.var)
			for i in self.optionsradiobtn:
				if i.GetId() != _id and i.GetState() is True:
					i.SetState(False)

	def Grid(self,row=0,column=0):
		self.frame.grid(row=row,column=column,sticky=tk.NW,columnspan=2)

	def Hide(self):
		self.frame.grid_forget()

class Section:
	def __init__(self,root,data=None):
		self.root = root
		self.frame = tk.Frame(self.root)
		self.questions = []
		self.sectionlbl = tk.Label(self.frame,text=data["section"],font=LARGE_FONT)
		self.sectionlbl.grid(row=0,column=0,sticky=tk.NW)
		self.currquestion = 0
		if data is not None:
			for i in range(0,len(data["questions"])):
				self.questions.append(Question(self.frame,data["questions"][i]))
				if i == 0:
					self.questions[i].Grid(1,0)
		self.prevbtn = tk.Button(self.frame,text="Back",font=MEDIUM_FONT,command=self.Back)
		self.prevbtn.grid(row=2,column=0,sticky=tk.NW)
		self.nextbtn = tk.Button(self.frame,text="Next",font=MEDIUM_FONT,command=self.Next)
		self.nextbtn.grid(row=2,column=1,sticky=tk.NW,)

	def Grid(self,row=0,column=0):
		self.frame.grid(row=row,column=column,sticky=tk.NW)

	def Next(self):
		if self.currquestion < len(self.questions)-1:
			self.questions[self.currquestion].Hide()
			self.currquestion += 1
			self.questions[self.currquestion].Grid(1,0)

	def Back(self):
		if self.currquestion > 0 :
			self.questions[self.currquestion].Hide()
			self.currquestion -= 1 
			self.questions[self.currquestion].Grid(1,0)

	def Hide(self):
		self.frame.grid_forget()

class Test:
	def __init__(self,root,data=None):
		self.root = root
		self.frame =tk.Frame(self.root)
		self.testlbl = tk.Label(self.frame,text=data["test"],font=LARGE_FONT)
		self.testlbl.grid(row=0,column=0,sticky=tk.NW)
		self.sections = []
		self.currsection = 0
		if data is not None:
			for i in range(0,len(data["sections"])):
				self.sections.append(Section(self.frame,data["sections"][i]))
				print(i)
		self.sections[0].Grid(row=1,column=0,)
		self.prevbtn = tk.Button(self.frame,text="Previous Section",font=MEDIUM_FONT,command=self.Back)
		self.prevbtn.grid(row=2,column=0,sticky=tk.NW)
		self.nextbtn =tk.Button(self.frame,text="Next Section",font=MEDIUM_FONT,command=self.Next)
		self.nextbtn.grid(row=2,column=1,sticky=tk.NW)
			
	def Grid(self,row=0,column=0):
		self.frame.grid(row=row,column=column)

	def Next(self):
		if self.currsection < len(self.sections)-1:
			self.sections[self.currsection].Hide()
			self.currsection += 1
			self.sections[self.currsection].Grid(row=1,column=0,)

	def Back(self):
		if self.currsection > 0 :
			self.sections[self.currsection].Hide()
			self.currsection -= 1
			self.sections[self.currsection].Grid(row=1,column=0,)

class Quiz:
	def __init__(self,root):
		self.root = root
		self.menuframe = tk.Frame(self.root)
		self.test = None
		self.conn = sqlite3.connect("Quiz.db")
		self.menubuttons = None
		self.Menu()
		self.menuframe.pack()

	def Menu(self):
		cursor =  self.conn.execute("SELECT * FROM quizzes")
		row = cursor.fetchall()
		label = tk.Label(self.menuframe,text="Quizzes Available!",font=("Verdana",50))
		label.pack()
		self.menubuttons = []
		for i in range(0,len(row)):
			self.menubuttons.append(tk.Button(self.menuframe,text=row[i][1],font=("Verdana",30),command=lambda:self.Start(row[i])))
			self.menubuttons[i].pack()

	def Start(self,row):
		file = open(row[2],"r")
		data = json.loads(file.read())
		self.test = Test(self.root,data)
		self.menuframe.pack_forget()
	
window = tk.Tk()
window.geometry("1024x768")
window.title("Quiz App")
file = open("quiz.json","r")
data = json.loads(file.read())
T = Test(window,data)
T.Grid()
window.mainloop()

		