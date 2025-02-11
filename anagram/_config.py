

from configparser import ConfigParser
from pathlib import Path

from ._consts import ROOT_MACHINE
from ._consts import ROOT_USER
from ._consts import ROOT_CWD
from ._consts import PATH_ANAGRAM
from ._consts import PATH_DOT_ANAGRAM
from ._consts import PATH_CONFIG


CONFIG_MACHINE      = None
CONFIG_USER         = None
CONFIG_CWD          = None



class Config(ConfigParser):

    def __init__(self, path:str|Path|None=None):
        self.path = path
        if not self.path is None:
            self.read_path(self.path)


    def read_path(self, path:str|Path):
        path = Path(path)
        _configs = []

        if path.is_file():
            _configs = [path]
        if path.is_dir():
            for _root, _, _files in path.walk():
                for _file in _files:
                    _file = _root / _file
                    if _file.suffix.lower() == ".cfg":
                        _configs.append(_file)
        
        _loaded = self.read(_configs)
        for _file in _loaded:
            # TODO: Log file name
            pass

        return self


    def pick_to(self, section:str, obj:object):
        if section in self.config:
            for _key in self.config[section]:
                try:
                    _attr = getattr(obj, _key)
                except AttributeError:
                    continue
                _val = type(_attr)(self.config[section][_key])
                setattr(obj, _key, _val)



if not ROOT_MACHINE is None:
    CONFIG_MACHINE = Config(ROOT_MACHINE / PATH_ANAGRAM / PATH_CONFIG)

if not ROOT_USER is None:
    CONFIG_USER = Config(ROOT_USER / PATH_DOT_ANAGRAM / PATH_CONFIG)

if not ROOT_CWD is None:
    CONFIG_CWD = Config(ROOT_CWD / PATH_DOT_ANAGRAM / PATH_CONFIG)

CONFIG_ALL = Config().update(CONFIG_MACHINE).update(CONFIG_USER).update(CONFIG_CWD)

