import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSplitter, 
                             QListWidget, QTextBrowser, QLineEdit, 
                             QVBoxLayout, QWidget, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class ImanIlmihaliApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("İman ve Ahlak İlmihali")
        self.resize(1000, 600)
        self.ekrani_ortala()
        
        # Ana dizin ve Konular dizini tespiti
        self.ana_dizin = os.path.dirname(os.path.abspath(__file__))
        self.konular_dizini = os.path.join(self.ana_dizin, "konular")
        
        # --- SİMGE (ICON) AYARI ---
        simge_yolu = os.path.join(self.ana_dizin, "iman.png")
        if os.path.exists(simge_yolu):
            self.setWindowIcon(QIcon(simge_yolu))

        self.setStyleSheet("""
            QMainWindow { background-color: #f4ecd8; }
            #sidePanel {
                background-color: #4a3728;
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
            }
            QLineEdit {
                background-color: #fdfaf1;
                border: 1px solid #8b5e3c;
                border-radius: 8px;
                padding: 8px;
                margin: 10px;
                color: #2c241e;
            }
            QListWidget {
                background-color: transparent;
                border: none;
                color: #fdfaf1;
                outline: none;
                font-size: 14px;
            }
            QListWidget::item { padding: 12px; margin: 2px 8px; border-radius: 8px; }
            QListWidget::item:selected { background-color: #8b5e3c; color: white; }
            #contentCard {
                background-color: #fdfaf1;
                border-radius: 15px;
                margin: 10px;
                border: 1px solid #d3c4a8;
            }
            QTextBrowser { background-color: transparent; border: none; padding: 30px; }
            QScrollBar:vertical {
                border: none;
                background: #efe4cc;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #8b5e3c;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        self.init_ui()
        self.dosyalari_yukle()
        self.ilk_dosyayi_sec()

    def ekrani_ortala(self):
        ekran = QApplication.primaryScreen().availableGeometry()
        pencere = self.frameGeometry()
        pencere.moveCenter(ekran.center())
        self.move(pencere.topLeft())

    def init_ui(self):
        merkezi_widget = QWidget()
        self.setCentralWidget(merkezi_widget)
        ana_layout = QVBoxLayout(merkezi_widget)
        ana_layout.setContentsMargins(0,0,0,0)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sol Panel (Navigasyon)
        self.sol_panel = QFrame()
        self.sol_panel.setObjectName("sidePanel")
        sol_layout = QVBoxLayout(self.sol_panel)
        
        self.arama_cubugu = QLineEdit()
        self.arama_cubugu.setPlaceholderText("Konu Ara...")
        self.arama_cubugu.textChanged.connect(self.arama_yap)
        
        self.list_widget = QListWidget()
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list_widget.setWordWrap(True) 
        
        sol_layout.addWidget(self.arama_cubugu)
        sol_layout.addWidget(self.list_widget)

        # Sağ Panel (İçerik)
        self.sag_panel = QFrame()
        self.sag_panel.setObjectName("contentCard")
        sag_layout = QVBoxLayout(self.sag_panel)
        self.text_browser = QTextBrowser()
        sag_layout.addWidget(self.text_browser)

        self.splitter.addWidget(self.sol_panel)
        self.splitter.addWidget(self.sag_panel)
        self.splitter.setSizes([260, 740])
        self.splitter.setHandleWidth(0)
        
        ana_layout.addWidget(self.splitter)
        self.list_widget.itemClicked.connect(self.icerik_goster)

    def dosyalari_yukle(self):
        self.list_widget.clear()
        
        # Klasör kontrolü
        if not os.path.exists(self.konular_dizini):
            self.text_browser.setHtml("<h2 style='color:red;'>'konular' klasörü bulunamadı!</h2>")
            return

        try:
            # Konular klasöründeki .txt dosyalarını oku
            dosyalar = sorted([f for f in os.listdir(self.konular_dizini) if f.lower().endswith('.txt')])
            
            for dosya in dosyalar:
                # Dosya adını temizleyip başlık yap (Örn: 01_iman-nedir.txt -> İman Nedir)
                baslik = dosya.replace(".txt", "").replace("-", " ").replace("_", " ").title()
                # Eğer başta sayı varsa (01 ) onu temizle
                if baslik[0:2].isdigit(): 
                    baslik = baslik[2:].strip()
                
                item = self.list_widget.addItem(baslik)
                # Dosyanın tam yolunu her bir listenin öğesine "UserRole" olarak gizle
                self.list_widget.item(self.list_widget.count()-1).setData(
                    Qt.ItemDataRole.UserRole, os.path.join(self.konular_dizini, dosya)
                )
        except Exception as e:
            self.text_browser.setText(f"Dosyalar yüklenirken hata oluştu: {e}")

    def ilk_dosyayi_sec(self):
        if self.list_widget.count() > 0:
            ilk_item = self.list_widget.item(0)
            self.list_widget.setCurrentItem(ilk_item)
            self.icerik_goster(ilk_item)

    def arama_yap(self, metin):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(metin.lower() not in item.text().lower())

    def icerik_goster(self, item):
        tam_yol = item.data(Qt.ItemDataRole.UserRole)
        try:
            with open(tam_yol, "r", encoding="utf-8") as f:
                icerik = f.read()
                # Metni HTML formatına sokarak daha okunaklı yapıyoruz
                html = f"""
                <div style='font-size: 15pt; line-height: 1.8; color: #2c241e; font-family: Georgia, serif; text-align: justify;'>
                    {icerik.replace(chr(10), '<br>')}
                </div>
                """
                self.text_browser.setHtml(html)
        except Exception as e:
            self.text_browser.setPlainText(f"Dosya okuma hatası: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Linux/Pardus için uygulama kimliği (Gerekirse)
    if os.name == 'posix':
        try:
            import ctypes
            # Bazı sistemlerde taskbar ikonu için gerekebilir
        except:
            pass

    pencere = ImanIlmihaliApp()
    pencere.show()
    sys.exit(app.exec())