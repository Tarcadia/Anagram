

from ._logging import logging_set

from ._anagram import Anagram
from ._command import Command

if __name__ == "__main__":
    logging_set(
        file_enable=True,
        console_enable=True
    )
    anagram = Anagram(".")
    commaind = Command(anagram)
    commaind()

