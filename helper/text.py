
def print_headline(text, symbol='-'):
    assert len(symbol) == 1
    underline = symbol * len(text)
    print(text + '\n' + underline)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
