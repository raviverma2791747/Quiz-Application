import tkinter as tk
import sqlite3

class User:
	def __init__(self):
		self.username = None
		self.password = None
		self.privilege = None
		self.conn = sqlite3.connect('Users.db')
		self.cursor = None

	def Login(self,username,password):
		if username == "":
			print("Invalid Username!")
			return False
		elif password == "":
			print("Invalid Password!")
			return False
		else:
			self.cursor = self.conn.execute("SELECT id,username,password,privilege from users")
			for row in self.cursor:
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

	def GetPrivilege(self):
		return self.privilege

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

class Application:
	def __init__(self,user):
		self.window = tk.Tk()
		self.window.title("Quiz App")
		self.window.geometry("1024x768")
		self.user = user

	def Run(self):
		self.window.mainloop()

U = User()
L = LoginWindow(U) 
L.Run()
A = Application(U)
A.Run()