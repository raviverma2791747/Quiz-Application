import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.figure
import matplotlib.patches
from tkinter import filedialog as fd 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox as mb
import sqlite3
import json
from fpdf import FPDF
from datetime import datetime
from datetime import date
import os

VERY_LARGE_FONT = ("Verdana",35)
LARGE_FONT = ("Verdana",25)
MEDIUM_FONT = ("Verdana",15)
SMALL_FONT =("Verdana",13)
VERY_SMALL_FONT = ("Verdana",8)

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

class User:
	def __init__(self,root,callback=None,_id=None,username=None,password=None,privilege=None):
		self.root =root
		self.callback = callback
		self._id = _id
		self.username =  username
		self.password = password
		self.privilege = privilege
		self.viewresponseframe = None
		self.frame =  None
		self.userleftframe =  None
		self.userdetailsframe=  None
		self.userresponseframe=  None
		self.userrightframe=  None
		self.usernameentry=  None
		self.passwordentry=  None
		self.passwordviewbtn=  None
		self.userdetailsframe=  None
		self.userleftbottomframe = None
		
		self.passwordviewstatus = False
		self.passwordstatus = False

	def DashBoard(self):
		if self.frame is not None:
			self.frame.pack(fill="both",expand="true")
			return
		self.frame = tk.Frame(self.root)
		self.userleftframe = tk.LabelFrame(self.frame,height=self.root.winfo_screenheight()/10*9,width=self.root.winfo_screenwidth()/20*6)

		self.userdetailsframe = tk.LabelFrame(self.userleftframe,)

		self.userresponseframe = ScrollableFrame(self.userleftframe,)

		self.userrightframe =  tk.Frame(self.frame,height=self.root.winfo_screenheight()/10*9,width=self.root.winfo_screenwidth()/20*14)

		usernamelbl = tk.Label(self.userdetailsframe,text="User Name :",font=SMALL_FONT)
		usernamelbl.grid(row=0,column=0)
		self.usernameentry = tk.Entry(self.userdetailsframe,width=16,font=SMALL_FONT,)
		self.usernameentry.insert(tk.INSERT,self.username)
		self.usernameentry.configure(state="disabled")
		self.usernameentry.grid(row=0,column=1,)

		passwordlbl =tk.Label(self.userdetailsframe,text="Password:",font=SMALL_FONT)
		passwordlbl.grid(row=1,column=0)
		self.passwordentry = tk.Entry(self.userdetailsframe,show="*",width=16,font=SMALL_FONT)
		self.passwordentry.insert(tk.INSERT,self.password)
		self.passwordentry.configure(state="disabled")
		self.passwordentry.grid(row=1,column=1)
		self.passwordviewbtn = tk.Button(self.userdetailsframe,text="Show",font=VERY_SMALL_FONT,command=self.PasswordViewStatusChange)
		self.passwordviewbtn.grid(row=1,column=2)
		self.passwordeditbtn = tk.Button(self.userdetailsframe,text="Edit",font=VERY_SMALL_FONT,command=self.PasswordEditStatusChange)
		self.passwordeditbtn.grid(row=1,column=3)

		privilegelbl =tk.Label(self.userdetailsframe,text="Role :",font=SMALL_FONT)
		privilegelbl.grid(row=2,column=0)
		privilege = None
		if self.privilege == 0:
			privilege = tk.Label(self.userdetailsframe,text="User",font=SMALL_FONT)
		else:
			privilege = tk.Label(self.userdetailsframe,text="User",font=SMALL_FONT)
		privilege.grid(row=2,column=1)

		responseslbl = tk.Label(self.userresponseframe.scrollable_frame,text="User Responses",font=MEDIUM_FONT)
		responseslbl .grid(row=0,column=0)

		conn = sqlite3.connect("Quiz.db")
		cur = conn.cursor()

		if self.privilege == 1:
			cur.execute("SELECT DISTINCT quiz FROM responses")
			row = cur.fetchall()
			if len(row) > 0:
				for i in range(0,len(row)):
					cur.execute("SELECT * FROM responses WHERE user=? AND quiz =?",(self._id,row[i][0]))
					rrow = cur.fetchone()
					cur.execute("SELECT * FROM quizzes WHERE id=? ",(row[i][0],))
					name = cur.fetchone()
					if name is not None:
						rbutton = tk.Button(self.userresponseframe.scrollable_frame,text=name[1],font=SMALL_FONT,command=lambda r=rrow ,n = name[1] ,: self.ViewResponse(r,n))
						rbutton.grid(row=i+1,column=0,sticky=tk.W+tk.E)
						if rrow is None:
							rbutton.configure(state="disabled")
					exportbtn = tk.Button(self.userresponseframe.scrollable_frame,text="Export",font=SMALL_FONT,command=lambda n=name[1],qid = name[0]:self.ExportResponse(n,qid))
					exportbtn.grid(row=i+1,column=1,sticky=tk.W+tk.E)
			else:
				noresponsemsglbl = tk.Label(self.userresponseframe.scrollable_frame,text="No Responses to Show",font=MEDIUM_FONT)
				noresponsemsglbl.grid(row=1,column=0,sticky="E")
		else:
			cur.execute("SELECT * FROM responses WHERE user=?",(self._id,))
			row = cur.fetchall()
			if len(row) > 0:
				for i in range(0,len(row)):
					cur.execute("SELECT * FROM quizzes WHERE id=? ",(row[i][1],))
					name = cur.fetchone()
					if name is not None:
						rbutton = tk.Button(self.userresponseframe.scrollable_frame,text=name[1],font=SMALL_FONT,command=lambda r=row[i] ,n = name[1] ,: self.ViewResponse(r,n))
						rbutton.grid(row=i+1,column=0,sticky=tk.W+tk.E)
			else:
				noresponsemsglbl = tk.Label(self.userresponseframe.scrollable_frame,text="No Responses to Show",font=MEDIUM_FONT,)
				noresponsemsglbl.grid(row=1,column=0,sticky="E")

		if self.callback is not None:
			exitbtn = tk.Button(self.userleftframe,text="Exit",font=MEDIUM_FONT,command=self.Exit)
			exitbtn.grid(row=3,column=0,sticky="w")

		self.userdetailsframe.grid(row=0,column=0,sticky="nwe")
		self.userresponseframe.grid(row=2,column=0,sticky="ns",)
		self.userleftframe.grid(row=0,column=0,sticky="nwse")
		self.userrightframe.grid(row=0,column=1,sticky="nwse")
		self.frame.pack(fill="both",expand="true")
		self.frame.rowconfigure(0,weight=1)

	def PasswordViewStatusChange(self):
		if self.passwordviewstatus == False:
			self.passwordviewstatus = True
			self.passwordviewbtn.configure(text="Hide")
			self.passwordentry.configure(show="")
		else:
			self.passwordviewstatus = False
			self.passwordviewbtn.configure(text="Show")
			self.passwordentry.configure(show="*")

	def PasswordEditStatusChange(self):
		if self.passwordstatus is False:
			if self.passwordviewstatus is False:
				self.PasswordViewStatusChange()
			self.passwordentry.configure(state="normal")
			self.passwordeditbtn.configure(text="Save")
			self.passwordstatus = True
			self.passwordviewbtn.configure(state="disabled")
		else:
			self.PasswordSave()
			self.passwordstatus = False
			self.passwordeditbtn.configure(text="Edit")
			self.passwordentry.configure(state="disabled")
			self.passwordviewbtn.configure(state="normal")



	def PasswordSave(self):
		if len(self.passwordentry.get()) > 7:
			conn = sqlite3.connect("Quiz.db")
			cursor = conn.cursor()
			cursor.execute("UPDATE users SET password=? WHERE id=?",(self.passwordentry.get(),self._id,))
			conn.commit()
			self.PasswordViewStatusChange()

	def ViewResponse(self,response=None,name=None):
		if response and name is not None:
			if self.viewresponseframe is not None:
				self.viewresponseframe.destroy()
				self.viewresponseframe = None
			self.viewresponseframe = tk.Frame(self.userrightframe,width=self.root.winfo_screenwidth()/20*14)

			file = open(response[2],"r")
			data = json.loads(file.read())
			testnamelbl = tk.Label(self.viewresponseframe,text=name,font=LARGE_FONT)
			testnamelbl.grid(row=0,column=1,sticky="ew",pady=20)
			if data["max_points"] == 0:
				scorelabel = tk.Label(self.viewresponseframe,text="Maximum score : None",font=MEDIUM_FONT)
				youscorelbl = tk.Label(self.viewresponseframe,text="Your score : None",font=MEDIUM_FONT)
			else:
				scorelabel = tk.Label(self.viewresponseframe,text="Maximum score : " + str(data["max_points"]),font=MEDIUM_FONT)
				youscorelbl = tk.Label(self.viewresponseframe,text="Your score : "  + str(data["score"]) ,font=MEDIUM_FONT)
			scorelabel.grid(row=1,column=0,pady=10,sticky="w")
			youscorelbl.grid(row=1,column=1,pady=10,sticky="w")
			totalscorelbl = tk.Label(self.viewresponseframe,text="Total Questions : " + str(len(data["response"])),font=MEDIUM_FONT)
			totalscorelbl.grid(row=1,column=2,pady=10,sticky="w")
			fig = matplotlib.figure.Figure(figsize=(5,5))
			ax = fig.add_subplot(111)

			correct = str(data["correct"])
			incorrect = str(data["incorrect"])
			noresponse = str(data["no_response"])

			correctlbl =  tk.Label(self.viewresponseframe,text="Correct : " + str(correct),font=MEDIUM_FONT)
			incorrectlbl =  tk.Label(self.viewresponseframe,text="Incorrect : " + str(incorrect),font=MEDIUM_FONT)
			noresponselbl =  tk.Label(self.viewresponseframe,text="No response : " + str(noresponse),font=MEDIUM_FONT)

			correctlbl.grid(row=2,column=0,pady=10,sticky="w")
			incorrectlbl.grid(row=2,column=1,pady=10,sticky="w")
			noresponselbl.grid(row=2,column=2,pady=10,sticky="w")

			ax.pie([correct,incorrect,noresponse]) 
			ax.legend(["Correct","Incorrect","No response"])
			#ax.color(["green","red","gray"])
			circle=matplotlib.patches.Circle( (0,0), 0.0, color='white')
			ax.add_artist(circle)
			canvas = FigureCanvasTkAgg(fig, master=self.viewresponseframe)
			canvas.get_tk_widget().grid(row=3,column=0,columnspan=2)
			canvas.draw()
			fig.savefig("temp.png",format="png", bbox_inches='tight')
			exportdata = (name,str(data["max_points"]),str(data["score"]),str(len(data["response"])),str(correct),str(incorrect),str(noresponse))
			exportbtn = tk.Button(self.viewresponseframe,text="Export",font=MEDIUM_FONT,command=lambda : self.Export(exportdata))
			exportbtn.grid(row=4,column=0,sticky="sw")
			self.viewresponseframe.pack(expand=True,fill="both",padx=100)

	def GetPrivilege(self):
		return self.privilege

	def GetUsername(self):
		return self.username

	def GetUserId(self):
		return self._id

	def Exit(self):
		self.frame.pack_forget()
		if self.viewresponseframe is not None:
			self.viewresponseframe.destroy()
		self.callback()

	def ExportResponse(self,name=None,quiz_id=None):
		if quiz_id is not None:
			try:
				conn = sqlite3.connect("Quiz.db")
				cursor = conn.cursor()
				cursor.execute("SELECT * FROM responses WHERE quiz=?",(quiz_id,))
				data = cursor.fetchall()
				filedialog = fd.asksaveasfile(filetypes = [("CSV","*.csv")], defaultextension = [("CSV","*.csv")])
				if filedialog is not None:
					filedialog.write("\"serial No.\",\"username\",\"quiz name\",\"maximum points\",\"score\",\"total questions\",\"correct\",\"incorrect\",\"no response\",\n")
					for i in range(0,len(data)):
						temp_file = open(data[i][2])
						rdata = json.loads(temp_file.read())
						cursor.execute("SELECT username FROM users WHERE id=?",(data[i][0],))
						username = cursor.fetchone()[0]
						rrow = (str(i+1),username,name,str(rdata["max_points"]),str(rdata["score"]),str(len(rdata["response"])),str(rdata["correct"]),str(rdata["incorrect"]),str(rdata["no_response"]),)
						temp_file.close()
						strrow = ",".join(rrow) + "\n"
						filedialog.write(strrow)
					filedialog.close()
					mb.showinfo("Export","File exported successfully!")
			except:
				mb.showerror("Export","File export error!")

	def Export(self,data=None):
		pdf = FPDF()
		pdf.add_page()
		pdf.set_font("Arial", size = 8)
		now = datetime.now()
		current_time = current_time = now.strftime("%H:%M:%S")
		pdf.cell(200, 10, txt = "Date : "+str(date.today())+" Time: "+current_time ,  ln = 1, align = 'L')
		pdf.set_font("Arial", size = 20)
		pdf.cell(200, 10, txt = "Quiz : "+data[0] ,  ln = 1, align = 'C')
		pdf.set_font("Arial", size = 15)
		pdf.cell(0, 10, txt = "Username           : "+self.username ,  ln = 1, align = 'L')
		pdf.cell(0, 10, txt = "Maximum Score      : "+data[1] ,  ln = 1, align = 'L')
		pdf.cell(0, 10, txt = "Scored             : "+data[2] ,  ln = 1, align = 'L')
		pdf.cell(0, 10, txt = "Total Questions    : "+data[3] ,  ln = 1, align = 'L')
		pdf.cell(0, 10, txt = "Correct            : "+data[4] ,  ln = 1, align = 'L')
		pdf.cell(0, 10, txt = "Incorrect          : "+data[5] ,  ln = 1, align = 'L')
		pdf.cell(0, 10, txt = "No Response        : "+data[6] ,  ln = 1, align = 'L')
		pdf.image(name="temp.png",)
		if os.path.exists("temp.png"):
			os.remove("temp.png")
		exportdialog = fd.asksaveasfile(filetypes = [("PDF","*.pdf")], defaultextension = [("PDF","*.pdf")])
		if exportdialog is not None:
			pdf.output(exportdialog.name)
			mb.showinfo("Export","Result exported successfully!")
		

if __name__ == "__main__":
	window = tk.Tk()
	U = User(window,None,1,"admin","password",1)
	U.DashBoard()
	window.mainloop()
