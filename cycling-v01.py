#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math, time, signal
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

class Example(QWidget):

	sizeWindow = 700
	radius = sizeWindow/2
	delta = -3
	rotation = 0
	dots = 4
	speed = 100

	def __init__(self):
		super(Example, self).__init__()
		self.setGeometry(100, 100, self.sizeWindow, self.sizeWindow)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		#self.setWindowOpacity(0.1)

		action1 = QAction("E&xit", self, 
								shortcut="Ctrl+Q",
								triggered=qApp.quit)
		action2 = QAction("Dots+1", self, 
								shortcut="Ctrl+D",
								triggered=self.incrementDots)
		action3 = QAction("Dots-1", self, 
								shortcut="Ctrl+S",
								triggered=self.decrementDots)
		action4 = QAction("Speed+", self, 
								shortcut="Ctrl+R",
								triggered=self.incrementSpeed)
		action5 = QAction("Speed-", self, 
								shortcut="Ctrl+E",
								triggered=self.decrementSpeed)

		self.addAction(action1)
		self.addAction(action2)
		self.addAction(action3)
		self.addAction(action4)
		self.addAction(action5)

		self.setContextMenuPolicy(Qt.ActionsContextMenu)
		
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.Time)
		self.timer.start(self.speed)
		self.show()

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawChord(qp)
		qp.end()

	def incrementDots(self):
		self.dots = self.dots + 1

	def decrementDots(self):
		self.dots = self.dots - 1

	def incrementSpeed(self):
		self.speed = self.speed - 10

	def decrementSpeed(self):
		self.speed = self.speed + 10


	def drawChord(self, qp):
		qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
		centre = self.sizeWindow / 2
		for i in range (0, self.dots-1):
			alfa = i * 2 * math.pi / self.dots + self.rotation
			x1 = centre + math.cos(alfa) * self.radius
			y1 = centre + math.sin(alfa) * self.radius
			for j in range (i, self.dots):
				alfa = j * 2 * math.pi / self.dots + self.rotation
				x2 = centre + math.cos(alfa) * self.radius
				y2 = centre + math.sin(alfa) * self.radius
				qp.drawLine(x1, y1, x2, y2)

	def redrawLine(self):
		if self.radius == self.sizeWindow / 2:
			self.delta = -5
		elif self.radius == 0:
			self.delta = 5
		self.radius = self.radius + self.delta
		self.rotation = self.rotation + self.delta/(self.speed*2)
		self.update()

	def Time(self):
		self.redrawLine()
		
	def keyPressEvent(self, event):	
		if event.key() == Qt.Key_Escape:
			self.close()

	def mousePressEvent(self, event):
		if (event.button() == Qt.LeftButton):
			self.drag_position = event.globalPos() - self.pos();
			event.accept();
 
	def mouseMoveEvent(self, event):
		if (event.buttons() == Qt.LeftButton):
			self.move(event.globalPos().x() - self.drag_position.x(),
				event.globalPos().y() - self.drag_position.y());
			event.accept(); 





def sigint_handler(*args):
	"""Handler for the SIGINT signal."""
	QApplication.quit()


def main():
    signal.signal(signal.SIGINT, sigint_handler)
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    

