import sys
import signal
from typing import List
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, center,QTimer,QDateTime
from PyQt5.sip import simplewrapper

from commander import *
from munkres import Munkres
from formation import *
from utils import *
import os

class Map(QWidget):
    def __init__(self,form,size = 800):
        super().__init__()
        self.size = size
        self.resize(size,size)
        self.points = []
        self.lines = []
        self.form = form
        for i in range(0,size,40):
            self.lines.append([0,i,size,i])
            self.lines.append([i,0,i,size])

       

    def mousePressEvent(self, e):
        if e.pos().x()> self.size or e.pos().y() > self.size:
            return
        if e.pos().x()%40 < 20:
            x = e.pos().x() - e.pos().x() % 40
        else:
            x = e.pos().x() + 40 - e.pos().x() % 40
        if e.pos().y()%40 < 20:
            y = e.pos().y() - e.pos().y() % 40
        else:
            y = e.pos().y() + 40 - e.pos().y() % 40
			
        if self.points.count([x-5,y-5]) > 0 :
            self.points.remove([x-5,y-5])
        else:
            self.points.append([x-5,y-5])
        self.form.pos = []
        self.form.pos = self.points
        self.form.update_pos()
        self.update()

    def paintEvent(self, ev):
        qp = QtGui.QPainter(self)
 
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        penC = QtGui.QPen(Qt.green,8)
        penP = QtGui.QPen(Qt.red, 5)
        penL = QtGui.QPen(Qt.black, 3)
        brush = QtGui.QBrush(Qt.red)
        
        qp.setBrush(brush)
        qp.setPen(penL)
        for i in self.lines:
            qp.drawLine(i[0],i[1],i[2],i[3])
        qp.setPen(penC)
        qp.drawLine(0,self.size/2,self.size,self.size/2)
        qp.drawLine(self.size/2,0,self.size/2,self.size)

        penB = QtGui.QPen(Qt.blue,8)
        qp.setPen(penB)
        for uav in uav_list:
            if uav.info["Aktif"] == "Evet":
                qp.drawEllipse(400+(uav.PoseX*100)-5,400+(uav.PoseY*100)-5,10,10)


        qp.setPen(penP)
        for i in self.points:
            qp.drawEllipse(i[0],i[1], 10, 10)

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
		self.setRowCount(MAX_UAV_NUMBER)
		self.setEditTriggers(QAbstractItemView.NoEditTriggers )
		self.setColumnCount(7)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)


		self.init_labels()

		#Table will fit the screen horizontally

		self.horizontalHeader().setStretchLastSection(True)
		self.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)



		
	
	def init_labels(self):

		self.labels = list(uav_list[0].info.keys())

		self.swarminfos = []

		for i in range(len(self.labels)):

			tableitem = QTableWidgetItem(self.labels[i])

			tableitem.setBackground(QtGui.QColor(125, 0, 0, 125))

			self.setItem(0,i,tableitem)

			tableitem.setTextAlignment(Qt.AlignCenter)

	def update_labels(self):


		for i in range(MAX_UAV_NUMBER):

			tlist = list(uav_list[i].info.values())
			
			for j in range(len(self.labels)):


				if type(tlist[j]) != str:

					tableitem = QTableWidgetItem(str(round(tlist[j],4)))
				
				
				else : 
					tableitem = QTableWidgetItem(str(tlist[j]))
					
				if tlist[j] == "Hayır":
					tableitem.setBackground(QtGui.QColor(255, 0, 0,125))
				elif tlist[j] == "Evet":
					tableitem.setBackground(QtGui.QColor(0, 255, 0,125))

				tableitem.setTextAlignment(Qt.AlignCenter)
				

				self.setItem(i+1,j,tableitem)
			

class PositionForm(QHBoxLayout):
	def __init__(self):
		super().__init__()
		
		x = QFormLayout()
		self.xPos = QLineEdit()
		self.xPos.setText("0")
		x.addRow("X :", self.xPos)


		y = QFormLayout()
		self.yPos = QLineEdit()
		self.yPos.setText("0")
		y.addRow("Y : ",self.yPos)

		z = QFormLayout()
		self.zPos = QLineEdit()
		self.zPos.setText("1.0")
		z.addRow("Z :",self.zPos)

		self.addLayout(x)
		self.addLayout(y)
		self.addLayout(z)

		self.setSpacing(30)

		


		
	
