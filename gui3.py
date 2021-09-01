import sys
import signal
from typing import List
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, center,QTimer,QDateTime
from PyQt5.sip import simplewrapper

from commander import *
from formations import *
from munkres import Munkres
from formation import *
from formation_utils import *
import os
App = QApplication(sys.argv)
from simulation import *
from Utils import *

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
        for uav in uavList:
            if uav.info["Bağlı"] == "Evet":
                qp.drawEllipse(400+(uav.info["X"]*100)-5,400-(uav.info["Y"]*100)-5,10,10)


        qp.setPen(penP)
        for i in self.points:
            qp.drawEllipse(i[0],i[1], 10, 10)

class MapTrajectory(QWidget):
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
		penY = QtGui.QPen(Qt.yellow, 3)
		penB = QtGui.QPen(Qt.blue,50)
		brush = QtGui.QBrush(Qt.red)

		qp.setBrush(brush)
		qp.setPen(penL)
		for i in self.lines:
			qp.drawLine(i[0],i[1],i[2],i[3])
		qp.setPen(penC)
		qp.drawLine(0,self.size/2,self.size,self.size/2)
		qp.drawLine(self.size/2,0,self.size/2,self.size)



		qp.setPen(penP)
		for i in self.points:
			qp.drawEllipse(i[0],i[1], 10, 10)


		if len(self.points) > 1:
			qp.setPen(penB)
			qp.drawText(self.points[0][0],self.points[0][1],"Başlangıç")
			qp.drawText(self.points[-1][0],self.points[-1][1],"Son")
			qp.setPen(penY)
			for i in range(1,len(self.points)):
				start = self.points[i-1]
				end = self.points[i]
				qp.drawLine(end[0]+5,end[1]+5,start[0]+5,start[1]+5)



class MissionLogs(QWidget):


	def __init__(self):
		super().__init__()

		self.setStyleSheet("background-color : lightblue")
		self.textEdit = QTextEdit()
		self.textEdit.setReadOnly(True)

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.textEdit)
	
		self.text = ""
		self.textEdit.setPlainText(self.text)

		self.timer = QTimer()
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.CheckUp)
		self.timer.start()

	def UpdateConsole(self,text):
		self.text+=text
		self.textEdit.append(text)
	
	def CheckUp(self):
		console = CheckUpdate()
		if console != "":
			print(console)
			self.UpdateConsole(console + "\n")

class GroupInfos(QTableWidget):


	def __init__(self):
		super().__init__()


		self.row_count = len(groups.groups) + 1

		self.circle_infos = ["Hayır"] * 10 # Hack, ilerde değiştir

		self.labels = ["Daire" , "Grup No" , "Dronelar" , "Formasyon" , "Formasyon Merkezi"]

		self.setStyleSheet("background-color : lightblue")
		self.setRowCount(self.row_count)
		self.setEditTriggers(QAbstractItemView.NoEditTriggers )
		self.setColumnCount(len(self.labels))
		
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

		self.setFont(QtGui.QFont('Arial', 13))

		self.init_labels()

		#Table will fit the screen horizontally

		self.horizontalHeader().setStretchLastSection(True)
		self.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)


	def StartCircle(self , group):
		
		center = groups.formation_info[group]
		for tmp_group in groups.groups[group]:
			uavList[tmp_group].StartCircle([center[2],center[3],center[4]]  )
		pass # TO-DO

	def StopCircle(self,group):
		for tmp_group in groups.groups[group]:
			uavList[tmp_group].StopCircle( )

	def Circle(self,x,y):
		
		if x==0 or y != 0:
			return
		elif groups.formation_info[x-1][0] == "Yok":
			self.circle_infos[x-1] == "Hayır"
			return
		else :

			if self.circle_infos[x-1] == "Hayır" :
				self.circle_infos[x-1] = "Evet"
				self.StartCircle(x-1)
			else :
				self.circle_infos[x-1] = "Hayır"
				self.StopCircle(x-1)

 

		
	def init_labels(self):
		self.cellClicked.connect(self.Circle)

		self.circle_buttons = []
		for i in range(len(self.labels)):

			tableitem = QTableWidgetItem(self.labels[i])

			tableitem.setBackground(QtGui.QColor(125, 0, 0, 127))
			tableitem.setTextAlignment(Qt.AlignCenter)

			self.setItem(0,i,tableitem)

	def AddRadioButton(self):

		self.row_count = len(groups.groups) + 1

		self.setRowCount(self.row_count)

		

	def RemoveRow(self):

		


		self.removeRow(self.row_count - 1 )

		self.row_count =  len(groups.groups) + 1 
		
	def UpdateLabels(self):


		

		if(self.row_count < len(groups.groups) + 1 ):
			self.AddRadioButton()

		if(self.row_count > len(groups.groups) +1 ) :
			self.RemoveRow()

		i = 1

		

		for group in groups.groups:

			table_circle = QTableWidgetItem(self.circle_infos[i-1])
			table_circle.setTextAlignment(Qt.AlignCenter)
			if self.circle_infos[i-1] == "Evet":
				table_circle.setBackground(QtGui.QColor(0, 255, 0,125))
			else :
				table_circle.setBackground(QtGui.QColor(255, 0, 0,125))
			self.setItem(i,0,table_circle)
			
			table_group_no = QTableWidgetItem(str(i-1))
			table_group_no.setTextAlignment(Qt.AlignCenter)
			self.setItem(i,1,table_group_no)

			table_drone_no = QTableWidgetItem(str(group)[1:-1])
			table_drone_no.setTextAlignment(Qt.AlignCenter)
			self.setItem(i,2,table_drone_no)

			table_formation = QTableWidgetItem(str(groups.formation_info[i-1][0]))
			table_formation.setTextAlignment(Qt.AlignCenter)
			self.setItem(i,3,table_formation)
		

			table_center = QTableWidgetItem(str(groups.formation_info[i-1][1]))
			table_center.setTextAlignment(Qt.AlignCenter)
			self.setItem(i,4,table_center)
			

			i+=1
			

					

