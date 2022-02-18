import os
import subprocess
import time
import threading

def updater():
  while True:
    subprocess.run(["touch", "output.txt"])
    changedbranch = uptodateCheck(folderName)
    if changedbranch == True:
      print("Your Repository was updated Auto run Started")
      runthread.join
      runthread.start
    else:
      print("New Check Say's Your repositor is up to date")
    time.sleep(10)
    print("new line")

def runfile(runfileName,folderName):
  os.chdir(folderName)
  subprocess.run(["python", runfileName])
  os.chdir("..")

def foldernamefinder(githuburl):
  spliturl = githuburl.split("/")
  spliturl = spliturl.pop(len(spliturl) - 1)
  return spliturl.split(".")[0]

def checkfolder():
  lsoutput = os.popen("ls").read().split("\n")

def uptodateCheck(folderName):
  os.chdir("..")
  lsoutput = os.popen("ls").read().split("\n")
  print(lsoutput)
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
runfileName = input("What is the name of the file that you want to run: ")

subprocess.run(["touch", "output.txt"])
subprocess.run(["git", "clone", githuburl])

updaterthread = threading.Thread(target=updater)
runthread = threading.Thread(target=runfile, args=(runfileName,folderName))

updaterthread.start()
runthread.start()
