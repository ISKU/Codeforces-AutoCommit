Codeforces-AutoCommit
==========
[![](http://st.codeforces.com/s/74869/images/codeforces-logo-with-telegram.png)](http://codeforces.com/)
----------
 `Codeforces-AutoCommit` is a tool that solves various algorithmic problems in [Codeforces](http://codeforces.com/) and automatically pushes source code to remote repositories such as [Github](https://github.com) if you get the correct answer. This tool uses your handle to search and analyze the source code in Codeforces. If the source code does not exist in your local repository, download the source code and save it to your local repository and use `Git` to automatically add, commit, and push to the remote repository.

Installation
----------
``` bash
$ git clone https://github.com/ISKU/Codeforces-AutoCommit
```

**Dependency**
``` bash
$ pip3 install requests
$ pip3 install bs4
```

> - [Python](https://www.python.org/)
> - [Git](https://git-scm.com/)

How to use
----------
- If you do not want to enter user information every time you run the tool, create `info.json` as in the following example:
``` json
{
	"handle": "my_codeforces_handle",
	"git_id": "my_github_id",
	"git_pw": "my_github_password",
	"remote_url": "https://github.com/ISKU/Algorithm"
}
```

- Make sure to enter the user information correctly when running the tool or in info.json. Then run the tool as follows.
``` bash
$ python3 main.py
```

- This tool has a very long wait time. It is recommended to run in `Background` as follows.
``` bash
$ nohup python3 main.py &
```

Default
----------
- **Commit message** is "Add solution for [contest_id][problem_index]".
- **Create a directory** named [contest_id] and **save the source code file** named [problem_index] in that directory.
- Search the source code every **10 minutes**.
- Search **all submitted** source code and analyze the correct source code.
- If there are multiple correct source codes, select the **last submitted** source code.

Extension
----------
- You can freely manage your own remote repositories by extending the tool.
- In the `option.json` file, enter the options you want, as in the following example:

``` json
{
	"commit_message": "Add for [CONTEST][INDEX] [TITLE]",
	"source_tree": "Algorithm/Codeforces/src",
	"mkdir": true,
	"dir_name": "[CONTEST]",
	"source_name": "[INDEX]",
	"poll": 600,
	"lang": "GNU C++17"
}
```
> :bulb: Unused options must be cleared.
<br>

**Key Options:**

| **Key**            | **Description**
|:-------------------|:-------------------------------------------------------------------------------------------
| **commit_message** | Set the commit message.
| **source_tree**    | Save the source code in that path. (The starting directory must match the repository name.)
| **mkdir**          | Decide if you want to create a directory when you save the source code. <br>(false: dir_name option is ignored.)
| **dir_name**       | Set the name of the directory where the source code is saved.
| **sourceName**     | Set the name of the source code file.
| **poll**           | Set the source code search cycle in seconds in Codeforces.
| **lang**           | Only the languages you submit in that language will be pushed.

> :bulb: [CONTEST]: If the content contains [CONTEST], it is replaced by contest_id. <br>
> :bulb: [INDEX]: If the content contains [INDEX], it is replaced by problem_index. <br>
> :bulb: [TITLE]: If the content contains [TITLE], it is replaced by problem_title.

Example
----------
- https://github.com/ISKU/Algorithm
- The above repository uses [Codeforces-AutoCommit](https://github.com/ISKU/Codeforces-AutoCommit) to manage the source code. Option used is as follows.

``` json
{
	"commit_message": "Codeforces #[CONTEST][INDEX]: [TITLE]",
	"source_tree": "Algorithm/Codeforces",
	"mkdir": true,
	"dir_name": "[CONTEST]",
	"source_name": "[INDEX]",
	"poll": 600,
	"lang": "Java 8"
}
```

License
----------
> - [MIT](LICENSE)

Author
----------
> - Minho Kim ([ISKU](https://github.com/ISKU))
> - http://codeforces.com/profile/isku
> - **E-mail:** minho.kim093@gmail.com
