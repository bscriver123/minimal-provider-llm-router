from enum import Enum


class ModelName(str, Enum):
    gpt_4o = "gpt-4o"
    claude_sonnet_3 = "claude-sonnet-3"
    claude_sonnet_3_5 = "claude-sonnet-3-5"
