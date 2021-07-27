import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, center
from missions import *


swarm_count = 10

groups = Groups(swarm_count)

swarms = []

for i in range(swarm_count):
	swarm = Swarm(i,0,0,0,0)
	swarms.append(swarm)



class MissionLogs(QTableWidget):


	def __init__(self):
		super().__init__()

		self.setAccessibleDescription("asdsad")
		self.pastLogs = 0

		self.setStyleSheet("background-color : lightblue")
		self.setRowCount(self.pastLogs+10)
		self.setEditTriggers(QAbstractItemView.NoEditTriggers )
		self.setColumnCount(2)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)


		self.init_labels()

		#Table will fit the screen horizontally

		self.horizontalHeader().setStretchLastSection(True)
		self.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)



		
	
	def init_labels(self):

		self.labels = ["Görev Adı" , "Görev Özeti"]

		for i in range(len(self.labels)):

			tableitem = QTableWidgetItem(self.labels[i])

			tableitem.setBackground(QtGui.QColor(125, 0, 0, 127))
			tableitem.setTextAlignment(Qt.AlignCenter)

			self.setItem(0,i,tableitem)
					

class Table(QTableWidget):
	def __init__(self):
		super().__init__()


		self.setStyleSheet("background-color : lightblue")
		self.setRowCount(swarm_count+1)
		self.setEditTriggers(QAbstractItemView.NoEditTriggers )
		self.setColumnCount(7)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)


		self.init_labels()

		#Table will fit the screen horizontally

		self.horizontalHeader().setStretchLastSection(True)
		self.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)



		
	
	def init_labels(self):

		self.labels = ["Drone NO" , "Aktif" , "X ","Y ","Z","Batarya","Grup"]

		self.swarminfos = []

		for i in range(swarm_count):

			list = swarms[i].getList()

			for j in range(len(self.labels)):
				tableitem = QTableWidgetItem(list[j])

				self.setItem(i+1,j,tableitem)


		

		

		for i in range(len(self.labels)):

			tableitem = QTableWidgetItem(self.labels[i])

			self.setItem(0,i,tableitem)
			

class PositionForm(QHBoxLayout):
	def __init__(self):
		super().__init__()
		
		x = QFormLayout()
		self.xPos = QLineEdit()
		x.addRow("X :", self.xPos)


		y = QFormLayout()
		self.yPos = QLineEdit()
		y.addRow("Y : ",self.yPos)

		z = QFormLayout()
		self.zPos = QLineEdit()
		z.addRow("Z :",self.zPos)

		self.addLayout(x)
		self.addLayout(y)
		self.addLayout(z)

		self.setSpacing(30)

		


		
	
		



		
class Form_SetFormation(QFormLayout):
	def __init__(self,dialog):

		super().__init__()

		self.setVerticalSpacing(40) 

		self.dialog = dialog 

		# formasyon şeçimi
		self.formations = {"Üçgen" : 3, "Kare" : 4 , "Beşgen " : 5 , "Altıgen" : 6 , "Yedigen" : 7 , "Sekizgen" : 8, "Dokuzgen" : 9 , "Ongen" : 10}
		self.cb = QComboBox()
		for i in self.formations:
			self.cb.addItem(i)
		self.addRow(QLabel("Formasyon : "), self.cb)
		
		
		# Center (x , y , z) seçimi
		self.positionform = PositionForm()
		self.addRow("Merkez : ",self.positionform)

		# Center (x , y , z) seçimi
		self.distance = QLineEdit()
		self.addRow("Swarmlar arası uzaklık : ",self.distance)

		#grup seçimi
		self.group = QLineEdit()
		self.group.setText("0")
		self.addRow(QLabel("Grup : " ) , self.group)

		#submit ve close buttonu
		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonbox.accepted.connect(self.submit)
		buttonbox.rejected.connect(self.CloseDialog)
		self.addWidget(buttonbox)

	def submit(self):

		#################################
		formation = SetFormation(self.positionform.xPos.text(),self.positionform.yPos.text(),self.positionform.zPos.text(),self.cb.currentText(),self.distance.text(),self.group.text())
		#################################

		self.CloseDialog()
		
	def CloseDialog(self):
		self.dialog.close()


class Form_Hareket(QFormLayout):
	def __init__(self,dialog):

		super().__init__()

		self.setVerticalSpacing(40) 

		self.dialog = dialog 
		
		
		# Center (x , y , z) seçimi
		self.positionform = PositionForm()
		self.addRow("Hedef : ",self.positionform)

		#grup seçimi
		self.group = QLineEdit()
		self.group.setText("0")
		self.addRow(QLabel("Grup : " ) , self.group)

		#submit ve close buttonu
		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonbox.accepted.connect(self.submit)
		buttonbox.rejected.connect(self.CloseDialog)
		self.addWidget(buttonbox)

	def submit(self):

		hareket = SetHareket(self.positionform.xPos.text(),self.positionform.yPos.text(),self.positionform.zPos.text(),self.group.text())

		self.CloseDialog()
		
		
	def CloseDialog(self):
		self.dialog.close()

def asd():
	print("a")
		
