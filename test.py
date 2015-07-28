import tkinter as tk       
from HHConverter import HHConverter
from urllib.request import urlopen
#import urllib2
import json

class Application(tk.Frame):

    def __init__(self, master=None):
        self.c_directory = ""
        tk.Frame.__init__(self, master)   
        self.grid()                       
        self.createWidgets()
        #pass the directory where converted HH should be saved. 
        self.hhC = HHConverter("SealsFullTiltHH")
        
    def askForDirectory(self):
        #askign for directory
        #from tkinter.filedialog import askopenfilename
        
        from tkinter.filedialog import askdirectory
        filename = askdirectory()
        #filename = "C:\\Users\\Public\\SealsWithClubs\\handhistories\\"
        print(filename)
        
        #pass folder name to hhC for processing.
        response = urlopen('https://coinbase.com/api/v1/prices/buy')
        strjson = response.read().decode('utf-8')
        #print (strjson)
        pdata = json.loads(strjson)   
        print(pdata["amount"])
        self.c_directory = filename
        self.hhC.processDirectory(filename, pdata["amount"])
        
        #self.hhC.processDirectory("C:/Users/keith/My Documents/Aptana Studio 3 Workspace/HHConverter/handhistories/")
        
    def redoDirectory(self):
        #askign for directory
        #from tkinter.filedialog import askopenfilename     
        #pass folder name to hhC for processing.
        response = urlopen('https://coinbase.com/api/v1/prices/buy')
        strjson = response.read().decode('utf-8')
        #print (strjson)
        pdata = json.loads(strjson)   
        print(pdata["amount"])

        self.hhC.processDirectory(self.c_directory, pdata["amount"])
        
    def askForCommandFile(self):
        #askign for directory
        from tkFileDialog import askopenfilename
        #from tkinter.filedialog import askdirectory
        filename = askopenfilename()
        print(filename)
        #pass folder name to hhC for processing.
        self.hhC.processCommandFile(filename)
        #self.hhC.processDirectory("C:/Users/keith/My Documents/Aptana Studio 3 Workspace/HHConverter/handhistories/")
        
        
    def createWidgets(self):
        #let's make two buttons... and one text box
        #convert by folder or directory
        #convert a command from client

        
        self.findDButton = tk.Button(self, text='Find Directory',command=self.askForDirectory)   
        self.redoDirButton = tk.Button(self, text='Reprocess Directory',command=self.redoDirectory)          
        self.findDButton.grid()
        self.redoDirButton.grid()
        #self.commandDButton = tk.Button(self, text='Find Command File',command=self.askForCommandFile)            
        #self.commandDButton.grid()
        

    

app = Application()                       
app.master.title('Sample application')    
app.mainloop() 


