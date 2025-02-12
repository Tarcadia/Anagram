

from dataclasses import dataclass

from git import Commit



@dataclass
class Message:
    commit      : Commit
    content     : str
    by_anagram  : bool

