

from pathlib import Path
from contextlib import contextmanager

from portalocker import Lock
from git import Repo

from ._meta import Meta
from .change import Change
from .llm import Llm

from ._config import Config
from ._config import CONFIG_MACHINE
from ._config import CONFIG_USER

from ._consts import SYM_ANAGRAM

from ._consts import PATH_DOT_ANAGRAM
from ._consts import PATH_LOCK
from ._consts import PATH_CONFIG
from ._consts import PATH_CHANGE
from ._consts import PATH_META

from ._consts import GIT_BRANCH_PREFIX
from ._consts import GIT_AUTHOR_NAME
from ._consts import GIT_AUTHOR_EMAIL

from ._consts import TIMEOUT
from ._consts import ENCODING



class Anagram:

    def __init__(self, path:str|Path):
        self.path = Path(path)
        self.path_anagram = self.path / PATH_DOT_ANAGRAM
        self.path_lock = self.path_anagram / PATH_LOCK
        self.path_config = self.path_anagram / PATH_CONFIG
        self.path_change = self.path_anagram / PATH_CHANGE
        self.path_meta = self.path_anagram / PATH_META

        self.git_branch_prefix = GIT_BRANCH_PREFIX
        self.git_author_name = GIT_AUTHOR_NAME
        self.git_author_email = GIT_AUTHOR_EMAIL
        self.lock_timeout = TIMEOUT
        self.encoding = ENCODING

        self.config = Config()
        self.config.update(CONFIG_MACHINE)
        self.config.update(CONFIG_USER)
        if self.path_config.exists():
            _config = Config(self.path_config)
            self.config.update(_config)
        
        self.config.pick_to(SYM_ANAGRAM, self)

        self._lock = Lock(self.path_lock, timeout=self.lock_timeout)

        with self._lock:
            self.path_change.mkdir(exist_ok=True)
            if not self.path_meta.exists():
                with self._get_meta() as meta:
                    meta.save(self.path_meta)


    @contextmanager
    def _get_meta(self):
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
            _change = meta.changes.get(name, None)
            return _change


    def get_current_change(self) -> Change|None:
        with self._get_meta() as meta:
            _change = meta.changes.get(meta.current, None)
            return _change


    def checkout_change(self, name:str) -> Change|None:
        with self._set_meta() as meta:
            _change = meta.changes.get(name, None)
            if _change is None:
                return

            meta.current = _change.name
            return _change


    def add_change(self, name:str, upstream:str=None, base:str=None) -> Change|None:
        with self._set_meta() as meta:
            _repo = Repo(self.path)
            _change = meta.changes.get(name, None)
            if _change is None:
                if not upstream is None:
                    _upstream = _repo.refs[upstream].name
                elif not meta.current is None:
                    _upstream = _repo.refs[meta.changes[meta.current].branch].name
                else:
                    _upstream = _repo.head.ref.name

                _branch = self.git_branch_prefix + name
                _worktree = self.path_change / name
                _change = Change(meta.path, name, _branch, _upstream, _worktree.relative_to(meta.path).as_posix())
                meta.changes[name] = _change

            if not base is None:
                _base = _repo.commit(base)
            else:
                _base = _repo.commit(_upstream)

            try:
                _repo.create_head(_change.branch, _base)
            except:
                # TODO: Implement warning message
                pass

            try:
                _repo.git.worktree("add", _change.worktree, _change.branch)
            except:
                # TODO: Implement warning message
                pass

            return _change


    def remove_change(self, name:str, remove_worktree:bool, remove_branch:bool, force:bool=False) -> Change|None:
        with self._set_meta() as meta:
            _repo = Repo(self.path)
            _change = meta.changes.pop(name, None)
            if _change is None:
                return

            if meta.current == name:
                meta.current = None

            if remove_worktree:
                _worktree = _change.path / _change.worktree
                _force = ["--force"] if force else []
                try:
                    _repo.git.worktree("remove", *_force, _worktree)
                except:
                    # TODO: Implement warning message
                    pass

            if remove_branch:
                _branch = _repo.heads[_change.branch]
                try:
                    _repo.delete_head(_branch, force=force)
                except:
                    # TODO: Implement warning message
                    pass

            return _change


    def modify_change(self, name:str, field:str, value) -> Change|None:
        with self._set_meta() as meta:
            _change = meta.changes.get(name, None)
            if _change is None:
                return

            try:
                setattr(_change, field, value)
            except:
                # TODO: Implement warning message
                pass
            return _change


    def modify_change_name(self, name:str, rename:str) -> Change|None:
        with self._set_meta() as meta:
            # TODO: Implement change name method to update name, branch, worktree.
            pass


    def modify_change_branch(self, name:str, branch:str) -> Change|None:
        with self._set_meta() as meta:
            _change = meta.changes.get(name, None)
            if _change is None:
                return

            _change.branch = branch
            return _change


    def modify_change_upstream(self, name:str, upstream:str) -> Change|None:
        with self._set_meta() as meta:
            _change = meta.changes.get(name, None)
            if _change is None:
                return

            _change.upstream = upstream
            return _change

