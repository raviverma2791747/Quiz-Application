import tkinter as tk
import json
import sqlite3
import time

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
		self.button = tk.Button(self.root,image=self.unchecked,command=self.Toggle,relief=tk.FLAT)
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
		self.button.grid(row=row,column=column)


	def Pack(self):
		self.button.pack()

class CheckButton:
	def __init__(self,root,_id=None,callback=None):
		self.root = root
		self.checked = tk.PhotoImage(file="resources/checked.png")
		self.unchecked = tk.PhotoImage(file="resources/unchecked.png")
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

	def Grid(self,row=0,column=0):
		self.button.grid(row=row,column=column)
		
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
		self.currquestion = 0
		if data is not None:
			for i in range(0,len(data["questions"])):
				self.questions.append(Question(self.frame,data["questions"][i]))
		self.prevbtn = tk.Button(self.frame,text="Back",font=MEDIUM_FONT,command=self.Back,)
		self.nextbtn = tk.Button(self.frame,text="Next",font=MEDIUM_FONT,command=self.Next,)
		if len(self.questions) == 1 or 0:
			self.prevbtn.configure(state="disabled")
			self.nextbtn.configure(state="disabled")

	def Grid(self,row=0,column=0):
		self.sectionlbl.grid(row=0,column=0,sticky=tk.NW)
		if len(self.questions) > 0:
			self.questions[0].Grid(1,0)
		self.prevbtn.grid(row=2,column=0,sticky=tk.NW)
		self.nextbtn.grid(row=2,column=1,sticky=tk.NW,)
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
		self.timelimit = []
		self.timelimitlbl = None
		self.sections = []
		self.currsection = 0
		self.instructionframe = None
		if data is not None:
			for i in range(0,len(data["sections"])):
				self.sections.append(Section(self.frame,data["sections"][i]))
			self.timelimit.append(int(data["time_limit"]["hour"]))
			self.timelimit.append(int(data["time_limit"]["minute"]))
			self.timelimit.append(int(data["time_limit"]["second"]))
			if self.timelimit[0]>9:
				timestr = str(self.timelimit[0])
			else:
				timestr = "0" + str(self.timelimit[0])
			if self.timelimit[1]>9:
				timestr = timestr+":"+str(self.timelimit[1])
			else:
				timestr = timestr+":0" + str(self.timelimit[1])
			if self.timelimit[2]>9:
				timestr = timestr+":"+str(self.timelimit[2])
			else:
				timestr = timestr+":0" + str(self.timelimit[2])
			self.timelimitlbl = tk.Label(self.frame,text=timestr,font=LARGE_FONT)
		self.prevbtn = tk.Button(self.frame,text="Previous Section",font=MEDIUM_FONT,command=self.Back,)
		self.nextbtn =tk.Button(self.frame,text="Next Section",font=MEDIUM_FONT,command=self.Next,)
		if len(self.sections) == 0 or 1:
			self.prevbtn.configure(state="disabled")
			self.nextbtn.configure(state="disabled")

			
	def Grid(self,row=0,column=0):
		self.HideInstruction()
		self.timelimitlbl.grid(row=0,column=1,sticky=tk.NE)
		self.timelimitlbl.after(1000,self.UpdateCountDownTimer)
		if len(self.sections) > 0 :
			self.sections[0].Grid(row=1,column=0,)
		self.prevbtn.grid(row=2,column=0,sticky=tk.NW)
		self.nextbtn.grid(row=2,column=1,sticky=tk.NW)
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

	def UpdateCountDownTimer(self):
		if self.timelimit[2] == 0:
			self.timelimit[2] = 59
			if self.timelimit[1] == 0:
				self.timelimit[1] = 59
				if self.timelimit[0] == 0:
					self.timelimit[1] = 0
					self.timelimit[2] = 0
				else:
					self.timelimit[0] -= 1
					self.timelimitlbl.after(1000,self.UpdateCountDownTimer)
			else:
				self.timelimit[1] -= 1
				self.timelimitlbl.after(1000,self.UpdateCountDownTimer)
		else:
			self.timelimit[2] -= 1
			self.timelimitlbl.after(1000,self.UpdateCountDownTimer)
		if self.timelimit[0]>9:
			timestr = str(self.timelimit[0])
		else:
			timestr = "0" + str(self.timelimit[0])
		if self.timelimit[1]>9:
			timestr = timestr+":"+str(self.timelimit[1])
		else:
			timestr = timestr+":0" + str(self.timelimit[1])
		if self.timelimit[2]>9:
			timestr = timestr+":"+str(self.timelimit[2])
		else:
			timestr = timestr+":0" + str(self.timelimit[2])
		self.timelimitlbl.configure(text=timestr)

	def Instruction(self,data=None,callback1=None,callback2=None):
		self.instructionframe = tk.Frame(self.root)
		testlbl = tk.Label(self.instructionframe,text=data["test"],font=LARGE_FONT)
		instructionlbl = tk.Label(self.instructionframe,text="Instructions",font=LARGE_FONT)
		instructiontxt = tk.Text(self.instructionframe,font=MEDIUM_FONT)
		if "instructions" in data:
			for i in range(0,len(data["instructions"])):
				instructiontxt.insert(tk.INSERT,"• " + data["instructions"][i]["instruction"]+ "\n")
		instructiontxt.configure(state="disabled")
		instructionacceptbtn = tk.Button(self.instructionframe,text="Accept",font=MEDIUM_FONT,command=callback1)
		instructiondeclinebtn = tk.Button(self.instructionframe,text="Decline",font=MEDIUM_FONT,command=callback2)
		testlbl.grid(row=0,column=0,sticky="W",padx=200)
		instructionlbl.grid(row=1,column=0,sticky="W",padx=200)
		instructiontxt.grid(row=2,column=0,columnspan=2,padx=200,sticky="W")
		instructionacceptbtn.grid(row=3,column=0,padx=200,sticky="W")
		instructiondeclinebtn.grid(row=3,column=1,padx=200,sticky="E")
		self.instructionframe.pack(expand=True,fill="both")

	def HideInstruction(self):
		self.instructionframe.pack_forget()


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
		if self.menubuttons is None:
			cursor =  self.conn.execute("SELECT * FROM quizzes")
			row = cursor.fetchall()
			label = tk.Label(self.menuframe,text="Quizzes Available!",font=("Verdana",50))
			label.grid(row=0,column=0,sticky="W")
			self.menubuttons = []
			for i in range(0,len(row)):
				self.menubuttons.append(tk.Button(self.menuframe,text=row[i][1],font=("Verdana",30),relief=tk.FLAT,command=lambda j=i:self.Start(row[j])))
				self.menubuttons[i].grid(row=i+1,column=0,padx=10,sticky="W")
			self.menuframe.pack()
		else:
			self.test.HideInstruction()
			self.menuframe.pack()

	def Start(self,row):
		file = open(row[2],"r")
		try:
			data = json.loads(file.read())
		except:
			return
		self.test = Test(self.root,data)
		self.menuframe.pack_forget()
		self.test.Instruction(data,self.test.Grid,self.Menu)
	
if __name__ == "__main__" :
	window = tk.Tk()
	window.geometry("1024x768")
	window.title("Quiz App")
	#file = open("quiz.json","r")
	#data = json.loads(file.read())

	Q =Quiz(window)
	window.mainloop()
		