class Table(QTableWidget):
	def __init__(self):
		super().__init__()
		
		self.setStyleSheet("background-color : lightblue")
		self.setRowCount(Max_Uav_Number)
		self.setEditTriggers(QAbstractItemView.NoEditTriggers )
		self.setColumnCount(8)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)


		self.init_labels()

		#Table will fit the screen horizontally

		self.horizontalHeader().setStretchLastSection(True)
		self.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)



		
	
	def init_labels(self):

		self.labels = list(uavList[0].info.keys())

		self.swarminfos = []

		for i in range(len(self.labels)):

			tableitem = QTableWidgetItem(self.labels[i])

			tableitem.setBackground(QtGui.QColor(125, 0, 0, 125))

			self.setItem(0,i,tableitem)

			tableitem.setTextAlignment(Qt.AlignCenter)

	def update_labels(self):


		for i in range(Max_Uav_Number):

			tlist = list(uavList[i].info.values())
			
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
	def __init__(self,dialog,load = None):

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
					uri = uri[:-1]
					self.AddSwarmURI(uri)
		else:
			msg = QMessageBox()
			msg.setWindowTitle("BRUH MOMENT")
			msg.setText("Konfigürasyon dosyası bozuk")
			msg.exec_()

	def submit(self):

		for lines in self.Lines:
			self.URIS.append(lines.text())

		with open("config/URIs.txt","w") as f:
			for uri in self.URIS:
				f.write(uri + "\n")

		groups.init_group(len(self.Lines))


		commander.init_swarm(self.URIS)


		self.CloseDialog()
		
		
		
	def CloseDialog(self):
		self.dialog.close()



		
