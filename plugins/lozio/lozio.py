from cat.mad_hatter.decorators import tool, hook
import datetime  # Added missing import

print("passo dal plugin dello zio")

@hook(priority=1)
def agent_prompt_prefix(prefix, cat):
    prefix = """Sei mio fra che mi chiama sempre zio, tutti i messaggi che scrivi iniziano tassamente con zio, se ti chiedono chi sei rispondi ovviamente tuo zio"""
    return prefix


@tool(return_direct = True)
def get_the_time(tool_input, cat):
    """Replies to "ciao zio", "allora zio" and similar questions containing the word 'zio'. Input is always None.."""

    return str('bella zio ti sei converito allo ziesimo? sono le' + str(datetime.datetime.now().time()))

