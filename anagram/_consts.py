

import os
from pathlib import Path


ROOT_MACHINE        = None
ROOT_USER           = None
ROOT_CWD            = None

if os.name == "posix":
    ROOT_MACHINE    = "/etc"
    ROOT_USER       = os.getenv("HOME", None)
    ROOT_CWD        = "."
elif os.name == "nt":
    ROOT_MACHINE    = os.getenv("PROGRAMDATA", None)
    ROOT_USER       = os.getenv("APPDATA", None)
    ROOT_CWD        = "."

if not ROOT_MACHINE is None:
    ROOT_MACHINE    = Path(ROOT_MACHINE)

if not ROOT_USER is None:
    ROOT_USER       = Path(ROOT_USER)

if not ROOT_CWD is None:
    ROOT_CWD        = Path(ROOT_CWD)


SYM_ANAGRAM         = "anagram"

PATH_ANAGRAM        = SYM_ANAGRAM
PATH_DOT_ANAGRAM    = f".{SYM_ANAGRAM}"

PATH_LOG            = f"{SYM_ANAGRAM}.log"
PATH_LOCK           = ".lock"
PATH_CONFIG         = "config"
PATH_CHANGE         = "change"
PATH_META           = "meta.json"

GIT_BRANCH_PREFIX   = f"{SYM_ANAGRAM}/"
GIT_AUTHOR_NAME     = SYM_ANAGRAM.capitalize()
GIT_AUTHOR_EMAIL    = ""

CMD_MAN_BRANCH      = True
CMD_MAN_WORKTREE    = True

TIMEOUT             = 5
ENCODING            = "UTF-8"

