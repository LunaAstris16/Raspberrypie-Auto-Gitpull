import os
import subprocess
import time
import threading
import multiprocessing
import runthread

class runThread:
    
    def __init__(self,runfileName,folderName):
        this.runfileName = runfileName
        this.folderName = folderName

    def runfile(self, runfileName, folderName):
        folderCheck(homeFolder)
        os.chdir(folderName)
        subprocess.run(["python", runfileName])
        os.chdir("..")

    def startrunthread(self, runfileName, folderName):
        runthread = threading.Thread(target=runfile, args=(runfileName,folderName))
        runthread.start()


def updater(): 
    runthreadob = runThread(runfileName, folderName)
    runthreadob.startrunthread()
    while True:
        folderCheck(homeFolder)
        subprocess.run(["touch", "output.txt"])
        lsoutput = os.popen("ls").read().split("\n")
        os.chdir(lsoutput[3])
        changedbranch = uptodateCheck(folderName)
        if changedbranch == True:
            print("Your Repository was updated Auto run Started")
            del runthreadob
        else:
            print("New Check Say's Your repositor is up to date")
            time.sleep(10)
            print("new line")

def foldernamefinder(githuburl):
    spliturl = githuburl.split("/")
    spliturl = spliturl.pop(len(spliturl) - 1)
    return spliturl.split(".")[0]

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

def uptodateCheck(folderName):
    folderCheck(homeFolder)
    lsoutput = os.popen("ls").read().split("\n")
    print("")
    print(lsoutput)
    print("")
    os.chdir(lsoutput[3])
    subprocess.run(["git", "fetch", "origin"])
    output = os.popen("git status").read()
    os.chdir("..")
    githubout = open("output.txt", "w")
    githubout.write(output)
    githubout.close()
    listtext = [(line.strip()) for line in open("output.txt", "r")]
    gitstatus = listtext[1].split(" ")
    if gitstatus[3] == "behind":
        os.chdir(lsoutput[3])
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
