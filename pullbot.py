import os
import subprocess
import threading
import time
from datetime import datetime

__debug_mode__: bool = False

class runThread:
    """
    Builds an object for the run thread. 
    Allows for expansion later 
    """
    def __init__(self, runfile_name: str, folder_name: str, home_folder: str):
        self.runfile_name: str = runfile_name
        self.folder_name: str = folder_name
        self.home_folder: str = home_folder
        self.run_thread = threading.Thread(target=self.run_file, daemon=False)
        self.p = None
      
    def run_file(self):
        folder_check(self.home_folder)
        os.chdir(self.folder_name)
        self.p = subprocess.Popen(["python", self.runfile_name])
        os.chdir("..")

    def start_run_thread(self):
        self.run_thread.start()

    def stop_process(self):
        if self.p is not None:
            self.p.terminate()

def updater(runfile_name: str, folder_name: str, home_folder: str, testing_folder_index: int): 
    runthreadob = runThread(runfile_name, folder_name, home_folder)
    runthreadob.start_run_thread()
    while True:
        folder_check(home_folder)
        subprocess.run(["touch", "output.txt"])
        ls_output: list[str] = os.popen("ls").read().split("\n")
        if __debug_mode__:
            print(ls_output)
        os.chdir(ls_output[testing_folder_index])
        #The line below is responsible for checking if the git is up to date and pulls the latest version if it is not
        changed_branch: bool = uptodate_check(testing_folder_index, home_folder)
        if changed_branch:
            print("Your Repository was updated Auto run Started")
            runthreadob.stop_process()
            runthreadob.run_file()
        else:
            now: str = datetime.now().strftime("%H:%M")
            print(f"Your repository is up to date. (last checked: {now})")
            time.sleep(60.0)
            print() # newline

def folder_name_finder(github_url: str) -> str:
    """
    Finds the folder name of the clone folder
    """
    # git_folder contains all the list element except the last one
    # which is stored in git_file
    *git_user_path, git_repository = github_url.split("/")
    return git_repository.removesuffix(".git")

def folder_check(home_folder: str) -> bool:
    """
    Checks the folder to make sure it's in the home directory.
    """
    current_folder: str = os.getcwd()
    if home_folder == current_folder:
        return True
    ls_output: list[str] = os.popen("ls").read().split("\n")
    for ls_dir in ls_output:
        if ls_dir == home_folder:
            os.chdir(home_folder)
            return True 
        os.chdir("..")
        current_folder: str = os.getcwd() # why is it reassigned?
        if home_folder == current_folder:
            return True
    return False # False is better than None honestly even if this latter also works

def uptodate_check(testing_folder_index: int, home_folder: str) -> bool:
    """
    This is what updates the file.
    """
    folder_check(home_folder)
    ls_output: list[str] = os.popen("ls").read().split("\n")
    os.chdir(ls_output[testing_folder_index])
    subprocess.run(["git", "fetch", "origin"])
    output: str = os.popen("git status").read()
    os.chdir("..")
    # It's safer to use with, because whatever happens it closes the file at the end
    with open("output.txt", "w") as github_out:
        github_out.write(output)
    list_text: list[str] = [line.strip() for line in output.split("\n")]
    if __debug_mode__:
        print(list_text)
    git_status = list_text[1].split() # split separator by default is already whitespace
    # Returns whether the files where updated or not
    if git_status[3] == "behind":
        os.chdir(ls_output[testing_folder_index])
        subprocess.run(["git", "pull"])
        os.chdir("..")
        os.remove("output.txt")
        return True 
    os.remove("output.txt")
    return False

def main():
    github_url: str = "https://github.com/LunaAstris16/RasberrypyPythonwebsite.git"
    folder_name: str = folder_name_finder(github_url)
    runfile_name: str = input("Enter the name of the file that you want to run: ")
    home_folder: str = os.getcwd()

    subprocess.run(["touch", "output.txt"])
    subprocess.run(["git", "clone", github_url])

    testing_folder_index: int = os.popen("ls").read().split("\n").index(folder_name)
    if __debug_mode__:
        print(testing_folder_index)

    updater_thread = threading.Thread(target=updater(runfile_name, folder_name, home_folder, testing_folder_index))

    updater_thread.start() # not executed because of line 32

if __name__ == "__main__":
    main()
