

import click
from click import Group

from git import Repo

from ._anagram import Anagram
from .change import Change
from .change import Message


OP_MANAGE_BRANCH    = True



def print_change(change:Change):
    print(change)


def print_message(message:Message):
    print("=" * 10)
    if message.by_anagram:
        # TODO: Use Anagram::git_author_name field for configuring
        print("Anagram:")
    else:
        print("User:")
    print(message.content)


def Command(anagram:Anagram) -> Group:

    _op_manage_branch = OP_MANAGE_BRANCH

    if not anagram.config is None:
        # TODO: Implement applying values read by Config.
        pass


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
    @click.option("--keep-branch/--!keep-branch", "-kb/-!kb",
                                        is_flag=True, default=not _op_manage_branch)
    @click.option("--force", "-F",      is_flag=True, default=False)
    def remove(name, keep_branch, force):
        _change = anagram.remove_change(
            name            = name,
            remove_branch   = not keep_branch,
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

