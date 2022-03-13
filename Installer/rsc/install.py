import tarfile, zipfile, platform, requests, json, os, sys, subprocess, git

colors = {"white":"\u001b[37m", "green":"\n\033[1;32m"}

print(colors["green"]+"Welcome to the Silent-Bot Installer."+colors["white"]+"\n")

links = {}

def fetchData():
    result = requests.get("https://raw.githubusercontent.com/IamPekka058/Silent-Bot/development-iampekka058/builds.txt")
    global links
    links = json.loads(result.content)

def getFFmpeg():
    print("Searching for an FFmpeg Installation...")
    p = subprocess.Popen("ffmpeg", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    if(p.returncode == 1):
        print("An FFmpeg Installation was found")
        return True
    else:
        print("No FFmpeg Installation was found")
        return False

def getgit():
    p = subprocess.Popen("git", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    if(p.returncode == 1):
        return True
    else:
        print("Git is not installed.")
        return False

def install():
    os_name = platform.system()
    
    if(os_name == "Windows"):

        if(getFFmpeg() == False):
            print("Downloading FFmpeg for Windows...")
            result = requests.get(links.get("windows"))

            with open("ffmpeg.zip", "wb+") as download_file:
                download_file.write(result.content)
            print("Successfully downloaded ffmpeg.zip")
            print("\u001b[37mExtracting content..."+colors['white'])
            zipfile.ZipFile("ffmpeg.zip").extractall("ffmpeg/")
            print("Successfully extracted to ffmpeg/")
            print("Deleting ffmpeg.zip...")
            os.remove("ffmpeg.zip")
            print("Successfully deleted ffmpeg.zip")
            file_path = os.path.dirname(os.path.abspath("ffmpeg/ffmpeg-master-latest-win64-gpl/ffmpeg.exe"))
            print("Adding FFmpeg to path variable...")
            os.environ["PATH"] += file_path 
            print("Successfully added FFmpeg to path variable")
        print("Downloading Silent-Bot...")
        try:
            git.Git(os.path.dirname(os.path.abspath("Installer/"))).clone("git://github.com/IamPekka058/Silent-Bot.git")
        except:
            git.Git(os.path.dirname(os.path.abspath("Installer/"))).pull()
        print("Downloaded Silent-Bot")

        print(colors["green"]+"Installation done.\n"+colors["white"])
        exit()

    if(os_name == "Linux"):
        if not getgit:
            print("Installing...")
            p = subprocess.Popen("sudo apt-get install git", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            p.wait()
            print("Git installed\n")
            
        if(getFFmpeg() == False):
            print("Installing FFmpeg for Linux...")
            p = subprocess.Popen("sudo apt-get install ffmpeg -y", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            p.wait()
            print("Installed FFmpeg for Linux")
        print("Downloading Silent-Bot...")
        try:
            git.Git(os.path.dirname(os.path.abspath("Installer/"))).clone("git://github.com/IamPekka058/Silent-Bot.git")
        except:
            git.Git(os.path.dirname(os.path.abspath("Installer/"))).pull()
        print("Downloaded Silent-Bot")
        print(colors["green"]+"Installation done.\n"+colors["white"])
        exit()

    print("Your OS is not supported.")

if __name__ == "__main__":
    fetchData()
    install()