import tkinter as tk
import sqlite3
import json
import quizeditor as QE
import quiz as Q

VERY_LARGE_FONT = ("Verdana",35)
LARGE_FONT = ("Verdana",25)
MEDIUM_FONT = ("Verdana",15)
SMALL_FONT =("Verdana",13)
VERY_SMALL_FONT = ("Verdana",8)

class User:
	def __init__(self,_id,username,password,privilege):
		self._id = _id
		self.username =  username
		self.password = password
		self.privilege = privilege

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
		
class Application:
	def __init__(self):
		self.window = None
		self.user = None
		self.app = None
		self.frame = None
		self.uentry  = None
		self.pentry = None

		self.window = tk.Tk()
		self.window.title("Quiz App Login")
		self.window.geometry("500x250+200+200")
		self.window.resizable(height = False , width = False)

		tlabel = tk.Label(self.window,text="Quiz App",font =VERY_LARGE_FONT)
		ulabel = tk.Label(self.window,text="Username",font = MEDIUM_FONT)
		self.uentry = tk.Entry(self.window,font =MEDIUM_FONT,width=14)
		plabel = tk.Label(self.window,text="Password",font = MEDIUM_FONT)
		self.pentry = tk.Entry(self.window,font = MEDIUM_FONT,show="*",width=14)
		lbutton = tk.Button(self.window,font = SMALL_FONT,text="Login",command=self.Login)
		sbutton = tk.Button(self.window,font = SMALL_FONT,text="Sign Up")

		tlabel.grid(row = 0 , column = 1,padx=10,pady=10)
		ulabel.grid(row = 1, column = 0,padx=10)
		self.uentry.grid(row = 1, column = 1)
		plabel.grid(row = 2, column = 0,padx=10)
		self.pentry.grid(row = 2, column = 1)
		lbutton.grid(row = 3, column = 0,sticky="E",pady=10)
		sbutton.grid(row = 3, column = 1,sticky="E",pady=10)
		self.window.mainloop()

	def Login(self):
		self.username = self.uentry.get()
		self.password = self.pentry.get()
		if  self.username == "" or self.password == "":
			pass
		else:
			conn = sqlite3.connect("Quiz.db")
			cursor = conn.execute("SELECT * FROM users WHERE username=? AND password=?",(self.username,self.password))
			row = cursor.fetchone()
			if row is not None:
				self.window.destroy()
				self.user = User(row[0],row[1],row[2],row[3])
				self.Run()

	def Run(self):
		self.window = tk.Tk()
		self.window.title("Quiz App")
		self.window.geometry("1024x768")
		self.frame =  tk.Frame(self.window)		
		if self.user.GetPrivilege() == 1:
			lbl = tk.Label(self.frame,text="Admin Menu",font=VERY_LARGE_FONT)
			quizbtn = tk.Button(self.frame,text="Quiz",relief=tk.FLAT,font=MEDIUM_FONT,command=self.RunQuiz)
			quizeditorbtn = tk.Button(self.frame,text="Quiz Editor",relief=tk.FLAT,font=MEDIUM_FONT,command=self.RunQuizEditor)
			userdashboardbtn = tk.Button(self.frame,text="User DashBoard (Under Development)",relief=tk.FLAT,font=MEDIUM_FONT)

			lbl.pack()
			quizbtn.pack()
			quizeditorbtn.pack()
			userdashboardbtn.pack()
		else:
			lbl = tk.Label(self.frame,text="User Menu",font=VERY_LARGE_FONT)
			quizbtn = tk.Button(self.frame,text="Quiz",relief=tk.FLAT,font=MEDIUM_FONT,command=self.RunQuiz)
			userdashboardbtn = tk.Button(self.frame,text="User DashBoard  (Under Development)",relief=tk.FLAT,font=MEDIUM_FONT)

			lbl.pack()
			quizbtn.pack()
			userdashboardbtn.pack()
		self.frame.pack()
		self.window.mainloop()

	def CallBack(self):
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
	
	def Hide(self):
		self.frame.pack_forget()

if __name__ == "__main__":
	A = Application()
