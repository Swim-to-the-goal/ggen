import os
import subprocess

FLAG_FILE = "init_done.flag"

def check_and_install(package, check_cmd, install_cmd=None, windows_url=None):
    try:
        subprocess.run(check_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{package} is already installed.")
    except subprocess.CalledProcessError:
        if os.name == "nt" and windows_url:
            try:
                print(f"{package} is not installed. Downloading from {windows_url}...")
                file_name = windows_url.split('/')[-1]
                subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {windows_url} -OutFile {file_name}"], check=True)
                subprocess.run(["powershell", "-Command", f"Start-Process {file_name} -ArgumentList '/quiet' -Wait"], check=True)
                return None
            except Exception as e:
                print(f"Failed to install {package} from {windows_url}: {e}")
                return package
        return install_cmd

def install_packages(install_commands):
    for cmd in install_commands:
        if cmd:
            try:
                print(f"Installing {cmd[0]}...")
                subprocess.run(cmd[1], check=True)
                print(f"{cmd[0]} installation completed.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {cmd[0]}: {e}")

def main():
    if os.path.exists(FLAG_FILE):
        print("Initialization already done. Skipping installation.")
        return

    packages = {
        "python": (["python", "--version"], None, "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"),
        "pip": (["pip", "--version"], None, "https://bootstrap.pypa.io/get-pip.py"),
        "git": (["git", "--version"], ["choco", "install", "git", "-y"] if os.name == "nt" else ["sudo", "apt-get", "install", "git", "-y"], None),
        "ansible": (["ansible", "--version"], ["choco", "install", "ansible", "-y"] if os.name == "nt" else ["sudo", "apt-get", "install", "ansible", "-y"], None),
        "curl": (["curl", "--version"], ["choco", "install", "curl", "-y"] if os.name == "nt" else ["sudo", "apt-get", "install", "curl", "-y"], None),
        "wget": (["wget", "--version"], ["choco", "install", "wget", "-y"] if os.name == "nt" else ["sudo", "apt-get", "install", "wget", "-y"], None),
    }

    missing_packages = [package for package, (check_cmd, install_cmd, windows_url) in packages.items() if check_and_install(package, check_cmd, install_cmd, windows_url) is not None]

    if not missing_packages:
        print("All required packages are already installed.")
    else:
        print("The following packages are required but not installed:")
        for pkg in missing_packages:
            print(f"- {pkg}")

        choice = input("Do you want to install these packages now? (yes/no): ").strip().lower()

        if choice == "yes":
            install_commands = [packages[pkg][1] for pkg in missing_packages if packages[pkg][1]]
            install_packages(install_commands)

    with open(FLAG_FILE, "w") as f:
        f.write("Initialization completed.")

if __name__ == "__main__":
    main()
