import os
import shutil
from modules.git_handler import clone_repo, copy_monitoring_files
from modules.docker_compose_generator import generate_docker_compose

def handle_remove_readonly(func, path, exc_info):
    os.chmod(path, 0o777)
    func(path)

def handle_prometheus_setup():
    repo_url = "https://github.com/Swim-to-the-goal/ggen-configuration.git"
    clone_dir = "cloned_repo"
    target_dir = os.path.join("services", "monitoring")

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    clone_repo(repo_url, clone_dir)
    copy_monitoring_files(clone_dir, target_dir)
    generate_docker_compose("docker-compose-mon.j2", os.path.join(target_dir, "docker-compose-mon.yml"))

    # Cleanup cloned repository with error handling
    shutil.rmtree(clone_dir, onerror=handle_remove_readonly)
    print("Cloned repository cleaned up")
