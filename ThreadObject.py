from PyQt5.QtCore import QObject, pyqtSignal

class SerialWriteThreadObject(QObject):
    write_finished = pyqtSignal()
    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port

    def serialWriteSlot(self, data, data_bytes,  mode):
        if data_bytes == b'':
            data_bytes = data.encode(encoding=mode)
        self.serial_port.writeData(data_bytes)
        self.write_finished.emit()

class SerialReadThreadObject(QObject):
    read_finished = pyqtSignal(str)
    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port

    def serialReadSlot(self, flag):
        data = bytes(self.serial_port.readAll())
        if not flag:
            try:
                data_str = data.decode(encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    data_str = data.decode(encoding='gbk')
                except UnicodeDecodeError:
                    data_str = '无法解码:%s' % str(data)
        else:
            string_list = list(data)
            hexString_list = [hex(string)[2:] for string in string_list]
            data_str = ' '.join(hexString_list)
        self.read_finished.emit(data_str)