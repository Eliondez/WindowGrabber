import sys
import main
from PyQt5 import QtGui, QtCore, QtMultimedia
from PyQt5.QtWidgets import *
from PyQt5.QtCore import qDebug, QTimer, QUrl, QFile, QFileInfo
from PyQt5.QtGui import QColor, QPixmap, QScreen
from PyQt5.QtMultimedia import *
from PIL.ImageQt import ImageQt
from PIL import Image

app = QApplication(sys.argv)

class MessageBox(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)

		
		self.setWindowTitle('Local watcher')		
		#self.setWindowOpacity(0.7)
		self.setWindowFlags(
			QtCore.Qt.WindowStaysOnTopHint 
			# |
			# QtCore.Qt.FramelessWindowHint
			)
		
		self.rects = [
			{
				'x': 424,
				'y': 42,
				'w': 88,
				'h': 400
			}
		]
		self.cb = QCheckBox(self)
		self.toggleButton = QPushButton("Toggle", self)
		self.toggleButton.setCheckable(True)
		self.toggleButton.clicked[bool].connect(self.toggleSettings)
		self.mayAlarm = True
		self.screen = app.primaryScreen()
		self.mediaPLayer = QMediaPlayer()
		url = QUrl.fromLocalFile(QFileInfo("E:\\Scr\\python-windowgrabber\\1.mp3").absoluteFilePath())
		content = QMediaContent(url)
		self.mediaPLayer.setMedia(content);
		self.mediaPLayer.setVolume(50);
		
		
		self.sbX = QSpinBox(self)
		self.sbX.setRange(0, 1600)
		self.sbX.setValue(self.rects[0]['x'])
		self.sbX.valueChanged[int].connect(self.changeValue)
		
		self.sbW = QSpinBox(self)
		self.sbW.setRange(50, 1600)
		self.sbW.setValue(self.rects[0]['w'])
		self.sbW.valueChanged[int].connect(self.changeValue)
		
		self.sbY = QSpinBox(self)
		self.sbY.setRange(10, 900)
		self.sbY.setValue(self.rects[0]['y'])
		self.sbY.valueChanged[int].connect(self.changeValue)
		
		self.sbH = QSpinBox(self)
		self.sbH.setRange(10, 900)
		
		self.sbH.setValue(self.rects[0]['h'])
		self.sbH.valueChanged[int].connect(self.changeValue)
		
		mainlo = QVBoxLayout(self)
		hbox = QHBoxLayout(self)
		self.characters = [
		'tirralion',
		# 'secundus',
		# 'primus'
		]
		# self.characters = ['notepad']
		self.labelsName = []
		self.labelsImage = []
		self.hwnds = []
		

		for char in self.characters:
			hwnd = main.get_hwnd(char)
			self.hwnds.append(hwnd)
			vbox = QVBoxLayout(self)
			lblText = QLabel(self)
			lblText.setText(char)
			self.labelsName.append(lblText)
			lblImage = QLabel(self)
			self.labelsImage.append(lblImage)
			
			vbox.addWidget(lblText)
			vbox.addWidget(lblImage)
			hbox.addLayout(vbox)
                
		self.timer = QTimer()
		self.timer.timeout.connect(self.onTimer)
		self.timer.start(300)
		mainlo.addWidget(self.toggleButton)
		mainlo.addWidget(self.cb)
		mainlo.addWidget(self.sbX)
		mainlo.addWidget(self.sbW)
		mainlo.addWidget(self.sbY)
		mainlo.addWidget(self.sbH)
		mainlo.addLayout(hbox)
		self.setLayout(mainlo)

	def showDialog(self):
		text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

		if ok:
			self.onRefresh(text)
			
	def changeValue(self):
		self.rects[0]['x'] = self.sbX.value()
		self.rects[0]['w'] = self.sbW.value()
		self.rects[0]['y'] = self.sbY.value()
		self.rects[0]['h'] = self.sbH.value()
		

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
		
		if isVisible:
			qDebug("Visible")
			self.setWindowFlags(flags | QtCore.Qt.FramelessWindowHint);
			self.show();
		else:
			qDebug("Invisible")
			self.setWindowFlags(flags ^ QtCore.Qt.FramelessWindowHint);
			self.show()
			
		
		
			
	def onRefresh(self, name):
		im = main.screenshot(name)
		im = im.convert("RGBA")
		image = ImageQt(im)
		pixmap = QPixmap.fromImage(image)
		self.lbl.setPixmap(pixmap.scaled(400, 300))
		
	def onTimer(self):
		for i in range(0,1):
			pixmap = self.screen.grabWindow(self.hwnds[i],
										self.rects[i]['x'],
										self.rects[i]['y'],
										self.rects[i]['w'],
										self.rects[i]['h'])
											  
				
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
				
			self.labelsImage[0].setPixmap(pixmap)
		
		


qb = MessageBox()
qb.show()
sys.exit(app.exec_())
