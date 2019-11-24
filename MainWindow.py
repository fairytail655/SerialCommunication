# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtSerialPort import QSerialPort
from Ui_MainWindow import Ui_MainWindow
from SerialPort import SerialPort
from MyCombox import MyCombox
from ThreadObject import *
import StringProcess
import datetime

class MainWindow(QMainWindow, Ui_MainWindow):
    serial_readyWrite_signal = QtCore.pyqtSignal(str, bytes, str)
    serial_readyRead_signal = QtCore.pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.comboBox = MyCombox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(750, 40, 193, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.enter_event_signal.connect(self.onComboxEnterSlot)

        self.serial_port = SerialPort()
        self.serial_port.searchPort()
        self.serial_list =  list(self.serial_port.port.keys())
        self.serial_list.sort()
        for item in self.serial_list:
            self.comboBox.addItem(item)

        self.comboBox_2.addItem('1200')
        self.comboBox_2.addItem('2400')
        self.comboBox_2.addItem('4800')
        self.comboBox_2.addItem('9600')
        self.comboBox_2.addItem('19200')
        self.comboBox_2.addItem('38400')
        self.comboBox_2.addItem('57600')
        self.comboBox_2.addItem('115200')
        self.comboBox_2.setCurrentIndex(3)
        self.comboBox_2.currentIndexChanged.connect(self.onCombox_2IncdeChangeSlot)
        self.comboBox_3.addItem('1')
        self.comboBox_3.addItem('1.5')
        self.comboBox_3.addItem('2')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_3.currentIndexChanged.connect(self.onCombox_3IncdeChangeSlot)
        self.comboBox_4.addItem('5')
        self.comboBox_4.addItem('6')
        self.comboBox_4.addItem('7')
        self.comboBox_4.addItem('8')
        self.comboBox_4.setCurrentIndex(3)
        self.comboBox_4.currentIndexChanged.connect(self.onCombox_4IncdeChangeSlot)
        self.comboBox_5.addItem('无')
        self.comboBox_5.addItem('奇校验')
        self.comboBox_5.addItem('偶校验')
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_5.currentIndexChanged.connect(self.onCombox_5IncdeChangeSlot)

        self.pushButton_flag = True
        self.pushButton.clicked.connect(self.onPushButtonClickedSlot)
        self.pushButton_2.clicked.connect(self.onPushButton_2ClickedSlot)
        self.pushButton_3.clicked.connect(self.onPushButton_3ClickedSlot)
        self.pushButton_4.clicked.connect(self.onPushButton_4ClickedSlot)
        self.pushButton_5.clicked.connect(self.onPushButton_5ClickedSlot)

        self.write_encodemode = 'utf-8'
        self.radioButton.toggled.connect(self.onRadioButtonToggledSlot)
        self.radioButton_2.toggled.connect(self.onRadioButton_2ToggledSlot)
        self.radioButton_3.toggled.connect(self.onRadioButton_3ToggledSlot)
        self.radioButton_4.toggled.connect(self.onRadioButton_4ToggledSlot)
        self.radioButton_5.toggled.connect(self.onRadioButton_5ToggledSlot)
        self.radioButton_6.toggled.connect(self.onRadioButton_6ToggledSlot)

        self.serial_write_thread = QtCore.QThread()
        self.serial_write_threadObject = SerialWriteThreadObject(self.serial_port)
        self.serial_write_threadObject.moveToThread(self.serial_write_thread)
        self.serial_write_threadObject.write_finished.connect(self.serialWriteThreadFinishedSlot)
        self.serial_readyWrite_signal.connect(self.serial_write_threadObject.serialWriteSlot)
        self.serial_write_thread.start()
        self.serial_read_thread = QtCore.QThread()
        self.serial_read_threadObject = SerialReadThreadObject(self.serial_port)
        self.serial_read_threadObject.moveToThread(self.serial_read_thread)
        self.serial_port.readyRead.connect(self.serialReadyReadSlot)
        self.serial_readyRead_signal.connect(self.serial_read_threadObject.serialReadSlot)
        self.serial_read_threadObject.read_finished.connect(self.serialReadThreadFinishedSlot)
        self.serial_read_thread.start()

        self.receive_color = QtGui.QColor(220, 20, 60)
        self.send_color = QtGui.QColor(153, 50, 204)
        self.textBrowser_text_list = []
        self.textBrowser_addTime_flag = False
        self.textBrowser_hex_flag = False
        self.write_newLine_flag = False
        self.write_hex_flag = False
        self.textEdit_textNum = 0

    def onComboxEnterSlot(self):
        if self.pushButton_flag:
            index = self.comboBox.currentIndex()
            text = self.comboBox.currentText()
            self.comboBox.clear()
            self.serial_port.searchPort()
            self.serial_list = list(self.serial_port.port.keys())
            self.serial_list.sort()
            for item in self.serial_list:
                self.comboBox.addItem(item)
            self.comboBox.setCurrentIndex(index)
            if self.comboBox.currentText() != text:
                self.comboBox.setCurrentIndex(0)

    def onCombox_2IncdeChangeSlot(self):
        current_index = self.comboBox_2.currentIndex()
        if current_index == 0:
            self.serial_port.baund_rate = QSerialPort.Baud1200
        elif current_index == 1:
            self.serial_port.baund_rate = QSerialPort.Baud2400
        elif current_index == 2:
            self.serial_port.baund_rate = QSerialPort.Baud4800
        elif current_index == 3:
            self.serial_port.baund_rate = QSerialPort.Baud9600
        elif current_index == 4:
            self.serial_port.baund_rate = QSerialPort.Baud19200
        elif current_index == 5:
            self.serial_port.baund_rate = QSerialPort.Baud38400
        elif current_index == 6:
            self.serial_port.baund_rate = QSerialPort.Baud57600
        elif current_index == 7:
            self.serial_port.baund_rate = QSerialPort.Baud115200

    def onCombox_3IncdeChangeSlot(self):
        current_index = self.comboBox_3.currentIndex()
        if current_index == 0:
            self.serial_port.stop_bits = QSerialPort.OneStop
        elif current_index == 1:
            self.serial_port.stop_bits = QSerialPort.OneAndHalfStop
        elif current_index == 2:
            self.serial_port.stop_bits = QSerialPort.TwoStop

    def onCombox_4IncdeChangeSlot(self):
        current_index = self.comboBox_4.currentIndex()
        if current_index == 0:
            self.serial_port.data_bits = QSerialPort.Data5
        elif current_index == 1:
            self.serial_port.data_bits = QSerialPort.Data6
        elif current_index == 2:
            self.serial_port.data_bits = QSerialPort.Data7
        elif current_index == 3:
            self.serial_port.data_bits = QSerialPort.Data8

    def onCombox_5IncdeChangeSlot(self):
        current_index = self.comboBox_5.currentIndex()
        if current_index == 0:
            self.serial_port.parity = QSerialPort.NoParity
        elif current_index == 1:
            self.serial_port.parity = QSerialPort.OddParity
        elif current_index == 2:
            self.serial_port.parity = QSerialPort.EvenParity

    def onPushButtonClickedSlot(self):
        if self.pushButton_flag:
            port_name = self.comboBox.currentText()
            if port_name != '':
                self.serial_port.setPort(self.serial_port.port[port_name])
                self.serial_port.open(QSerialPort.ReadWrite)
                self.serial_port.setBaudRate(self.serial_port.baund_rate)
                self.serial_port.setStopBits(self.serial_port.stop_bits)
                self.serial_port.setDataBits(self.serial_port.data_bits)
                self.serial_port.setParity(self.serial_port.parity)
            self.pushButton_flag = False
            self.pushButton.setStyleSheet("border-image: url(:/pic/on.png);")
            self.comboBox.setEnabled(False)
            self.comboBox_2.setEnabled(False)
            self.comboBox_3.setEnabled(False)
            self.comboBox_4.setEnabled(False)
            self.comboBox_5.setEnabled(False)
        else:
            self.serial_port.close()
            self.pushButton_flag = True
            self.pushButton.setStyleSheet("border-image: url(:/pic/off.png);")
            self.comboBox.setEnabled(True)
            self.comboBox_2.setEnabled(True)
            self.comboBox_3.setEnabled(True)
            self.comboBox_4.setEnabled(True)
            self.comboBox_5.setEnabled(True)

    def onPushButton_2ClickedSlot(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, '文件保存', './untitled.txt', 'Text files (*.txt)')
        result = ''
        with open(file_name,'w') as fp:
            for text_list in self.textBrowser_text_list:
                text = "%s%s\n%s"%(text_list[0],text_list[2],text_list[1])
                result = result + '\n' + text
            fp.write(result)

    def onPushButton_3ClickedSlot(self):
        self.textBrowser.clear()
        self.textBrowser_text_list = []

    def onPushButton_4ClickedSlot(self):
        self.textEdit.clear()

    def onPushButton_5ClickedSlot(self):
        if not self.pushButton_flag:
            text = self.textEdit.toPlainText()
            if text != '':
                text_bytes = b''
                if self.write_newLine_flag:
                    text = text + '\r\n'
                if self.write_hex_flag:
                    text_bytes = StringProcess.hexStringToStingBytes(text)
                self.serial_readyWrite_signal.emit(text, text_bytes, self.write_encodemode)

    def onRadioButtonToggledSlot(self):
        if self.radioButton.isChecked():
            self.textBrowser_addTime_flag = True
            self.textBrowser.clear()
            for text_list in self.textBrowser_text_list:
                text = "%s%s\n%s"%(text_list[0],text_list[2],text_list[1])
                result_filter = StringProcess.stringToHtmlFilter(text)
                if text_list[0] == '[SEND]:':
                    result = StringProcess.stringToHtml(result_filter, self.send_color)
                else:
                    result = StringProcess.stringToHtml(result_filter, self.receive_color)
                self.textBrowser.append(result)
        else:
            self.textBrowser_addTime_flag = False
            self.textBrowser.clear()
            for text_list in self.textBrowser_text_list:
                text = "%s\n%s" % (text_list[0], text_list[1])
                result_filter = StringProcess.stringToHtmlFilter(text)
                if text_list[0] == '[SEND]:':
                    result = StringProcess.stringToHtml(result_filter, self.send_color)
                else:
                    result = StringProcess.stringToHtml(result_filter, self.receive_color)
                self.textBrowser.append(result)


    def onRadioButton_2ToggledSlot(self):
        if self.radioButton_2.isChecked():
            self.textBrowser_hex_flag = True
        else:
            self.textBrowser_hex_flag = False

    def onRadioButton_3ToggledSlot(self):
        text = self.textEdit.toPlainText()
        if self.radioButton_3.isChecked():
            self.write_hex_flag = True
            self.textEdit.textChanged.connect(self.textEditTextChangeSlot)
            if text != '':
                result = StringProcess.stringToHexString(text, self.write_encodemode)
                self.textEdit.clear()
                self.textEdit.setText(result)
        else:
            self.write_hex_flag = False
            self.textEdit.textChanged.disconnect(self.textEditTextChangeSlot)
            if text != '':
                result, flag = StringProcess.hexStringToSting(self.textEdit.toPlainText(), self.write_encodemode)
                if not flag:
                    self.write_hex_flag = True
                    self.radioButton_3.toggled.disconnect(self.onRadioButton_3ToggledSlot)
                    self.radioButton_3.setChecked(True)
                    self.radioButton_3.toggled.connect(self.onRadioButton_3ToggledSlot)
                    QtWidgets.QMessageBox.warning(self, '警告', '输入的16进制字节串无法用utf-8解码，请确认！')
                    self.textEdit.textChanged.connect(self.textEditTextChangeSlot)
                else:
                    self.textEdit.clear()
                    self.textEdit.setText(result)

    def onRadioButton_4ToggledSlot(self):
        self.write_encodemode = 'utf-8'

    def onRadioButton_5ToggledSlot(self):
        self.write_encodemode = 'gbk'

    def onRadioButton_6ToggledSlot(self):
        if self.radioButton_6.isChecked():
            self.write_newLine_flag = True
        else:
            self.write_newLine_flag = False

    def textEditTextChangeSlot(self):
        text = self.textEdit.toPlainText()
        if text != '':
            cursor = self.textEdit.textCursor()
            col = cursor.columnNumber()
            row = cursor.blockNumber()
            document = self.textEdit.document()
            block_text = document.findBlockByNumber(row).text()
            self.textEdit.textChanged.disconnect(self.textEditTextChangeSlot)
            if self.textEdit_textNum < len(text):
                if col > 0:
                    if ('0' <= block_text[col-1] <= '9') or ('a' <= block_text[col-1] <= 'f') \
                            or ('A' <= block_text[col-1] <= 'F'):
                        if col > 1:
                            if block_text[col-2] != ' ' :
                                if col == len(block_text):
                                    self.textEdit.insertPlainText(' ')
                                elif  block_text[col] != ' ' and block_text[col] != '\n':
                                    self.textEdit.insertPlainText(' ')
                    elif block_text[col-1] != ' ' and block_text[col-1] != '\n':
                        QtWidgets.QMessageBox.warning(self, '输入警告', '在16进制输入下只允许0-9、a-f、A-F！')
                        ch = block_text[col-1]
                        text = text.strip(ch)
                        self.textEdit.setText(text)
                        self.textEdit.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.textEdit.textChanged.connect(self.textEditTextChangeSlot)
        self.textEdit_textNum = len(text)

    def serialWriteThreadFinishedSlot(self):
        text = self.textEdit.toPlainText()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        setting = '[SEND]:'
        if self.write_hex_flag:
            setting = setting + '(hex)'
        temp_list = [setting, text, current_time]
        self.textBrowser_text_list.append(temp_list)
        if self.textBrowser_addTime_flag:
            result = "%s(%s)\n%s"%(setting, current_time, text)
        else:
            result = "%s\n%s"%(setting, text)
        result_filter = StringProcess.stringToHtmlFilter(result)
        self.textBrowser.append(StringProcess.stringToHtml(result_filter, self.send_color))

    def serialReadThreadFinishedSlot(self, data):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        setting = '[RECEIVE]:'
        if self.textBrowser_hex_flag:
            setting = setting + '(hex)'
        temp_list = [setting, data, current_time]
        self.textBrowser_text_list.append(temp_list)
        if self.textBrowser_addTime_flag:
            result = "%s(%s)\n%s"%(setting, current_time, data)
        else:
            result = "%s\n%s"%(setting, data)
        result_filter = StringProcess.stringToHtmlFilter(result)
        self.textBrowser.append(StringProcess.stringToHtml(result_filter, self.receive_color))

    def serialReadyReadSlot(self):
        self.serial_readyRead_signal.emit(self.textBrowser_hex_flag)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
