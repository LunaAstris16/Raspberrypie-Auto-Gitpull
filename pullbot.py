import os
import subprocess
import time

def foldernamefinder(githuburl):
    spliturl = githuburl.split("/")
    spliturl = spliturl.pop(len(spliturl) - 1)
    return spliturl.split(".")[0]


def foldernameFound(folderName, lsoutput):
    for i in range(len(lsoutput)):
        if lsoutput[i] == folderName:
            return True
        else:
            return False



def uptodateCheck(folderName):
    lsoutput = os.popen("ls").read().split("\n")
    #folderfound = foldernameFound(folderName, lsoutput)
    #if folderfound == True:
    #os.chdir(folderName)
    #return os.popen("git status -uno").read()
    #else:
    os.chdir(lsoutput[5])
    subprocess.run(["git", "fetch", "origin"])
    output = os.popen("git status").read()
    os.chdir("..")
    githubout = open("output.txt", "w")
    githubout.write(output)
    githubout.close()
    listtext = [(line.strip()) for line in open("output.txt", "r")]
    gitstatus = listtext[1].split(" ")
    print(" ")
    print(gitstatus)
    print(" ")
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

subprocess.run(["touch", "output.txt"])
subprocess.run(["git", "clone", githuburl])

while True:
    subprocess.run(["touch", "output.txt"])
    changedbranch = uptodateCheck(folderName)
    if changedbranch == True:
      print("Your Repository was updated Auto run Started")
    else:
      print("New Check Say's Your repositor is up to date")
    time.sleep(10)
    print("new line")
