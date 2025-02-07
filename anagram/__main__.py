

from ._anagram import Anagram
from ._command import Command

if __name__ == "__main__":
    anagram = Anagram(".")
    commaind = Command(anagram)
    commaind()

