

from dataclasses import dataclass



@dataclass
class Message:
    content     : str
    by_anagram  : bool

