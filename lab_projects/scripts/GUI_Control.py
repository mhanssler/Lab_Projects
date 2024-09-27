import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
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
        
        #Add a display to read the channel, voltage and current
        self.channelDisplay = QLabel('Channel: ')
        layout.addWidget(self.channelDisplay)
        self.voltageDisplay = QLabel('Voltage: ')
        layout.addWidget(self.voltageDisplay)
        self.currentDisplay = QLabel('Current: ')
        layout.addWidget(self.currentDisplay)


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
