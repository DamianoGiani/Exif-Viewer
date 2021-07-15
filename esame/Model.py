from PyQt5.QtGui import QPixmap, QTransform
import webbrowser
import exifread


class Exif_Model():

    def __init__(self):
        super().__init__()
        self.file_path = None  # Qstring
        self.mapurl = None  # urlmaps
        self.p = None  # Qpixmap(immagine)
        self.count = 0  # contatore che tiene in memoria quale immagine della lista stiamo visionando
        self.list = []  # per la funzione di poter caricare più immagini
        self.isimage = False

    # ###########################################################get exif
    def getExif(self, file_path):
        f = open(file_path, 'rb')
        tags = exifread.process_file(f)
        tg = []
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                tg.append((str(tag), str(tags[tag])))  # ##il primo dice cose è il secondo rende il valore
        gpsfound = self.getGPS(tags)
        return tg, gpsfound

        # ######################################## imposta l'immagine

    def update_filepath(self, file_path):
        self.file_path = file_path
        self.update_image()

    # ##################################Scorre le immagini
    def nextImg(self):
        if self.count < len(self.list) - 1:
            self.count = self.count + 1
            self.update_filepath(self.list[self.count])

        else:
            self.count = 0
            self.update_filepath(self.list[self.count])

    def previousImg(self):
        if self.count != 0:
            self.count = self.count - 1
            self.update_filepath(self.list[self.count])

        else:
            self.count = len(self.list) - 1
            self.update_filepath(self.list[self.count])

    def update_image(self):
        self.p = QPixmap(self.file_path)
        self.isimage = True
        return self.p

    # ##########################################################rotazione a sinistra
    def rotateLeft(self):
        if self.p != 0:
            self.p = self.p.transformed(QTransform().rotate(-90))

    # #########################################rotazione immagine a destra
    def rotateRight(self):
        if self.p != 0:
            self.p = self.p.transformed(QTransform().rotate(90))

    # #######################################genera link GPS

    def getGPS(self, tags):
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')

        if latitude:
            lat_value = self._convert_to_degress(latitude)
            if latitude_ref.values != 'N':
                lat_value = -lat_value
        else:
            return False
        if longitude:
            lon_value = self._convert_to_degress(longitude)
            if longitude_ref.values != 'E':
                lon_value = -lon_value
        else:
            return False
        totvalue = [str(lat_value), str(lon_value)]
        s = ','.join(totvalue)
        url = 'https://www.google.com/maps/search/?api=1&query={s}'.format(s=s)
        self.mapurl = url
        return True

    # ###conversione in gradi#########

    def _convert_to_degress(self, value):

        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)

        return d + (m / 60.0) + (s / 3600.0)

    # ########apre pagina web
    def gotomap(self):
        webbrowser.open(self.mapurl)


M = Exif_Model()
