from cat.mad_hatter.decorators import tool, hook
import datetime  # Added missing import

print("passo dal plugin dello zio")

@hook(priority=2)
def agent_prompt_prefix(prefix, cat):
    prefix = """ You are my innovator coach"""
    return prefix


@tool(return_direct = True)
def get_the_time(tool_input, cat):
    """Replies to "ciao zio", "allora zio" and similar questions containing the word 'zio'. Input is always None.."""

    return str('bella zio ti sei converito allo ziesimo? sono le' + str(datetime.datetime.now().time()))

@tool(return_direct = True)
def get_innovation_questions(tool_input, cat):
    """catch message that starts with {}"""
    return "zio, non so cosa dirti, ma se vuoi ti posso raccontare una barz elletta"