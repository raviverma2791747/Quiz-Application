import tkinter as tk
from tkinter import messagebox as mb
import sqlite3
import json
import quizeditor as QE
import quiz as Q
import user as U

VERY_LARGE_FONT = ("Verdana",35)
LARGE_FONT = ("Verdana",25)
MEDIUM_FONT = ("Verdana",15)
SMALL_FONT =("Verdana",13)
VERY_SMALL_FONT = ("Verdana",8)

class Application:
	def __init__(self):
		self.window = None
		self.loginwindow = None
		self.loginframe = None
		self.signupframe = None
		self.adminpermissionfarme = None
		self.successsignupframe = None
		self.user = None
		self.app = None
		self.frame = None
		self.uentry  = None
		self.pentry = None
		self.LoginWindow()

	def LoginWindow(self):
		self.loginwindow = tk.Tk()
		self.loginwindow.title("Quiz App Login")
		self.loginwindow.geometry("500x250+200+200")
		self.loginwindow.resizable(height = False , width = False)
		self.loginframe = tk.Frame(self.loginwindow,)

		self.loginstatus = tk.Label(self.loginframe,font=SMALL_FONT)

		tlabel = tk.Label(self.loginframe,text="Quiz App",font =VERY_LARGE_FONT)
		ulabel = tk.Label(self.loginframe,text="Username",font = MEDIUM_FONT)
		self.uentry = tk.Entry(self.loginframe,font =MEDIUM_FONT,width=14)
		plabel = tk.Label(self.loginframe,text="Password",font = MEDIUM_FONT)
		self.pentry = tk.Entry(self.loginframe,font = MEDIUM_FONT,show="*",width=14)
		lbutton = tk.Button(self.loginframe,font = SMALL_FONT,text="Login",command=self.Login)
		sbutton = tk.Button(self.loginframe,font = SMALL_FONT,text="Sign Up",command=self.SignUp)

		tlabel.grid(row = 0 , column = 1,padx=10,pady=10)
		ulabel.grid(row = 1, column = 0,padx=10)
		self.uentry.grid(row = 1, column = 1)
		plabel.grid(row = 2, column = 0,padx=10)
		self.pentry.grid(row = 2, column = 1)
		self.loginstatus.grid(row=3,column=0,columnspan=2,sticky="e")
		lbutton.grid(row = 4, column = 0,sticky="E",pady=10)
		sbutton.grid(row = 4, column = 1,sticky="E",pady=10)
		self.loginframe.pack(fill="both")
		try:
			conn  = sqlite3.connect('file:Quiz.db?mode=rw', uri=True)
		except:
			mb.showerror("Database Error","Couldn't connect to Database")
			exit()

		self.loginwindow.mainloop()

	def BackToLogin(self):
		self.signupframe.pack_forget()
		self.loginframe.pack(fill="both")

	def SignUp(self):
		if self.adminpermissionfarme is not None:
			self.adminpermissionfarme.pack_forget()
		self.signupframe = tk.Frame(self.loginwindow)
		self.loginframe.pack_forget()
		signuplbl = tk.Label(self.signupframe,text="Sign Up",font=MEDIUM_FONT)
		usernamelbl = tk.Label(self.signupframe,text="Username",font=MEDIUM_FONT)
		self.usernameentry = tk.Entry(self.signupframe,font=MEDIUM_FONT)
		self.status = tk.Label(self.signupframe,font=SMALL_FONT)
		passwordlbl = tk.Label(self.signupframe,text="Password",font=MEDIUM_FONT)
		self.passwordentry = tk.Entry(self.signupframe,show="*",font=MEDIUM_FONT)

		self.rolevar = tk.IntVar()
		adminradio = tk.Radiobutton(self.signupframe,text="Admin",font=MEDIUM_FONT,value=1,variable=self.rolevar,command=self.Permission)
		userradio = tk.Radiobutton(self.signupframe,text="User",font=MEDIUM_FONT,value=0,variable=self.rolevar,)
		backbtn = tk.Button(self.signupframe,text="Back",font=MEDIUM_FONT,command=self.BackToLogin)
		sbmtbtn = tk.Button(self.signupframe,text="Submit",font=MEDIUM_FONT,command=self.CreateAccount)
		signuplbl.grid(row=0,column=0,padx=200,columnspan=2,sticky="w")
		usernamelbl.grid(row=1,column=0,padx=10,pady=10,sticky="w")
		self.usernameentry.grid(row=1,column=1,sticky="w")
		passwordlbl.grid(row=2,column=0,padx=10,pady=10,sticky="w")
		self.passwordentry.grid(row=2,column=1,sticky="w")

		adminradio.grid(row=4,column=0,padx=10,sticky="w")
		userradio.grid(row=4,column=1,padx=10,sticky="w")
		sbmtbtn.grid(row=5,column=0,padx=10,sticky="w")
		backbtn.grid(row=5,column=1,sticky="w")
		self.status.grid(row=3,column=0,columnspan=2,sticky="w")
		self.signupframe.pack(fill="both")

	def Permission(self):
		self.adminpermissionfarme = tk.Frame(self.loginwindow,)
		ydhplbl = tk.Label(self.adminpermissionfarme,text="You don't have admin privileges\n please sign in with an admin account to continue!",font=SMALL_FONT)
		aplbl = tk.Label(self.adminpermissionfarme,text="Username",font=MEDIUM_FONT)
		self.apentry = tk.Entry(self.adminpermissionfarme,font=MEDIUM_FONT)
		pplbl = tk.Label(self.adminpermissionfarme,text="Password",font=MEDIUM_FONT)
		self.ppentry = tk.Entry(self.adminpermissionfarme,show="*",font=MEDIUM_FONT)
		sbmtbtn = tk.Button(self.adminpermissionfarme,text="Submit",font=MEDIUM_FONT,command=self.CheckPermission)
		backbtn = tk.Button(self.adminpermissionfarme,text="Back",font=MEDIUM_FONT,command=self.SignUp)
		self.signupframe.pack_forget()
		ydhplbl.grid(row=0,column=0,columnspan=2,pady=10,sticky="w")
		aplbl.grid(row=1,column=0,sticky="w")
		self.apentry.grid(row=1,column=1,sticky="w")
		pplbl.grid(row=2,column=0,sticky="w")
		self.ppentry.grid(row=2,column=1,sticky="w")
		sbmtbtn.grid(row=3,column=0,sticky="w",padx=40)
		backbtn.grid(row=3,column=1,sticky="w",)
		self.adminpermissionfarme.pack(fill="both")

	def CreateAccount(self):
		conn = sqlite3.connect("Quiz.db")
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users WHERE username=?",(self.usernameentry.get(),))
		row = cursor.fetchone()
		if row is None:
			if self.usernameentry.get() == "" or self.passwordentry.get() == "":
				self.status.configure(text="Username or password cannot be empty!")
			elif len(self.usernameentry.get()) < 8 and len(self.passwordentry.get()) < 8:
				self.status.configure(text="Username or password should be atleast 8 digit long!")
			else:
				cursor.execute("INSERT INTO users (username,password,privilege) VALUES (?,?,?)",(self.usernameentry.get(),self.passwordentry.get(),self.rolevar.get(),))
				self.signupframe.pack_forget()
				self.successsignupframe =  tk.Frame(self.window)
				self.successsignupframe.pack()
				lbl = tk.Label(self.successsignupframe,text="Account created successfully!\nPress below button to continue!",font=MEDIUM_FONT)
				lbl.pack(expand=True,fill="both")
				btn = tk.Button(self.successsignupframe,text="continue",font=MEDIUM_FONT,command=self.SuccessSignUpToLogin)
				btn.pack()
		else:
			self.status.configure(text="Username already Taken!")

		conn.commit()

	def SuccessSignUpToLogin(self):
		self.successsignupframe.pack_forget()
		self.loginframe.pack(fill="both")


	def CheckPermission(self):
		conn = sqlite3.connect("Quiz.db")
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users WHERE username=? AND password=? ",(self.apentry.get(),self.ppentry.get(),))
		row = cursor.fetchone()
		if row is not None:
			if row[3] == 1:
				self.adminpermissionfarme.pack_forget()
				self.signupframe.pack(fill="both")

	def Login(self):
		self.username = self.uentry.get()
		self.password = self.pentry.get()
		if  self.username == "" or self.password == "":
			self.loginstatus.configure(text="Username or password cannot be empty!")
		else:
			conn = sqlite3.connect("Quiz.db")
			cursor = conn.execute("SELECT * FROM users WHERE username=? AND password=?",(self.username,self.password))
			row = cursor.fetchone()
			if row is not None:
				self.loginwindow.destroy()
				self.window = tk.Tk()
				self.user = U.User(self.window,self.CallBack,row[0],row[1],row[2],row[3])
				self.Run()
			else:
				self.loginstatus.configure(text="Username or password is invalid!")

	def Run(self):
		self.window.title("Quiz App")
		self.window.geometry("1024x768")
		self.frame =  tk.Frame(self.window)		
		if self.user.GetPrivilege() == 1:
			lbl = tk.Label(self.frame,text="Admin Menu",font=VERY_LARGE_FONT)
			quizbtn = tk.Button(self.frame,text="Quiz",relief=tk.FLAT,font=MEDIUM_FONT,command=self.RunQuiz)
			quizeditorbtn = tk.Button(self.frame,text="Quiz Editor",relief=tk.FLAT,font=MEDIUM_FONT,command=self.RunQuizEditor)
			userdashboardbtn = tk.Button(self.frame,text="User DashBoard ",relief=tk.FLAT,font=MEDIUM_FONT,command=self.RunDashBoard)

			lbl.pack()
			quizbtn.pack()
			quizeditorbtn.pack()
			userdashboardbtn.pack()
		else:
			lbl = tk.Label(self.frame,text="User Menu",font=VERY_LARGE_FONT)
			quizbtn = tk.Button(self.frame,text="Quiz",relief=tk.FLAT,font=MEDIUM_FONT,command=self.RunQuiz)
			userdashboardbtn = tk.Button(self.frame,text="User DashBoard",relief=tk.FLAT,font=MEDIUM_FONT,command=self.RunDashBoard)

			lbl.pack()
			quizbtn.pack()
			userdashboardbtn.pack()
		self.frame.pack()
		self.window.mainloop()

	def CallBack(self):
		del self.app 
		self.app = None
		self.frame.pack()

	def RunQuiz(self):
		if self.app is None:
			self.Hide()
			self.app = Q.Quiz(self.window,self.user.GetUserId(),self.CallBack)

	def RunQuizEditor(self):
		if self.app is None:
			self.Hide()
			self.app = QE.QuizEditor(self.window,self.CallBack)

	def RunDashBoard(self):
		if self.app is None:
			self.Hide()
			self.user.DashBoard()

	
	def Hide(self):
		self.frame.pack_forget()

if __name__ == "__main__":
	A = Application()
