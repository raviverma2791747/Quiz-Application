import tkinter as tk
import json

class Option:
	def __init__(self,root):
		self.root = root 
		self.text = tk.StringVar() 
		self.id = None

		self.optiontxtlbl = tk.Label(self.root,text="Option")
		self.optiontxt = tk.Text(self.root,height=1)

	def SetText(self,text=None):
		if text is not None:
			self.text = text
		else:
			pass

	def Show(self):
		print("Option")
		if self.text is not None:
			print("Text: " + self.text)
		else:
			print("Text: None ")

	def Grid(self,row=0,column=0):
		self.optiontxtlbl.grid(row=row,column=column)
		self.optiontxt.grid(row=row,column=column+1)

	def Destroy(self):
		self.optiontxtlbl.destroy()
		self.optiontxt.destroy()

	def Export(self):
		data = {}
		data["option"] = self.optiontxt.get("1.0","end")
		return data

	def TestView(self):
		img1 = tk.PhotoImage(file='unchecked.png')
		img2 = tk.PhotoImage(file='checked.png')
		R = tk.Checkbutton(self.root,image=img1, compound='left',selectimage=img2).grid(row=0,column=0,)
		self.optiontxt.grid(row=0,column=1)

class Question:
	def __init__(self,root,options=None,keys=None,time_limit=None,note=None,answer=None,jumble=None,responses=None):
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

		self.frame = tk.Frame(self.root,highlightbackground="black",highlightthickness=1,)
		self.questiontxtlbl = tk.Label(self.frame,text="Question")
		self.questiontxt = tk.Text(self.frame,height=4)
		self.quesbtnframe = tk.Frame(self.frame,)
		self.questionsavebtn = tk.Button(self.quesbtnframe,text="Save",)
		self.addoptionsbtn = tk.Button(self.quesbtnframe,text="Add Option",command=self.AddOption)
		
	def SetText(self,text=None):
		if text is not None:
			self.text = text
		else:
			pass

	def SetTimeLimit(self,time_limit=None):
		if time_limit is not None:
			pass
		else:
			pass

	def IsJumbled(self,jumble = False):
		self.jumble = jumble

	def AddOption(self):
		if self.options is None:
			self.options = list()
			self.options.append(Option(self.frame))
			self.options[len(self.options)-1].Grid(len(self.options),0)

			self.removeoptionsbtn = list()
			self.removeoptionsbtn.append(tk.Button(self.frame,text="Remove",command=lambda i=len(self.options) : self.RemoveOption(i-1)))
			self.removeoptionsbtn[len(self.removeoptionsbtn)-1].grid(row=len(self.removeoptionsbtn),column=2,)
		else:
			self.options.append(Option(self.frame))
			self.options[len(self.options)-1].Grid(len(self.options),0)

			self.removeoptionsbtn.append(tk.Button(self.frame,text="Remove",command=lambda i=len(self.options) : self.RemoveOption(i-1)))
			self.removeoptionsbtn[len(self.removeoptionsbtn)-1].grid(row=len(self.removeoptionsbtn),column=2,)
	
	def AddKey(self,key):
		if key is not None:
			if self.keys is None:
				self.keys = list()
				self.keys.append(key)
			else:
				self.keys.append(key)
		else:
			pass

	def AddRespose(self,responses =  None):
		if responses is not None:
			if self.responses is None:
				self.responses = list()
				self.responses.append(responses)
		else:
			pass

	def Show(self):
		print("Question: ")
		if self.text is not None:
			print("Text: " + self.text)
		else:
			print("Text: None ")

		if self.options is not None:
			for i in self.options:
				i.Show()
		else:
			print("Options: None")

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
		self.questionsavebtn.grid(row=0,column=0,)
		self.addoptionsbtn.grid(row=2,column=0)
		self.frame.grid(row=row,column=column,pady=10,padx=30)

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
	def __init__(self,root,name = None,time_limit = None,questions = None,jumble = False):
		self.root = root
		self.id = None
		self.name = None
		self.time_limit = None
		self.questions = None
		self.jumble = jumble
		self.removequestionsbtn = None

		self.frame = tk.Frame(self.root,)
		self.sectionframe = tk.Frame(self.frame,highlightbackground="black",highlightthickness=1,)
		self.questionframe = tk.Frame(self.frame,)

		self.sectionnamelbl = tk.Label(self.sectionframe,text="Section Name")
		self.sectionametext= tk.Text(self.sectionframe,height="2")
		self.sectionbtnframe = tk.Frame(self.sectionframe,)
		#self.sectionremovebtn = tk.Button(self.sectionbtnframe,text="Remove",command=lambda:self.frame.destroy())
		self.addquestionbtn = tk.Button(self.sectionbtnframe,text="Add Question",command=self.AddQuestion)

	def SetName(self,name=None):
		if name is not None:
			self.name = name

	def SetTimeLimit(self,time_limit=None):
		if time_limit is not None:
			pass

	def AddQuestion(self):
		if self.questions is None:
			self.questions = list()
			self.questions.append(Question(self.questionframe))
			self.questions[len(self.questions)-1].Grid(len(self.questions)-1,0)

			self.removequestionsbtn = list()
			self.removequestionsbtn.append(tk.Button(self.questionframe,text="Remove",command=lambda i=len(self.questions):self.RemoveQuestion(i-1)))
			self.removequestionsbtn[len(self.removequestionsbtn)-1].grid(row=len(self.questions)-1,column=1,sticky= tk.NW)
		else:
			self.questions.append(Question(self.questionframe))
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
		self.sectionframe.grid(row=0,column=0,pady=10,padx=10)
		self.questionframe.grid(row=1,column=0,padx=10,pady=10)
		self.frame.grid(row=row,column=column,sticky=tk.NW)

	def Export(self):
		data = {}
		data["section"] = self.name
		data["questions"] = []
		if self.questions is not None:
			for i in self.questions:
				data["questions"].append(i.Export())
		return data

