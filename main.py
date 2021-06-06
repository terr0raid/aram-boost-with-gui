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
    def __init__(self, title, x1, y1, x2, y2):
        super(AramBoostGUI,self).__init__()
        self.initUI(title, x1, y1, x2,y2)

    def warningMessageBox(self, title, msg):
       QMessageBox.warning(self, title, msg)
    def aboutMessageBox(self, title, msg):
       QMessageBox.about(self, title, msg)

    def boostAram(self):
        try:        
            command = "WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline"

            outputText = subprocess.Popen(command, stdout=subprocess.PIPE,
                                          shell=True).stdout.read().decode('utf-8')

            port = re.findall(r'"--app-port=(.*?)"', outputText)[0]
            password = re.findall(r'"--remoting-auth-token=(.*?)"', outputText)[0]

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            session = requests.session()
            session.verify = False
            while True:
                try:
                    result = session.post('https://127.0.0.1:%s/lol-login/v1/session/invoke?destination=lcdsServiceProxy&method=call&args=["","teambuilder-draft","activateBattleBoostV1",""]' %
                        port, data={}, auth=requests.auth.HTTPBasicAuth('riot', password))
                    if result.status_code == 200:
                        self.aboutMessageBox('Basarili', 'Takviye islemi gerceklesti! Uygulama kapatiliyor.')
                        exit()
                    else:
                        self.warningMessageBox('Hata', 'Bir hata olustu, oyunun acik oldugundan ve secim ekraninda oldugunuzdan emin olun! status code hatasi')
                        exit()
                except:
                    self.warningMessageBox('Hata', 'Bir hata olustu, oyunun acik oldugundan ve secim ekraninda oldugunuzdan emin olun! post islemi hatasi')
                    break
        except:
            self.warningMessageBox('Hata', 'Bir hata olustu, oyunun acik oldugundan ve secim ekraninda oldugunuzdan emin olun! client kapali hatasi')
            exit()

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
        self.createButton("Aram Boost BGY OZEL", "Bas boostu amugagoyum", self.boostAram)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    exe = AramBoostGUI('Aram Boost',400,400,300,260)
    exe.show()
    sys.exit(app.exec_()) 
