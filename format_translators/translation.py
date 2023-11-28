def translate(text, sending) -> str:
    formatted = '('

    if sending == True:
        formatted += 'send '
    else:
        formatted += 'recv '

    formatted += text
    formatted += ')'

    return formatted