class Test:
	def __init__(self,root,name = None,time_limit = None):
		self.root = root
		self.name = name
		self.sections = None
		self.removesectionsbtn = None
		self.time_limit = time_limit

		self.wrapperframe = tk.Frame(self.root,)
		self.canvas = tk.Canvas(self.wrapperframe,)
		self.yscollbar = tk.Scrollbar(self.wrapperframe,orient="vertical",command=self.canvas.yview)

		self.canvas.configure(yscrollcommand=self.yscollbar.set)
		self.canvas.bind("<Configure>",lambda e:self.canvas.configure(scrollregion = self.canvas.bbox("all")))

		self.frame  = tk.Frame(self.canvas,)
		self.testframe  = tk.Frame(self.frame,highlightbackground="black",highlightthickness=1,)
		self.sectionframe = tk.Frame(self.frame,)

		self.testnamelabel = tk.Label(self.testframe,text="Test Name",)
		self.testnametext = tk.Text(self.testframe,height=1)
		self.testtimelimit = tk.Entry(self.testframe)

		self.testbtnframe = tk.Frame(self.testframe,)
		self.addsectionbtn = tk.Button(self.testbtnframe,text="Add Section",command=self.AddSection)
		self.savebtn = tk.Button(self.testbtnframe,text="Save",command=self.Export)

	def SetName(self,name = None):
		if name is not None:
			self.name = name

	def AddSection(self):
		if self.sections is None:
			self.sections = list()
			self.sections.append(Section(self.sectionframe))
			self.sections[len(self.sections)-1].Grid(len(self.sections)-1,0)

			self.removesectionsbtn = list()
			self.removesectionsbtn.append(tk.Button(self.sectionframe,text="Remove",command=lambda i=len(self.sections): self.RemoveSection(i-1)))
			self.removesectionsbtn[len(self.removesectionsbtn)-1].grid(row=len(self.sections)-1,column=1,sticky=tk.NW)
		else:
			self.sections.append(Section(self.sectionframe))
			self.sections[len(self.sections)-1].Grid(len(self.sections)-1,0)

			self.removesectionsbtn.append(tk.Button(self.sectionframe,text="Remove",command=lambda i=len(self.sections): self.RemoveSection(i-1)))
			self.removesectionsbtn[len(self.sections)-1].grid(row=len(self.sections)-1,column=1,sticky=tk.NW)
		
	def Show(self):
		print("Test")
		if self.name is not None:
			print("Name: " + self.name)
		else:
			print("Name: None ")

		if self.sections is not None:
			for i in self.sections:
				i.Show()
		else:
			print("Sections: None")

	def Grid(self,row=0,column=0):
		self.testnamelabel.grid(row=0,column=0)
		self.testnametext.grid(row=0,column=1)
		#self.testtimelimit.pack()
		self.addsectionbtn.grid(row=0,column=0)
		self.savebtn.grid(row=2,column=0)
		self.testbtnframe.grid(row=0,column=2)
		self.testframe.grid(row = 0,column = 0,sticky=tk.NW)
		self.sectionframe.grid(row = 1,column = 0)
		#self.canvas.pack(side=tk.LEFT,fill="both",expand="yes")
		#self.yscollbar.pack(side=tk.RIGHT,fill="y")
		self.canvas.pack(side=tk.LEFT,fill="both",expand="yes")
		self.yscollbar.pack(side=tk.LEFT,fill="y",)
		self.canvas.create_window((0,0),window=self.frame,width=1050,anchor="nw")
		self.wrapperframe.pack(fill="both",expand="yes",padx=10,pady=10)

	def RemoveSection(self,index=None):
		if index is not None:
			self.sections[index].Destroy()
			self.removesectionsbtn[index].destroy()
			del self.sections[index]
			del self.removesectionsbtn[index]
			for i in range(0,len(self.sections)):
				self.removesectionsbtn[i].config(command=lambda:self.RemoveSection(i))

	def Destroy(self):
		pass

	def Export(self):
		data = {}
		data["test"] = self.name
		data["sections"] = []
		if self.sections is not None:
			for i in self.sections:
			    data["sections"].append(i.Export())
		file = open("data.json","w")
		json.dump(data,file)

class QuizEditor:
	def __init__(self,window):
		self.window = window
		self.mainframe = tk.Frame(window,width=window.winfo_screenwidth(),height=window.winfo_screenheight(),highlightbackground="black",highlightthickness=1,)
		self.mainframe.pack_propagate(0)
		self.contentframe = tk.Frame(self.mainframe,width=self.mainframe.winfo_width()/10*7,height=self.mainframe.winfo_height(),highlightbackground="black",highlightthickness=1,)
		self.test = Test(self.contentframe)
		self.contentframe.grid(row = 0 , column = 0)
		self.mainframe.pack(expand=True,fill="both",side = tk.LEFT)


window = tk.Tk()
window.title("Quiz App")
window.geometry("1024x768+10+10")
O = Option(window)
O.TestView()
window.mainloop()