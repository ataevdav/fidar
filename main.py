#импортируем модули шифров
import caesar
import polybius
import vigenere
import ataty

#импортируем PyQT
from PyQt6 import uic  #uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QDialog, QLabel, QTextBrowser, QMessageBox #виджеты
from PyQt6.QtGui import QPixmap, QIntValidator, QIcon, QTextDocument #элементы пользовательского интерфейса
from PyQt6.QtCore import Qt, QRect, QUrl #ядро модуля

#importing other modules
import sys

#обработка ошибок
def error(err_code):
    errs = {
        -1001: 'Неизвестная ошибка : неизвестная ошибка',
        -2001: 'Ошибки работы с шифром Цезаря: некорректный ключ',
        -3001: 'Ошибки работы с квадратом Полибия: дублирующиеся символы алфавита',
        -3002: 'Ошибки работы с квадратом Полибия: превышение допустимой длины алфавита',
        -3003: 'Ошибки работы с квадратом Полибия: символ открытого текста отсутствует в алфавите',
        -3004: 'Ошибки работы с квадратом Полибия: акодированный символ отсутсвует в таблице шифра',
        -4001: 'Ошибки работы с шифром Виженера: неккоректный ключ',
        -5001: 'Ошибки работы с шифром Дзивгис: не указан файл ключа'
        }

    if err_code:
        ErrDialog = QMessageBox()
        ErrDialog.setIcon(QMessageBox.Icon.Warning)
        err_text = f'Код ошибки: {err_code}\n{errs[err_code]}'
        ErrDialog.setText(err_text)
        ErrDialog.setWindowTitle('Ошибка | FIDAR')
        err_close_PB = QPushButton()
        err_help_PB = QPushButton()
        err_close_PB.setText('Закрыть')
        err_help_PB.setText('Справка')
        ErrDialog.addButton(err_close_PB, QMessageBox.ButtonRole.AcceptRole)
        ErrDialog.addButton(err_help_PB, QMessageBox.ButtonRole.HelpRole)
        err_help_PB.clicked.connect(MainWidget.help_)
        ErrDialog.exec()


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        #подключение файла графического интерфейса
        uic.loadUi('fidar.ui', self)
        #загрузка изображения логотипа на главной вкладке
        pixmap = QPixmap('images/logo.jpg')
        self.ST_logo_Lb.setPixmap(pixmap)
        #установка иконки приложения
        self.setWindowIcon(QIcon('images/icon.ico'))
        
        #массив кнопок квадрата Полибия
        self.PS_GRID = [[self.PS_grid_11_PB, self.PS_grid_12_PB, self.PS_grid_13_PB, self.PS_grid_14_PB,
            self.PS_grid_15_PB, self.PS_grid_16_PB, self.PS_grid_17_PB], 
            [self.PS_grid_21_PB, self.PS_grid_22_PB, self.PS_grid_23_PB,  self.PS_grid_24_PB,
            self.PS_grid_25_PB, self.PS_grid_26_PB, self.PS_grid_27_PB],
            [self.PS_grid_31_PB, self.PS_grid_32_PB, self.PS_grid_33_PB, self.PS_grid_34_PB,
            self.PS_grid_35_PB, self.PS_grid_36_PB, self.PS_grid_37_PB],
            [self.PS_grid_41_PB, self.PS_grid_42_PB, self.PS_grid_43_PB, self.PS_grid_44_PB, 
            self.PS_grid_45_PB, self.PS_grid_46_PB, self.PS_grid_47_PB], 
            [self.PS_grid_51_PB, self.PS_grid_52_PB, self.PS_grid_53_PB, self.PS_grid_54_PB,
            self.PS_grid_55_PB, self.PS_grid_56_PB, self.PS_grid_57_PB],
            [self.PS_grid_61_PB, self.PS_grid_62_PB, self.PS_grid_63_PB, self.PS_grid_64_PB,
            self.PS_grid_65_PB, self.PS_grid_66_PB, self.PS_grid_67_PB],
            [self.PS_grid_71_PB, self.PS_grid_72_PB, self.PS_grid_73_PB, self.PS_grid_74_PB,
            self.PS_grid_75_PB, self.PS_grid_76_PB, self.PS_grid_77_PB]]
        
        #валидация ввода целочисленного ключа шифра Цезаря
        self.CC_key_LE.setValidator(QIntValidator(-2147483648, 2147483647, self))
 
        #обработка кнопок квадрата Полибия
        self.PS_GRID[0][0].clicked.connect(lambda: self.PS_grid_clicked(0, 0))
        self.PS_GRID[0][1].clicked.connect(lambda: self.PS_grid_clicked(0, 1))
        self.PS_GRID[0][2].clicked.connect(lambda: self.PS_grid_clicked(0, 2))
        self.PS_GRID[0][3].clicked.connect(lambda: self.PS_grid_clicked(0, 3))
        self.PS_GRID[0][4].clicked.connect(lambda: self.PS_grid_clicked(0, 4))
        self.PS_GRID[0][5].clicked.connect(lambda: self.PS_grid_clicked(0, 5))
        self.PS_GRID[0][6].clicked.connect(lambda: self.PS_grid_clicked(0, 6))
        self.PS_GRID[1][0].clicked.connect(lambda: self.PS_grid_clicked(1, 0))
        self.PS_GRID[1][1].clicked.connect(lambda: self.PS_grid_clicked(1, 1))
        self.PS_GRID[1][2].clicked.connect(lambda: self.PS_grid_clicked(1, 2))
        self.PS_GRID[1][3].clicked.connect(lambda: self.PS_grid_clicked(1, 3))
        self.PS_GRID[1][4].clicked.connect(lambda: self.PS_grid_clicked(1, 4))
        self.PS_GRID[1][5].clicked.connect(lambda: self.PS_grid_clicked(1, 5))
        self.PS_GRID[1][6].clicked.connect(lambda: self.PS_grid_clicked(1, 6))
        self.PS_GRID[2][0].clicked.connect(lambda: self.PS_grid_clicked(2, 0))
        self.PS_GRID[2][1].clicked.connect(lambda: self.PS_grid_clicked(2, 1))
        self.PS_GRID[2][2].clicked.connect(lambda: self.PS_grid_clicked(2, 2))
        self.PS_GRID[2][3].clicked.connect(lambda: self.PS_grid_clicked(2, 3))
        self.PS_GRID[2][4].clicked.connect(lambda: self.PS_grid_clicked(2, 4))
        self.PS_GRID[2][5].clicked.connect(lambda: self.PS_grid_clicked(2, 5))
        self.PS_GRID[2][6].clicked.connect(lambda: self.PS_grid_clicked(2, 6))
        self.PS_GRID[3][0].clicked.connect(lambda: self.PS_grid_clicked(3, 0))
        self.PS_GRID[3][1].clicked.connect(lambda: self.PS_grid_clicked(3, 1))
        self.PS_GRID[3][2].clicked.connect(lambda: self.PS_grid_clicked(3, 2))
        self.PS_GRID[3][3].clicked.connect(lambda: self.PS_grid_clicked(3, 3))
        self.PS_GRID[3][4].clicked.connect(lambda: self.PS_grid_clicked(3, 4))
        self.PS_GRID[3][5].clicked.connect(lambda: self.PS_grid_clicked(3, 5))
        self.PS_GRID[3][6].clicked.connect(lambda: self.PS_grid_clicked(3, 6))
        self.PS_GRID[4][0].clicked.connect(lambda: self.PS_grid_clicked(4, 0))
        self.PS_GRID[4][1].clicked.connect(lambda: self.PS_grid_clicked(4, 1))
        self.PS_GRID[4][2].clicked.connect(lambda: self.PS_grid_clicked(4, 2))
        self.PS_GRID[4][3].clicked.connect(lambda: self.PS_grid_clicked(4, 3))
        self.PS_GRID[4][4].clicked.connect(lambda: self.PS_grid_clicked(4, 4))
        self.PS_GRID[4][5].clicked.connect(lambda: self.PS_grid_clicked(4, 5))
        self.PS_GRID[4][6].clicked.connect(lambda: self.PS_grid_clicked(4, 6))
        self.PS_GRID[5][0].clicked.connect(lambda: self.PS_grid_clicked(5, 0))
        self.PS_GRID[5][1].clicked.connect(lambda: self.PS_grid_clicked(5, 1))
        self.PS_GRID[5][2].clicked.connect(lambda: self.PS_grid_clicked(5, 2))
        self.PS_GRID[5][3].clicked.connect(lambda: self.PS_grid_clicked(5, 3))
        self.PS_GRID[5][4].clicked.connect(lambda: self.PS_grid_clicked(5, 4))
        self.PS_GRID[5][5].clicked.connect(lambda: self.PS_grid_clicked(5, 5))
        self.PS_GRID[5][6].clicked.connect(lambda: self.PS_grid_clicked(5, 6))
        self.PS_GRID[6][0].clicked.connect(lambda: self.PS_grid_clicked(6, 0))
        self.PS_GRID[6][1].clicked.connect(lambda: self.PS_grid_clicked(6, 1))
        self.PS_GRID[6][2].clicked.connect(lambda: self.PS_grid_clicked(6, 2))
        self.PS_GRID[6][3].clicked.connect(lambda: self.PS_grid_clicked(6, 3))
        self.PS_GRID[6][4].clicked.connect(lambda: self.PS_grid_clicked(6, 4))
        self.PS_GRID[6][5].clicked.connect(lambda: self.PS_grid_clicked(6, 5))
        self.PS_GRID[6][6].clicked.connect(lambda: self.PS_grid_clicked(6, 6))

        #файл ключа изображения шифра Дзивгис
        self.AC_file_name = ''

        #обработка нажатий на кнопки
        self.CC_encode_PB.clicked.connect(self.CC_encode)
        self.CC_decode_PB.clicked.connect(self.CC_decode)
        self.PS_encode_PB.clicked.connect(self.PS_encode)
        self.PS_decode_PB.clicked.connect(self.PS_decode)
        self.VC_encode_PB.clicked.connect(self.VC_encode)
        self.VC_decode_PB.clicked.connect(self.VC_decode)
        self.VC_tabula_recta_PB.clicked.connect(self.VC_tabula_recta)
        self.AC_encode_PB.clicked.connect(self.AC_encode)
        self.AC_decode_PB.clicked.connect(self.AC_decode)
        self.AC_file_PB.clicked.connect(self.AC_file)
        self.ST_ciphers_PB.clicked.connect(self.ciphers)
        self.ST_help_PB.clicked.connect(self.help_)
        self.ST_info_PB.clicked.connect(self.about)

        self.PS_alphabet_LE.textChanged.connect(self.PS_alphabet_upper)
        self.PS_alphabet_LE.editingFinished.connect(self.PS_set_button_grid)


    #шифровка шифром Цезаря
    def CC_encode(self):
        try:
            in_text = self.CC_plaintext_TE.toPlainText().upper()
            key = ''.join(self.CC_key_LE.text().split())
            out_text = caesar.encrypt(in_text, int(key))
            self.CC_plaintext_TE.setPlainText(in_text)
            self.CC_ciphertext_TE.setPlainText(out_text)
        except ValueError:
            error(-2001)
        except Exception:
            error(-1001)


    #дешифровка шифра Цезаря
    def CC_decode(self):
        try:
            in_text = self.CC_ciphertext_TE.toPlainText().upper()
            key = ''.join(self.CC_key_LE.text().split())
            out_text = caesar.decrypt(in_text, int(key))
            self.CC_ciphertext_TE.setPlainText(in_text)
            self.CC_plaintext_TE.setPlainText(out_text)
        except ValueError:
            error(-2001)
        except Exception:
            error(-1001)


    #ввод текста для шифровки квадратом Полибия заглавными буквами
    def PS_alphabet_upper(self):
        al = self.PS_alphabet_LE.text().upper()
        self.PS_alphabet_LE.setText(al)


    #заполнение кнопок квадрата Полибия
    def PS_set_button_grid(self):
        al = self.PS_alphabet_LE.text()
        if len(list(al)) != len(set(list(al))):
            error(-3001)
        elif len(list(al)) > 49:
            error(-3002)
        else:
            lal = polybius.create_table(al)
            a = len(lal)
            for x in range(7):
                for y in range(7):
                    if x >= a or y >= a:
                        self.PS_GRID[x][y].setText('')
                        self.PS_GRID[x][y].setEnabled(False)
                    elif lal[x][y] == '':
                        self.PS_GRID[x][y].setText('')
                        self.PS_GRID[x][y].setEnabled(False)
                    else:
                        self.PS_GRID[x][y].setText(lal[x][y])
                        self.PS_GRID[x][y].setEnabled(True)


    #ввод символа текста для шифровки квадратом Полибия с кнопок
    def PS_grid_clicked(self, x, y):
        ntext = self.PS_plaintext_TE.toPlainText() + self.PS_GRID[x][y].text()
        self.PS_plaintext_TE.setText(ntext)
        self.PS_encode()


    #шифрока квадратом Полибия
    def PS_encode(self):
        try:
            in_text = self.PS_plaintext_TE.toPlainText().upper()
            al = self.PS_alphabet_LE.text()
            if len(list(al)) != len(set(list(al))):
                error(-3001)
            elif polybius.in_validation(in_text, self.PS_alphabet_LE.text().upper()):
                out_text = polybius.encrypt(in_text, self.PS_alphabet_LE.text())
                self.PS_plaintext_TE.setPlainText(in_text)
                self.PS_ciphertext_TE.setPlainText(out_text)
            else:
                error(-3003)
        except Exception:
            error(-1001)


    #дешифровка квадрата Полибия
    def PS_decode(self):
        try:
            in_text = self.PS_ciphertext_TE.toPlainText().upper()
            al = self.PS_alphabet_LE.text()
            if len(list(al)) != len(set(list(al))):
                error(-3001)
            if polybius.out_validation(in_text, self.PS_alphabet_LE.text()):
                out_text = polybius.decrypt(in_text, self.PS_alphabet_LE.text().upper())
                self.PS_ciphertext_TE.setPlainText(in_text)
                self.PS_plaintext_TE.setPlainText(out_text)
            else:
                error(-3004)
        except Exception:
            error(-1001)


    #шифровка шифром Виженера
    def VC_encode(self):
        try:
            in_text = self.VC_plaintext_TE.toPlainText().upper()
            key = ''.join(self.VC_key_LE.text().split()).upper()
            if vigenere.key_validation(key):
                out_text = vigenere.encrypt(in_text, key)
                self.VC_plaintext_TE.setPlainText(in_text)
                self.VC_ciphertext_TE.setPlainText(out_text)
                self.VC_key_LE.setText(key)
            else:
                error(-4001)
        except Exception:
            error(-1001)


    #дешифровка шифра Виженера
    def VC_decode(self):
        try:
            in_text = self.VC_ciphertext_TE.toPlainText().upper()
            key = ''.join(self.VC_key_LE.text().split()).upper()
            if vigenere.key_validation(key):
                out_text = vigenere.decrypt(in_text, key)
                self.VC_ciphertext_TE.setPlainText(in_text)
                self.VC_plaintext_TE.setPlainText(out_text)
                self.VC_key_LE.setText(key)
            else:
                error(-4001)
        except Exception:
            error(-1001)


    #отображение tabula recta в диалоговом окне
    def VC_tabula_recta(self):
        tab_recta_window = QDialog()
        tab_recta_window.setFixedSize(640, 640)
        tab_recta_window.setWindowTitle('Tabula recta | FIDAR')
        tab_recta_window.setWindowIcon(QIcon('images/icon.ico'))
        tab_recta_window.tr_Lb = QLabel(tab_recta_window)
        tab_recta_window.tr_Lb.setObjectName(u"tr_Lb")
        tab_recta_window.tr_Lb.setGeometry(QRect(0, 0, 640, 640))
        tb = QPixmap('images/tabula_recta.jpg').scaledToHeight(640)
        tab_recta_window.tr_Lb.setPixmap(tb)
        tab_recta_window.exec()


    #шифровка шифром Дзивгис
    def AC_encode(self):
        try:
            if self.AC_file_name != '':
                in_text = self.AC_plaintext_TE.toPlainText()
                out_file = QFileDialog.getSaveFileName(self,
                    "Save Cipher Image", "", "Image Files (*.bmp)")[0]
                cipher_img, de_key = ataty.encrypt(in_text, self.AC_file_name, out_file)
                self.AC_dekey_TE.setPlainText(de_key)
            else:
                error(-5001)
        except Exception:
            error(-1001)


    #шифровка шифром Дзивгис
    def AC_decode(self):
        try:
            if self.AC_file_name != '':
                de_key = self.AC_dekey_TE.toPlainText()
                in_file = QFileDialog.getOpenFileName(self,
                    "Open Cipher Image", "", "Image Files (*.bmp)")[0]
                out_text = ataty.decrypt(in_file, self.AC_file_name, de_key)
                self.AC_plaintext_TE.setPlainText(out_text)
            else:
                error(-5001)
        except Exception:
            error(-1001)


    #выбор файла изображения ключа шифра Дзивгис
    def AC_file(self):
        self.AC_file_name = QFileDialog.getOpenFileName(self,
            "Open Key Image", "", "Image Files (*.bmp)")[0]
        self.AC_key_im_LE.setText(self.AC_file_name.split("/")[-1])


    #окно информации о шифрах
    def ciphers(self):
        ciphers_window = QDialog()
        ciphers_window.setFixedSize(400, 500)
        ciphers_window.setWindowTitle('Шифры | FIDAR')
        ciphers_window.setWindowIcon(QIcon('images/icon.ico'))
        ciphers_window.ciphers_TB = QTextBrowser(ciphers_window)
        ciphers_window.ciphers_TB.resize(400, 500)
        ciphers_window.ciphers_TB.setSource(QUrl('ciphersRU.html'), QTextDocument.ResourceType.HtmlResource)
        ciphers_window.exec()


    #окно справки
    def help_(self):
        help_window = QDialog()
        help_window.setFixedSize(400, 500)
        help_window.setWindowTitle('Справка | FIDAR')
        help_window.setWindowIcon(QIcon('images/icon.ico'))
        help_window.ciphers_TB = QTextBrowser(help_window)
        help_window.ciphers_TB.resize(400, 500)
        help_window.ciphers_TB.setSource(QUrl('helpRU.html'), QTextDocument.ResourceType.HtmlResource)
        help_window.exec()


    #окно информации о программе
    def about(self):
        about_window = QDialog()
        uic.loadUi('about.ui', about_window)
        about_window.setWindowTitle('О программе | FIDAR')
        about_window.setWindowIcon(QIcon('images/icon.ico'))
        pixmap = QPixmap('images/logo.jpg')
        about_window.label.setPixmap(pixmap)
        about_window.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()       
    ex.show()
    sys.exit(app.exec())