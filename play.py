from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSize, QCoreApplication
from legionarek.parser import Parser
from legionarek.canvas import Canvas
from legionarek.constants import CANVAS_HEIGHT, CANVAS_WIDTH
from legionarek.gui import CardsOnTable

if __name__ == '__main__':
    parser = Parser()
    parser.parse()
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, parser.cards)
    rendered_cards = canvas.render()
    app = QApplication([])
    card_gallery = CardsOnTable()
    card_gallery.populate(rendered_cards, QSize(50, 50))

    card_gallery.show()
    app.exec()
