

from pathlib import Path
from dataclasses import dataclass

from git import Repo

from . import Chat

@dataclass
class Change:
    path:Path
    name:str
    base:str
    branch:str
    worktree:str

    def __post_init__(self):
        self._repo = Repo(self.path / self.worktree)
        self._chat = Chat(self._repo, self.base, self.branch)

    def get_chat(self) -> Chat:
        return self._chat

    def get_repo(self) -> Repo:
        return self._repo

