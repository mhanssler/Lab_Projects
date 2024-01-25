import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import pyqtgraph as pg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Layout
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Plot Widget
        self.plotWidget = pg.PlotWidget()
        layout.addWidget(self.plotWidget)
        self.plotData = self.plotWidget.plot()

        # Buttons for device control
        self.buttonControlDP832 = QPushButton('Control DP832')
        layout.addWidget(self.buttonControlDP832)
        # Connect this button to a function to control DP832

        # ... Add more buttons and controls for other devices

        # Window setup
        self.setWindowTitle('Device Control GUI')
        self.setGeometry(100, 100, 800, 600)

    # ... Add methods for device control and plot updating

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
