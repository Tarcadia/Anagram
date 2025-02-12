

from dataclasses import dataclass

from git import Repo
from git import Commit
from git import Actor

from ._message import Message

from .._consts import ENCODING
from .._consts import GIT_AUTHOR_NAME



@dataclass
class _Cache:
    base        : list[Commit]
    messages    : list[Commit]

    def __post_init__(self):
        self._update_files()
        self._update_messages()

    def _update_files(self):
        _files = {}
        for _item in self.base[0].tree.traverse():
            if _item.type == "blob":
                # TODO: Use Anagram::encoding field for configuring
                _files[_item.path] = _item.data_stream.read().decode(ENCODING)
        self._files = _files

    def _update_messages(self):
        _messages = []
        for _message in self.messages:
            # TODO: Use Anagram::git_author_name field for configuring
            _by_anagram = (_message.author.name == GIT_AUTHOR_NAME)
            _messages.append(Message(_message, _message.message, _by_anagram))
            for _diff in _message.parents[0].diff(_message, create_patch=True):
                _messages.append(Message(_message, str(_diff), _by_anagram))
        self._messages = _messages

    def update_messages(self, messages):
        self.messages = messages
        self._update_messages()



@dataclass
class Chat:
    repo        : Repo
    branch      : str
    upstream    : str

    def __post_init__(self):
        self._cache = None
        self._cache = self._get_cache()

    def _get_cache(self) -> _Cache:
        _branch = self.repo.refs[self.branch]
        _upstream = self.repo.refs[self.upstream]
        _base = self.repo.merge_base(_branch, _upstream)
        _messages = []
        for _commit in self.repo.iter_commits(_branch):
            if _commit == _base[0]:
                break
            _messages.append(_commit)
        if self._cache is None:
            self._cache = _Cache(_base, _messages)
        elif self._cache.base != _base:
            self._cache = _Cache(_base, _messages)
        elif self._cache.messages != _messages:
            self._cache.update_messages(_messages)
        return self._cache

    def get_files_messages(self) -> tuple[dict[str, str], list[Message]]:
        _cache = self._get_cache()
        return _cache._files, _cache._messages

    def add_message(self, content:str, by_anagram:bool=False):
        _args = {}
        if by_anagram:
            # TODO: Use Anagram::git_author_name, Anagram::git_author_email field for configuring
            _args["author"] = Actor(GIT_AUTHOR_NAME, "")
        self.repo.index.commit(content, *_args)

