

from pathlib import Path
from dataclasses import dataclass

from git import Repo

from ._chat import Chat

@dataclass
class Change:
    path        : Path
    name        : str
    branch      : str
    upstream    : str
    worktree    : str

    def get_repo(self) -> Repo:
        return Repo(self.path / self.worktree)

    def get_chat(self) -> Chat:
        return Chat(self.get_repo(), self.branch, self.upstream)

