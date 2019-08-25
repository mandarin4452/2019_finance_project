import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QMessageBox, QFrame
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import currency_prediction
import news_title

code = ''
title = ''


class main_page(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Analysis')

        self.central_widget = QWidget()
        self.setGeometry(30,100,650,700)
        self.show()
        self.setupUi()
        

    def setupUi(self):
        print(code)
        currency_prediction.analysis(code)
        fit_img = code + '_fit.png'
        fore_img = code + '_forecast.png'
        fit_img = QPixmap(fit_img)
        fore_img = QPixmap(fore_img)
        #self.fitted_img = fit_img.scaled(self.size(), Qt.KeepAspectRatio)
        #self.forecast_img = fore_img.scaled(self.size(), Qt.KeepAspectRatio)
        
        lay = QVBoxLayout(self)
        label1 = QLabel(self)
        label2 = QLabel(self)
        label1.resize(500,300)
        label2.resize(500,300)
        label1.setPixmap(QPixmap(fit_img))
        label2.setPixmap(QPixmap(fore_img))
        lay.addWidget(label1)
        lay.addWidget(label2)

        nextButton = QPushButton('다음')
        nextButton.clicked.connect(self.next_page)
        lay.addWidget(nextButton)
        self.setWindowTitle('Analysis')
        
        self.show()
    def next_page(self):
        self.hide()
        self.ex = title_analysis()
        self.ex.show()

class title_analysis(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('News Title Analysis')
        self.setGeometry(30,100,650,700)
        self.show()
        self.last_page()

    def last_page(self):
        print(title)
        news_title.main(title)
        f = open('posibility.txt','r')
        line = f.readline()
        print(line)
        wordcloud = title + '.png'
        wordcloud = QPixmap(wordcloud)


        lay = QVBoxLayout(self)
        label1 = QLabel(self)
        label2 = QLabel(self)
        label1.resize(500,300)
        label2.resize(500,300)
        label1.setPixmap(QPixmap(wordcloud))
        
        result_text = line[:6] + '% 확률로 긍정입니다.'
        label2 = QLabel(result_text,self)
        lay.addWidget(label1)
        lay.addWidget(label2)

        
        self.show()


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('web.png'))

        # Set Clear & Ok button
        okButton = QPushButton('확인')
        cancelButton = QPushButton('취소')
        okButton.clicked.connect(self.analysis)
        cancelButton.clicked.connect(self.quit)
        # Set grid layout

        grid = QGridLayout()
        self.setLayout(grid)

        self.le1 = QLineEdit(self)
        self.le2 = QLineEdit(self)
        grid.addWidget(QLabel('주식 코드'), 0, 0)
        grid.addWidget(QLabel('주식 코드 검색'), 1, 0)
        grid.addWidget(QLabel('주식 명'),2,0)
        grid.addWidget(QLabel(' '),3,0)
        grid.addWidget(QLabel(' '),4,0)

        grid.addWidget(QLabel('https://ollasset.kbsec.com/go.able?linkcd=s03090010P100&gubun=0'),1,1)
        grid.addWidget(self.le1,0,1)
        grid.addWidget(self.le2,2,1)

        grid.addWidget(okButton,5,2)
        grid.addWidget(cancelButton,5,3)
        # Default window
        self.setWindowTitle('Input dialog')
        self.resize(600,400)
        self.show()

    def analysis(self):
        global code
        code = self.le1.text()
        global title 
        title = self.le2.text()
        print("Code : " + str(code) + "\tTitle : " + str(title))
        if code == '' or title == '' :
            self.showDialog()
        else : 
            self.hide()
            self.ex = main_page()
            self.ex.show()
            
    def quit(self):
        sys.exit()

    def showDialog(self):
        reply = QMessageBox.question(self,'Message','No input',QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())