import tkinter as tk
from tkinter import messagebox as mb
import tkinter.scrolledtext as st
import json
import sqlite3
import time
from datetime import datetime
from datetime import date
LARGE_FONT = ("Verdana",25)
MEDIUM_FONT = ("Verdana",15)
SMALL_FONT =("Verdana",10)

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y",)

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
		self.button = tk.Button(self.root,image=self.unchecked,relief=tk.FLAT,command=self.Toggle)
		self.callback = callback

	def Toggle(self):
		if self.state is True:
			self.state = False
			if self.callback is not None:
				self.callback(self._id)
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
		

class Question:
	def __init__(self,root,data=None,num=0):
		self.root = root
		self._id = None
		self.frame = tk.Frame(self.root)
		self.optionstxt = []
		self.optionsbtn = []
		self.var =  None
		self.keys = []
		self._type = None
		if data is not None:
			self._id=data["id"]
			self.questionlbl = tk.Label(self.frame,width=3,text=str(num),font=LARGE_FONT)
			self.questionlbl.grid(row=0,column=0)
			self.questiontxt = st.ScrolledText(self.frame,font=MEDIUM_FONT,height=2,width=65,wrap=tk.WORD)
			self.questiontxt.insert(tk.INSERT,data["question"])
			self.questiontxt.configure(state="disabled")
			self.questiontxt.grid(row=0,column=1,)
			self.point = data["point"]
			self.optionframe = ScrollableFrame(self.frame)
			if data["type"] == "single":
				self._type = "single"
				for i in range(0,len(data["options"])):
					if data["options"][i]["key"] == True:
						self.keys.append(data["options"][i]["id"])
					self.optionsbtn.append(RadioButton(self.optionframe.scrollable_frame,data["options"][i]["id"],self.CallBackRadio))
					self.optionsbtn[i].Grid(i+1,0)

					self.optionstxt.append(st.ScrolledText(self.optionframe.scrollable_frame,font=MEDIUM_FONT,height=2,width=60))
					self.optionstxt[i].insert(tk.INSERT,data["options"][i]["option"])
					self.optionstxt[i].configure(state="disabled")
					self.optionstxt[i].grid(row=i+1,column=1,)
			else:
				self._type = "multiple"
				self.var = []
				for i in range(0,len(data["options"])):
					if data["options"][i]["key"] == True:
						self.keys.append(data["options"][i]["id"])
					self.optionsbtn.append(CheckButton(self.optionframe.scrollable_frame,data["options"][i]["id"],self.CallBackCheck))
					self.optionsbtn[i].Grid(i+1,0)

					self.optionstxt.append(st.ScrolledText(self.optionframe.scrollable_frame,font=MEDIUM_FONT,height=2,width=50))
					self.optionstxt[i].insert(tk.INSERT,data["options"][i]["option"])
					self.optionstxt[i].configure(state="disabled")
					self.optionstxt[i].grid(row=i+1,column=1,)
			self.optionframe.grid(row=1,column=1,sticky="nwse")

	def CallBackRadio(self,_id=None):
		if _id is not None:
			if _id == -1:
				self.var = None
				for i in self.optionsbtn:
					i.SetState(False)
			else:
				self.var = _id
				for i in self.optionsbtn:
				    if i.GetId() != _id and i.GetState() == True:
				    	i.SetState(False)

	def CallBackCheck(self,_id=None):
		if _id is not None:
			for i in range(0,len(self.var)):
				if _id == self.var[i]:
					del self.var[i]
					break
			else:
				self.var.append(_id)
			self.var.sort()

	def Grid(self,row=0,column=0):
		self.frame.grid(row=row,column=column,columnspan=2,sticky="nwse",padx=50)

	def Hide(self):
		self.frame.grid_forget()

	def Response(self):
		#data = ["section id","question id","keys","point","options id chosen",]
		if self._type == "single":
			if self.var is None:
				self.var = []
			else:
				self.var = [self.var,]
		data = [0,self._id,self.keys,self.point,self.var,]
		return data

