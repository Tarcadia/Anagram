

from pathlib import Path

from dataclasses import dataclass

from git import Repo

from ..llm import Llm

@dataclass
class Change:
    path:Path
    name:str
    chat:str
    branch:str
    worktree:str

    def get_llm(self) -> Llm:
        pass

    def get_repo(self) -> Repo:
        Repo(self.path / self.worktree)
