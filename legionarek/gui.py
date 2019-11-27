from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from legionarek.constants import CANVAS_HEIGHT, CANVAS_WIDTH
from tqdm import tqdm


class CardsOnTable(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Legionářek")
        self.setLayout(QGridLayout(self))

    def populate(self, cards, size):
        self.size = size
        for i in tqdm(range(CANVAS_HEIGHT)):
            for j in tqdm(range(CANVAS_WIDTH)):
                label = CardOnTable(self, cards[i][j])
                pixmap = QPixmap(cards[i][j].config.visible_side)
                pixmap = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding)
                label.setPixmap(pixmap)
                self.layout().addWidget(label, i, j)


class CardOnTable(QLabel):
    def __init__(self, parent, card):
        self.parent = parent
        self.card = card
        super().__init__(parent)

    def enterEvent(self, event):
        self.p = CardPopup(self)
        self.p.show()
        event.accept()

    def flip(self):
        self.card.flip()
        pixmap = QPixmap(self.card.config.visible_side)
        pixmap = pixmap.scaled(self.parent.size, Qt.KeepAspectRatioByExpanding)
        self.setPixmap(pixmap)


class CardPopup(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._draw()

    def _draw(self):
        # set pixmap and size, which is the double of the original pixmap
        thumb = self.parent.pixmap()
        imageSize = thumb.size()
        imageSize.setWidth(imageSize.width()*2)
        imageSize.setHeight(imageSize.height()*2)
        self.setPixmap(thumb.scaled(imageSize, Qt.KeepAspectRatioByExpanding))

        # center the zoomed image on the thumb
        position = self.cursor().pos()
        position.setX(position.x() - thumb.size().width())
        position.setY(position.y() - thumb.size().height())
        self.move(position)

        # FramelessWindowHint may not work on some window managers on Linux
        # so I force also the flag X11BypassWindowManagerHint
        self.setWindowFlags(Qt.Popup | Qt.WindowStaysOnTopHint
                            | Qt.FramelessWindowHint
                            | Qt.X11BypassWindowManagerHint)

    def leaveEvent(self, event):
        """ When the mouse leave this widget, destroy it. """
        self.destroy()

    def mousePressEvent(self, event):
        if not self.parent.card.flipped:
            reply = QMessageBox.question(self, 'Do you want to flip a card ?', 'Do you want to flip a card ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.parent.flip()
                self._draw()
