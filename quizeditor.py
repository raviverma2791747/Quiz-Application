import tkinter as tk
from tkinter import filedialog as fd 
from tkcalendar import Calendar,DateEntry
from tkinter import messagebox as mb
import datetime as dt
import json
import sqlite3

class Option:
	def __init__(self,root,data=None,):
		self.root = root 
		self.text = tk.StringVar() 
		self._id = None

		self.optiontxtlbl = tk.Label(self.root,text="Option")
		self.optiontxt = tk.Text(self.root,height=1)

		if data is not None:
			if "option" in data:
				self.optiontxt.insert(tk.INSERT,data["option"])
			
	def Grid(self,row=0,column=0):
		self.optiontxtlbl.grid(row=row,column=column,)
		self.optiontxt.grid(row=row,column=column+1)

	def Destroy(self):
		self.optiontxtlbl.destroy()
		self.optiontxt.destroy()

	def Export(self):
		data = {}
		data["option"] = self.optiontxt.get("1.0","end").rstrip("\n")
		return data

	def View(self):
		pass

class Question:
	def __init__(self,root,data=None,):
		self.root = root 
		self.id = None
		self.options = None
		self.removeoptionsbtn = None
		self.keys = None
		self.time_limit = None
		self.note = None
		self.answer = None
		self.jumble = None
		self.responses = None

		self.frame = tk.LabelFrame(self.root,)
		self.questiontxtlbl = tk.Label(self.frame,text="Question")
		self.questiontxt = tk.Text(self.frame,height=2)
		self.quesbtnframe = tk.Frame(self.frame,)
		self.addoptionsbtn = tk.Button(self.quesbtnframe,text="Add Option",command=self.AddOption)		

		if data is not None:
				if "question" in data:
					self.questiontxt.insert(tk.INSERT,data["question"])
					for i in range(0,len(data["options"])):
						self.AddOption(data["options"][i])

	def AddOption(self,data=None):
		if self.options is None:
			self.options = list()
			if data is None:
				self.options.append(Option(self.frame))
			else:
				self.options.append(Option(self.frame,data))
			self.options[len(self.options)-1].Grid(len(self.options),0)

			self.removeoptionsbtn = list()
			self.removeoptionsbtn.append(tk.Button(self.frame,text="Remove",command=lambda i=len(self.options) : self.RemoveOption(i-1)))
			self.removeoptionsbtn[len(self.removeoptionsbtn)-1].grid(row=len(self.removeoptionsbtn),column=2,)
		else:
			if data is None:
				self.options.append(Option(self.frame))
			else:
				self.options.append(Option(self.frame,data))
			self.options[len(self.options)-1].Grid(len(self.options),0)

			self.removeoptionsbtn.append(tk.Button(self.frame,text="Remove",command=lambda i=len(self.options) : self.RemoveOption(i-1)))
			self.removeoptionsbtn[len(self.removeoptionsbtn)-1].grid(row=len(self.removeoptionsbtn),column=2,)
	
	def RemoveOption(self,index=None):
		if index is not None:
			self.options[index].Destroy()
			self.removeoptionsbtn[index].destroy()
			del self.options[index]
			del	self.removeoptionsbtn[index]
			for i in range(0,len(self.options)):
				self.removeoptionsbtn[i].config(command=lambda: self.RemoveOption(i))

	def Grid(self,row=0,column=0):
		self.questiontxtlbl.grid(row=0,column=0)
		self.questiontxt.grid(row=0,column=1)
		self.quesbtnframe.grid(row=0,column=2)
		self.addoptionsbtn.grid(row=2,column=0)
		self.frame.grid(row=row,column=column,)

	def Destroy(self):
		self.frame.destroy()

	def Export(self):
		data = {}
		data["question"] = self.questiontxt.get("1.0","end").rstrip("\n")
		data["options"] = []
		if self.options is not None:
			for i in self.options:
				data["options"].append(i.Export())
		return data
		
