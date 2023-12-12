def translateMessage(text, sending) -> str:
    formatted = '('

    if sending == True:
        formatted += 'send ('
    else:
        formatted += 'recv ('

    formatted += text + ')'
    formatted += ')'

    return formatted


def createTrace(messages) -> str:
    formatted_trace = '(trace\n\t'
    for m in messages:
        formatted_trace += m
        formatted_trace += '\n\t'
    formatted_trace += ')\n'
    return formatted_trace


def buildProtocol(name, algebra, roles) -> str:
    return


def createHerald(title, algebra) -> str:

    al = 'basic' if algebra.get() == 1 else 'diffie-hellman'
    herald = '(herald' + f""" "{title.get()}" (algebra """ + al + '))'

    return herald