
def print_headline(text, symbol='-'):
    assert len(symbol) == 1
    underline = symbol * len(text)
    print('\n' + text + '\n' + underline)

