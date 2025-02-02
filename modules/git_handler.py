import os
import shutil
import git

def clone_repo(repo_url, clone_dir):
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    os.makedirs(clone_dir)
    git.Repo.clone_from(repo_url, clone_dir)
    print(f"Repository cloned to {clone_dir}")

def copy_monitoring_files(clone_dir, target_dir):
    monitoring_path = os.path.join(clone_dir, "monitoring")
    if os.path.exists(monitoring_path):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for item in os.listdir(monitoring_path):
            s = os.path.join(monitoring_path, item)
            d = os.path.join(target_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        print(f"Copied monitoring files to {target_dir}")
    else:
        print("Monitoring folder not found in the cloned repository")
