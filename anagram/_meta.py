

import json
from pathlib import Path
from contextlib import contextmanager
from dataclasses import dataclass
from dataclasses import field
from dataclasses import asdict

from .change import Change


META_KEY_CURRENT    = "current"
META_KEY_CHANGES    = "changes"



@dataclass
class Meta:

    path        : Path
    current     : str | None            = None
    changes     : dict[str,Change]      = field(default_factory=dict)

    def load(self, filename:str|Path):
        if Path(filename).exists():
            _current = None
            _changes = {}
            with open(filename, "r") as fp:
                meta = json.load(fp)
                if META_KEY_CURRENT in meta:
                    _current = meta[META_KEY_CURRENT]
                if META_KEY_CHANGES in meta:
                    _changes = meta[META_KEY_CHANGES]
            self.current = _current
            self.changes = {
                _name : Change(self.path, name=_name, **_change)
                for _name, _change in _changes.items()
            }

    def save(self, filename:str|Path):
        _current = self.current
        _changes = {}
        for _name, _change in self.changes.items():
            _change = asdict(_change)
            _name = _change.pop("name", _name)
            _change.pop("path", None)
            _changes[_name] = _change
        with open(filename, "w") as fp:
            json.dump({
                META_KEY_CURRENT: _current,
                META_KEY_CHANGES: _changes,
            }, fp)

    @classmethod
    @contextmanager
    def ascontext(cls, filename:str|Path):
        _path = Path(filename).parent
        _meta = Meta(_path)
        _meta.load(filename)
        try:
            yield _meta
        finally:
            _meta.save(filename)

