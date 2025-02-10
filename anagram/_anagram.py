

import json
from pathlib import Path
from contextlib import contextmanager

from portalocker import Lock
from git import Repo

from ._meta import Meta
from .change import Change
from .llm import Llm


PATH_ANAGRAM        = ".anagram"
PATH_LOCK           = ".lock"
PATH_CONFIG         = "config"
PATH_CHANGE         = "change"
PATH_META           = "meta.json"

TIMEOUT_LOCK        = 5
GIT_BRANCH_PREFIX   = "anagram/"
GIT_AUTHOR_NAME     = "anagram"
GIT_AUTHOR_EMAIL    = ""
ENCODING            = "UTF-8"



class Anagram:

    def __init__(self, path:str|Path):
        self.path = Path(path)
        self.path_anagram = self.path / PATH_ANAGRAM
        self.path_lock = self.path_anagram / PATH_LOCK
        self.path_config = self.path_anagram / PATH_CONFIG
        self.path_change = self.path_anagram / PATH_CHANGE
        self.path_meta = self.path_anagram / PATH_META

        self.timeout_lock = TIMEOUT_LOCK
        self.git_branch_prefix = GIT_BRANCH_PREFIX
        self.git_author_name = GIT_AUTHOR_NAME
        self.git_author_email = GIT_AUTHOR_EMAIL
        self.encoding = ENCODING

        self.config = None

        if self.path_config.exists():
            # TODO: Implement Config for a configurable Anagram instance.
            # TODO: Implement applying values read by Config.
            pass

        self._lock = Lock(self.path_lock, timeout=self.timeout_lock)

        with self._lock:
            self.path_change.mkdir(exist_ok=True)
            if not self.path_meta.exists():
                with self._get_meta() as meta:
                    meta.save(self.path_meta)


    @contextmanager
    def _get_meta(self):
        with self._lock:
            _meta = Meta.from_file(self.path_meta)
            yield _meta


    @contextmanager
    def _set_meta(self):
        with self._get_meta() as _meta:
            try:
                yield _meta
            finally:
                _meta.save(self.path_meta)


    def list_changes(self) -> list[str]:
        with self._get_meta() as meta:
            return list(meta.changes)


    def get_change(self, name:str) -> Change|None:
        with self._get_meta() as meta:
            if name in meta.changes:
                return meta.changes[name]
            else:
                return None


    def get_current_change(self) -> Change|None:
        with self._get_meta() as meta:
            if meta.current in meta.changes:
                return meta.changes[meta.current]
            else:
                return None


    def checkout_change(self, name:str) -> Change|None:
        with self._set_meta() as meta:
            if name in meta.changes:
                meta.current = name
                return meta.changes[name]
            else:
                return None


    def add_change(self, name:str, upstream:str=None, base:str=None) -> Change|None:
        with self._set_meta() as meta:
            _repo = Repo(self.path)

            if not upstream is None:
                _upstream = _repo.refs[upstream].name
            elif not meta.current is None:
                _upstream = _repo.refs[meta.changes[meta.current].branch].name
            else:
                _upstream = _repo.head.ref.name
            if not base is None:
                _base = _repo.commit(base)
            elif not meta.current is None:
                _base = _repo.refs[_upstream].commit
            else:
                _base = _repo.head.ref.commit

            _name = self.git_branch_prefix + name
            _worktree = self.path_change / name
            _branch = _repo.create_head(_name, _base).name
            _repo.git.worktree("add", _worktree, _branch)
            _change = Change(meta.path, name, _branch, _upstream, _worktree.relative_to(meta.path).as_posix())
            meta.changes[name] = _change
            return _change


    def remove_change(self, name:str, force:bool=False) -> Change|None:
        _args = []
        if force:
            _args.append("--force")
        
        with self._set_meta() as meta:
            _repo = Repo(self.path)

            if meta.current == name:
                meta.current = None
            
            _change = meta.changes.pop(name, None)
            if not _change is None:
                _worktree = _change.path / _change.worktree
                _repo.git.worktree("remove", *_args, _worktree)
            
            return _change


    def modify_change(self, name:str, field:str, value) -> Change|None:
        with self._set_meta() as meta:
            if name in meta.changes:
                setattr(meta.changes[name], field, value)
                return meta.changes[name]
            else:
                return None


    def modify_change_name(self, name:str, rename:str) -> Change|None:
        with self._set_meta() as meta:
            # TODO: Implement change name method to update name, branch, worktree.
            pass


    def modify_change_branch(self, name:str, branch:str) -> Change|None:
        with self._set_meta() as meta:
            if name in meta.changes:
                meta.changes[name].branch = branch
                return self.changes[name]
            else:
                return None


    def modify_change_upstream(self, name:str, upstream:str) -> Change|None:
        with self._set_meta() as meta:
            if name in meta.changes:
                meta.changes[name].upstream = upstream
                return self.changes[name]
            else:
                return None

