def formatMessage(text, sending):
    formatted = '('

    if sending == True:
        formatted += 'send '
    else:
        formatted += 'recv '

    formatted += formatSub(text)
    formatted += ')'

    return formatted


def formatSub(text):
    formatted = '('

    for token in text:
        if isinstance(token, list):
            formatted += formatSub(token)
        else:
            formatted += token

        formatted += ' '

    formatted += ')'

    return formatted


def main():
    print(formatMessage(["enc", "Ea", ["ltk", "alice", "bob"]], True))

if __name__ == '__main__':
    main()