import tkinter as tk

class Option:
	def __init__(self,root):
		self.root = root 
		self.text = None
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


class Question:
	def __init__(self,root,text=None,options=None,keys=None,time_limit=None,note=None,answer=None,jumble=None,responses=None):
		self.root = root 
		self.id = None
		self.text = None
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
		self.questionremovebtn = tk.Button(self.quesbtnframe,text="Remove",command=lambda:self.frame.destroy())
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

	def Grid(self,row=0,column=0):
		self.questiontxtlbl.grid(row=0,column=0)
		self.questiontxt.grid(row=0,column=1)
		self.quesbtnframe.grid(row=0,column=2)
		self.questionsavebtn.grid(row=0,column=0,)
		self.questionremovebtn.grid(row=1,column=0)
		self.addoptionsbtn.grid(row=2,column=0)
		self.frame.grid(row=row,column=column,pady=10,)

	def Destroy(self):
		self.frame.destroy()


		
class Section:
	def __init__(self,root,name = None,time_limit = None,questions = None,jumble = False):
		self.root = root
		self.id = None
		self.name = None
		self.time_limit = None
		self.questions = []
		self.jumble = jumble

		self.frame = tk.Frame(self.root,highlightbackground="black",highlightthickness=1,)
		self.sectionframe = tk.Frame(self.frame,highlightbackground="black",highlightthickness=1,)
		self.questionframe = tk.Frame(self.frame,)

		self.sectionnamelbl = tk.Label(self.sectionframe,text="Section Name")
		self.sectionametext= tk.Text(self.sectionframe,height="4")
		self.sectionbtnframe = tk.Frame(self.sectionframe,)
		self.sectionremovebtn = tk.Button(self.sectionbtnframe,text="Remove",command=lambda:self.frame.destroy())
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
		else:
			self.questions.append(Question(self.questionframe))
			self.questions[len(self.questions)-1].Grid(len(self.questions)-1,0)
	

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

	def Grid(self,row=None,column=None):
		self.sectionnamelbl.grid(row=0,column=0)
		self.sectionametext.grid(row=0,column=1)
		self.sectionbtnframe.grid(row=0,column=2)
		self.sectionremovebtn.grid(row=0,column=0)
		self.addquestionbtn.grid(row=1,column=0)
		self.sectionframe.grid(row=0,column=0,pady=10,padx=10)
		self.questionframe.grid(row=1,column=0,pady=10)
		self.frame.grid(row=0,column=0,pady=10)

class Test:
	def __init__(self,root,name = None,time_limit = None):
		self.root = root
		self.name = name
		self.sections = None
		self.time_limit = time_limit

		self.testframe  = tk.Frame(root,highlightbackground="black",highlightthickness=1,)
		self.sectionsframe = tk.Frame(root,highlightbackground="black",highlightthickness=1,)

		self.testnamelabel = tk.Label(self.testframe,text="Test Name",)
		self.testnametext = tk.Text(self.testframe,height=1)
		self.testtimelimit = tk.Entry(self.testframe)
		self.addsectionbtn = tk.Button(self.testframe,text="Add Section",command=self.AddSection)
		self.savebtn = tk.Button(self.testframe,text="Save")

		self.testnamelabel.pack()
		self.testnametext.pack()
		self.testtimelimit.pack()
		self.addsectionbtn.pack()
		self.savebtn.pack()
		self.testframe.grid(row = 0,column = 0)
		self.sectionsframe.grid(row = 1,column = 0)

	def SetName(self,name = None):
		if name is not None:
			self.name = name

	def AddSection(self):
		if self.sections is None:
			self.sections = list()
			self.sections.append(Section(self.sectionsframe))
		else:
			self.sections.append(Section(self.sectionsframe))
		
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

	def Update():
		for i in sections:
			sections.Update()


class QuizEditor:
	def __init__(self,window):
		self.window = window
		self.mainframe = tk.Frame(window,width=window.winfo_screenwidth(),height=window.winfo_screenheight(),highlightbackground="black",highlightthickness=1,)
		self.mainframe.pack_propagate(0)
		self.contentframe = tk.Frame(self.mainframe,width=self.mainframe.winfo_width()/10*7,height=self.mainframe.winfo_height(),highlightbackground="black",highlightthickness=1,)
		self.test = Test(self.contentframe)
		self.contentframe.grid(row = 0 , column = 0)
		self.mainframe.pack(expand=True,fill="both",side = tk.LEFT)

	def __del__(self):
		pass


window = tk.Tk()
window.title("Quiz App")
window.geometry("1024x768+10+10")
T = Test(window)
T.Grid()
window.mainloop()

