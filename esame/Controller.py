import sys
from exif import Ui_ExifReader
from AboutExif import Ui_AboutExif
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QTableWidgetItem, QMainWindow, QAbstractItemView
from PyQt5.QtCore import Qt, QDir
from Model import M


class AboutDialog(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set up the user interface from Designer.
        self.ui = Ui_AboutExif()
        self.ui.setupUi(self)


class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self._aboutDialog = AboutDialog()
        self._model = M
        self.ui = Ui_ExifReader()
        self.ui.setupUi(self)
        self.ui.action_About.triggered.connect(self._aboutDialog.exec_)
        self.ui.action_Quit.triggered.connect(QApplication.exit)
        self.ui.actionLoad_Multiple_Images.triggered.connect(self.multi_load)  # inserire più immagini
        self.ui.label.installEventFilter(self)  # riscalamento
        self.ui.tableView.hide()
        self.ui.left_rotate.hide()
        self.ui.aprimappa.hide()
        self.ui.right_rotate.hide()
        self.ui.previousImgButton.hide()
        self.ui.nextImgButton.hide()
        self.ui.load.clicked.connect(lambda: self.load_click())
        self.ui.right_rotate.clicked.connect(lambda: self.setRotateRight())
        self.ui.left_rotate.clicked.connect(lambda: self.setRotateLeft())
        self.ui.previousImgButton.clicked.connect(lambda: self.previousImage())
        self.ui.nextImgButton.clicked.connect(lambda: self.nextImage())
        self.ui.left_rotate.setShortcut("L")
        self.ui.right_rotate.setShortcut("R")
        self.ui.previousImgButton.setShortcut(Qt.Key_Left)
        self.ui.nextImgButton.setShortcut(Qt.Key_Right)
        self.ui.aprimappa.clicked.connect(lambda: self._model.gotomap())
        self.setAcceptDrops(True)

    # ########funzioni per poter trascinare jpeg

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)  
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.lower().endswith(('.jpg', '.jpeg')):  # controlla che sia droppato un jpeg
                self._model.update_filepath(file_path)
                self.addImage(self._model.p)
                # #####togliere tasto per scorrere immagini e cancellare la lista
                self.ui.nextImgButton.hide()
                self.ui.previousImgButton.hide()
                self._model.list = []
            self.ui.label.setText('Inserire JPEG')
            event.accept()
        else:
            self.ui.label.setText('Inserire JPEG')
            event.ignore()

    def setRotateLeft(self):
        self._model.rotateLeft()
        self.addImage(self._model.p)

    def setRotateRight(self):
        self._model.rotateRight()
        self.addImage(self._model.p)

    # #############################scorrere immagini in caso di multiload
    def previousImage(self):
        self._model.previousImg()
        self.addImage(self._model.p)

    def nextImage(self):
        self._model.nextImg()
        self.addImage(self._model.p)

    def addImage(self, pixmap):
        self.ui.label.setScaledContents(False)  # mi setta i giusti parametri per visualizzare bene l'immagine
        if (pixmap.size().height() > 512) or (pixmap.size().width() > 512):
            pixmap = pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.ui.label.setPixmap(pixmap)

        initpixmapheight = pixmap.size().height()  # parametri per impostare dimensione minima dell'immagine
        initpixmapwidth = pixmap.size().width()
        self.ui.label.setMinimumSize(int(initpixmapwidth), int(initpixmapheight))

        self.ui.label.setStyleSheet('''QLabel{}''')  # mi toglie riquadratura (estetica)
        self.ui.label.setAlignment(Qt.AlignCenter)
        self.ui.left_rotate.setVisible(True)  # attiva tasti per ruotare immagine
        self.ui.right_rotate.setVisible(True)
        self.on_load()

    def on_load(self):
        tg, gpsfound = self._model.getExif(self._model.file_path)
        if gpsfound:
            self.ui.aprimappa.setVisible(True)  # tasto per andare su maps
        else:
            self.ui.aprimappa.setVisible(False)
        self.ui.tableView.setVisible(True)  # rende visibile gli exif
        self.ui.tableView.clear()
        self.ui.tableView.setRowCount(0)
        self.ui.tableView.setColumnCount(0)  # imposta i dati della tabella con gli ecif
        if len(tg) != 0:
            self.ui.tableView.setRowCount(len(tg))
            self.ui.tableView.setColumnCount(2)
            for i in range(len(tg)):
                self.ui.tableView.setItem(i, 0, QTableWidgetItem(str(tg[i][0])))
                self.ui.tableView.setItem(i, 1, QTableWidgetItem(str(tg[i][1])))
        else:
            self.ui.tableView.setRowCount(1)
            self.ui.tableView.setColumnCount(1)
            self.ui.tableView.setItem(0, 0, QTableWidgetItem('NESSUN EXIF TROVATO...'))
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)  # non far modificare la tabella

    def eventFilter(self, source, event):
        if self._model.isimage:  # se l'immagine è presente l'adatta alla dimensione della finestra
            if (self.ui.label.size().height() < 2000) and (
                    self.ui.label.size().width() < 2000):  # dimensione massima scelta
                pixmap = self._model.p.scaled(
                    self.ui.label.size().width(), self.ui.label.size().height(), Qt.KeepAspectRatio,
                    Qt.SmoothTransformation)  # riscalamento dell'immagine con le giuste dimensioni del suo contenitore
                self.ui.label.setPixmap(pixmap)
        return super(AppDemo, self).eventFilter(source, event)

    def load_click(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Single File', QDir.rootPath(), '*.jpg *.JPEG')
        if file_path:
            self._model.update_filepath(file_path)
            self.addImage(self._model.p)
            # ###############nasconde tasti inutili e cancella la lista
            self._model.list = []
            self.ui.nextImgButton.hide()
            self.ui.previousImgButton.hide()

    def multi_load(self):
        self._model.list, _ = QFileDialog.getOpenFileNames(self, 'Multiple File', QDir.rootPath(), '*.jpg *.JPEG')
        if self._model.list:
            self.ui.previousImgButton.setVisible(True)
            self.ui.nextImgButton.setVisible(True)
            self._model.update_filepath(self._model.list[self._model.count])
            self.addImage(self._model.p)


app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
