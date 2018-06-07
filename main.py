import sys
import os
import json
import getpass
import time
from crawler import Crawler
from git import Git
from option import Option

ERROR_FORMAT = '* Error: %s'

class Main:

    def __init__(self, crawler, git, option, user_info):
        self.crawler = crawler
        self.git = git
        self.option = option
        self.user_info = user_info

        self.user_name = user_info['user_name']
        self.repo_url = user_info['repo_url']
        self.repo_name = user_info['repo_name']
        
        self.solved_list = []

    def run(self):
        self.init_clone()

        while True:
            self.find_solved_problem()
            self.push_source()
            self.idle()

    def init_clone(self): 
        git_id = self.user_info['git_id']
        git_pw = self.user_info['git_pw']
        remote_url = 'https://%s:%s@github.com/%s/%s' % (git_id, git_pw, git_id, self.repo_name)
 
        git.clone(self.repo_name, self.repo_url) 
        git.pull(self.repo_name, remote_url)

    def find_solved_problem(self):
        self.solved_list = []
        solved_set = set()

        user_status_error, user_status = self.crawler.get_user_status(self.user_name)
        if user_status_error:
            print(ERROR_FORMAT % ('get_user_status, ' + user_status))
            return
 
        for submission in user_status:
            if not submission['verdict'] == 'OK':
                continue

            key = str(submission['contestId']) + submission['problem']['index']
            if key in solved_set:
                continue
            solved_set.add(key)

            solved = {}
            solved['submission_id'] = submission['id']
            solved['contest_id'] = submission['contestId']
            solved['problem_id'] = submission['problem']['index']
            solved['problem_title'] = submission['problem']['name']
            solved['language'] = submission['programmingLanguage']
            solved['cp_id'] = key
            self.solved_list.append(solved)

    def push_source(self):
        for solved in self.solved_list:
            submission_id = solved['submission_id']
            contest_id = solved['contest_id']
            problem_id = solved['problem_id']
            language = solved['language']

            source_tree = self.option.source_tree(solved)
            source_name = self.option.source_name(solved)
            file_path = '%s%s%s' % (source_tree, source_name, self.option.get_ext(language))

            support, same = self.option.lang(solved)
            if support:
                if not same:
                    print("* '%s' language is not supported (submission: %d, contest: %d, index: %s)" % (language, submission_id, contest_id, problem_id))
                    continue

            if os.path.exists(file_path):
                print('* source already exists (submission: %d, contest: %d, index: %s)' % (submission_id, contest_id, problem_id))
                continue
       
            print('* Downloading source (submission: %d, contest: %d, index: %s)' % (submission_id, contest_id, problem_id))
            source_error, source = self.crawler.get_source(submission_id, contest_id)
            if source_error:
                print(ERROR_FORMAT % ('get_source, ' + source))
                print('* Failed to download the source (submission: %d, contest: %d, index: %s)\n' % (submission_id, contest_id, problem_id))
                continue
            print(source)

            self.save_source(source_tree, file_path, source)
            print("* Successfully saved the '%s'" % (file_path))

            self.git_all(file_path, solved)
            print('* Successfully pushed the source (submission: %d, contest: %d, index: %s)\n' % (submission_id, contest_id, problem_id))

    def save_source(self, source_tree, file_path, source):
        if not os.path.isdir(source_tree):
            os.makedirs(source_tree)

        f = open(file_path, 'w')
        f.write(source)
        f.close()

    def git_all(self, file_path, solved):
        git_id = self.user_info['git_id']
        git_pw = self.user_info['git_pw']
        remote_url = 'https://%s:%s@github.com/%s/%s' % (git_id, git_pw, git_id, self.repo_name)
        file_path = file_path.replace(self.repo_name, '.', 1)
        commit_message = self.option.commit_message(solved)
        
        self.git.all(self.repo_name, remote_url, 'master', file_path, commit_message)

    def idle(self):
        poll = self.option.poll()

        print('* Wait %d seconds... \n' % (poll))
        time.sleep(poll)
        print('* Restart work')

if __name__ == '__main__':
    user_info = {}
    if os.path.isfile('option.json'):
        user_info = json.loads(open('option.json', 'r').read())

    if os.path.isfile('info.json'):
        private_info = json.loads(open('info.json', 'r').read())
        user_info['user_name'] = private_info['handle']
        user_info['repo_url'] = private_info['remote_url']
        user_info['repo_name'] = private_info['remote_url'].split('/')[-1].split('.')[0]
        user_info['git_id'] = private_info['git_id']
        user_info['git_pw'] = private_info['git_pw']
    else:
        user_info['user_name'] = input('* Handle for Codeforces: ')
        user_info['repo_url'] = input('* URL for a remote repository: ')
        user_info['repo_name'] = user_info['repo_url'].split('/')[-1].split('.')[0]
        user_info['git_id'] = input("* Username for 'https://github.com': ")
        user_info['git_pw'] = getpass.getpass("* Password for 'https://%s@github.com': " % (user_info['git_id']))

    crawler = Crawler()
    git = Git()
    option = Option(user_info)
    try:
        Main(crawler, git, option, user_info).run()
    except KeyboardInterrupt:
        print('\n* bye\n')
