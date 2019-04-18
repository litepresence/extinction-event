"""
Confirm SSD Drive
Confirm Adequate RAM
Confirm Linux OS
Apt-Get Packages
Python Version Update
Create Virtual Environment
"""
from sys import platform, version_info
from time import time, sleep
from subprocess import call
import urllib.request
import re
import os


class ChangeDirectory:
    """
    Context manager for changing the current working directory
    h/t @ brianmhunt
    """

    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)
        self.saved_path = os.getcwd()

    def __enter__(self):
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


def it(style, text):
    """
    Colored text in terminal
    """
    emphasis = {
        "red": 91,
        "green": 92,
        "yellow": 93,
        "blue": 94,
        "purple": 95,
        "cyan": 96,
    }
    return ("\033[%sm" % emphasis[style]) + str(text) + "\033[0m"

def proceed():
    """
    Y/N Prompt to Continue or Exit
    """
    select = False
    while select not in ["y", "n", ""]:
        print("\n")
        select = input("Do you want to continue? [Y/n] ")
        try:
            select = select.lower()[0]
        except BaseException:
            continue
        if select not in ["y", "n", ""]:
            print("Invalid Entry")
    if select == "n":
        exit()
    print("\n")    


def get_latest_python():
    """
    Web scrape docs.python.org for latest version number
    STANDARD libarary ONLY (sys / urllib / re)
    """
    url = "https://www.python.org/downloads/"
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    text = str(resp.read())
    # text = requests.get(url).text
    # make list of all A.B.C version numbers
    versions = re.findall(r"\d+\.\d+\.\d+", text)
    versions += re.findall(r"\d+\.\d+", text)
    versions = sorted(list(set(versions)), reverse=True)
    # include only versions with A=3
    version_3s = [i for i in versions if int(i[0]) == 3][:10]
    version_id = (str(version_info[0]) +
                  "." +
                  str(version_info[1]) +
                  "." +
                  str(version_info[2]))
    print(it("yellow", "Python Version Update \n\n"))
    print("Version numbers found at", url, "\n")
    print(version_3s, "\n")
    print("It APPEARS that the current stable release is:", "\n")
    print(version_3s[0], "\n")
    print("It APPERS that the current version on this system is:", "\n")
    print(version_id, "\n")
    print("bitsharesQUANT requires:", "\n")
    print("3.6 or greater", "\n")
    print("As of April 2019 bitsharesQUANT recommends:", "\n")
    print("3.7.3", "\n")
    print("WARN: The highest version available may be a development fork")
    print("WARN: Please visit", url)
    print("WARN: to determine the latest STABLE release version\n\n")
    version = ""
    version = input("Input version number to UPGRADE or ENTER to skip: ")
    print("\n")
    return version


def install_latest_python(version):
    """
    Prepare system for Python version update
    Optionally download tarball and update Python
    """
    # h/t https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/
    tarball_url = "https://www.python.org/ftp/python/%s/Python-%s.tgz" % (
        version,
        version,
    )
    tarball_name = "Python-%s.tgz" % version
    file_location = "Python-%s" % version
    step0 = ["sudo", "apt-get", "update"]
    step1 = ["sudo", "apt-get", "install", "build-essential", "checkinstall"]
    step2 = [
        "sudo",
        "apt-get",
        "install",
        "libreadline-gplv2-dev",
        "libncursesw5-dev",
        "libssl-dev",
        "libsqlite3-dev",
        "tk-dev",
        "libgdbm-dev",
        "libc6-dev",
        "libbz2-dev",
        "libffi-dev",
    ]
    step3 = ["sudo", "wget", tarball_url]
    step4 = ["sudo", "tar", "xzf", tarball_name]
    step5 = ["sudo", "./configure", "--enable-optimizations"]
    step6 = ["sudo", "-H", "make", "altinstall"]
    print(it("yellow", "Check Install and Update Apt Get \n"))
    print(" ".join(step0))
    print(" ".join(step1), "\n")
    print(it("yellow", "Install base libraries \n"))
    print(" ".join(step2), "\n")
    if version:
        print(it("yellow", "Get tarball \n"))
        print(" ".join(step3), "\n")
        print(it("yellow", "Extract tarball \n"))
        print(" ".join(step4), "\n")
        print(it("yellow", "Compile \n"))
        print(" ".join(step5))
        print(" ".join(step6), "\n")
    proceed()
    call(step0)
    call(step1)
    call(step2)
    if version:
        with ChangeDirectory("/usr/src"):
            call(step3)
            call(step4)
        with ChangeDirectory("/usr/src/" + file_location):
            call(step5)
            call(step6)
        print("\nThe latest verion of python has been installed\n")
        print("Checking Version\n")
        print("python%s -V\n" % version[:3])
        call(["python%s" % version[:3], "-V"])


