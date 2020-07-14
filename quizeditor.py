import tkinter as tk
from tkinter import filedialog as fd 
import json
import sqlite3

class Option:
	def __init__(self,root,data=None):
		self.root = root 
		self.text = tk.StringVar() 
		self.id = None

		self.optiontxtlbl = tk.Label(self.root,text="Option")
		self.optiontxt = tk.Text(self.root,height=1)

		if data is not None:
			if data["option"] is not None:
				self.optiontxt.insert(tk.INSERT,data["option"])

	def Grid(self,row=0,column=0):
		self.optiontxtlbl.grid(row=row,column=column,)
		self.optiontxt.grid(row=row,column=column+1)

	def Destroy(self):
		self.optiontxtlbl.destroy()
		self.optiontxt.destroy()

	def Export(self):
		data = {}
		data["option"] = self.optiontxt.get("1.0","end")
		return data

class Question:
	def __init__(self,root,data=None):
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
			if data["question"] is not None:
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
		data["question"] = self.questiontxt.get("1.0","end")
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
			if data["section"] is not None:
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
		data["section"] = self.sectionametext.get("1.0","end")
		data["questions"] = []
		if self.questions is not None:
			for i in self.questions:
				data["questions"].append(i.Export())
		return data

class Test:
	def __init__(self,root,data=None,_id=None,name=None,path=None,):
		self.root = root
		self._id = _id
		self.name = name
		self.path = path
		self.sections = None
		self.removesectionsbtn = None
		self.time_limit = None

		self.wrapperframe = tk.Frame(self.root,)
		self.canvas = tk.Canvas(self.wrapperframe,)
		self.yscollbar = tk.Scrollbar(self.wrapperframe,orient="vertical",command=self.canvas.yview)

		self.canvas.configure(yscrollcommand=self.yscollbar.set)
		self.canvas.bind("<Configure>",lambda e:self.canvas.configure(scrollregion = self.canvas.bbox("all")))

		self.frame  = tk.LabelFrame(self.canvas,)
		self.testframe  = tk.Frame(self.frame,)
		self.sectionframe = tk.LabelFrame(self.frame,)

		self.testnamelabel = tk.Label(self.testframe,text="Test Name",)
		self.testnametext = tk.Text(self.testframe,height=1)
		self.testtimelimit = tk.Entry(self.testframe)

		self.testbtnframe = tk.Frame(self.testframe,)
		self.addsectionbtn = tk.Button(self.testbtnframe,text="Add Section",command=self.AddSection)

		if data is not None:
			if data["test"] is not None:
				self.testnametext.insert(tk.INSERT,data["test"])
				for i in range(0,len(data["sections"])):
					self.AddSection(data["sections"][i])

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
		#self.testtimelimit.pack()
		self.addsectionbtn.grid(row=0,column=0)
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

	def Export(self,savedialog=None):
		if self.path and  self._id and self.name is not None:
			data = {}
			data["test"] = self.testnametext.get("1.0","end")
			data["sections"] = []
			if self.sections is not None:
				for i in self.sections:
					data["sections"].append(i.Export())
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
			data["sections"] = []
			if self.sections is not None:
				for i in self.sections:
					data["sections"].append(i.Export())
			savedialog.write(json.dumps(data))

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
				data = json.loads(file.read())
				self.test = Test(self.root,data,_id,name,path)
				self.openwindow.destroy()
				self.openwindow = None
			else:
				self.test = Test(self.root,)
			self.test.Grid()
		else:
			pass

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
					self.openwindowbtns.append(tk.Button(self.openwindow,text=quizzes[i][1],command=lambda:self.New(quizzes[i][0],quizzes[i][1],quizzes[i][2])))
					self.openwindowbtns[i].pack()
		else:
			self.Save()

	def Save(self):
		if self.test is not None:
			if self.test.GetID() is None:
				self.SaveDialog()
			else:
				self.test.Export()

	def Exit(self):
		self.root.destroy()

	def SaveDialog(self):
		self.savedialog = fd.asksaveasfile(filetypes = [("JSON","*.json")], defaultextension = [("JSON","*.json")]) 
		if self.savedialog is not None:
			self.test.Export(self.savedialog)

	def DestroyTest(self):
		self.test.Destroy()
		self.test = None
		self.savedialog.destroy()

window = tk.Tk()
window.geometry("1024x768")
window.title("QuizEditor")

QE = QuizEditor(window)

window.mainloop()