class Section:
	def __init__(self,root,data=None):
		self.root = root
		self.id = None
		self.name = None
		self.time_limit = None
		self.questions = None
		self.jumble = None
		self.removequestionsbtn = None

		self.frame = tk.Frame(self.root,)
		self.sectionframe = tk.LabelFrame(self.frame,)
		self.questionframe = tk.Frame(self.frame,)

		self.sectionnamelbl = tk.Label(self.sectionframe,text="Section Name")
		self.sectionametext= tk.Text(self.sectionframe,height="2")
		self.sectionbtnframe = tk.Frame(self.sectionframe,)
		#self.sectionremovebtn = tk.Button(self.sectionbtnframe,text="Remove",command=lambda:self.frame.destroy())
		self.addquestionbtn = tk.Button(self.sectionbtnframe,text="Add Question",command=self.AddQuestion)

		if data is not None:
			if "section" in data:
				self.sectionametext.insert(tk.INSERT,data["section"])
				for i in range(0,len(data["questions"])):
					self.AddQuestion(data["questions"][i])

	def SetName(self,name=None):
		if name is not None:
			self.name = name

	def SetTimeLimit(self,time_limit=None):
		if time_limit is not None:
			pass

	def AddQuestion(self,data=None):
		if self.questions is None:
			self.questions = list()
			if data is None:
				self.questions.append(Question(self.questionframe))
			else:
				self.questions.append(Question(self.questionframe,data))
			self.questions[len(self.questions)-1].Grid(len(self.questions)-1,0)

			self.removequestionsbtn = list()
			self.removequestionsbtn.append(tk.Button(self.questionframe,text="Remove",command=lambda i=len(self.questions):self.RemoveQuestion(i-1)))
			self.removequestionsbtn[len(self.removequestionsbtn)-1].grid(row=len(self.questions)-1,column=1,sticky= tk.NW)
		else:
			if data is None:
				self.questions.append(Question(self.questionframe))
			else:
				self.questions.append(Question(self.questionframe,data))
			self.questions[len(self.questions)-1].Grid(len(self.questions)-1,0)

			self.removequestionsbtn.append(tk.Button(self.questionframe,text="Remove",command=lambda i=len(self.questions):self.RemoveQuestion(i-1)))
			self.removequestionsbtn[len(self.removequestionsbtn)-1].grid(row=len(self.questions)-1,column=1,sticky= tk.NW)
	
	def IsJumbled(self,jumble = False):
		self.jumble = jumble

	def Show(self):
		print("Section")
		if self.name is not None:
			print("Name: " + self.name)
		else:
			print("Name: None ")
		if self.questions is not None:
			for i in self.questions:
				i.Show()
		else:
			print("Sections: None")

	def RemoveQuestion(self,index=None):
		if index is not None:
			self.questions[index].Destroy()
			self.removequestionsbtn[index].destroy()
			del self.questions[index]
			del self.removequestionsbtn[index]
			for i in range(0,len(self.questions)):
				self.removequestionsbtn[i].config(command=lambda:self.RemoveQuestion(i))

	def Destroy(self):
		self.frame.destroy()

	def Grid(self,row=0,column=0):
		self.sectionnamelbl.grid(row=0,column=0)
		self.sectionametext.grid(row=0,column=1)
		self.sectionbtnframe.grid(row=0,column=2)
		#self.sectionremovebtn.grid(row=0,column=0)
		self.addquestionbtn.grid(row=1,column=0)
		self.sectionframe.grid(row=0,column=0,sticky=tk.NW)
		self.questionframe.grid(row=1,column=0,sticky=tk.NW,padx=50)
		self.frame.grid(row=row,column=column,sticky=tk.NW)

	def Export(self):
		data = {}
		data["section"] = self.sectionametext.get("1.0","end").rstrip("\n")
		data["questions"] = []
		if self.questions is not None:
			for i in self.questions:
				data["questions"].append(i.Export())
		return data

class Instruction:
	def __init__(self,data=None):
		self.data = data

	def Export(self):
		data = {}
		data["instructions"] = []
		if "time_limit" in self.data:
			if self.data["time_limit"]["hour"] == "0" and self.data["time_limit"]["minute"] == "0":
				data["instructions"].append({"instruction":"There is no limit for the quiz.",})
			else:
				if self.data["time_limit"]["hour"] == "0" and self.data["time_limit"]["minute"] != "0" :
					data["instructions"].append({"instruction":"You have " + self.data["time_limit"]["minute"] + " minutes", })
				elif self.data["time_limit"]["hour"] != "0" and self.data["time_limit"]["minute"] == "0":
					data["instructions"].append({"instruction":"You have " + self.data["time_limit"]["hour"] + " hours", })
				else:
					data["instructions"].append({"instruction":"You have " + self.data["time_limit"]["hour"] + " hours and " + self.data["time_limit"]["minute"] + " minutes", })
		
		if "sections" in self.data:
			if len(self.data["sections"]) > 0:
				data["instructions"].append({"instruction": "There are " + str(len(self.data["sections"])) + " sections in total",})
				for i in range(0,len(self.data["sections"])):
					if "questions" in self.data["sections"][i]:
						if len(self.data["sections"][i]["questions"]) > 0 :
							data["instructions"].append({"instruction":"In the section " + self.data["sections"][i]["section"] + " there are " + str(len(self.data["sections"][i]["questions"])) + " questions in total",})

		return data

