import subprocess
import sys
import os
import re
import time

def print_progress_bar(iteration, total, length=50):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = "\033[93m" + "█" * filled_length + "\033[0m" + "█" * (length - filled_length)
    print(f'\r{bar} {percent}% Complete', end='')

def execute_command(command, *args):
    """コマンドを実行し、リアルタイムで出力を取得して進捗を表示する"""
    process = subprocess.Popen([*command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 出力をリアルタイムで表示し、進捗バーを更新する
    output = ""
    while process.poll() is None:
        line = process.stdout.readline()
        if line:
            output += line
            # pip の進捗バーを抽出して表示
            if "Progress" in line or re.search(r'\d+%', line):
                print_progress_bar(50, 100)  # 仮の進捗として50%を表示
        time.sleep(0.1)
    process.wait()
    print_progress_bar(100, 100)  # 完了
    print(output)  # 最後に全ての出力を表示

def clone_repository(repo_url, destination_folder):
    """GitHubリポジトリをクローンする"""
    print(f"Cloning repository from {repo_url}...")
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    execute_command(['git', 'clone', repo_url, destination_folder])

def install_requirements(requirements_file):
    """requirements.txtからパッケージをインストールする"""
    print(f"Installing requirements from {requirements_file}...")
    execute_command([sys.executable, "-m", "pip", "install", "-r", requirements_file])

# 使用例
if __name__ == "__main__":
    repo_name = input("Enter the GitHub repository name (e.g., user/repository): ")
    destination_folder = input("Enter the destination folder for cloning: ")
    requirements_file = input("Enter the path to the requirements.txt file within the cloned repository: ")

    # GitHub URLを生成
    repo_url = f"https://github.com/{repo_name}.git"

    clone_repository(repo_url, destination_folder)
    install_requirements(requirements_file)
