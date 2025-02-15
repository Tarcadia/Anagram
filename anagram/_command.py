

import logging
from ._logging import logging_set

from dataclasses import dataclass

import click
from click import Group

from ._anagram import Anagram
from .change import Change
from .change import Message

from ._consts import CMD_MAN_BRANCH
from ._consts import CMD_MAN_WORKTREE



def print_change(change:Change):
    print(f"Branch : {change.branch}")
    print(f"Upstream : {change.upstream}")
    print(f"Worktree : {change.worktree}")


def print_message(message:Message):
    _title = message.commit.author.name
    if message.commit.author.email:
        _title += f" <{message.commit.author.email}>"
    print(f"{_title}:")
    print(message.content)


@dataclass
class _Config:
    manage_branch:bool = CMD_MAN_BRANCH
    manage_worktree:bool = CMD_MAN_WORKTREE


def Command(anagram:Anagram) -> Group:

    _config = _Config()
    if not anagram.config is None:
        anagram.config.pick_to("command", _config)


    @click.group()
    @click.option("--verbose", "-v",    count=True, default=0)
    def cli(verbose:int):
        _logging_level = logging.WARNING-10*verbose
        logging_set(console_level=max(0, _logging_level))
        pass


    @cli.command()
    def list():
        _changes = anagram.list_changes()
        logging.debug(_changes)

        print("List of changes:")
        print("=" * 10)
        for _name in _changes:
            print(_name)


    @cli.command()
    @click.argument("name",             type=str, required=False, default=None)
    def status(name):
        _change = anagram.get_change(name) or anagram.get_current_change()
        logging.debug(_change)

        if _change is None:
            logging.error(f"Change {name} not found.")
            return

        print(f"Status of change {name}:")
        logging.info(f"Status of change {name}: ...")
        print("=" * 10)
        print_change(_change)


    @cli.command()
    @click.argument("name",             type=str)
    def checkout(name):
        _change = anagram.checkout_change(name)
        logging.debug(_change)

        if _change is None:
            logging.error(f"Checking out change {name} failed.")
            return

        print(f"Checked out change {name}:")
        logging.info(f"Checked out change {name}: ...")
        print("=" * 10)
        print_change(_change)


    @cli.command()
    @click.argument("name",             type=str)
    @click.option("--upstream", "-u",   type=str, default=None)
    @click.option("--base", "-b",       type=str, default=None)
    def add(name, upstream, base):
        _change = anagram.add_change(
            name,
            upstream        = upstream,
            base            = base
        )
        logging.debug(_change)

        if _change is None:
            logging.error(f"Adding change {name} failed.")
            return

        print(f"Added change {name}:")
        logging.info(f"Added change {name}: ...")
        print("=" * 10)
        print_change(_change)


    @cli.command()
    @click.argument("name",             type=str)
    @click.option("--remove-worktree/--keep-worktree", "-rw/-kw",
                                        is_flag=True, default=_config.manage_branch)
    @click.option("--remove-branch/--keep-branch", "-rb/-kb",
                                        is_flag=True, default=_config.manage_worktree)
    @click.option("--force", "-F",      is_flag=True, default=False)
    def remove(name, remove_worktree, remove_branch, force):
        _change = anagram.remove_change(
            name,
            remove_worktree = not remove_worktree,
            remove_branch   = not remove_branch,
            force           = force
        )
        logging.debug(_change)

        if _change is None:
            logging.error(f"Removing change {name} failed.")
            return

        print(f"Removed change {name}:")
        logging.info(f"Removed change {name}: ...")
        print("=" * 10)
        print_change(_change)


    @cli.command()
    @click.argument("name",             type=str)
    @click.argument("field",            type=str)
    @click.argument("value",            type=str)
    def modify(name, field, value):
        _change = anagram.modify_change(name, field, value)
        logging.debug(_change)

        if _change is None:
            logging.error(f"Modifying change {name} failed.")
            return

        print(f"Modified change {name}:")
        logging.info(f"Modified change {name}: ...")
        print("=" * 10)
        print_change(_change)


    @cli.command()
    @click.argument("name",             type=str)
    def chat_log(name):
        _change = anagram.get_change(name) or anagram.get_current_change()
        logging.debug(_change)

        if _change is None:
            logging.error(f"Change {name} not found.")
            return
        
        _chat = _change.get_chat()
        _, _messages = _chat.get_files_messages()
        print(f"Log of change {name}:")
        logging.info(f"Log of change {name}: ...")
        print("=" * 10)
        for _message in _messages:
            print_message(_message)
            print("=" * 10)


    @cli.command()
    @click.argument("name",             type=str, required=False, default=None)
    @click.argument("message",          type=str)
    def chat_message(name, message):
        _change = anagram.get_change(name) or anagram.get_current_change()
        logging.debug(_change)

        if _change is None:
            logging.error(f"Change {name} not found.")
            return

        _chat = _change.get_chat()
        _chat.add_message(message)
        _, _messages = _chat.get_files_messages()
        print(f"Messaged to change {name}:")
        logging.info(f"Messaged to change {name}: ...")
        print("=" * 10)
        print_message(_messages[-1])
        print("=" * 10)


    @cli.command()
    @click.argument("name",             type=str, required=False, default=None)
    def chat_complete(name, message):
        _change = anagram.get_change(name) or anagram.get_current_change()
        logging.debug(_change)

        if _change is None:
            logging.error(f"Change {name} not found.")
            return

        _chat = _change.get_chat()
        _chat.add_message(message)
        _llm = anagram.get_llm(name)
        _, _messages = _chat.get_files_messages()
        print(f"Completed to change {name}:")
        logging.info(f"Completed to change {name}: ...")
        print("=" * 10)
        print_message(_messages[-1])
        print("=" * 10)


    return cli