def dependency_manager():
    """
    apt-get dependency intallation
    """
    dependencies = [
        "python3-pip",
        "python3-tk",
        "python3-dev",
        "libsecp256k1-dev",
        "virtualenv",
    ]
    # update the apt-get utility
    step1 = ["sudo", "apt-get", "update"]
    # pip, tk, dev, 256k1
    step2 = ["sudo", "apt-get", "install", "-y", "python3-pip"]
    step3 = ["sudo", "apt-get", "install", "python3-tk"]
    step4 = ["sudo", "apt-get", "install", "python3-dev"]
    step5 = ["sudo", "apt-get", "install", "libsecp256k1-dev"]
    # install and create a virtual environment
    step6 = ["sudo", "-H", "pip3", "install", "virtualenv"]
    steps = [step1, step2, step3, step4, step5, step6]
    print("Installing the following dependencies: \n")
    for dependency in dependencies:
        print(dependency)
    for step in steps:
        print(" ".join(step))
        call(step)


def create_virtual_env(version):
    """
    Create virtual environment
    Prompt to finish setup
    """
    print("Creating virtual environment\n")
    call(["virtualenv", "-p", "python3", "env"])
    print(it("green", "Environment created!\n"))
    print("To complete installation ENTER these commands:\n")
    if version:
        print(it("yellow", "    alias python3=python%s" % version[:3]), "\n")
    print(it("yellow", "    source env/bin/activate"))
    print(it("yellow", "    sudo python3 setup.py install\n"))


def linux_test():
    """
    Confirm installation is occuring on linux operating system
    """
    assert "linux" in platform.lower(), it(
        "red", "not linux OS, format drive and try again"
    )
    print(it("green", "Linux Found"))


def python_test():
    """
    check python version number is greater than 3.6, else warn
    """
    version = int(version_info[0]) + int(version_info[1]) / 10.0
    version_id = (str(version_info[0]) +
                  "." +
                  str(version_info[1]) +
                  "." +
                  str(version_info[2]))
    print("Version", version_id)
    if version < 3.6:
        print(it("red", "WARN: Python Version must be 3.6 or greater"))
        print(it("yellow", "You will be prompted to upgrade, " +
                 "follow the instructions.", ))
    else:
        print(it("green", "Python 3.6+ Found"))


def ram_test():
    """
    Ensure at least 3 gigs of ram
    """
    mem_bytes = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    mem_gib = mem_bytes / (1024.0 ** 3)
    print("%.1f GB RAM" % mem_gib)
    assert mem_gib > 3, it(
        "red", "you will need at least 3GB RAM to run this suite")
    print(it("green", "minimum adequate RAM found"))


def cat_scsi_test():
    """
    Check for drive labeled "solid state"
    """
    print('confirming an SSD in this machine with "cat /proc/scsi/scsi"')
    call(["cat", "/proc/scsi/scsi"])
    scsi = str(os.popen("cat /proc/scsi/scsi").read()).lower()
    if "ssd" not in scsi:
        print(it("red", "***WARN*** no drive LABELED SSD on this machine"))
        _ = input(r"press ENTER to continue or ctrl+shft+\ to EXIT")
    else:
        print(it("green", "Drive LABELED SSD found on this machine"))


def drive_speed_test():
    """
    Test read and write speed of drive to correlate to SSD
    """
    doc = "ssd_test.txt"
    start = time()
    for _ in range(10000):
        with open(doc, "w+") as handle:
            handle.write("ssd test")
            handle.close()
        with open(doc, "r") as handle:
            _ = handle.read()
            handle.close()
    stop = time()
    elapsed = stop - start
    ios = int(10000 / elapsed)
    drive = "HDD"
    if ios > 6000:  # ssd>8000; hdd <4000
        drive = "SSD"
    print("detecting hard drive type by read and write speed")
    print("ios", ios, "hard drive type", drive)
    if drive == "HDD":
        print(it("red", "***WARN*** it does not APPEAR" +
                 " you are INSTALLING on an SSD"))
        _ = input(r"press ENTER to continue or ctrl+shft+\ to EXIT")
    print(it("green", "it appears you are installing on an SSD drive"))


def system_compatibility():
    """
    Process for linux, python, ram, and ssd checks
    """
    print("\033c")
    print("")
    print("")
    print(it("yellow", "litepresence presents"))
    print("")
    print(it("blue", "bitsharesQUANT"))
    print("")
    print("")
    print("ENSURING LINUX OS")
    sleep(0.1)
    linux_test()
    print("ENSURING PYTHON 3")
    sleep(0.1)
    python_test()
    print("CHECKING YOUR SYSTEM RAM")
    sleep(0.1)
    ram_test()
    print("SOLID STATE DRIVE IS REQUIRED")
    print("RUNNING SOME TESTS WHICH MAY THROW FALSE NEGATIVE")
    print("SKIP IF YOU ARE SURE YOU ARE INSTALLING ON AN SSD")
    sleep(0.1)
    cat_scsi_test()
    drive_speed_test()
    print("SSD TEST COMPLETE")
    print("")


def main():
    """
    Primary environment creation backbone
    """
    print("\033c", "\n\n\n")
    print("Ubuntu, Debian, and LinuxMint", "\n")
    print("bitshareQUANT Environment Manager", "\n")
    system_compatibility()
    version = get_latest_python()
    install_latest_python(version)
    dependency_manager()
    create_virtual_env(version)


if __name__ == "__main__":
    main()
