from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from legionarek.constants import CANVAS_HEIGHT, CANVAS_WIDTH
from tqdm import tqdm

class ImageGallery(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Legionářek")
        self.setLayout(QGridLayout(self))

    def populate(self, cards, size):
        self.size = size
        self.cards = cards
        for i in tqdm(range(CANVAS_HEIGHT)):
            for j in tqdm(range(CANVAS_WIDTH)):
                label = ImageLabel(self)
                pixmap = QPixmap(cards[i][j].config.visible_side)
                pixmap = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding)
                label.setPixmap(pixmap)
                self.layout().addWidget(label, i, j)

    def reload(self, i, j):
        print('flipping:', i, j)
        try:
            self.cards[i][j].flip()
        except IndexError:
            print('Tried to flip card out of range')
            return
        pixmap = QPixmap(self.cards[i][j].config.visible_side)
        pixmap = pixmap.scaled(self.size, Qt.KeepAspectRatioByExpanding)
        label = ImageLabel(self)
        label.setPixmap(pixmap)
        self.layout().addWidget(label, i, j)


class ImageLabel(QLabel):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)

    def enterEvent(self, event):
        self.p = ImagePopup(self)
        self.p.show()
        event.accept()


class ImagePopup(QLabel):
    """
    The ImagePopup class is a QLabel that displays a popup, zoomed image
    on top of another label.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # set pixmap and size, which is the double of the original pixmap
        thumb = parent.pixmap()
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
        thumb = self.parent.pixmap()
        image_size = thumb.size()
        position = self.cursor().pos()
        #TOOD: better calculation
        self.parent.parent.reload(position.y() // image_size.height() - 1, position.x() // image_size.width() - 1)
