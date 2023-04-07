# this program define that color schema for the application
# @author: Wolfgang Rafelt


def fullColorMatrix(matIndex: int):
    colorList = []
    colorList = [
    # red
    ['#000000','#080000','#100000','#180000','#200000','#280000','#300000','#380000',
     '#400000','#480000','#500000','#580000','#600000','#680000','#700000','#780000',
     '#800000','#880000','#900000','#980000','#A00000','#A80000','#B00000','#B80000',
     '#C00000','#C80000','#D00000','#D80000','#E00000','#E80000','#F00000','#F80000'],
    # cyan
    ['#000000','#000808','#001010','#001818','#002020','#002828','#003030','#003838',
     '#004040','#004848','#005050','#005858','#006060','#006868','#007070','#007878',
     '#008080','#008888','#009090','#009898','#00A0A0','#00A8A8','#00B0B0','#00B8B8',
     '#00C0C0','#00C8C8','#00D0D0','#00D8D8','#00E0E0','#00E8E8','#00F0F0','#00F8F8'],
    # green
    ['#000000','#008000','#001000','#001800','#002000','#002800','#003000','#003800',
     '#004000','#004800','#005000','#005800','#006000','#006800','#007000','#007800',
     '#008000','#008800','#009000','#009800','#00A000','#00A800','#00B000','#00B800',
     '#00C000','#00C800','#00D000','#00D800','#00E000','#00E800','#00F000','#00F800'],
    # magenta
    ['#000000','#080008','#100010','#180018','#200020','#280028','#300030','#380038',
     '#400040','#480048','#500050','#580058','#600060','#680068','#700070','#780078',
     '#800080','#880088','#900090','#980098','#A000A0','#A800A8','#B000B0','#B800B8',
     '#C000C0','#C800C8','#D000D0','#D800D8','#E000E0','#E800E8','#F000F0','#F800F8'],
    # blue
    ['#000000','#000008','#000010','#000018','#000020','#000028','#000030','#000038',
     '#000040','#000048','#000050','#000058','#000060','#000068','#000070','#000078',
     '#000080','#000088','#000090','#000098','#0000A0','#0000A8','#0000B0','#0000B8',
     '#0000C0','#0000C8','#0000D0','#0000D8','#0000E0','#0000E8','#0000F0','#0000F8'],
    # yellow
    ['#000000','#080800','#101000','#181800','#202000','#282800','#303000','#383800',
     '#404000','#484800','#505000','#585800','#606000','#686800','#707000','#787800',
     '#808000','#888800','#909000','#989800','#A0A000','#A8A800','#B0B000','#B8B800',
     '#C0C000','#C8C800','#D0D000','#D8D800','#E0E000','#E8E800','#F0F000','#F8F800'],
    # gray
    ['#000000','#080808','#101010','#181818','#202020','#282828','#303030','#383838',
     '#404040','#484848','#505050','#585858','#606060','#686868','#707070','#787878',
     '#808080','#888888','#909090','#989898','#A0A0A0','#A8A8A8','#B0B0B0','#B8B8B8',
     '#C0C0C0','#C8C8C8','#D0D0D0','#D8D8D8','#E0E0E0','#E8E8E8','#F0F0F0','#F8F8F8']
    ]
    return colorList[matIndex]

