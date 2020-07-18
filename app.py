import tkinter as tk
import sqlite3
import json
import quizeditor as QE
import quiz as Q


LARGE_FONT = ("Verdana",25)
MEDIUM_FONT = ("Verdana",15)
SMALL_FONT =("Verdana",13)
VERY_SMALL_FONT = ("Verdana",8)

class User:
	def __init__(self,username=None,password=None,privilege=None):
		self.username = username
		self.password = password
		self.privilege = privilege
		self.conn = sqlite3.connect('Quiz.db')
		self.cursor = None
		self.root = None
		self.frame = None

	def Login(self,username,password):
		if username == "":
			print("Invalid Username!")
			return False
		elif password == "":
			print("Invalid Password!")
			return False
		else:
			self.cursor = self.conn.execute("SELECT id,username,password,privilege FROM users WHERE username=? AND password=?",(username,password))
			row = self.cursor.fetchone()
			if( username == row[1] and password == row[2]):
				self.username = row[1]
				self.password = row[2]
				self.privilege = row[3]
				print("Username : " + str(self.username))
				print("Password : " + str(self.password))
				print("Privilege : " + str(self.privilege))
				print("success")
				return True
			else:
				print("Failure")
				return False

	def DashBoard(self):
		window =tk.Tk()
		window.geometry("1024x768")
		frame = tk.Frame(window)
		userleftframe = tk.LabelFrame(frame,height=window.winfo_screenheight(),width=window.winfo_screenwidth()/20*6)
		userdetailsframe = tk.LabelFrame(userleftframe,)

		userrightframe =  tk.LabelFrame(frame,height=window.winfo_screenheight(),width=window.winfo_screenwidth()/20*14)
		
		usernamelbl = tk.Label(userdetailsframe,text="User Name :",font=SMALL_FONT)
		usernamelbl.grid(row=0,column=0)
		usernameentry = tk.Entry(userdetailsframe,width=16,font=SMALL_FONT,)
		usernameentry.insert(tk.INSERT,self.username)
		usernameentry.configure(state="disabled")
		usernameentry.grid(row=0,column=1,)
		usernameeditbtn = tk.Button(userdetailsframe,text="Edit",font=VERY_SMALL_FONT,command=lambda:usernameentry.configure(state="normal"))
		usernameeditbtn.grid(row=0,column=2)
		usernamesavebtn = tk.Button(userdetailsframe,text="Save",font=VERY_SMALL_FONT,command=lambda:usernameentry.configure(state="disabled"))
		usernamesavebtn.grid(row=0,column=3)

		passwordlbl =tk.Label(userdetailsframe,text="Password:",font=SMALL_FONT)
		passwordlbl.grid(row=1,column=0)
		passwordentry = tk.Entry(userdetailsframe,width=16,font=SMALL_FONT)
		passwordentry.insert(tk.INSERT,self.password)
		passwordentry.configure(state="disabled")
		passwordentry.grid(row=1,column=1)
		passwordviewbtn = tk.Button(userdetailsframe,text="View",font=VERY_SMALL_FONT)
		passwordviewbtn.grid(row=1,column=2)
		passwordeditbtn = tk.Button(userdetailsframe,text="Edit",font=VERY_SMALL_FONT)
		passwordeditbtn.grid(row=1,column=3)
		passwordsavebtn = tk.Button(userdetailsframe,text="Save",font=VERY_SMALL_FONT)
		passwordsavebtn.grid(row=1,column=4)

		privilegelbl =tk.Label(userdetailsframe,text="Role :",font=SMALL_FONT)
		privilegelbl.grid(row=2,column=0)
		privilege = None
		if self.privilege == 0:
			privilege = tk.Label(userdetailsframe,text="User",font=SMALL_FONT)
		else:
			privilege = tk.Label(userdetailsframe,text="User",font=SMALL_FONT)
		privilege.grid(row=2,column=1)
		userdetailsframe.grid(row=0,column=0,sticky="E")
		userleftframe.grid(row=0,column=0)
		userleftframe.grid_propagate(0)
		userrightframe.grid(row=0,column=1)
		userrightframe.grid_propagate(0)
		frame.pack(fill="both",expand="true")
		window.mainloop()


	def GetPrivilege(self):
		return self.privilege

	def GetUsername(self):
		return self.username

	def GetUserId(self):
		return self._id

class LoginWindow:
	def __init__(self,user):
		self.window = tk.Tk()
		self.window.title("Quiz App Login")
		self.window.geometry("500x300+200+200")
		self.window.resizable(height = False , width = False)

		self.user = user

		self.tlabel = tk.Label(self.window,text="Quiz App",font = ("Arial",30))
		self.ulabel = tk.Label(self.window,text="Username",font = ("Arial",20))
		self.uentry = tk.Entry(self.window,font = ("Times",20),width=14)
		self.plabel = tk.Label(self.window,text="Password",font = ("Arial",20))
		self.pentry = tk.Entry(self.window,font = ("Arial",20),show="*",width=14)
		self.lbutton = tk.Button(self.window,font = ("Arial",15),text="Login",command= self.Submit)
		self.sbutton = tk.Button(self.window,font = ("Arial",15),text="Sign Up")

	def Run(self):
		self.tlabel.grid(row = 0 , column = 1)
		self.ulabel.grid(row = 1, column = 0)
		self.uentry.grid(row = 1, column = 1)
		self.plabel.grid(row = 2, column = 0)
		self.pentry.grid(row = 2, column = 1)
		self.lbutton.grid(row = 3, column = 0)
		self.sbutton.grid(row = 3, column = 1)
		self.window.mainloop()

	def Submit(self):
		if self.user.Login(self.uentry.get(),self.pentry.get()) is True:
			self.window.destroy()
			self.user.DashBoard()

class QuizMenu:
	def __init__(self,root,user):
		self.root = root
		self.frame = tk.Frame(self.root,)
		self.user = user
		self.conn = sqlite3.connect("Quiz.db")
		self.cursor = self.conn.execute("SELECT * FROM quizzes")
		self.quizzes = self.cursor.fetchall()
		self.Menu()
		self.frame.grid(row=0,column=0)
	
	def Menu(self):
		if len(self.quizzes) == 0:
			lbl = tk.Label(self.frame,text="No Quizzes Available!")
			lbl.grid(row=0,column=1)
		for i in range(0,len(self.quizzes)):
			btn = tk.Button(self.frame,text=self.quizzes[i][2],)
			btn.grid(row=i,column=1)

class Application:
	def __init__(self,user):
		self.window = tk.Tk()
		self.window.title("Quiz App")
		self.window.geometry("1024x768")
		self.user = user
		self.quizeditor =None
		self.quiz = None
		if self.user.GetPrivilege() == 1:
			self.quizeditor = QE.QuizEditor(self.window)
		else:
			self.quiz = Q.Quiz(self.window,self.user.GetUserId())

	def Run(self):
		self.window.mainloop()

if __name__ == "__main__":
	U = User("admin","password",0)
	U.DashBoard()
	#L = LoginWindow(U) 
	#L.Run()
	'''A = Application(U)
	A.Run()'''


