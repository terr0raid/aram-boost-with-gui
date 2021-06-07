import subprocess
import re
import sys
try:
    import requests
    import urllib3
    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
except ModuleNotFoundError:
    print('Gerekli moduller bulunamadi')
    exit()

class AramBoostGUI(QWidget):

    #constant
    command = "WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline"
    url = 'https://127.0.0.1:%s/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","activateBattleBoostV1",""]'
    checker = False
    
    def __init__(self, title, x1, y1, x2, y2):
        super(AramBoostGUI,self).__init__()
        self.initUI(title, x1, y1, x2,y2)


    def postProcess(self, port, password):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.session = requests.session()
        self.session.verify = False
        result = self.session.post(self.url % port, data={}, auth=requests.auth.HTTPBasicAuth('riot', password))
        return result

    def warningMessageBox(self, title, msg):
       QMessageBox.warning(self, title, msg)

    def infoMessageBox(self, title, msg):
       QMessageBox.information(self, title, msg)

    def createButton(self, text, toolTip, func):
        self.button = QPushButton(self)
        self.button.setText(text)          
        # self.button.setIcon(QIcon("close.png")) 
        # self.button.setShortcut('Ctrl+D') 
        self.button.clicked.connect(func)
        self.button.setToolTip(toolTip)
        self.button.move(100,100)

    def initUI(self, title, x1, y1, x2, y2):
        self.setWindowTitle(title)
        self.setGeometry(x1, y1, x2, y2)
        self.createButton("Aram Boost", "Bas boostu amugagoyum", self.boostAram)

    def boostAram(self):
        try:        
            outputText = subprocess.Popen(self.command, stdout=subprocess.PIPE,
                                          shell=True).stdout.read().decode('utf-8')

            port = re.findall(r'"--app-port=(.*?)"', outputText)[0]
            password = re.findall(r'"--remoting-auth-token=(.*?)"', outputText)[0]

            while True:
                if (self.checker == True):
                    self.infoMessageBox('Basarisiz', 'Takviye islemi zaten gerceklestirildi! Gerceklesmediyse uygulamayi yeniden baslatin.')
                    break
                result = self.postProcess(port, password)
                if result.status_code == 200:
                    self.infoMessageBox('Basarili', 'Takviye islemi gerceklesti! Uygulamayi kapatabilirsiniz')
                    self.checker = True
                    break
                else:
                    self.warningMessageBox('Hata', 'Bir hata olustu, oyunun acik oldugundan ve secim ekraninda oldugunuzdan emin olun! Uygulamayi yonetici olarak calistirin.')
                    break
        except:
            self.warningMessageBox('Hata', 'Bir hata olustu, lutfen oyunu baslatin.')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    exe = AramBoostGUI('Aram Boost',400,400,300,260)
    exe.show()
    sys.exit(app.exec_()) 
