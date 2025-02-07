

from dataclasses import dataclass

from git import Repo
from git import Commit


@dataclass
class Chat:
    repo        : Repo
    branch      : str
    upstream    : str

    def __post_init__(self):
        _branch = self.repo.refs[self.branch]
        _upstream = self.repo.refs[self.branch]
        _base = self.repo.merge_base(_branch, _upstream)[0]
        _history = []
        for _commit in self.repo.iter_commits(_branch):
            _history.append(_commit)
            if _commit == _base:
                break
        self._history = reversed(_history)

    def get_history(self) -> list[Commit]:
        return self._history

