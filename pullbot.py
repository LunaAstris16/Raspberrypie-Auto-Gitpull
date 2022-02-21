import os
import subprocess
import time
import threading

#builds an object for the run thread 
#Allows for expantion later 
class runThread:
    
    def __init__(self, runfileName, folderName, homeFolder):
        self.runfileName = runfileName
        self.folderName = folderName
        self.homeFolder = homeFolder
        self.runthread = threading.Thread(target=self.runfile,daemon = True)
        self.p = None
      
    def runfile(self):
        folderCheck(self.homeFolder)
        os.chdir(self.folderName)
        self.p = subprocess.Popen(["python", self.runfileName])
        os.chdir("..")

    def startrunthread(self):
        self.runthread.start()

    def stopprocess(self):
        self.p.terminate()

def updater(): 
    runthreadob = runThread(runfileName, folderName, homeFolder)
    runthreadob.startrunthread()
    while True:
        folderCheck(homeFolder)
        subprocess.run(["touch", "output.txt"])
        lsoutput = os.popen("ls").read().split("\n")
        print(lsoutput)
        os.chdir(lsoutput[5])
        #The line below this is responsible for seeing if the git is up to date and pulls the latest version if it does
        changedbranch = uptodateCheck(folderName)
        if changedbranch == True:
            print("Your Repository was updated Auto run Started")
            runthreadob.stopprocess()
            runthreadob.runfile()
        else:
            print("New Check Say's Your repositor is up to date")
            time.sleep(10)
            print("new line")

#Finds the folder name of the clone folder
def foldernamefinder(githuburl):
    spliturl = githuburl.split("/")
    spliturl = spliturl.pop(len(spliturl) - 1)
    return spliturl.split(".")[0]

#Checks the folder to make sure its in the home Dirc
def folderCheck(homeFolder):
    currentFolder = os.getcwd()
    if homeFolder == currentFolder:
        return True
    else:
        lsoutput = os.popen("ls").read().split("\n")
        for i in range(len(lsoutput)):
            if lsoutput[i] == homeFolder:
                os.chdir(homeFolder)
                return True 
            else:
                os.chdir("..")
                currentFolder = os.getcwd()
                if homeFolder == currentFolder:
                    return True

#this is what updates the file
def uptodateCheck(folderName):
    folderCheck(homeFolder)
    lsoutput = os.popen("ls").read().split("\n")
    os.chdir(lsoutput[5])
    subprocess.run(["git", "fetch", "origin"])
    output = os.popen("git status").read()
    os.chdir("..")
    githubout = open("output.txt", "w")
    githubout.write(output)
    githubout.close()
    listtext = [(line.strip()) for line in open("output.txt", "r")]
    gitstatus = listtext[1].split(" ")
    #Returns wether the files where updated or not
    if gitstatus[3] == "behind":
        os.chdir(lsoutput[5])
        subprocess.run(["git", "pull"])
        os.chdir("..")
        os.remove("output.txt")
        return True 
    else:
        return False 
        os.remove("output.txt")

githuburl = "https://github.com/LunaAstris16/testing.git"
folderName = foldernamefinder(githuburl)
runfileName = input("What is the name of the file that you want to run: ")
homeFolder = os.getcwd()

subprocess.run(["touch", "output.txt"])
subprocess.run(["git", "clone", githuburl])

updaterthread = threading.Thread(target=updater)

updaterthread.start()
