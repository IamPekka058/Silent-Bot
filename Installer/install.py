import subprocess, platform

def installProgram(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    return p.returncode

def getRequirements():
    p = subprocess.Popen("pip3 install -r -y requirements.txt", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    return p.returncode

def searchFor(program_name):
    p = subprocess.Popen(program_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    return p.returncode

def collectPackages():
    print("Collecting packages...")
    if(platform.system() == "Linux"):
        p = getRequirements()
        
        if(p != 0):
            print("Pip is not installed.\nInstalling...")
            installProgram("sudo apt-get install python3-pip -y")
            print("Pip installed\n")
            getRequirements()

        print("Searching for git...")
        p = searchFor("git")

        if(p != 0):
            print("Installing git...")
            installProgram("sudo apt-get install git -y")
            print("Git installed\n")
        else:
            print("Git found")

    if(platform.system() == "Windows"):
        getRequirements()
        
        p=searchFor("git")
        if(p != 1):
            print("Es wurde kein git gefunden... entweder installierst du es oder du wartest noch bis der Installer auch die GIT-Installation auf Windows unterstützt...")
            exit()
    print("Collected all packages.")

if __name__ == "__main__":
    collectPackages()
    from rsc.source import fetchData, install
    fetchData()
    install()