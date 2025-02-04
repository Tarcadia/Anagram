

from dataclasses import dataclass

from git import Repo


@dataclass
class Chat:
    repo: Repo
    base: str
    branch: str

    def __post_init__(self):
        self._base = self.repo.commit(self.base)
        _history = []
        for _commit in self.repo.iter_commits(self.branch):
            _history.append(_commit)
            if _commit == self._base:
                break
        self._history = reversed(_history)