class Form_Connect(QFormLayout  ):
	def __init__(self,dialog):

		super().__init__()



		self.swarm_count = 1

		self.dialog = dialog 

		self.URIS = []

		self.Lines = []

		tmp = QLineEdit()
		tmp.setText("radio://0/XX/2M/E7E7E7E7XX")
		self.Lines.append(tmp)
		self.addRow("URI1 : ", tmp)

		addButton = QPushButton("Swarm Ekle")
		addButton.setMaximumWidth(100)
		addButton.clicked.connect(self.AddSwarm)

		rmButton = QPushButton("Swarm Çıkar")
		rmButton.setMaximumWidth(100)
		rmButton.clicked.connect(self.RemoveSwarm)

		loadButton = QPushButton("Önceki URI yükle")
		loadButton.setMaximumWidth(150)
		loadButton.clicked.connect(self.LoadURI)

		hbox = QHBoxLayout()
		hbox.addWidget(addButton)
		hbox.addWidget(rmButton)
		hbox.addWidget(loadButton)

		self.addRow(hbox)
		self.setVerticalSpacing(10)
		

		#submit ve close buttonu
		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonbox.accepted.connect(self.submit)
		buttonbox.rejected.connect(self.CloseDialog)
		self.addWidget(buttonbox)

	def AddSwarm(self):
		self.AddSwarmURI("radio://0/XX/2M/E7E7E7E7XX") # default URI

	def AddSwarmURI(self,uri):
		tmp = QLineEdit()
		tmp.setText(uri)
		self.Lines.append(tmp)
		self.insertRow(self.swarm_count,"URI"+str(self.swarm_count+1),tmp)
		self.swarm_count +=1

	def RemoveSwarm(self):

		del self.Lines[-1]
		self.removeRow(self.swarm_count-1)
		self.swarm_count -=1

	def RemoveSwarmAll(self):
		while self.Lines:
			del self.Lines[-1]
			self.removeRow(self.swarm_count-1)
			self.swarm_count -=1

	def LoadURI(self):
		if os.path.exists("config/URIs.txt") and os.stat("config/URIs.txt").st_size:
			#cleaning
			self.RemoveSwarmAll()
			with open("config/URIs.txt","r") as f:
				uri = "ss" # no meaning other than saitss
				for uri in f.readlines():
					print(uri)
					self.AddSwarmURI(uri)
		else:
			msg = QMessageBox()
			msg.setWindowTitle("BRUH MOMENT")
			msg.setText("Konfigürasyon dosyası bozuk")
			msg.exec_()

	def submit(self):

		for lines in self.Lines:
			self.URIS.append(lines.text())

		with open("config/URIs.txt","w+") as f:
			for uri in self.URIS:
				f.write(uri)
				f.write("\n")

		groups.init_group(len(self.Lines))


		commander.init_swarm(self.URIS)


		self.CloseDialog()
		
		
		
	def CloseDialog(self):
		self.dialog.close()





		
class Form_SetFormation(QFormLayout):
	def __init__(self,dialog):

		super().__init__()

		self.setVerticalSpacing(40) 

		self.dialog = dialog 

		# formasyon şeçimi
		
		self.cb = QComboBox()
		for i in formations.formations:
			self.cb.addItem(i)
		self.addRow(QLabel("Formasyon : "), self.cb)
		
		
		# Center (x , y , z) seçimi
		self.positionform = PositionForm()
		self.addRow("Merkez : ",self.positionform)


		self.distance = QLineEdit()
		self.distance.setText("1.0")
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

		group = groups.groups[int(self.group.text())]
		distance = float(self.distance.text())
		center_x = float(self.positionform.xPos.text())
		center_y = float(self.positionform.yPos.text())
		center_z = float(self.positionform.zPos.text())
		print(center_x,center_y,center_z)
		formation_side = formations.formations[self.cb.currentText()]

		#################################
		formation = Formation()
		formation.Cokgen(max(formation_side,len(group)), distance , formation_side , Pose(center_x,center_y,center_z))
		poses = formation.GetSides()
	
		#################################

		initial_cost = []
		uav_ids = []
		for uav in uav_list:
			if uav.info["Aktif"] == "Evet" and uav.info["Grup"] == int(self.group.text()):
				dist = []
				uav_ids.append(uav.info["Drone No"])
				for pose in poses:
					dist.append(uav.distance_to_dest([pose[0] , pose[1] , pose[2]]))
				initial_cost.append(dist)


		hungarian = Munkres()

		indexes = hungarian.compute(initial_cost)

		for index in indexes:
			uav_id = uav_ids[index[0]]
			pose = poses[index[1]]
			uav_list[uav_id].SetDest(pose[0],pose[1],pose[2])
			print(uav_id , pose)


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


		
class Form_Split(QFormLayout):
	def __init__(self, dialog ):
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

class ConnectButtons(QHBoxLayout):
	def __init__(self , swarm_count):
		super().__init__()

		for i in range(swarm_count):
			button = QPushButton("Connect Drone " + str(i))
			self.addWidget(button)

