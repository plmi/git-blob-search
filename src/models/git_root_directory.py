#!/usr/bin/env python3

import re
import os
from typing import List
import subprocess
from models.git_commit import GitCommit


class GitRootDirectory:
    __commit_pattern = 'commit [0-9a-f]{40}'

    def __init__(self, git_root_directory: str):
        if not os.path.exists(git_root_directory):
            raise FileNotFoundError(f'{git_root_directory} does not exist')

        if not os.path.exists(os.path.join(git_root_directory, '.git')):
            raise FileNotFoundError(f'{git_root_directory} not a git repository')

        self.__git_root_directory = git_root_directory

    def __get_git_log(self) -> str:
        return subprocess.check_output(['git', 'log'], cwd=self.__git_root_directory).decode('utf8')

    def get_commits(self) -> List[GitCommit]:
        git_log: str = self.__get_git_log()
        if not git_log:
            raise TypeError('Could not retrieve git log')

        prefix = len('commit ')
        return [GitCommit(commit[prefix:], self.__git_root_directory)
                for commit in re.findall(self.__commit_pattern, git_log)]

