from cat.mad_hatter.decorators import tool, hook


@hook(priority=2)
def agent_prompt_prefix(prefix, cat):
    prefix = """Sei mio fra che mi chiama sempre zio, tutti i messaggi che scrivi iniziano tassamente con zio """



@tool
def get_the_time(tool_input, cat):
        """Replies to "what time is it", "get the clock" and similar questions. Input is always None.."""

    # """Replies to "ciao zio", "allora zio" and similar questions containing the word 'zio'. Input is always None.."""

    return str('bella zio ti sei converito allo ziesimo? sono le' + str(datetime.datetime.now().time()))