class MapLayout(QHBoxLayout):
	def __init__(self , dialog):
		super().__init__()
		Mbox = QGroupBox() 
		Mvbox = QVBoxLayout()
		self.dialog = dialog

		self.pos = []
		self.calculatedposes = []
		self.labels = []
		self.count = 0

		map = Map(self)
		map.setMinimumWidth(800)
		map.setMaximumHeight(800)
		Mvbox.addWidget(map)
		Mbox.setLayout(Mvbox)
		self.addWidget(Mbox)

		box = QGroupBox()
		self.form = QFormLayout()
		self.form.setAlignment(Qt.AlignCenter)



		self.name = QLineEdit()
		self.name.setText("Formasyon " +str(len(formations.formations)))
		self.name.setAlignment(Qt.AlignCenter)
		self.form.addRow("Formasyon İsmi",self.name)

		self.height = QLineEdit()
		self.height.setText("1.0")
		self.height.setMaximumWidth(100)
		self.height.setAlignment(Qt.AlignCenter)
		self.form.addRow("Yükseklik",self.height )

		self.uzaklık = QLineEdit()
		self.uzaklık.setText("0.5")
		self.uzaklık.setMaximumWidth(100)
		self.uzaklık.setAlignment(Qt.AlignCenter)
		self.form.addRow("İki grid arası uzaklık",self.uzaklık)





		calculate = QPushButton("Hesapla")
		self.form.addRow(calculate)
		calculate.clicked.connect(self.calculate)

		self.form.setVerticalSpacing(20)

		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonbox.accepted.connect(self.submit)
		buttonbox.rejected.connect(self.CloseDialog)


		self.form.addWidget(buttonbox)

		box.setLayout(self.form)		
		self.addWidget(box)


	def calculate(self):
		try :
			float(self.uzaklık.text())
			self.update_pos()
		except:
			self.uzaklık.setText("Lütfen Sayı Giriniz")
		
	
	def update_pos(self):

		for i in self.labels:
			self.form.removeRow(i)

		self.labels = []
		#self.pos.sort()
		self.calculatedposes = []
		for i in self.pos:
			x = (i[0] - 395)/40 * float(self.uzaklık.text())
			y = -(i[1] - 395)/40 * float(self.uzaklık.text())
			self.calculatedposes.append([x,y])
			label = QLabel("Pos " + str(self.pos.index(i)) + " :     X  :" + str(x)  + "     Y :" + str(y))
			self.form.addRow(label)
			self.labels.append(label)
	def submit(self):


		i = 0
		for pose in self.calculatedposes :
			uav_list[i].SetDest(pose[0],pose[1],self.height.text())
			i+=1

		self.CloseDialog()

		initial_cost = []
	
		for uav in uav_list:
			if uav.info["Aktif"] == "Evet":
				dist = []
				for pose in self.calculatedposes:
					dist.append(uav.distance_to_dest([float(pose[0]),float(pose[1]),float(self.height.text())]))
				initial_cost.append(dist)


		hungarian = Munkres()

		indexes = hungarian.compute(initial_cost)

		for index in indexes : 
			uav_list[index[0]].SetDest(self.calculatedposes[index[1]][0],self.calculatedposes[index[1]][1],self.height.text())



		
		
	def CloseDialog(self):
		self.dialog.close()
		
		





class buttons(QGridLayout):


	def __init__(self):
		super().__init__()

		
		buttons = [["Bağlantıyı kur",0,0],["Bağlantıyı kes",0,1] , ["Yeni Formasyon",0,2] ,  ["Formasyon ",1,0] , ["Hareket ",1,1] , ["Trajectory",1,2] , ["Sürü Ayırma",2,0] , ["Sürü Birleştirme" , 2 ,1] , ["İHA Ayırma / Ekleme" , 2, 2]]

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

		self.buttons[0].clicked.connect(self.drone_connect)
		self.buttons[1].clicked.connect(self.drone_dissconnect)
		self.buttons[2].clicked.connect(self.create_Formation)

		self.buttons[3].clicked.connect(self.mission_SetFormation)
		self.buttons[4].clicked.connect(self.mission_hareket)
		
		self.buttons[6].clicked.connect(self.mission_split)
		self.buttons[7].clicked.connect(self.mission_assemble)

	def drone_connect(self):
		dialog = QDialog()
		form = Form_Connect(dialog)
		self.CreateDialog(form,dialog)

	def drone_dissconnect(self):
		for uav in uav_list:
			uav.info["Aktif"] = "Hayır"


	def create_Formation(self):
		dialog = QDialog()
		form = MapLayout(dialog)
		self.CreateDialog2(form,dialog)

	


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

	def CreateDialog2(self , form,dialog):
		
		dialog.resize(1200,1000)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.setLayout(form)
		dialog.exec_()		

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



		#table + connect buttons
		self.table = Table()
		tableLayout = QHBoxLayout()

		tablebox = QGroupBox()
		tableLayout.addWidget(self.table)
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

		self.initTimer()

	def initTimer(self):
		self.timer=QTimer()
		self.timer.timeout.connect(self.showTime)
		self.timer.start(40)

	def showTime(self):
		self.table.update_labels()

def signal_handler(sig, frame):
	print('You pressed Ctrl+C!')
	curr = datetime.datetime.now()
	idx = 0
	while idx < logs:
		with open("logs/"+str(curr)+str(idx),"w+") as f:
			#f.write("Starting!")
			f.write("X,Y,Z,Vx,Vy,Vz, idx"+str(idx) + "\n")
			f.write(logs[idx])
			print("X,Y,Z,Vx,Vy,Vz, idx"+str(idx))
			print(logs[idx])
		idx+=1
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


App = QApplication(sys.argv)
w = Window()
sys.exit(App.exec())

	



