

import json
import os
from pathlib import Path
from dataclasses import dataclass

from git import Repo

from .change import Change
from .llm import Llm



class Anagram:

    PATH_ANAGRAM = ".anagram"
    PATH_LOCK = ".lock"
    PATH_CONFIG = "config"
    PATH_CHANGE = "change"
    PATH_CHANGE_META = "meta.json"

    META_KEY_CURRENT = "current"
    META_KEY_CHANGES = "list"
    META_EMPTY = {META_KEY_CURRENT:None, META_KEY_CHANGES:{}}


    def __init__(self, path:str|Path):
        self.path = Path(path)
        self.path_anagram = self.path / Anagram.PATH_ANAGRAM
        self.path_lock = self.path_anagram / Anagram.PATH_LOCK
        self.path_config = self.path_anagram / Anagram.PATH_CONFIG
        self.path_change = self.path_anagram / Anagram.PATH_CHANGE
        self.path_change_meta = self.path_change / Anagram.PATH_CHANGE_META
        self.path_change.mkdir(exist_ok=True)

        if not self.path_change_meta.exists():
            with self.path_change_meta.open("w") as fp:
                json.dump(Anagram.META_EMPTY, fp)

        if self.path_config.exists():
            pass


    def get_meta(self) -> tuple[str|None, dict[str, Change]]:
        current = None
        changes = {}
        with self.path_change_meta.open("r") as fp:
            meta = json.load(fp)
            if Anagram.META_KEY_CURRENT in meta:
                current = meta[Anagram.META_KEY_CURRENT]
            if Anagram.META_KEY_CHANGES in meta:
                changes = meta[Anagram.META_KEY_CHANGES]
        changes = {_name:Change(self.path_change, name=_name, *_change) for _name, _change in changes}
        return current, changes


    def get_change(self, name) -> Change|None:
        _, changes = self.get_meta()
        if name in changes:
            return changes[name]
        else:
            return None


    def get_current_change(self) -> Change|None:
        current, changes = self.get_meta()
        if current in changes:
            return changes[current]
        else:
            return None


    def list_changes(self) -> list[str]:
        _, changes = self.get_meta()
        return list(changes)

