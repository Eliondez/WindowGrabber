import sys
import main
from PyQt5 import QtGui, QtCore, QtMultimedia
from PyQt5.QtWidgets import *
from PyQt5.QtCore import qDebug, QTimer, QUrl, QFile, QFileInfo, QDir
from PyQt5.QtGui import QColor, QPixmap, QScreen
from PyQt5.QtMultimedia import *
from PIL.ImageQt import ImageQt
from PIL import Image

app = QApplication(sys.argv)

class MessageBox(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		self.setWindowTitle('Local watcher')		
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


		# media content 
		self.screen = app.primaryScreen()
		self.mediaPLayer = QMediaPlayer()
		url = QUrl.fromLocalFile(QFileInfo("D:\\1.mp3").absoluteFilePath())
		qDebug(QDir.currentPath())
		content = QMediaContent(url)
		self.mediaPLayer.setMedia(content);
		self.mediaPLayer.setVolume(50);
		##

		self.rect = {
			'x': 424,
			'y': 42,
			'w': 88,
			'h': 400
		}
		
		## Settings

		self.initUi()

		self.timer = QTimer()
		self.timer.timeout.connect(self.onTimer)
		self.timer.start(300)
		

	def initUi(self):
		formLo = QFormLayout()

		labelAlarm = QLabel("Alarm?")
		self.cb = QCheckBox(self)

		formLo.addRow(labelAlarm, self.cb)

		labelName = QLabel("Name")
		self.inputName = QLineEdit(self)

		formLo.addRow(labelName, self.inputName)

		labelPin = QLabel("Pin")
		self.toggleButton = QPushButton("Toggle", self)
		self.toggleButton.setCheckable(True)
		self.toggleButton.clicked[bool].connect(self.toggleSettings)

		formLo.addRow(labelPin, self.toggleButton)

		self.labelX = QLabel("X:")
		self.sbX = QSpinBox(self)
		self.sbX.setRange(0, 1600)
		self.sbX.setValue(self.rect['x'])
		self.sbX.valueChanged[int].connect(self.changeValue)
		
		formLo.addRow(self.labelX, self.sbX)

		self.labelW = QLabel("W:")
		self.sbW = QSpinBox(self)
		self.sbW.setRange(50, 1600)
		self.sbW.setValue(self.rect['w'])
		self.sbW.valueChanged[int].connect(self.changeValue)

		formLo.addRow(self.labelW, self.sbW)
		
		self.labelY = QLabel("Y:")
		self.sbY = QSpinBox(self)
		self.sbY.setRange(10, 900)
		self.sbY.setValue(self.rect['y'])
		self.sbY.valueChanged[int].connect(self.changeValue)

		formLo.addRow(self.labelY, self.sbY)
		
		self.labelH = QLabel("H:")
		self.sbH = QSpinBox(self)
		self.sbH.setRange(10, 900)
		self.sbH.setValue(self.rect['h'])
		self.sbH.valueChanged[int].connect(self.changeValue)

		formLo.addRow(self.labelH, self.sbH)
		
		mainlo = QVBoxLayout(self)

		self.character = 'sublime'
		self.labelName = QLabel(self)
		self.labelName.setText(self.character)
		self.labelImage = QLabel()
		#self.labelImage.show()
		self.hwnd = main.get_hwnd(self.character)
		
		mainlo.addLayout(formLo)
		mainlo.addWidget(self.labelName)
		mainlo.addWidget(self.labelImage)

		self.setLayout(mainlo)

		
	def changeValue(self):
		self.rect['x'] = self.sbX.value()
		self.rect['w'] = self.sbW.value()
		self.rect['y'] = self.sbY.value()
		self.rect['h'] = self.sbH.value()
		

	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Message',
			"Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()
			

	def toggleSettings(self, isVisible):
		flags = self.windowFlags();	
		self.sbX.setVisible(not isVisible)
		self.sbY.setVisible(not isVisible)
		self.sbW.setVisible(not isVisible)
		self.sbH.setVisible(not isVisible)
		self.labelX.setVisible(not isVisible)
		self.labelY.setVisible(not isVisible)
		self.labelW.setVisible(not isVisible)
		self.labelH.setVisible(not isVisible)

		
		if isVisible:
			qDebug("Visible")
			self.setWindowFlags(flags | QtCore.Qt.FramelessWindowHint);
			self.show();
		else:
			qDebug("Invisible")
			self.setWindowFlags(flags ^ QtCore.Qt.FramelessWindowHint);
			self.show()

		
	def onTimer(self):
		pixmap = self.screen.grabWindow(self.hwnd,
									self.rect['x'],
									self.rect['y'],
									self.rect['w'],
									self.rect['h'])
										  
			
		if self.cb.isChecked():
			img = pixmap.toImage()
			gridY = [y for y in range(img.height()) if y % 5 == 0]
			x = 5
			targetColor = QtGui.QColor(255,0,0)
			minDelta = 99999999
			for i in gridY:
				deltaR = targetColor.red() - QColor(img.pixel(x, i)).red()
				deltaG = targetColor.green() - QColor(img.pixel(x, i)).green()
				deltaB = targetColor.blue() - QColor(img.pixel(x, i)).blue()
				delta = abs(deltaR) + abs(deltaG) + abs(deltaB)
				if delta < minDelta:
					minDelta = delta
			
			# qDebug(str(minDelta))
			if minDelta < 200:
				QtCore.qDebug("ALERT!!!")
				self.mediaPLayer.play();
				self.cb.setChecked(False)
				
				# img.setPixel(x, i, targetColor.rgb())
				# pixmap = QtGui.QPixmap.fromImage(img)
			
		self.labelImage.setPixmap(pixmap)
		
		


qb = MessageBox()
qb.show()
sys.exit(app.exec_())
