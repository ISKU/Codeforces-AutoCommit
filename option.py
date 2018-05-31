class Option:

    def __init__(self, user_info):
        self.user_info = user_info

    def commit_message(self, solved):
        if not 'commit_message' in self.user_info:
            return 'Add solution for %d%s' % (solved['contest_id'], solved['problem_id'])
        return self.replace_info(self.user_info['commit_message'], solved)

    def source_tree(self, solved):
        if not 'source_tree' in self.user_info:
            if self.mkdir():
                return '%s/%s/' % (self.user_info['repo_name'], self.dir_name(solved))
            return '%s/' % (self.user_info['repo_name'])

        if self.user_info['source_tree'][-1] == '/':
            if self.mkdir():
                return '%s%s/' % (self.replace_info(self.user_info['source_tree'], solved), self.dir_name(solved))
            return self.replace_info(self.user_info['source_tree'])

        if self.mkdir():
            return '%s/%s/' % (self.replace_info(self.user_info['source_tree'], solved), self.dir_name(solved))
        return '%s/' % (self.replace_info(self.user_info['source_tree']))

    def mkdir(self):
        if not 'mkdir' in self.user_info:
            return True
        return self.user_info['mkdir']

    def dir_name(self, solved):
        if not 'dir_name' in self.user_info:
            return solved['contest_id']
        return self.replace_info(self.user_info['dir_name'], solved)

    def source_name(self, solved):
        if not 'source_name' in self.user_info:
            return solved['problem_id']
        return self.replace_info(self.user_info['source_name'], solved)

    def poll(self):
        if not 'poll' in self.user_info:
            return 600
        return self.user_info['poll']

    def lang(self, solved):
        if not 'lang' in self.user_info:
            return False, None
        if not self.user_info['lang'] == solved['language']:
            return True, False 
        return True, True

    def replace_info(self, value, solved):
        value = value.replace('[CONTEST]', str(solved['contest_id']))
        value = value.replace('[INDEX]', solved['problem_id'])
        value = value.replace('[TITLE]', solved['problem_title'])
        return value

    def get_ext(self, language):
        return {
            'GNU C': '.c',
            'GNU C11': '.c',
            'Clang++17 Diagnostics': '.cpp',
            'GNU C++': '.cpp',
            'GNU C++11': '.cpp',
            'GNU C++14': '.cpp',
            'GNU C++17': '.cpp',
            'GNU C++17 Diagnostics': '.cpp',
            'MS C++': '.cpp',
            'Mono C#': '.cs',
            'D': '.d',
            'Go': '.go',
            'Haskell': '.hs',
            'Java 8': '.java',
            'Kotlin': '.kt',
            'Ocaml': '.ml',
            'Delphi': '.dpr',
            'FPC': '.pas',
            'PascalABC.NET': '.pas',
            'Perl': '.pl',
            'PHP': '.php',
            'Python 2': '.py',
            'Python 3': '.py',
            'PyPy 2': '.py',
            'PyPy 3': '.py',
            'Ruby': '.rb',
            'Rust': '.rs',
            'Scala': '.scala',
            'JavaScript': '.js',
            'Node.js': '.js',
        }[language]
