import subprocess, platform

from rsc.install import fetchData, install

def collectPackages():
    print("Collect packages...")
    if(platform.system == "Linux"):
        p = subprocess.Popen("sudo pip install -r requirements.txt", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen("pip install -r requirements.txt", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    print("Collected all packages.")

if __name__ == "__main__":
    collectPackages()
    import rsc.install
    fetchData()
    install()