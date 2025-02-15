

from dataclasses import dataclass

import click
from click import Group

from ._anagram import Anagram
from .change import Change
from .change import Message

from ._consts import CMD_MAN_BRANCH
from ._consts import CMD_MAN_WORKTREE



def print_change(change:Change):
    print(change.name)
    print(f"Branch : {change.branch}")
    print(f"Upstream : {change.upstream}")
    print(f"Worktree : {change.worktree}")


def print_message(message:Message):
    print("=" * 10)
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
        pass


    @cli.command()
    def list():
        _changes = anagram.list_changes()
        print(_changes)


    @cli.command()
    @click.argument("name",             type=str, default=None)
    def status(name):
        if name is None:
            _change = anagram.get_current_change()
        else:
            _change = anagram.get_change(name)
        
        if _change is None:
            # TODO: Implement error handling
            return
        
        print_change(_change)


    @cli.command()
    @click.argument("name",             type=str)
    def checkout(name):
        _change = anagram.checkout_change(
            name            =name
        )
        if _change is None:
            # TODO: Implement error handling
            return
        
        print_change(_change)


    @cli.command()
    @click.argument("name",             type=str)
    @click.option("--upstream", "-u",   type=str, default=None)
    @click.option("--base", "-b",       type=str, default=None)
    def add(name, upstream, base):
        _change = anagram.add_change(
            name            = name, 
            upstream        = upstream,
            base            = base
        )

        if _change is None:
            # TODO: Implement error handling
            return
        
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
            name            = name,
            remove_worktree = not remove_worktree,
            remove_branch   = not remove_branch,
            force           = force
        )
        if _change is None:
            # TODO: Implement error handling
            return
        
        print_change(_change)


    @cli.command()
    @click.argument("name",             type=str)
    @click.argument("field",            type=str)
    @click.argument("value",            type=str)
    def modify(name, field, value):
        _change = anagram.modify_change(name, field, value)
        if _change is None:
            # TODO: Implement error handling
            return
        
        print_change(_change)


    @cli.command()
    @click.argument("name",             type=str)
    def chat_log(name):
        _change = anagram.get_change(name)
        if _change is None:
            # TODO: Implement error handling
            return
        
        _chat = _change.get_chat()
        _, _messages = _chat.get_files_messages()
        for _message in _messages:
            print_message(_message)


    @cli.command()
    @click.argument("name",             type=str)
    def chat(name):
        _change = anagram.get_change(name)
        if _change is None:
            # TODO: Implement error handling
            return
        
        print_change(_change)


    return cli

