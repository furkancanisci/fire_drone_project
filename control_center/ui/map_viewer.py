import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer
from control_center.maps.map_generator import generate_map

class MapViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Control Center - Harita")
        self.setGeometry(100, 100, 800, 600)

        # Web View
        self.web_view = QWebEngineView()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.web_view)
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.update_map()  # İlk haritayı yükle

        # Timer: Her 2 saniyede bir haritayı yenile
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_map)
        self.timer.start(2000)  # 2000 ms → 2 saniye

    def update_map(self):
        generate_map()  # Haritayı güncelle
        file_path = Path(__file__).resolve().parent.parent / "maps" / "drone_map.html"
        self.web_view.load(QUrl.fromLocalFile(str(file_path)))
        print("Harita yüklendi.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.show()
    sys.exit(app.exec_())