class Section:
	def __init__(self,root,data=None):
		self.root = root
		self._id = None
		self.frame = tk.Frame(self.root)
		self.questions = []
		self.sectionlbl = tk.Label(self.frame,text=data["section"],font=LARGE_FONT)
		self.currquestion = 0
		if data is not None:
			self._id = data["id"]
			for i in range(0,len(data["questions"])):
				self.questions.append(Question(self.frame,data["questions"][i],i+1))
		self.prevbtn = tk.Button(self.frame,text="Back",font=MEDIUM_FONT,command=self.Back,)
		self.nextbtn = tk.Button(self.frame,text="Next",font=MEDIUM_FONT,command=self.Next,)
		if len(self.questions) == 1 or 0:
			self.prevbtn.configure(state="disabled")
			self.nextbtn.configure(state="disabled")

	def Jump(self,i=0):
		self.questions[self.currquestion].Hide()
		self.currquestion = i
		self.questions[self.currquestion].Grid(1,0)

	def Grid(self,row=0,column=0):
		self.sectionlbl.grid(row=0,column=0,sticky="nw",pady=10,padx=50)
		if len(self.questions) > 0:
			self.questions[0].Grid(1,0)
		self.prevbtn.grid(row=2,column=0,sticky="nw",pady=10,padx=50)
		self.nextbtn.grid(row=2,column=1,sticky="ne",pady=10,)
		self.frame.grid(row=row,column=column,sticky="nwse")

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

	def Response(self):
		data = [] 
		for i in range(0,len(self.questions)):
			response = self.questions[i].Response()
			response[0] = self._id
			data.append(response)
		return data

class Test:
	def __init__(self,root,data=None,callback=None):
		self.root = root
		self.callback = callback
		self._id =None
		self.frame =tk.Frame(self.root)
		self.btnframe = ScrollableFrame(self.frame,height=100,width=50)
		self.testlbl = tk.Label(self.frame,text=data["test"],font=LARGE_FONT,pady=10,padx=50)
		self.timelimit = []
		self.timelimitlbl = None
		self.sections = []
		self.currsection = 0
		self.instructionframe = None
		self.data = data
		if data is not None:
			self._id = data["id"] 
			for i in range(0,len(data["sections"])):
				self.sections.append(Section(self.frame,data["sections"][i]))
			if data["time_limit"]["hour"] == "0" and data["time_limit"]["minute"] == "0":
				timestr = "No Time Limit"
			else:
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
		if len(self.sections) == 1 or 0:
			self.prevbtn.configure(state="disabled")
			self.nextbtn.configure(state="disabled")
		self.submitbtn = tk.Button(self.frame,text="Submit",font=MEDIUM_FONT,command=self.Submit,)
		self.exitbtn = tk.Button(self.frame,text="Exit",font=MEDIUM_FONT,command=self.Exit)

		for i in range(0,len(data["sections"])):
			lbl =tk.Label(self.btnframe.scrollable_frame,text=data["sections"][i]["section"],font=MEDIUM_FONT)
			lbl.grid(row=i*2,column=0,sticky=tk.NW,padx=50)
			frame = tk.Frame(self.btnframe.scrollable_frame)
			for j in range(0,len(data["sections"][i]["questions"])):
				btn = tk.Button(frame,text=str(j+1),width=3,font=MEDIUM_FONT,bg="gray",fg="white",relief="flat",command=lambda ii=i,jj=j:self.Jump(ii,jj))
				btn.grid(row=int(j/4),column=j%4,padx=5,pady=5,sticky="nw")
			frame.grid(row=i*2+1,column=0,sticky="nw",padx=50)
			 
	def Grid(self,):
		self.HideInstruction()
		self.testlbl.grid(row=0,column=0,sticky="nw",)
		self.timelimitlbl.grid(row=0,column=1,sticky="ne",padx=50)
		if self.data["time_limit"]["hour"] == "0" and self.data["time_limit"]["minute"] == "0":
			pass
		else:
			self.timelimitlbl.after(1000,self.UpdateCountDownTimer)
		if len(self.sections) > 0 :
			self.sections[0].Grid(row=1,column=0,)
		self.prevbtn.grid(row=2,column=0,sticky="nw",pady=30,padx=50)
		self.nextbtn.grid(row=2,column=1,sticky="ne",pady=30,padx=50)
		self.submitbtn.grid(row=3,column=0,sticky="nw",pady=30,padx=50)
		self.exitbtn.grid(row=3,column=1,sticky="ne",pady=30,padx=50)
		self.btnframe.grid(row=1,column=1,sticky="nwse",)
		#self.frame.pack(expand=True,fill="both",)
		self.frame.grid(row=0,column=0,sticky="nwse")
		self.frame.rowconfigure(0,weight=1)
		self.frame.columnconfigure(0,weight=1)



	def Jump(self,i=0,j=0):
		self.sections[self.currsection].Hide()
		self.currsection = i
		self.sections[self.currsection].Grid(row=1,column=0,)
		self.sections[self.currsection].Jump(j)

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
					self.Response()
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
		if self.timelimit[0] == 0 and self.timelimit[1] == 0 and self.timelimit[2] == 0:
			pass
		else:
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

	def Exit(self):
		exitmb = mb.askquestion("Exit","Are you sure you want to exit?",icon="warning")
		if exitmb == "yes":
			self.Response()

	def Submit(self):
		submitmb = mb.askquestion("Exit","Are you sure you want to submit now?",icon="question")
		if submitmb == "yes":
			self.Response()

	def Response(self):
		if self.callback is not None:
			data = {}
			data["test"] = self._id
			data["response"] = []
			for i in range(0,len(self.sections)):
				data["response"].extend(self.sections[i].Response())
			self.callback(data)

	def Destroy(self):
		self.frame.destroy()