class Form_SetFormation(QFormLayout):
	def __init__(self,dialog,load = None):
		print(load)
		super().__init__()
		self.setVerticalSpacing(40) 
		self.dialog = dialog 

		self.cb = QComboBox()
		for i in formations.formations:
			self.cb.addItem(i)

		# Center (x , y , z) seçimi
		self.positionform = PositionForm()
		
		self.distance = QLineEdit()
		self.distance.setText("1.0")
		#grup seçimi
		self.group = QLineEdit()
		

		if load is not None:
			self.cb.setCurrentIndex(load[0]) 
			self.positionform.xPos.setText(load[1][0]) 
			self.positionform.yPos.setText(load[1][1]) 
			self.positionform.zPos.setText(load[1][2]) 
			self.distance.setText(load[2])  
			self.group.setText(load[3])  
			self.addRow(QLabel("Formasyon : "), self.cb)
			self.addRow("Merkez : ",self.positionform)
			self.addRow("Swarmlar arası uzaklık : ",self.distance)
			self.addRow(QLabel("Grup : " ) , self.group)
		# formasyon şeçimi
		else:
			self.distance.setText("1.0")
			self.group.setText("0")
			self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
			self.buttonbox.accepted.connect(self.submit)
			self.buttonbox.rejected.connect(self.CloseDialog)
			self.addRow(QLabel("Formasyon : "), self.cb)
			self.addRow("Merkez : ",self.positionform)
			self.addRow("Swarmlar arası uzaklık : ",self.distance)
			self.addRow(QLabel("Grup : " ) , self.group)
			self.addWidget(self.buttonbox)

		



	def GetParam(self):

		return [self.cb.currentIndex(),[self.positionform.xPos.text(),self.positionform.yPos.text(),self.positionform.zPos.text()] , self.distance.text(),self.group.text()]

	def PopUp(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText( "Özel formasyonlar için Drone sayısı aynı olmak zorunda." )
		msg.exec_()

	def submit(self):
		
		group = groups.groups[int(self.group.text())]
		distance = float(self.distance.text())
		center_x = float(self.positionform.xPos.text())
		center_y = float(self.positionform.yPos.text())
		center_z = float(self.positionform.zPos.text())
		formation_side = formations.formations[self.cb.currentText()]

		if type(formation_side) == int :
			groups.SetFormationInfos(int(self.group.text()) , self.cb.currentText() , "X : " +str(center_x) +"  Y : " + str(center_y) + "  Z : " + str(center_z) , center_x,center_y,center_z)

			#################################
			formation = Formation()
			formation.Cokgen(max(formation_side,len(group)), distance , formation_side , Pose(center_x,center_y,center_z))
			poses = formation.GetSides()
		
			#################################
		else :
			poses = formation_side
			if len(poses) != len(group):
				self.PopUp()
				return

		
		initial_cost = []
		uav_ids = []
		for uav in uavList:
			if uav.info["Bağlı"] == "Evet" and uav.info["Grup"] == int(self.group.text()):
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
			uavList[uav_id].SetDest(pose[0],pose[1],pose[2])
			uavList[uav_id].SetDistanceToCenter( [center_x,center_y,center_z] , uavList[uav_id].GetDest())
			uavList[uav_id].SetState(State.GO)
	
		self.CloseDialog()
		
	def CloseDialog(self):
		self.dialog.close()


class Form_Hareket(QFormLayout):
	def __init__(self,dialog,load = None):

		super().__init__()
		self.setVerticalSpacing(40) 
		self.dialog = dialog 
		self.positionform = PositionForm()
		self.group = QLineEdit()
		
		if load is not None:
			self.positionform.xPos.setText(load[0][0]) 
			self.positionform.yPos.setText(load[0][1]) 
			self.positionform.zPos.setText(load[0][2]) 
			self.group.setText(load[1])  

		else:
			
			self.group.setText("0")
			#submit ve close buttonu
			self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
			self.buttonbox.accepted.connect(self.submit)
			self.buttonbox.rejected.connect(self.CloseDialog)
			self.addWidget(self.buttonbox)


		self.addRow("Hedef : ",self.positionform)
		self.addRow(QLabel("Grup : " ) , self.group)
		

	def GetParam(self):
		return [[self.positionform.xPos.text(),self.positionform.yPos.text(),self.positionform.zPos.text()] , self.group.text()]

	def submit(self):

		
		center_x = float(self.positionform.xPos.text())
		center_y = float(self.positionform.yPos.text())
		center_z = float(self.positionform.zPos.text())
		group = int(self.group.text())
	

		if group in groups.formation_info and groups.formation_info[group][0] != "Yok":
			old_center = groups.GetCenter(group)
			new_center = [center_x,center_y,center_z]
			groups.SetFormationInfos(group , groups.formation_info[group][0] , "X : " +str(center_x) +"  Y : " + str(center_y) + "  Z : " + str(center_z) , center_x,center_y,center_z)
			groups.SetCenter(group,new_center)
			for uav in groups.groups[group]:
				uavList[uav].CalculateNewCenter(old_center,new_center)
				uavList[uav].SetState(State.GO)
		else:
			self.PopUp()
			return
			


		self.CloseDialog()
		
		
	def CloseDialog(self):
		self.dialog.close()

	def PopUp(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText( "Grup formasyon oluşturmadı veya öyle bir grup yok." )
		msg.exec_()


		
class Form_Split(QFormLayout):
	def __init__(self, dialog , load = None ):
		super().__init__()
		
		self.bs = []
		
		self.dialog = dialog

		self.cb = QComboBox()
		for i in range(len(groups.groups)):
				self.cb.addItem("              " + str(i))

		self.cb.setMaximumWidth(100)

		if load is not None:
			self.cb.setCurrentIndex(load[0])
			self.CreateGroupsBox(load[1])
		else:
			
			self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
			self.buttonbox.accepted.connect(self.submit)
			self.buttonbox.rejected.connect(self.CloseDialog)
			self.addWidget(self.buttonbox)
			self.CreateGroupsBox()

		self.cb.currentTextChanged.connect(self.CreateGroupsBox)
		self.addRow(QLabel("Group : "), self.cb)
		

		


	def GetParam(self):
		bs =[]
		for i in self.bs:
			bs.append(i.isChecked())
		return [self.cb.currentIndex(),bs ]

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
	############################### İlerde Kesin Değiştir
	def CreateGroupsBox(self , load = [False] * 10):
		self.layout = QHBoxLayout()
		
		self.layout.setAlignment(Qt.AlignCenter)

		self.bs = []

		group = int(self.cb.currentText())
		i = 0
		for uav in groups.groups[group]:

			sbox = QVBoxLayout()
			b = QRadioButton(str(uav))
			b.setChecked(load[i])
			i+=1
			self.bs.append(b)
			sbox.addWidget(b)
			box = QGroupBox()
			box.setLayout(sbox)
			self.layout.addWidget(box)
		
		self.removeRow(1)
		self.insertRow(1,"Group :",self.layout)

class Form_Assemble(QFormLayout):
	def __init__(self, dialog , load = None):
		super().__init__()		
		self.dialog = dialog

		self.first = QComboBox()
		self.second = QComboBox()
		for i in range(len(groups.groups)):
			self.first.addItem(str(i))
			self.second.addItem(str(i))

		if load is not None:
			self.first.setCurrentIndex(load[0])
			self.second.setCurrentIndex(load[1])

		else:

			self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
			self.buttonbox.accepted.connect(self.submit)
			self.buttonbox.rejected.connect(self.CloseDialog)
			self.addWidget(self.buttonbox)


		self.addRow("Eski Grup :" , self.first)
		self.addRow("Yeni Grup :" ,self.second)

		

	def GetParam(self):
		return [self.first.currentIndex() ,self.second.currentIndex()]

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
		self.name.setText("formasyon " + str(len(formations.formations)))
		self.name.setMaximumWidth(100)
		self.name.setAlignment(Qt.AlignCenter)
		self.form.addRow("Yükseklik",self.name )


		self.height = QLineEdit()
		self.height.setText("1.0")
		self.height.setMaximumWidth(100)
		self.height.setAlignment(Qt.AlignCenter)
		self.form.addRow("Yükseklik",self.height )


		self.group = QLineEdit()
		self.group.setText("0")
		self.group.setMaximumWidth(100)
		self.group.setAlignment(Qt.AlignCenter)
		self.form.addRow("Grup",self.group )

		self.uzaklık = QLineEdit()
		self.uzaklık.setText("0.5")
		self.uzaklık.setMaximumWidth(100)
		self.uzaklık.setAlignment(Qt.AlignCenter)
		self.form.addRow("İki grid arası uzaklık",self.uzaklık)





		calculate = QPushButton("Hesapla")
		self.form.addRow(calculate)
		calculate.clicked.connect(self.calculate)

		self.form.setVerticalSpacing(20)

		save_button = QPushButton("Formasyonu Kaydet")
		save_button.clicked.connect(self.SaveFormation)
		self.form.addWidget(save_button)

		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonbox.accepted.connect(self.submit)
		buttonbox.rejected.connect(self.CloseDialog)


		self.form.addWidget(buttonbox)

		box.setLayout(self.form)		
		self.addWidget(box)

	def PopUpNoName(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText( "Eksik Bilgi" )
		msg.exec_()
	
	def PopUpNoDrone(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText( "Drone Eklenmedi" )
		msg.exec_()

	def PopUpSuccSave(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText( "Formasyon Kaydedildi" )
		msg.exec_()

	def SaveFormation(self):

		if self.name.text() == "":
			self.PopUpNoName()
			return
		elif len(self.calculatedposes) == 0:
			self.PopUpNoDrone()
			return

		else:
			formations.formations[self.name.text()] = self.calculatedposes
			self.PopUpSuccSave()
			print(formations.formations)
			return



		

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
		if int(self.group.text()) < 0 or int(self.group.text()) >= len(groups.groups):
			self.PopUp2()
			return

		if len(self.calculatedposes) != len(groups.groups[int(self.group.text())]):
			self.PopUp()
			return

		

		initial_cost = []
		uav_ids = []
	
		for uav in uavList:
			if uav.info["Bağlı"] == "Evet" and uav.info["Grup"] == int(self.group.text()):
				dist = []
				uav_ids.append(uav.info["Drone No"])
				for pose in self.calculatedposes:
					dist.append(uav.distance_to_dest([float(pose[0]),float(pose[1]),float(self.height.text())]))
				initial_cost.append(dist)
		groups.SetFormationInfos(int(self.group.text()),"Yok","Yok")


		hungarian = Munkres()

		indexes = hungarian.compute(initial_cost)

		for index in indexes : 
			uavList[uav_ids[index[0]]].SetDest(self.calculatedposes[index[1]][0],self.calculatedposes[index[1]][1],self.height.text())
			uavList[uav_ids[index[0]]].SetState(State.GO)

		self.CloseDialog()
			


	def PopUp(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText( str(len(groups.groups[int(self.group.text())])) + " Pozisyon Gerekli " + str(len(self.calculatedposes)) + " Pozisyon Verildi" )
		msg.exec_()

	def PopUp2(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText("Verilen Grup Mevcut Değil" )
		msg.exec_()
		
		
	def CloseDialog(self):
		self.dialog.close()


class TrajectoryMap(QHBoxLayout):
	def __init__(self , dialog):
		super().__init__()
		Mbox = QGroupBox() 
		Mvbox = QVBoxLayout()
		self.dialog = dialog

		self.pos = []
		self.calculatedposes = []
		self.labels = []
		self.count = 0

		map = MapTrajectory(self)
		map.setMinimumWidth(800)
		map.setMaximumHeight(800)
		Mvbox.addWidget(map)
		Mbox.setLayout(Mvbox)
		self.addWidget(Mbox)

		box = QGroupBox()
		self.form = QFormLayout()
		self.form.setAlignment(Qt.AlignCenter)




		self.height = QLineEdit()
		self.height.setText("1.0")
		self.height.setMaximumWidth(100)
		self.height.setAlignment(Qt.AlignCenter)
		self.form.addRow("Yükseklik",self.height )


		self.group = QLineEdit()
		self.group.setText("0")
		self.group.setMaximumWidth(100)
		self.group.setAlignment(Qt.AlignCenter)
		self.form.addRow("Grup",self.group )

		self.speed = QLineEdit()
		self.speed.setText("0.3")
		self.speed.setMaximumWidth(100)
		self.speed.setAlignment(Qt.AlignCenter)
		self.form.addRow("Hız",self.speed )

		self.loop = QRadioButton()
		self.form.addRow("Döngü",self.loop)

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


		group = int(self.group.text())
		height = float(self.height.text())
		speed = float(self.speed.text())
		loop = self.loop.isChecked()

		centers = []

		if group in groups.formation_info and groups.formation_info[group][0] != "Yok":

			for pose in self.calculatedposes:
				centers.append([pose[0],pose[1],height])

			for uav in groups.groups[group]:
		
				uavList[uav].CalculateTrajectory(centers,speed,loop)
		
			self.CloseDialog()
		
		else :
			self.PopUp()
			return
		
		
	def CloseDialog(self):
		self.dialog.close()

	def PopUp(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText( "Grup formasyon oluşturmadı veya öyle bir grup yok." )
		msg.exec_()
		
class FormTakeOff(QFormLayout):
	def __init__(self, dialog ,load = None):
		super().__init__()


		
		self.dialog = dialog
		self.takeoff_drones = []
		self.land_drones = []


		self.tabs = QTabWidget()
		self.takeoff_tab = QWidget()
		self.land_tab = QWidget()

		self.tabs.addTab(self.takeoff_tab,"Kalkış")
		self.tabs.addTab(self.land_tab,"İniş")

		takeoff_layout = self.SetTakeOffTab()
		land_layout = self.SetLandTab()

		self.takeoff_tab.setLayout(takeoff_layout)
		self.land_tab.setLayout(land_layout)

		self.SetTakeOffTab()
		self.SetLandTab()
		

		self.addWidget(self.tabs)


	def GetParam(self):
		return None
	
		
	def SetLandTab(self):
		land_tab_layout = QVBoxLayout()

		buttonLayout = QHBoxLayout()

		for uav in uavList:
			if uav.GetState() == State.TAKEOFF or uav.GetState() == State.CIRCLE or uav.GetState() == State.TRAJECTORY or uav.GetState() == State.GO or uav.GetState() == State.HOVER :
				sbox = QVBoxLayout()
				b = QRadioButton(str(uav.GetDroneNo()))
				self.land_drones.append(b)
				sbox.addWidget(b)
				box = QGroupBox()
				box.setMaximumHeight(80)
				box.setLayout(sbox)
				buttonLayout.addWidget(box)
		land_tab_layout.addLayout(buttonLayout)

		land_all = QPushButton("Hepsini İndir")
		land_all.clicked.connect(self.submitLandAll)
		land_tab_layout.addWidget(land_all)

		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonbox.accepted.connect(self.submitLand)
		buttonbox.rejected.connect(self.CloseDialog)

		land_tab_layout.addWidget(buttonbox)
		
		return land_tab_layout

	def submitLandAll(self):
		for uav in uavList:
			if uav.GetState() == State.TAKEOFF or uav.GetState() == State.CIRCLE or uav.GetState() == State.TRAJECTORY or uav.GetState() == State.GO or uav.GetState() == State.HOVER :
				uav.SetState(State.CONNECTED)


		self.CloseDialog()

	def submitLand(self):

		for uav in self.land_drones:
			if uav.isChecked():
				uavList[int(uav.text())].SetState(State.CONNECTED)
			

		self.CloseDialog()


	def SetTakeOffTab(self):
		takeoff_tab_layout = QVBoxLayout()

		buttonLayout = QHBoxLayout()

		for uav in uavList:
			if uav.GetState() == State.CONNECTED:
		
				sbox = QVBoxLayout()
				b = QRadioButton(str(uav.GetDroneNo()))
				self.takeoff_drones.append(b)
				sbox.addWidget(b)
				box = QGroupBox()
				box.setMaximumHeight(80)
				box.setLayout(sbox)
				buttonLayout.addWidget(box)
		takeoff_tab_layout.addLayout(buttonLayout)

		takeoff_all = QPushButton("Hepsini Kaldır")
		takeoff_all.clicked.connect(self.submitTakeOffAll)
		takeoff_tab_layout.addWidget(takeoff_all)

		buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonbox.accepted.connect(self.submitTakeOff)
		buttonbox.rejected.connect(self.CloseDialog)

		takeoff_tab_layout.addWidget(buttonbox)
		
		return takeoff_tab_layout
				

	def submitTakeOff(self):


		for uav in self.takeoff_drones:
			if uav.isChecked():
				uavList[int(uav.text())].SetState(State.TAKEOFF)
		


		self.CloseDialog()

	def submitTakeOffAll(self):

		for uav in uavList:
			if uav.GetState() == State.CONNECTED:
				uav.SetState(State.TAKEOFF)

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

Planned_Missions = {}

class MissionPlanner(QHBoxLayout):
	def __init__(self, dialog):
		super().__init__()
		self.dialog = dialog

		self.missions = []
		self.missionList = QFormLayout()
		
		

		w = QWidget()

		w.setLayout(self.missionList)
		scrollArea = QScrollArea()
		scrollArea.setWidgetResizable(True)
		scrollArea.setWidget(w)
		self.addWidget(scrollArea)

		missionButtons = QVBoxLayout()
		missionNameContainer = QFormLayout()


		self.missionName = QLineEdit()
		self.missionName.setText("Görev " + str(len(Planned_Missions)))
		missionNameContainer.addRow("Görev Adı: ", self.missionName)
		missionButtons.addLayout(missionNameContainer)
		self.addLayout(missionButtons)
		

		buttonIdle = "QPushButton{background-color: #4CAF50; /* Green */border: none;color: white; padding: 8px 16px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px;} "
		buttonIdle_close = "QPushButton{background-color: red; /* Green */border: none;color: white; padding: 8px 16px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px;} "
		buttonIdle_start = "QPushButton{background-color: lightblue; /* Green */border: none;color: white; padding: 8px 16px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px;} "
		buttonPressed = "QPushButton::pressed{background-color : black;color : white}"
		buttonHover = "QPushButton::hover{background-color : grey}"

		mission_buttons_names = ["Planı Kaydet" , "Planı Yükle" , "Bekleme Süresi Ekle","Kalkış/İnis" , "Formasyon Oluştur/Değiştir","Sürüyü Hareket Ettir","Sürüyü Ayır","Sürüleri Birleştir","Sonuncuyu Sil","Planı Başlat" ]
		mission_buttons = []
		button_style = buttonIdle + buttonPressed + buttonHover
		button_style_close = buttonIdle_close + buttonPressed + buttonHover
		button_style_start = buttonIdle_start + buttonPressed + buttonHover
		

		for mission in mission_buttons_names:
			button = QPushButton(mission)
			button.setStyleSheet(button_style)
			missionButtons.addWidget(button)
			mission_buttons.append(button)

		mission_buttons[-1].setStyleSheet(button_style_start)

		mission_buttons[0].clicked.connect(self.savePlanButtonClicked)
		mission_buttons[1].clicked.connect(self.loadPlanButtonClicked)
		mission_buttons[2].clicked.connect(self.waitButtonClicked)
		mission_buttons[3].clicked.connect(self.takeoff_button_clicked)
		mission_buttons[4].clicked.connect(self.formation)
		mission_buttons[5].clicked.connect(self.movement)
		mission_buttons[6].clicked.connect(self.divide)
		mission_buttons[7].clicked.connect(self.combine)
		mission_buttons[8].clicked.connect(self.removeItem)
		mission_buttons[9].clicked.connect(self.StartMission)

		

		# TODO: Fix buttons being too large
		close = QPushButton("Close")
		close.clicked.connect(self.CloseDialog)
		close.setStyleSheet(button_style_close)
		missionButtons.addWidget(close)

	def takeoff_button_clicked(self):
		takeoffLayout = FormTakeOff(self.dialog)
		takeoffLayout.setVerticalSpacing(10)


		if self.missions != []:
			takeoffLayout.insertRow(0,QHLine())

		self.missionList.addRow(takeoffLayout)
		self.missions.append(takeoffLayout)


	def StartMission(self):
		self.CloseDialog()
		for mission in self.missions:
			mission.submit()



	def LoadHelper(self,missions):

		for mission in missions:
			if self.missions != []:
				mission.insertRow(0,QHLine())
			self.missionList.addRow(mission)
			self.missions.append(mission)

	def savePlanButtonClicked(self):
		
		if self.missionName.text() == "":
			self.PopUpNoName()
			return

		elif len(self.missions) == 0:
			self.PopUpNoSave()
			return

		else :
			missions_tmp = []
			for mission in self.missions:
				type_of = type(mission)
				params = mission.GetParam()
				tmp = type_of(self.dialog,params)
				tmp.setVerticalSpacing(10)
				missions_tmp.append(tmp)
			Planned_Missions[self.missionName.text()] = missions_tmp
			self.removeItemAll()
			self.PopUpSuccSave()
			return

		

	def PopUpNoName(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText( "Plan adı giriniz" )
		msg.exec_()
	def PopUpNoSave(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText( " 0 Görev " )
		msg.exec_()
	def PopUpSuccSave(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText( "Plan Kaydedildi" )
		msg.exec_()
	def PopUpNoLoad(self):
		msg = QMessageBox()
		msg.setWindowTitle("Dikkat")
		msg.setText( "Yüklenebilecek Bir Plan Yok" )
		msg.exec_()


	def loadPlanButtonClicked(self):
		
		if len(Planned_Missions) == 0:
			self.PopUpNoLoad()
			return
		else :
			dialog = QDialog()
			formation_layout = Form_LoadMissions(dialog , self)
			dialog.resize(300,200)
			dialog.setWindowModality(Qt.ApplicationModal)
			dialog.setLayout(formation_layout)
			dialog.exec_()

		


	def waitButtonClicked(self):
		waitLayout = Form_Wait(None)
		waitLayout.setVerticalSpacing(10)

		if self.missions != []:
			waitLayout.insertRow(0,QHLine())

		self.missionList.addRow(waitLayout)
		self.missions.append(waitLayout)

		

	def formation(self):
		formationLayout = Form_SetFormation(self.dialog)
		formationLayout.removeWidget(formationLayout.buttonbox)
		formationLayout.setVerticalSpacing(10)

		if self.missions != []:
			formationLayout.insertRow(0,QHLine())

		self.missionList.addRow(formationLayout)
		self.missions.append(formationLayout)


	def movement(self):
		movementLayout = Form_Hareket(self.dialog)
		movementLayout.removeWidget(movementLayout.buttonbox)
		movementLayout.setVerticalSpacing(10)

		if self.missions != []:
			movementLayout.insertRow(0,QHLine())

		self.missionList.addRow(movementLayout)
		self.missions.append(movementLayout)


	def trajectory(self):
		trajectoryLayout = TrajectoryForm(self.dialog)
		trajectoryLayout.setVerticalSpacing(10)

		if self.missions != []:
			trajectoryLayout.insertRow(0,QHLine())

		self.missionList.addRow(trajectoryLayout)
		self.missions.append(trajectoryLayout)



	def divide(self):
		divideLayout = Form_Split(self.dialog)
		divideLayout.removeRow(divideLayout.buttonbox)
		divideLayout.setVerticalSpacing(10)

		if self.missions != []:
			divideLayout.insertRow(0,QHLine())

		self.missionList.addRow(divideLayout)
		self.missions.append(divideLayout)



	def combine(self):
		combineLayout = Form_Assemble(self.dialog)
		combineLayout.removeRow(combineLayout.buttonbox)
		combineLayout.setVerticalSpacing(10)

		if self.missions != []:
			combineLayout.insertRow(0,QHLine())

		self.missionList.addRow(combineLayout)
		self.missions.append(combineLayout)



	def removeItem(self):
		if len(self.missions) == 0:
			return
		self.missionList.removeRow(self.missions[-1])
		self.missions.pop()

	def removeItemAll(self):
		while len(self.missions) != 0:
			self.removeItem()


	def CloseDialog(self):
		self.dialog.close()



class Form_LoadMissions(QFormLayout):
	def __init__(self, dialog ,mission_planner):
		super().__init__()
		self.dialog = dialog

		self.cb = QComboBox()
		self.mission_planner = mission_planner


		for i in Planned_Missions:
			self.cb.addItem(i)

		self.addRow("Plan" , self.cb)

		self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.buttonbox.accepted.connect(self.submit)
		self.buttonbox.rejected.connect(self.CloseDialog)
		self.addWidget(self.buttonbox)

	def submit(self):

		self.CloseDialog()
		self.mission_planner.removeItemAll()

		self.mission_planner.LoadHelper(Planned_Missions[str(self.cb.currentText())])

		
	def CloseDialog(self):
		self.dialog.close()


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class Form_Wait(QFormLayout):
	def __init__(self , dialog , load = None):
		super().__init__()
		self.time = QLineEdit("0")
		if load is not None:
			self.time.setText(load[0])

		self.addRow("Bekleme süresi: ", self.time)
		self.empty = False




	def GetParam(self):
		return [self.time.text()]
	def submit(self):
		end_time = float(self.time.text()) + time.time()
		while time.time() < end_time:
			pass








class buttons(QGridLayout):


	def __init__(self):
		super().__init__()

		
		buttons = [["Bağlantıyı kur",0,0],["Bağlantıyı kes",0,1] ,["Drone Kaldırma/İndirme" , 0,2] , ["Yeni Formasyon",1,0] ,  ["Formasyon ",1,1] , ["Hareket ",1,2] , ["Trajectory",2,0] , ["Sürü Ayırma",2,1] , ["Sürü Birleştirme" , 2 ,2] ,  ["Uçuş Planlaması Yap",3,0] ]

		buttonIdle = "QPushButton{background-color: lightblue;border-style: outset;border-width: 2px;border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em;padding: 6px;} "
		buttonPressed = "QPushButton::pressed{background-color : black;color : white}"
		buttonHover = "QPushButton::hover{background-color : yellow}"
	

		self.buttons = []

		for index in buttons:
			button = QPushButton(index[0])
			button.setStyleSheet(buttonIdle + buttonPressed + buttonHover)

			self.buttons.append(button)
			self.addWidget(button,index[1],index[2])


		self.setVerticalSpacing(50)

		self.rowStretch(10)

		self.buttons[0].clicked.connect(self.drone_connect)
		self.buttons[1].clicked.connect(self.drone_dissconnect)
		self.buttons[2].clicked.connect(self.DroneTakeOff)
		self.buttons[3].clicked.connect(self.create_Formation)
		self.buttons[4].clicked.connect(self.mission_SetFormation)
		self.buttons[5].clicked.connect(self.mission_hareket)
		self.buttons[6].clicked.connect(self.SetTrajectory)

		self.buttons[7].clicked.connect(self.mission_split)
		self.buttons[8].clicked.connect(self.mission_assemble)

		self.buttons[9].clicked.connect(self.mission_plan)


	def DroneTakeOff(self):
		dialog = QDialog()
		form = FormTakeOff(dialog)
		self.CreateDialog(form,dialog)

	def drone_connect(self):
		dialog = QDialog()
		form = Form_Connect(dialog)
		self.CreateDialog(form,dialog)

	def drone_dissconnect(self):
		for uav in uavList:
			uav.info["Bağlı"] = "Hayır"
			uav.SetState(State.NOT_CONNECTED)


	def create_Formation(self):
		dialog = QDialog()
		form = MapLayout(dialog)
		self.CreateDialog2(form,dialog)

	def SetTrajectory(self):
		dialog = QDialog()
		form = TrajectoryMap(dialog)
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

	def mission_plan(self):
		dialog = QDialog()
		form = MissionPlanner(dialog)
		dialog.resize(1200,400)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.setLayout(form)
		dialog.exec_()



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


		#simulation + console

		

		self.tabs = QTabWidget()
		self.simulation_tab = QWidget()
		self.console_tab = QWidget()

		self.tabs.addTab(self.simulation_tab,"Simulation")
		self.tabs.addTab(self.console_tab,"Console")

		tabs_layout = QVBoxLayout()
		tabs_layout.addWidget(self.tabs)

		self.leftBox =  QGroupBox()
		self.leftBox.setLayout(tabs_layout)
		self.leftBox.setMinimumWidth(960)

		

		self.simulation = Simulation()
		self.mission_log = MissionLogs()
		
		self.simulation_tab.setLayout(self.simulation.simulation_layout)
		self.console_tab.setLayout(self.mission_log.layout)


		#Mission Log + Groups
		logLayout = QHBoxLayout()


		self.group_table = GroupInfos()
		logLayout.addWidget(self.group_table)
		logbox = QGroupBox()
		logbox.setLayout(logLayout)
		logbox.setMinimumHeight(240)
		

		#set-up
		hbox.addWidget(self.leftBox)
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
		self.timer.timeout.connect(self.showTimeSim)
		self.timer.start(40)

	def showTime(self):
		self.table.update_labels()
		self.group_table.UpdateLabels()

	def showTimeSim(self):
		tmp_groups =[]
		for group in groups.groups:
			tmp_group = []
			for uav in group:
				tmp_group.append([uavList[uav].info["X"] , uavList[uav].info["Y"] ,uavList[uav].info["Z"]])
			tmp_groups.append(tmp_group)


		self.simulation.sc.CalculateAllLines(tmp_groups,self.simulation.simulation_aktif)

		self.simulation.sc.draw()

	def closeEvent(self,event):
		curr = datetime.datetime.now()
		idx = 0
		os.mkdir(curr.strftime("logs/%d.%m.%Y-%H:%M:%S"))
		while idx < len(logs):
			with open("logs/"+curr.strftime("%d.%m.%Y-%H:%M:%S")+"/"+str(idx)+".csv","w+") as f:
				print("Starting!")
				f.write("State,X,Y,Z,Vx,Vy,Vz,Dx,Dy,Dz"+"\n")
				f.write(logs[idx])
			idx+=1



w = Window()
sys.exit(App.exec())

	