class Test:
	def __init__(self,root,data=None,_id=None,name=None,path=None):
		self.root = root
		self._id = _id
		self.name = name
		self.path = path
		self.sections = None
		self.removesectionsbtn = None
		self.time_limit = None
		self.instruction = None

		self.testdatevar = tk.IntVar()
		self.testtimevar = tk.IntVar()
		self.testtimelimitvar = tk.IntVar()

		self.wrapperframe = tk.Frame(self.root,)
		self.canvas = tk.Canvas(self.wrapperframe,)
		self.yscollbar = tk.Scrollbar(self.wrapperframe,orient="vertical",command=self.canvas.yview)

		self.canvas.configure(yscrollcommand=self.yscollbar.set)
		self.canvas.bind("<Configure>",lambda e:self.canvas.configure(scrollregion = self.canvas.bbox("all")))
		self.canvas.bind("")

		self.frame  = tk.LabelFrame(self.canvas,)
		self.testframe  = tk.Frame(self.frame,)
		self.sectionframe = tk.LabelFrame(self.frame,)

		self.testnamelabel = tk.Label(self.testframe,text="Quiz Name",)
		self.testnametext = tk.Text(self.testframe,height=1)

		self.testbtnframe = tk.Frame(self.testframe,)
		self.testtimelimitlbl = tk.Label(self.testbtnframe,text="Quiz Time Limit")
		self.testtimelimitframe = tk.Frame(self.testbtnframe)
		self.testtimelimithrlbl = tk.Label(self.testtimelimitframe,text="Hours")
		self.testtimelimithrspnbox = tk. Spinbox(self.testtimelimitframe,from_=0,to=24,wrap=True,width=2,state="disabled")
		self.testtimelimitminlbl = tk.Label(self.testtimelimitframe,text="Minutes")
		self.testtimelimitminspnbox = tk. Spinbox(self.testtimelimitframe,from_=0,to=59,wrap=True,width=2,state="disabled")
		#self.testtimelimitseclbl = tk.Label(self.testtimelimitframe,text="Seconds")
		#self.testtimelimitsecspnbox = tk. Spinbox(self.testtimelimitframe,from_=0,to=60,wrap=True,width=2,state="disabled")
		self.testtimelimitchkbtn = tk.Checkbutton(self.testbtnframe,variable=self.testtimelimitvar ,command=self.ToggleTimeLimit)
		self.addsectionbtn = tk.Button(self.testbtnframe,text="Add Section",command=self.AddSection)
		self.testtimelbl =tk.Label(self.testbtnframe,text="Quiz Time")
		self.testdatelbl = tk.Label(self.testbtnframe,text="Quiz Date")
		self.testtimeframe = tk.Frame(self.testbtnframe)
		self.testtimehrlbl = tk.Label(self.testtimeframe,text="Hours")
		self.testtimehrspnbox = tk. Spinbox(self.testtimeframe,from_=0,to=24,wrap=True,width=2,state="disabled")
		self.testtimeminlbl = tk.Label(self.testtimeframe,text="Minutes")
		self.testtimeminspnbox = tk. Spinbox(self.testtimeframe,from_=0,to=59,wrap=True,width=2,state="disabled")
		#self.testtimeseclbl = tk.Label(self.testtimeframe,text="Seconds")
		#self.testtimesecspnbox = tk. Spinbox(self.testtimeframe,from_=0,to=60,wrap=True,width=2,state="disabled")
		self.testtimechkbtn = tk.Checkbutton(self.testbtnframe,variable=self.testtimevar,command=self.ToggleTime)
		self.testdate = DateEntry(self.testbtnframe,width=30,bg="darkblue",fg="white",year=2020,mindate=dt.date.today(),state="disabled")
		self.testdatechkbtn = tk.Checkbutton(self.testbtnframe,variable=self.testdatevar,command=self.ToggleDate)
		if data is not None:
			if "test" in data:
				self.testnametext.insert(tk.INSERT,data["test"])
				for i in range(0,len(data["sections"])):
					self.AddSection(data["sections"][i])
			if "date" in data:
				if data["date"]["day"] == "0" and data["date"]["month"] == "0" and data["date"]["year"] == "0":
					self.testdatevar.set(0)
				else:
					self.testdatevar.set(1)
					self.testdate.configure(state="enabled")
					self.testdate.set_date(dt.datetime(int(data["date"]["year"]),int(data["date"]["month"]),int(data["date"]["day"])))
			if "time" in data:
				if data["time"]["hour"] == "0" and data["time"]["minute"] == "0":
					self.testtimevar.set(0)
				else:
					self.testtimevar.set(1)
					self.testtimehrspnbox.configure(state="normal")
					self.testtimehrspnbox.delete(0,"end")
					self.testtimehrspnbox.insert(tk.INSERT,data["time"]["hour"])
					self.testtimeminspnbox.configure(state="normal")
					self.testtimeminspnbox.delete(0,"end")
					self.testtimeminspnbox.insert(tk.INSERT,data["time"]["minute"])
			if "time_limit" in data:
				if data["time_limit"]["hour"] == "0" and data["time_limit"]["minute"] == "0":
					self.testtimelimitvar.set(0)
				else:
					self.testtimelimitvar.set(1)
					self.testtimelimithrspnbox.configure(state="normal")
					self.testtimelimithrspnbox.delete(0,"end")
					self.testtimelimithrspnbox.insert(tk.INSERT,data["time_limit"]["hour"])
					self.testtimelimitminspnbox.configure(state="normal")
					self.testtimelimitminspnbox.delete(0,"end")
					self.testtimelimitminspnbox.insert(tk.INSERT,data["time_limit"]["minute"])

	def AddSection(self,data=None):
		if self.sections is None:
			self.sections = list()
			if data is not None:
				self.sections.append(Section(self.sectionframe,data))
			else:
				self.sections.append(Section(self.sectionframe,))
			self.sections[len(self.sections)-1].Grid(len(self.sections)-1,0)

			self.removesectionsbtn = list()
			self.removesectionsbtn.append(tk.Button(self.sectionframe,text="Remove",command=lambda i=len(self.sections): self.RemoveSection(i-1)))
			self.removesectionsbtn[len(self.removesectionsbtn)-1].grid(row=len(self.sections)-1,column=1,sticky=tk.NW)
		else:
			if data is not None:
				self.sections.append(Section(self.sectionframe,data))
			else:
				self.sections.append(Section(self.sectionframe,))
			self.sections[len(self.sections)-1].Grid(len(self.sections)-1,0)

			self.removesectionsbtn.append(tk.Button(self.sectionframe,text="Remove",command=lambda i=len(self.sections): self.RemoveSection(i-1)))
			self.removesectionsbtn[len(self.sections)-1].grid(row=len(self.sections)-1,column=1,sticky=tk.NW)

	def Grid(self,row=0,column=0):
		self.testnamelabel.grid(row=0,column=0)
		self.testnametext.grid(row=0,column=1)
		self.addsectionbtn.grid(row=0,column=0)
		self.testtimelimitlbl.grid(row=3,column=0)
		self.testtimelimithrlbl.grid(row=0,column=0)
		self.testtimelimithrspnbox.grid(row=0,column=1)
		self.testtimelimitminlbl.grid(row=0,column=2)
		self.testtimelimitminspnbox.grid(row=0,column=3)
		#self.testtimelimitseclbl.grid(row=0,column=4)
		#self.testtimelimitsecspnbox.grid(row=0,column=5)
		self.testtimelimitframe.grid(row=3,column=1)
		self.testtimelimitchkbtn.grid(row=3,column=2)
		self.testdatelbl.grid(row=1,column=0)
		self.testdate.grid(row=1,column=1)
		self.testdatechkbtn.grid(row=1,column=2)
		self.testtimelbl.grid(row=2,column=0)
		self.testtimehrlbl.grid(row=0,column=0)
		self.testtimehrspnbox.grid(row=0,column=1)
		self.testtimeminlbl.grid(row=0,column=2)
		self.testtimeminspnbox.grid(row=0,column=3)
		#self.testtimeseclbl.grid(row=0,column=4)
		#self.testtimesecspnbox.grid(row=0,column=5)
		self.testtimechkbtn.grid(row=2,column=2)
		self.testtimeframe.grid(row=2,column=1)
		self.testbtnframe.grid(row=0,column=2)
		self.testframe.grid(row = 0,column = 0,sticky=tk.NW)
		self.sectionframe.grid(row = 1,column = 0,padx = 70)
		#self.canvas.pack(side=tk.LEFT,fill="both",expand="yes")
		#self.yscollbar.pack(side=tk.RIGHT,fill="y")
		self.canvas.pack(side=tk.LEFT,fill="both",expand="yes")
		self.yscollbar.pack(side=tk.LEFT,fill="y",)
		self.canvas.create_window((0,0),window=self.frame,anchor="nw")
		self.wrapperframe.pack(fill="both",expand="yes")

	def RemoveSection(self,index=None):
		if index is not None:
			self.sections[index].Destroy()
			self.removesectionsbtn[index].destroy()
			del self.sections[index]
			del self.removesectionsbtn[index]
			for i in range(0,len(self.sections)):
				self.removesectionsbtn[i].config(command=lambda:self.RemoveSection(i))

	def Destroy(self):
		self.wrapperframe.destroy()

	def GetID(self):
		return self._id

	def ToggleTimeLimit(self):
		if self.testtimelimitvar.get() == 0:
			self.testtimelimithrspnbox.configure(state="disabled")
			self.testtimelimitminspnbox.configure(state="disabled")
			#self.testtimelimitsecspnbox.configure(state="disabled")
		else:
			self.testtimelimithrspnbox.configure(state="normal")
			self.testtimelimitminspnbox.configure(state="normal")
			#self.testtimelimitsecspnbox.configure(state="normal")

	def ToggleTime(self):
		if self.testtimevar.get() == 0:
			self.testtimehrspnbox.configure(state="disabled")
			self.testtimeminspnbox.configure(state="disabled")
			#self.testtimesecspnbox.configure(state="disabled")
		else:
			self.testtimehrspnbox.configure(state="normal")
			self.testtimeminspnbox.configure(state="normal")
			#self.testtimesecspnbox.configure(state="normal")

	def ToggleDate(self):
		if self.testdatevar.get() == 0:
			self.testdate.configure(state="disabled")
		else:
			self.testdate.configure(state="enabled")

	def Export(self,savedialog=None):
		if self.path and  self._id and self.name is not None:
			data = {}
			data["test"] = self.testnametext.get("1.0","end").rstrip("\n")
			if self.testdatevar.get() == 0:
				data["date"] = {"day":"0","month":"0","year":"0",}
			else:
				date = str(self.testdate.get_date())
				date = date.split("-")
				data["date"] = {"day":date[2],"month":date[1],"year":date[0],}
			if self.testtimevar.get() == 0:
				data["time"] = {"hour":"0" ,"minute": "0","second":"0",}
			else:
				data["time"] = {"hour":self.testtimehrspnbox.get() ,"minute": self.testtimeminspnbox.get(),"second":"0",}
			if self.testtimelimitvar.get() == 0:
				data["time_limit"] = {"hour": "0", "minute": "0","second":"0",}
			else:
				data["time_limit"] = {"hour": self.testtimelimithrspnbox.get() , "minute": self.testtimelimitminspnbox.get(),"second":"0",}
			data["sections"] = []
			if self.sections is not None:
				for i in self.sections:
					data["sections"].append(i.Export())
			I = Instruction(data)
			data.update(I.Export())
			file = open(self.path,"w")
			json.dump(data,file)
		else:
			self.name = savedialog.name.split("/")
			self.name = self.name[len(self.name)-1]
			self.name = self.name.split(".")
			self.name = self.name[0]
			self.path = savedialog.name
			conn = sqlite3.connect("Quiz.db")
			cursor = conn.cursor()
			cursor.execute("INSERT INTO quizzes (name,path) VALUES (?,?)",(self.name,self.path))
			conn.commit()
			cursor.execute("SELECT id FROM quizzes WHERE path=?",(self.path,))
			self._id = cursor.fetchone()[0]
			data = {}
			data["test"] = self.testnametext.get("1.0","end")
			if self.testdatevar.get() == 0:
				data["date"] = {"day":"0","month":"0","year":"0",}
			else:
				date = str(self.testdate.get_date())
				date = date.split("-")
				data["date"] = {"day":date[2],"month":date[1],"year":date[0],}
			if self.testtimevar.get() == 0:
				data["time"] = {"hour":"0" ,"minute": "0","second":"0",}
			else:
				data["time"] = {"hour":self.testtimehrspnbox.get() ,"minute": self.testtimeminspnbox.get(),"second":"0",}
			if self.testtimelimitvar.get() == 0:
				data["time_limit"] = {"hour": "0", "minute": "0","second":"0",}
			else:
				data["time_limit"] = {"hour": self.testtimelimithrspnbox.get() , "minute": self.testtimelimitminspnbox.get(),"second":"0",}
			data["sections"] = []
			if self.sections is not None:
				for i in self.sections:
					data["sections"].append(i.Export())
			I = Instruction(data)
			data.update(I.Export())
			savedialog.write(json.dumps(data))
		mb.showinfo('Saved', "File has been saved successfully!")

