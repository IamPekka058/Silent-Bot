import subprocess, platform

def collectPackages():
    print("Collect packages...")
    if(platform.system() == "Linux"):
        p = subprocess.Popen("sudo pip install -r -y requirements.txt", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p.wait()
        if(p.returncode != 1):
            print("Pip is not installed.\nInstalling...")
            p = subprocess.Popen("sudo apt-get install python3-pip", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            p.wait()
            print("Pip installed\n")
        print("Searching for git...")
        p = subprocess.Popen("git", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p.wait()
        if(p.returncode != 1):
            print("Installing git...")
            p = subprocess.Popen("sudo apt-get install git -y", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            p.wait()
            print("Git installed\n")
        else:
            print("Git found")
        from rsc.install import fetchData, install
        fetchData()
        install()
    else:
        p = subprocess.Popen("pip install -r -y requirements.txt", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p.wait()
    print("Collected all packages.")

if __name__ == "__main__":
    collectPackages()
    from rsc.install import fetchData, install
    fetchData()
    install()