class Form_Split(QFormLayout):
	def __init__(self, dialog):
		super().__init__()


		
		self.dialog = dialog


		self.cb = QComboBox()

		

		self.cb.setMaximumWidth(100)

		

		for i in range(len(groups.groups)):
			self.cb.addItem("              " + str(i))
		self.addRow(QLabel("Group : "), self.cb)

		self.cb.currentTextChanged.connect(self.CreateGroupsBox)
		
		self.CreateGroupsBox()
		
		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonbox.accepted.connect(self.submit)
		buttonbox.accepted.connect(asd)
		buttonbox.rejected.connect(self.CloseDialog)
		self.addWidget(buttonbox)

	def submit(self):

		group = int(self.cb.currentText())

		new_group = []

		for i in range(len(groups.groups[group])):
			if self.bs[i].isChecked():
				new_group.append(groups.groups[group][i])

		
		groups.SplitGroup(group,new_group)


		self.CloseDialog()
		
		
	def CloseDialog(self):


		self.dialog.close()

	def CreateGroupsBox(self):
		self.layout = QHBoxLayout()
		
		self.layout.setAlignment(Qt.AlignCenter)

		self.bs = []

		group = int(self.cb.currentText())

		for i in groups.groups[group]:

			sbox = QVBoxLayout()
			b = QRadioButton(str(i))
			self.bs.append(b)
			sbox.addWidget(b)
			box = QGroupBox()
			box.setLayout(sbox)
			self.layout.addWidget(box)
		
		self.removeRow(1)
		self.insertRow(1,"Group :",self.layout)

class Form_Assemble(QFormLayout):
	def __init__(self, dialog):
		super().__init__()		
		self.dialog = dialog


		self.first = QComboBox()
		self.second = QComboBox()

		for i in range(len(groups.groups)):
			self.first.addItem(str(i))
			self.second.addItem(str(i))


		self.addRow("Eski Grup :" , self.first)
		self.addRow("Yeni Grup :" ,self.second)

		
		
		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonbox.accepted.connect(self.submit)
		buttonbox.rejected.connect(self.CloseDialog)
		self.addWidget(buttonbox)

	def submit(self):

		group_f = int(self.first.currentText())
		group_s = int(self.second.currentText())

		groups.AppendGroups(group_f,group_s)


		self.CloseDialog()
		
		
	def CloseDialog(self):
		self.dialog.close()

	

	




class buttons(QGridLayout):


	def __init__(self):
		super().__init__()
		
		buttons = [["Formasyon ",0,0] , ["Hareket ",0,1] , ["Trajectory",1,0] , ["Sürü Ayırma",1,1] , ["Sürü Birleştirme" , 2 ,0] , ["İHA Ayırma / Ekleme" , 2, 1]]

		buttonIdle = "QPushButton{background-color: lightblue;border-style: outset;border-width: 2px;border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em;padding: 6px;} "
		buttonPressed = "QPushButton::pressed{background-color : black;color : white}"
		buttonHover = "QPushButton::hover{background-color : yellow}"
	

		self.buttons = []

		for index in buttons:
			button = QPushButton(index[0])
			button.setStyleSheet(buttonIdle + buttonPressed + buttonHover)

			self.buttons.append(button)
			self.addWidget(button,index[1],index[2])


		self.setVerticalSpacing(100)

		self.rowStretch(10)

		self.buttons[0].clicked.connect(self.mission_SetFormation)
		self.buttons[1].clicked.connect(self.mission_hareket)
		
		self.buttons[3].clicked.connect(self.mission_split)
		self.buttons[4].clicked.connect(self.mission_assemble)

	def mission_assemble(self):
		dialog = QDialog()
		form = Form_Assemble(dialog)
		self.CreateDialog(form,dialog)

	
	def mission_SetFormation(self):

		dialog = QDialog()
		form = Form_SetFormation(dialog)
		self.CreateDialog(form,dialog)
	
	def mission_hareket(self):
		dialog = QDialog()
		form = Form_Hareket(dialog)
		self.CreateDialog(form,dialog)

	def mission_split(self):
		dialog = QDialog()
		form = Form_Split(dialog)
		self.CreateDialog(form,dialog)

		

	def CreateDialog(self , form,dialog):
		
		dialog.resize(400,400)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.setLayout(form)
		dialog.exec_()










class Window(QWidget):
	def __init__(self):
		super().__init__()
		self.title = "PyQt5 Frame"
		self.resize(1920,1080)
		self.setWindowTitle(self.title)
		self.setStyleSheet('background-color:#393E46')

		hbox = QHBoxLayout()
		
		vbox = QVBoxLayout()


		#table
		table = Table()
		tableLayout = QHBoxLayout()
		tableLayout.addWidget(table)
		tablebox = QGroupBox()
		tablebox.setLayout(tableLayout)



		#buttons
		btns = buttons()
		btnLayout = QVBoxLayout()
		btnLayout.addLayout(btns)
		btnbox = QGroupBox()
		btnbox.setLayout(btnLayout)
		btnbox.setMinimumHeight(300)


		#video Player
		videoPlayerLayout = QVBoxLayout()
		videoPlayerbox = QGroupBox()
		videoPlayerbox.setLayout(videoPlayerLayout)
		videoPlayerbox.setMinimumWidth(960)


		#Mission Log + Groups
		logLayout = QHBoxLayout()

		missionLog = MissionLogs()
		grouptable = QTableWidget()
		logLayout.addWidget(missionLog)
		logLayout.addWidget(grouptable)
		logbox = QGroupBox()
		logbox.setLayout(logLayout)
		logbox.setMinimumHeight(240)
		
		



		#set-up
		hbox.addWidget(videoPlayerbox)
		vbox.addWidget(btnbox)
		vbox.addWidget(logbox)
		vbox.addWidget(tablebox)
		hbox.addLayout(vbox)
		self.setLayout(hbox)
		self.showMaximized()



		
	


if __name__=="__main__":

	App = QApplication(sys.argv)
	window = Window()
	sys.exit(App.exec())