class QuizEditor:
	def __init__(self,root):
		self.root = root
		self.test = None
		self.conn =  sqlite3.connect("Quiz.db")
		self.openwindow = None
		self.openwindowbtns = None
		self.menubar = tk.Menu(root)

		self.filemenubar = tk.Menu(self.menubar,tearoff=0)
		self.filemenubar.add_command(label="New",command=self.New)
		self.filemenubar.add_command(label="Open",command=self.Open)
		self.filemenubar.add_command(label="Save",command=self.Save)
		self.filemenubar.add_command(label="Exit",command=self.Exit)

		self.menubar.add_cascade(label="File",menu=self.filemenubar)
		self.menubar.add_command(label="About",command=self.About)
		self.root.configure(menu=self.menubar)

		self.savedialog = None

	def About(self):
		aboutwindow = tk.Toplevel(self.root)
		aboutwindow.title("About")
		aboutwindow.geometry("300x100+100+100")
		aboutwindow.resizable(height = False , width = False)
		abouttext = tk.Text(aboutwindow,font=("Verdana", 20))
		abouttext.insert(tk.INSERT,"Version 1.0")
		abouttext.configure(state='disabled')
		abouttext.pack()

	def New(self,_id=None,name=None,path=None):
		if self.test is None:
			if _id and name and path is not None:
				file = open(path,"r")
				try :
					data = json.loads(file.read())
				except:
					print("json file error")
					return 
				self.test = Test(self.root,data,_id,name,path)
				self.openwindow.destroy()
				self.openwindow = None
			else:
				self.test = Test(self.root,)
			self.test.Grid()
		else:
			self.Save()
			self.DestroyTest()
			self.New()

	def Open(self):
		if self.test is None:
			self.openwindow = tk.Toplevel(self.root)
			self.openwindow.geometry("200x200")
			self.openwindow.title("Open")
			cursor = self.conn.cursor().execute("SELECT * FROM quizzes")
			quizzes = cursor.fetchall()
			if len(quizzes) == 0:
				lbl = tk.Label(self.openwindow,text="No quizzes to edit")
				lbl.pack()
			else:
				self.openwindowbtns = []
				for i in range(0,len(quizzes)):
					self.openwindowbtns.append(tk.Button(self.openwindow,text=quizzes[i][1],command=lambda j=i:self.New(quizzes[j][0],quizzes[j][1],quizzes[j][2])))
					self.openwindowbtns[i].pack()
		else:
			self.Save()
			self.DestroyTest()
			self.Open()

	def Save(self):
		if self.test is not None:
			if self.test.GetID() is None:
				self.SaveDialog()
			else:
				self.test.Export()

	def Exit(self):
		if self.test is not None:
			self.Save()
		self.root.destroy()

	def SaveDialog(self):
		self.savedialog = fd.asksaveasfile(filetypes = [("JSON","*.json")], defaultextension = [("JSON","*.json")]) 
		if self.savedialog is not None:
			self.test.Export(self.savedialog)

	def DestroyTest(self):
		self.test.Destroy()
		self.test = None
		if self.savedialog is not None:
			self.savedialog.destroy()
	
window = tk.Tk()
window.geometry("1024x768")
window.title("Quiz App")
Q =  QuizEditor(window)
window.mainloop()