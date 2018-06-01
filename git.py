import sys
import os
import subprocess

ERROR_FORMAT = '* Error: %s'

class Git:

    def __init__(self):
        self.pipe = subprocess.PIPE

    def clone(self, repo_name, repo_url):
        if os.path.isdir(repo_name):
            print("* Repository '%s' already exists." % (repo_name))
            return

        command = ['git', 'clone', repo_url]
        proc = subprocess.Popen(command, stdout=self.pipe, stderr=self.pipe)
        stdout, stderr = proc.communicate()

        if not stdout is None:
            print(stdout.decode())
        if not stderr is None:
            print(stderr.decode())
        if not proc.returncode == 0:
            sys.exit(ERROR_FORMAT % ('git clone, ' + proc.returncode))

    def pull(self, cwd, repo_url):
        command = ['git', 'pull', repo_url]
        proc = subprocess.Popen(command, cwd=cwd, stdout=self.pipe, stderr=self.pipe)
        stdout, stderr = proc.communicate()
        
        if not stdout is None:
            print(stdout.decode())
        if not stderr is None:
            print(stderr.decode())
        if not proc.returncode == 0:
            sys.exit(ERROR_FORMAT % ('git pull, ' + proc.returncode))

    def add(self, cwd, file_path):
        command = ['git', 'add', file_path]
        proc = subprocess.Popen(command, cwd=cwd, stdout=self.pipe, stderr=self.pipe)
        stdout, stderr = proc.communicate()
        
        if not stdout is None:
            print(stdout.decode())
        if not stderr is None:
            print(stderr.decode())
        if not proc.returncode == 0:
            sys.exit(ERROR_FORMAT % ('git add, ' + proc.returncode))

    def commit(self, cwd, commit_message):
        command = ['git', 'commit', '-m', commit_message]
        proc = subprocess.Popen(command, cwd=cwd, stdout=self.pipe, stderr=self.pipe)
        stdout, stderr = proc.communicate()
        
        if not stdout is None:
            print(stdout.decode())
        if not stderr is None:
            print(stderr.decode())
        if not proc.returncode == 0:
            sys.exit(ERROR_FORMAT % ('git commit, ' + proc.returncode))

    def push(self, cwd, remote_url, branch):
        command = ['git', 'push', remote_url, branch]
        proc = subprocess.Popen(command, cwd=cwd, stdout=self.pipe, stderr=self.pipe)
        stdout, stderr = proc.communicate()

        if not proc.returncode == 0:
            sys.exit(ERROR_FORMAT % ('git push, ' + proc.returncode))

    def all(self, repo_name, remote_url, branch, file_path, commit_message):
        self.add(repo_name, file_path)
        self.commit(repo_name, commit_message)
        self.push(repo_name, remote_url, branch)