def colorWidgetScheme(scheme: str):
    farbMatrix = []
    kompMatrix = []
    if scheme   == 'red':
        farbMatrix = fullColorMatrix(0)
        kompMatrix = fullColorMatrix(1)
    elif scheme == 'green':
        farbMatrix = fullColorMatrix(2)
        kompMatrix = fullColorMatrix(3)
    elif scheme == 'blue':
        farbMatrix = fullColorMatrix(4)
        kompMatrix = fullColorMatrix(5)
    elif scheme == 'gray':
        farbMatrix = fullColorMatrix(6)
        kompMatrix = fullColorMatrix(6)
    elif scheme == 'cyan':
        farbMatrix = fullColorMatrix(1)
        kompMatrix = fullColorMatrix(0)
    elif scheme == 'magenta':
        farbMatrix = fullColorMatrix(3)
        kompMatrix = fullColorMatrix(2)
    elif scheme == 'yellow':
        farbMatrix = fullColorMatrix(5)
        kompMatrix = fullColorMatrix(4)
    if farbMatrix == []:
        return ''
    return str('MainWindow{color:' + farbMatrix[0] + '}'
               'QWidget{color:' + kompMatrix[0] + '}'
               'QTabBar{color:' + kompMatrix[24] + '}'
               'QGroupBox{color:' + kompMatrix[20] + '}'
               'QLineEdit{color:' + kompMatrix[0] + '}'
               'QPushButton{color:' + kompMatrix[0] + '}'

               'MainWindow{background-color:' + farbMatrix[8] + '}'
               'QWidget{background-color:' + farbMatrix[8] + '}'
               'QTabBar{background-color:' + farbMatrix[8] + '}'
               'QTabBar{selection-background-color:' + farbMatrix[10] + '}'
               'QGroupBox{background-color:' + farbMatrix[12] + '}'
               'QLabel{background-color:' + farbMatrix[12] + '}'
               'QLineEdit{background-color:' + farbMatrix[14] + '}'
               'QPushButton{background-color:' + farbMatrix[14] + '}'
               'QRadioButton{background-color:' + farbMatrix[14] + '}'
               'QComboBox{background-color:' + farbMatrix[14] + '}'

               'QWidget{border-color:' + farbMatrix[20] + '}'
               'QWidget{border-width: 1px}'
               'QWidget{border-style: solid}'
               'QTabBar{border-color:' + farbMatrix[20] + '}'
               'QTabBar{border-width: 1px}'
               'QTabBar{border-style: solid}'
               'QTabWidget{border-color:' + farbMatrix[20] + '}'
               'QTabWidget{border-width: 1px}'
               'QTabWidget{border-style: solid}'
               'QGroupBox{border-color:' + farbMatrix[20] + '}'
               'QGroupBox{border-width: 1px}'
               'QGroupBox{border-style: solid}'
               'QLabel{border-width: 0px}'

               'QLineEdit:hover{background-color:' + farbMatrix[28] + '}'
               'QPushButton:hover{background-color:' + farbMatrix[28] + '}'
               'QRadioButton:hover{background-color:' + farbMatrix[28] + '}'
               'QComboBox:hover{background-color:' + farbMatrix[28] + '}')

def colorMenuScheme(scheme: str):
    farbMatrix = []
    kompMatrix = []
    if scheme   == 'red':
        farbMatrix = fullColorMatrix(0)
        kompMatrix = fullColorMatrix(1)
    elif scheme == 'green':
        farbMatrix = fullColorMatrix(2)
        kompMatrix = fullColorMatrix(3)
    elif scheme == 'blue':
        farbMatrix = fullColorMatrix(4)
        kompMatrix = fullColorMatrix(5)
    elif scheme == 'gray':
        farbMatrix = fullColorMatrix(6)
        kompMatrix = fullColorMatrix(6)
    elif scheme == 'cyan':
        farbMatrix = fullColorMatrix(1)
        kompMatrix = fullColorMatrix(0)
    elif scheme == 'magenta':
        farbMatrix = fullColorMatrix(3)
        kompMatrix = fullColorMatrix(2)
    elif scheme == 'yellow':
        farbMatrix = fullColorMatrix(5)
        kompMatrix = fullColorMatrix(4)
    if farbMatrix == []:
        return ''
    return str('QMenu{color:' + kompMatrix[28] + '}'
               'QMenuBar{color:' + kompMatrix[28] + '}'
               'QMenu{background-color:' + farbMatrix[8] + '}'
               'QMenuBar{background-color:' + farbMatrix[8] + '}'
               'QMenuBar:item:selected{background:' + farbMatrix[24] + '}'

               'QMenu:item:selected{background:' + farbMatrix[24] + '}'
               'QMenu{border-color:' + farbMatrix[20] + '}'
               'QMenu{border-width: 1px}'
               'QTabWidget{border-width: 1px}'
               'QTabWidget{border-style: solid}')

def colorPopupDialogScheme(scheme: str):
    if scheme   == 'red':
        head = fullColorMatrix(0)[12]
        body = fullColorMatrix(0)[26]
    elif scheme == 'green':
        head = fullColorMatrix(2)[12]
        body = fullColorMatrix(2)[26]
    elif scheme == 'blue':
        head = fullColorMatrix(4)[12]
        body = fullColorMatrix(4)[26]
    elif scheme == 'cyan':
        head = fullColorMatrix(1)[12]
        body = fullColorMatrix(1)[26]
    elif scheme == 'magenta':
        head = fullColorMatrix(3)[12]
        body = fullColorMatrix(3)[26]
    elif scheme == 'yellow':
        head = fullColorMatrix(5)[12]
        body = fullColorMatrix(5)[26]
    else: # scheme == 'gray':
        head = fullColorMatrix(6)[12]
        body = fullColorMatrix(6)[26]
    return head, body
