from PySide6 import QtCore, QtWidgets, QtGui
import ctypes, os, flv


NAME = "FLv-Analyze"
ICON = "icon.png"

MyAppId = 'flv-analyze.github.pennilessfor@gmail' 

if os.name == 'nt':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MyAppId)



class pMainWidget(QtWidgets.QWidget):
    'Flv-analyze 分析文件GUI控制'
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.flvStruct = None 
        self.showContent()

    def showContent(self):
        '展示 flv tag 全部信息'
        # 展示当前所有Tag的列表组件
        self.pTagListTree = QtWidgets.QListWidget()    
        self.pTagListTree.clicked.connect(self.pClickFlvItem)
        # 展示当前点击后的tag info内容
        self.pTagInfoText = QtWidgets.QTextEdit()
        self.pTagInfoText.setReadOnly(True)
        # 展示原始字节流
        self.pTagInfoHex  = QtWidgets.QPlainTextEdit()
        self.pTagInfoHex.setReadOnly(True)

        # 增加上下布局
        right = QtWidgets.QVBoxLayout()
        right.addWidget(self.pTagInfoText)
        right.setStretchFactor(self.pTagInfoText,3)
        right.addWidget(self.pTagInfoHex)
        right.setStretchFactor(self.pTagInfoHex,2)
        

        # 全局布局
        content = QtWidgets.QHBoxLayout()
        content.addWidget(self.pTagListTree)
        content.addLayout(right)
        content.setStretchFactor(self.pTagListTree,1)
        content.setStretchFactor(right,4)
        self.layout.addLayout(content)


    def pOpenFlv(self):
        '打开FLv文件操作。'
        pwd = QtWidgets.QFileDialog.getOpenFileName(self, "打开文件", " ",'*.flv')
        self.flvStruct = flv.newFLv(pwd[0])

        self.pTagListTree.addItem(self.flvStruct.header.name)
        self.pTagListTree.addItems(self.flvStruct.tagList)

    def pClickFlvItem(self,item):
        '点击某个tag list触发的事件'
        # 如果是FLV header 则特殊处理
        if(item.row() == 0):
            self.pTagInfoHex.setPlainText(self.flvStruct.header.data.hex(' '))
            return

        tag = self.flvStruct.body[item.row()-1]
        # 填充解析后的详情
        self.pTagInfoText.setText("Tag Type: " + str(tag.tagType))
        self.pTagInfoText.append("Tag Data Size: " + str(tag.dataSize))
        self.pTagInfoText.append("Tag TimeStamp: " + str(tag.timeStamp))
        self.pTagInfoText.append("Tag TimeStamp Extended: " + str(tag.timeStampExtended))
        self.pTagInfoText.append("Tag streamID: " + str(tag.streamID))
        self.pTagInfoText.append("PreviousTagSize: " + str(tag.previousTagSize))
        
        # 填充hex当前tag的所有数据。
        self.pTagInfoHex.setPlainText(tag.data.hex(' '))

class pMainWindow(QtWidgets.QMainWindow):
    'Flv-analyze 分析文件GUI控制'
    def __init__(self):
        super().__init__()
        self.pCentent = pMainWidget()
        self.pSetMenuBar()
        self.setCentralWidget(self.pCentent)
        self.resize(960, 800)
        self.setWindowTitle(NAME)

    def pSetMenuBar(self):
        '设置菜单栏'
        menu = self.menuBar()
        menuFlv = menu.addMenu("File")
        actionOpen = QtGui.QAction('Open', self)
        actionOpen.triggered.connect(self.pCentent.pOpenFlv)
        menuFlv.addAction(actionOpen)

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    app.setWindowIcon(QtGui.QIcon(ICON))

    window = pMainWindow()
    window.show()

    app.exec()

