from legionarek.parser import Parser


if __name__ == '__main__':
    parser = Parser()
    parser.parse()
    for card in parser.cards:
        print(card)
    parser.cards[10].flip()