class Quiz:
	def __init__(self,root,user_id=None,callback=None):
		self.root = root
		self.user_id =user_id
		self.quiz_id = None
		self.menuframe = tk.Frame(self.root)
		self.test = None
		self.conn = sqlite3.connect("Quiz.db")
		self.menubuttons = None
		self.Menu()
		self.menuframe.pack()
		self.data = None
		self.callback  = callback

	def Menu(self):
		if self.menubuttons is None:
			cursor =  self.conn.execute("SELECT * FROM quizzes")
			row = cursor.fetchall()
			label = tk.Label(self.menuframe,text="Quizzes Available!",font=("Verdana",50))
			label.grid(row=0,column=0,sticky="W")
			exitbtn = tk.Button(self.menuframe,text="Exit",font=MEDIUM_FONT,command=self.Exit)
			exitbtn.grid(row=0,column=2,sticky="E")
			self.menubuttons = []
			for i in range(0,len(row)):
				self.menubuttons.append(tk.Button(self.menuframe,text=row[i][1],font=("Verdana",30),relief=tk.FLAT,command=lambda j=i:self.Start(row[j],j)))
				self.menubuttons[i].grid(row=i+1,column=0,padx=10,sticky="W")
			self.menuframe.pack()
		else:
			self.test.HideInstruction()
			self.menuframe.pack()

	def Start(self,row,button_row):
		file = open(row[2],"r")
		try:
			data = json.loads(file.read())
		except:
			return
		if  data["date"]["year"] != 0 and data["date"]["month"] != 0 and  data["date"]["day"] != 0 :
			if date.today().year == data["date"]["year"] and date.today().month == data["date"]["month"] and date.today().day == data["date"]["day"]:
				pass
			else:
				lbl = tk.Label(self.menuframe,text="Quiz will be available on " + str(data["date"]["day"]) + "/" + str(data["date"]["month"]) + "/" + str(data["date"]["year"]),font=MEDIUM_FONT)
				lbl.grid(row=button_row+1,column=1)
				return
		if data["time"]["hour"] != 0 or data["time"]["minute"] != 0:
			now = datetime.now()
			current_time = current_time = now.strftime("%H:%M:%S")
			current_time = current_time.split(":")
			current_time[0] = int(current_time[0])
			current_time[1] = int(current_time[1])
			if current_time[0] >= data["time"]["hour"] and current_time[1] >= data["time"]["minute"]:
				pass
			else:
				quiz_time = ""
				if data["time"]["hour"] < 10:
					quiz_time = "0"+ str(data["time"]["hour"])
				else:
					quiz_time = str(data["time"]["hour"])
				quiz_time += ":"
				if data["time"]["minute"] < 10:
					quiz_time += "0"+ str(data["time"]["minute"])
				else:
					quiz_time +=  str(data["time"]["minute"])
				lbl = tk.Label(self.menuframe,text="Quiz will be available at " + quiz_time,font=MEDIUM_FONT)
				lbl.grid(row=button_row+1,column=1)
				return
		self.test = Test(self.root,data,self.CallBack)
		conn = sqlite3.connect("Quiz.db")
		cur = conn.cursor()
		cur.execute("SELECT response_count FROM responses WHERE user=? AND quiz=?",(self.user_id,data["id"]))
		rrow = cur.fetchall()
		if len(rrow) > 0:
			if rrow[0][0] < data["response_limit"] or data["response_limit"] == 0:
				self.test = Test(self.root,data,self.CallBack)
				self.menuframe.pack_forget()
				self.test.Instruction(data,self.test.Grid,self.Menu)
				self.data = data
			else:
				lbl = tk.Label(self.menuframe,text="Already Exceeded Response Limit!",font=MEDIUM_FONT)
				lbl.grid(row=button_row+1,column=1)
		else:
			self.test = Test(self.root,data,self.CallBack)
			self.menuframe.pack_forget()
			self.test.Instruction(data,self.test.Grid,self.Menu)
			self.data = data


	def CallBack(self,data=None):
		conn = sqlite3.connect("Quiz.db")
		curr = conn.cursor()
		curr.execute("SELECT * FROM responses WHERE user=? AND quiz=?",(self.user_id,data["test"],))
		row = curr.fetchall()
		if len(row) == 0:
			curr.execute("SELECT username FROM users WHERE id=?",(self.user_id,))
			row = curr.fetchall()
			uname = row[0][0]
			curr.execute("SELECT name,id FROM quizzes WHERE id=?",(data["test"],))
			row = curr.fetchall()
			qname = row[0][0]
			path = "response/"+uname+"_"+qname+".json"
			file = open(path,"w")
			self.Evaluate(data)
			json.dump(data,file)
			curr.execute("INSERT INTO responses(user,quiz,response) VALUES(?,?,?)",(self.user_id,row[0][1],path,))
		else:
			curr.execute("UPDATE responses SET response_count=response_count+1 WHERE user=? AND quiz=? ",(self.user_id,row[0][1],))
			file = open(row[0][2],"w")
			self.Evaluate(data)
			json.dump(data,file)
		conn.commit()
		self.test.Destroy()
		del self.test 
		self.test = None
		self.menuframe.pack()


	def Evaluate(self,response=None,):
		if self.data and response is not None:
			response["max_points"] = 0
			response["score"] = 0
			response["correct"] = 0
			response["incorrect"] = 0
			response["no_response"] = 0
			for i in range(0,len(response["response"])):
				response["max_points"] += response["response"][i][3]
				if response["response"][i][2] ==  response["response"][i][4]:
					#correct
					response["score"] += response["response"][i][3]
					response["response"][i].append(1)
					response["correct"] += 1
				elif  len(response["response"][i][4]) == 0:
					#no response
					response["response"][i].append(0)
					response["no_response"] += 1
				else:
					#wrong
					response["response"][i].append(-1)
					response["incorrect"] += 1

	def Exit(self):
		if self.menuframe is not None:
			self.menuframe.destroy()
		if __name__ == "__main__":
			self.root.destroy()
		else:
			if self.callback is not None:
				self.callback()

						
if __name__ == "__main__" :
	window = tk.Tk()
	window.geometry("1024x768")
	window.title("Quiz App")
	#file = open("quiz.json","r")
	#data = json.loads(file.read())

	Q =Quiz(window,1)
	window.mainloop()
		