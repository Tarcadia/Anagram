

from dataclasses import dataclass

from ._llm import Llm
from .openai import OpenAiLlm

from ..change import Chat

from .._config import Config



def get_llm(chat:Chat, config:Config):
    return

