from PyQt5.QtGui import QColor

def stringToHexString(data: str, mode: str) -> str:
    """
    将字符串转换为字符串ASCII码/utf-8码的Hex值输出
    :param mode: 编码模式
    :param data: 输入字符串
    :return: Hex格式的字符串
    """
    string_bytes = data.encode(encoding=mode)
    string_list = list(string_bytes)
    hexString_list = [hex(string)[2:] for string in string_list]
    return ' '.join(hexString_list)

def hexStringToStingBytes(data: str) -> bytes:
    """
    将16进制格式的字符串转换为值对应的字节型字符串
    :param data: 16进制格式字符串（"xx xx xx ..."）
    :return: 值对应的字节型字符串
    """
    hexString_list = data.split(' ')
    while '' in hexString_list:
        hexString_list.remove('')
    string_list = [int(hexString, 16) for hexString in hexString_list]
    string_bytes = bytes(string_list)
    return string_bytes

def hexStringToSting(data: str, mode: str) -> tuple:
    """
    将16进制格式的字符串解码为对应的字符串
    :param data: 16进制格式字符串（"xx xx xx ..."）
    :param mode: 解码模式
    :return: 解码后的字符串
    """
    hexString_list = data.split(' ')
    string_list = [int(hexString, 16) for hexString in hexString_list]
    string_bytes = bytes(string_list)
    try:
        string = string_bytes.decode(encoding=mode)
    except:
        string = data
        flag = False
    else:
        flag = True
    return string, flag

def stringToHtmlFilter(data: str) -> str:
    """
    将字符串中的特殊字符替换为Html格式
    :param data: 输入字符串
    :return: 替换后的字符串
    """
    # 注意这几行代码的顺序不能乱，否则会造成多次替换
    data = data.replace("&", "&amp;")
    data = data.replace(">", "&gt;")
    data = data.replace("<", "&lt;")
    data = data.replace("\"", "&quot;")
    data = data.replace("\'", "&#39;")
    data = data.replace(" ", "&nbsp;")
    data = data.replace("\n", "<br/>")
    data = data.replace("\r", "<br>")
    return data

def stringToHtml(data: str, col: QColor) -> str:
    """
    将字符串调整为Html格式
    :param data: 输入的字符串
    :param col: 指定的字体颜色
    :return: Html格式的字符串
    """
    red = col.red()
    green = col.green()
    blue = col.blue()
    if red > 15:
        red_hex = hex(red)[2:]
    else:
        red_hex = '0' + hex(red)[2:]
    if green > 15:
        green_hex = hex(green)[2:]
    else:
        green_hex = '0' + hex(green)[2:]
    if blue > 15:
        blue_hex = hex(blue)[2:]
    else:
        blue_hex = '0' + hex(blue)[2:]
    col_string = red_hex + green_hex + blue_hex
    return "<span style=\"color:#%s\">%s</span>"%(col_string, data)
