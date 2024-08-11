from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.Lablename = QtWidgets.QLabel(self.centralwidget)
        self.Lablename.setObjectName("Lablename")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Lablename)
        self.BooksName = QtWidgets.QComboBox(self.centralwidget)
        self.BooksName.setObjectName("BooksName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.BooksName)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_3.setLineWidth(5)
        self.label_3.setMidLineWidth(3)
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_3)
        self.Price = QtWidgets.QPushButton(self.centralwidget)
        self.Price.setObjectName("Price")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Price)
        self.verticalLayout.addLayout(self.formLayout)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setScaledContents(False)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setFrameShape(QtWidgets.QFrame.Box)
        self.label_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_6.setLineWidth(5)
        self.label_6.setMidLineWidth(3)
        self.label_6.setTextFormat(QtCore.Qt.RichText)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_6)
        self.Cost = QtWidgets.QPushButton(self.centralwidget)
        self.Cost.setObjectName("Cost")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Cost)
        self.verticalLayout.addLayout(self.formLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Populate ComboBox with book titles
        self.populate_books()

        # Connect button signals to respective slots
        self.Price.clicked.connect(self.Price_clicked)
        self.Cost.clicked.connect(self.Cost_clicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Lablename.setText(_translate("MainWindow", "Book Title"))
        self.label_2.setText(_translate("MainWindow", "Book Price"))
        self.label_3.setText(_translate("MainWindow", "0.0"))
        self.Price.setText(_translate("MainWindow", "Get Price"))
        self.label_4.setText(_translate("MainWindow", "Label Quantity"))
        self.label_5.setText(_translate("MainWindow", "Total Cost"))
        self.label_6.setText(_translate("MainWindow", "0.0"))
        self.Cost.setText(_translate("MainWindow", "Get Total Cost"))

    def populate_books(self):
        self.BooksName.addItem("---Select Book---")
        try:
            Books_file = sqlite3.connect('Books.db')
            cursor_books = Books_file.cursor()
            cursor_books.execute('SELECT Books_Name FROM Books;')
            record = cursor_books.fetchone()
            while record:
                self.BooksName.addItem(record[0])
                record = cursor_books.fetchone()
            Books_file.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def Price_clicked(self):
        book_title = self.BooksName.currentText()
        if book_title == "---Select Book---":
            self.label_3.setText("0.0")
            return
        try:
            Books_file = sqlite3.connect('Books.db')
            cursor_books = Books_file.cursor()
            cursor_books.execute('SELECT Books_Price FROM Books WHERE Books_Name = ?', (book_title,))
            record = cursor_books.fetchone()
            if record:
                book_price = record[0]
                self.label_3.setText(str(book_price))
            else:
                self.label_3.setText("0.0")
            Books_file.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def Cost_clicked(self):
        quantity_text = self.lineEdit.text()
        if not quantity_text.isdigit():
            self.label_6.setText("Invalid Quantity")
            return
        
        quantity = int(quantity_text)
        book_price_text = self.label_3.text()
        if book_price_text == "0.0":
            self.label_6.setText("0.0")
            return
        
        book_price = float(book_price_text)
        total_cost = quantity * book_price
        self.label_6.setText(str(total_cost))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
