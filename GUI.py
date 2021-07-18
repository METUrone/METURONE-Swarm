import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class GCSGui( QMainWindow ):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUI()

    def setupUI(self):

        ## Here we create the layout and other widgets in the usual Qt way.

        if self.objectName() is None:
            self.setObjectName("MainWindow")

        self.resize(1600, 900)

        """
        self.actionScenarioSave = QAction(self)
        self.actionScenarioSave.setObjectName("actionSenaryo_Kaydet")
        self.actionScenarioSave.triggered.connect(self.saveScenario)
        self.actionScenarioLoad = QAction(self)
        self.actionScenarioLoad.setObjectName("actionSenaryo_Yukle")
        self.actionScenarioLoad.triggered.connect(self.loadScenario)
        self.actionRealScenario = QAction(self);
        self.actionRealScenario.setObjectName("actionGercek_Senaryo");
        self.actionRealScenario.setCheckable(True)
        self.actionRealScenario.triggered.connect(self.setCaseAsReal)
        self.actionSimulation = QAction(self);
        self.actionSimulation.setObjectName("actionSimulasyon");
        self.actionSimulation.setCheckable(True)
        self.actionSimulation.setChecked(True)
        self.actionSimulation.triggered.connect(self.setCaseAsSimulation)
        """

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        ## rviz.VisualizationFrame is the main container widget of the
        ## regular RViz application, with menus, a toolbar, a status
        ## bar, and many docked subpanels.  In this example, we
        ## disable everything so that the only thing visible is the 3D
        ## render window.
        # self.frame = rviz.VisualizationFrame()

        ## The "splash path" is the full path of an image file which
        ## gets shown during loading.  Setting it to the empty string
        ## suppresses that behavior.
        # self.frame.setSplashPath( "" )

        ## VisualizationFrame.initialize() must be called before
        ## VisualizationFrame.load().  In fact it must be called
        ## before most interactions with RViz classes because it
        ## instantiates and initializes the VisualizationManager,
        ## which is the central class of RViz.
        # self.frame.initialize()

        ## The reader reads config file data into the config object.
        ## VisualizationFrame reads its data from the config object.
        # reader = rviz.YamlConfigReader()
        # config = rviz.Config()
        # reader.readFile( config, "config.myviz" )
        # self.frame.load( config )

        ## You can also store any other application data you like in
        ## the config object.  Here we read the window title from the
        ## map key called "Title", which has been added by hand to the
        ## config file.
        # self.setWindowTitle( config.mapGetChild( "MainWindow" ).getValue() )

        #scriptDir = os.path.dirname(os.path.realpath(__file__))
        #self.setWindowIcon(QIcon(scriptDir + os.path.sep + '../resources/logo.png'))

        ## Here we disable the menu bar (from the top), status bar
        ## (from the bottom), and the "hide-docks" buttons, which are
        ## the tall skinny buttons on the left and right sides of the
        ## main render window.
        # self.frame.setMenuBar( None )
        # self.frame.setStatusBar( None )
        # self.frame.setHideButtonVisibility( False )

        ## frame.getManager() returns the VisualizationManager
        ## instance, which is a very central class.  It has pointers
        ## to other manager objects and is generally required to make
        ## any changes in an rviz instance.
        # self.manager = self.frame.getManager()

        ## Since the config file is part of the source code for this
        ## example, we know that the first display in the list is the
        ## grid we want to control.  Here we just save a reference to
        ## it for later.
        # self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 0 )

        self.mapBox = QGroupBox(self.centralwidget)
        self.mapBox.setObjectName("mapBox")
        self.mapBox.setGeometry(QRect(10, 30, 741, 811))
        self.mapBox.setStyleSheet("QGroupBox#mapBox { \
                                        border: 1px solid gray;\
                                        border-color: #FF17365D;\
                                        font-size: 14px;\
                                        border-radius: 9px; }\
                                    QGroupBox:title {\
                                        color: rgb(255,255,255);\
                                        background-color: rgb(1, 130, 153);\
                                        subcontrol-origin: margin;\
                                        subcontrol-position: top center;\
                                        padding-left: 400px;\
                                        padding-right: 400px;  \
                                        border-radius: 9px;\
                                        }")
        self.mapBox.setAlignment(Qt.AlignCenter)

        self.mapTabWidget = QTabWidget(self.mapBox)
        self.mapTabWidget.setObjectName("mapTabWidget")
        self.mapTabWidget.setGeometry(QRect(10, 20, 721, 781))
        self.mapTab = QWidget()
        self.mapTab.setObjectName("mapTab")

        """
        self.map = MissionView(self.mapTab, self)
        self.map.setObjectName("map")
        self.map.setGeometry(QRect(10, 10, 701, 731))
        self.map.setLineWidth(1)
        self.map.setMidLineWidth(0)
        self.map.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.map.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.map.setStyleSheet("background-image: url(../resources/gui_real_background.png);")
        """
        self.mapTabWidget.addTab(self.mapTab, "")

        # self.layout = QVBoxLayout()
        # self.layout.addWidget( self.frame )

        # self.rvizTab = QWidget()
        # self.rvizTab.setObjectName("rvizTab")
        # self.rvizWidget = QWidget(self.rvizTab)
        # self.rvizWidget.setObjectName("rvizWidget")
        # self.rvizWidget.setGeometry(QRect(10, 10, 701, 731))
        # self.rvizWidget.setLayout( self.layout )
        # self.mapTabWidget.addTab(self.rvizTab, "")

        self.missionBox = QGroupBox(self.centralwidget)
        self.missionBox.setObjectName("missionBox")
        self.missionBox.setGeometry(QRect(760, 30, 821, 181))
        self.missionBox.setStyleSheet("QGroupBox#missionBox { \
                                            border: 1px solid gray;\
                                            border-color: #FF17365D;\
                                            font-size: 14px;\
                                            border-radius: 9px; }\
                                        QGroupBox:title {\
                                            color: rgb(255,255,255);\
                                            background-color: rgb(1, 130, 153);\
                                            subcontrol-origin: margin;\
                                            subcontrol-position: top center;\
                                            padding-left: 380px;\
                                            padding-right: 380px;  \
                                            border-radius: 9px;\
                                        }")


        self.missionTabWidget = QTabWidget(self.missionBox)
        self.missionTabWidget.setObjectName("missionTabWidget")
        self.missionTabWidget.setGeometry(QRect(10, 20, 801, 151))
        
        self.missionParameterTab1 = QWidget()
        self.missionParameterTab1.setObjectName("missionParameterTab1")
        
        # self.substituteComboBox = CheckableComboBox(self.missionParameterTab1)
        # self.substituteComboBox.setObjectName("substituteComboBox")
        # self.substituteComboBox.setGeometry(QRect(140, 45, 80, 27))
        # self.substituteComboBox.addItem("UAV " + str(1))
        # self.substituteComboBox.setItemChecked(0, False)

        # self.substitutesLabel = QLabel(self.missionParameterTab1)
        # self.substitutesLabel.setObjectName("substitutesLabel")
        # self.substitutesLabel.setGeometry(QRect(20, 45, 120, 31))
        
        self.borderHeightLabel = QLabel(self.missionParameterTab1)
        self.borderHeightLabel.setObjectName("borderHeightLabel")
        self.borderHeightLabel.setGeometry(QRect(20, 30, 160, 31))
        
        self.borderHeightSpinBox = QSpinBox(self.missionParameterTab1)
        self.borderHeightSpinBox.setObjectName("borderHeightSpinBox")
        self.borderHeightSpinBox.setGeometry(QRect(180, 30, 50, 27))

        self.motionHeightLabel = QLabel(self.missionParameterTab1)
        self.motionHeightLabel.setObjectName("motionHeightLabel")
        self.motionHeightLabel.setGeometry(QRect(20, 60, 160, 31))
        
        self.motionHeightSpinBox = QSpinBox(self.missionParameterTab1)
        self.motionHeightSpinBox.setObjectName("motionHeightSpinBox")
        self.motionHeightSpinBox.setGeometry(QRect(180, 60, 50, 27))
        
        self.uavNumberLabel = QLabel(self.missionParameterTab1)
        self.uavNumberLabel.setObjectName("uavNumberLabel")
        self.uavNumberLabel.setGeometry(QRect(20, 0, 120, 31))
        
        self.uavNumberSpinBox = QSpinBox(self.missionParameterTab1)
        self.uavNumberSpinBox.setObjectName("uavNumberSpinBox")
        self.uavNumberSpinBox.setGeometry(QRect(140, 0, 50, 27))
        self.uavNumberSpinBox.setMinimum(1)
        self.uavNumberSpinBox.setMaximum(10)
        #self.uavNumberSpinBox.valueChanged.connect(self.changeUavCount)
        self.uavNumberSpinBox.setValue(1)

        self.hideShowBorderButton = QPushButton(self.missionParameterTab1)
        self.hideShowBorderButton.setObjectName("hideShowBorderButton")
        self.hideShowBorderButton.setGeometry(QRect(20, 87, 210, 30))
        #self.hideShowBorderButton.clicked.connect(self.hideShowBorders)
        
        self.secondBorderButton = QPushButton(self.missionParameterTab1)
        self.secondBorderButton.setObjectName("secondBorderButton")
        self.secondBorderButton.setGeometry(QRect(280, 40, 221, 30))
        #self.secondBorderButton.clicked.connect(self.selectSecondBorder)

        
        self.firstBorderButton = QPushButton(self.missionParameterTab1)
        self.firstBorderButton.setObjectName("firstBorderButton")
        self.firstBorderButton.setGeometry(QRect(280, 10, 221, 30))
        #self.firstBorderButton.clicked.connect(self.selectFirstBorder)

        self.emergencyLandPointButton = QPushButton(self.missionParameterTab1)
        self.emergencyLandPointButton.setObjectName("emergencyLandPointButton")
        self.emergencyLandPointButton.setGeometry(QRect(280, 70, 221, 30))
        #self.emergencyLandPointButton.clicked.connect(self.selectEmergencyLandPoint)


        self.separator = QLabel(self.missionParameterTab1)
        self.separator.setObjectName("separator")
        self.separator.setGeometry(QRect(541, 0, 1, 118))
        self.separator.setStyleSheet("QLabel {background-color: #FF17365D; padding: 0; margin: 0; border-bottom: 1 solid gray; border-top: 1 solid gray;}")
        
        self.notamTypeComboBox = QComboBox(self.missionParameterTab1)
        self.notamTypeComboBox.setObjectName("notamTypeComboBox")
        self.notamTypeComboBox.setGeometry(QRect(672, 10, 110, 27))
        
        self.notamTypeLabel = QLabel(self.missionParameterTab1)
        self.notamTypeLabel.setObjectName("notamTypeLabel")
        self.notamTypeLabel.setGeometry(QRect(568, 10, 91, 31))
        
        self.notamHeightLabel = QLabel(self.missionParameterTab1)
        self.notamHeightLabel.setObjectName("notamHeightLabel")
        self.notamHeightLabel.setGeometry(QRect(570, 45, 131, 31))
        
        self.notamHeightSpinBox = QSpinBox(self.missionParameterTab1)
        self.notamHeightSpinBox.setObjectName("notamHeightSpinBox")
        self.notamHeightSpinBox.setGeometry(QRect(710, 45, 48, 27))
        #self.notamHeightSpinBox.valueChanged.connect(self.changeNotamHeight)

        
        self.selectNotamButton = QPushButton(self.missionParameterTab1)
        self.selectNotamButton.setObjectName("selectNotamButton")
        self.selectNotamButton.setGeometry(QRect(630, 80, 99, 30))
        #self.selectNotamButton.clicked.connect(self.selectNotam)

        
        self.separator_2 = QLabel(self.missionParameterTab1)
        self.separator_2.setObjectName("separator_2")
        self.separator_2.setGeometry(QRect(245, 0, 1, 118))
        self.separator_2.setStyleSheet("QLabel {background-color: #FF17365D; padding: 0; margin: 0; border-bottom: 1 solid gray; border-top: 1 solid gray;}")
        
        self.selectScanAreaButton = QPushButton(self.missionParameterTab1)
        self.selectScanAreaButton.setObjectName("selectScanAreaButton")
        self.selectScanAreaButton.setGeometry(QRect(50, 80, 151, 30))
        #self.selectScanAreaButton.clicked.connect(self.selectScanArea)
        
        self.missionTabWidget.addTab(self.missionParameterTab1, "")
        
        self.missionParameterTab2 = QWidget()
        self.missionParameterTab2.setObjectName("missionParameterTab2")
        
        self.missionTypeLabel = QLabel(self.missionParameterTab2)
        self.missionTypeLabel.setObjectName("missionTypeLabel")
        self.missionTypeLabel.setGeometry(QRect(6, 10, 91, 31))

        self.formationTypeLabel = QLabel(self.missionParameterTab2)
        self.formationTypeLabel.setObjectName("missionTypeLabel")
        self.formationTypeLabel.setGeometry(QRect(520, 10, 91, 31))
        
        self.missionTypeComboBox = QComboBox(self.missionParameterTab2)
        self.missionTypeComboBox.setObjectName("missionTypeComboBox")
        self.missionTypeComboBox.setGeometry(QRect(140, 10, 111, 27))
        #self.missionTypeComboBox.currentIndexChanged.connect(self.changeMissionType)

        self.scanPatternLabel = QLabel(self.missionParameterTab2)
        self.scanPatternLabel.setObjectName("scanPatternLabel")
        self.scanPatternLabel.setGeometry(QRect(6, 40, 121, 31))

        self.surveillanceHeightLabel = QLabel(self.missionParameterTab2)
        self.surveillanceHeightLabel.setObjectName("surveillanceHeightLabel")
        self.surveillanceHeightLabel.setGeometry(QRect(290, 40, 151, 31))

        self.scanPatternComboBox = QComboBox(self.missionParameterTab2)
        self.scanPatternComboBox.setObjectName("scanPatternComboBox")
        self.scanPatternComboBox.setGeometry(QRect(140, 40, 111, 27))

        self.surveillanceHeightSpinBox = QSpinBox(self.missionParameterTab2)
        self.surveillanceHeightSpinBox.setObjectName("surveillanceHeightSpinBox")
        self.surveillanceHeightSpinBox.setGeometry(QRect(450, 40, 48, 27))  
        #self.surveillanceHeightSpinBox.setValue(globals()["defaultSurveillanceHeight"]) 
        #self.surveillanceHeightSpinBox.valueChanged.connect(self.changeSurveillanceHeight)
        
        self.formationHeightLabel = QLabel(self.missionParameterTab2)
        self.formationHeightLabel.setObjectName("formationHeightLabel")
        self.formationHeightLabel.setGeometry(QRect(290, 70, 151, 31))

        self.formationHeightSpinBox = QSpinBox(self.missionParameterTab2)
        self.formationHeightSpinBox.setObjectName("formationHeightSpinBox")
        self.formationHeightSpinBox.setGeometry(QRect(450, 70, 48, 27))  
        #self.formationHeightSpinBox.setValue(globals()["defaultSurveillanceHeight"]) 

        self.cameraFocusDistanceLabel = QLabel(self.missionParameterTab2)
        self.cameraFocusDistanceLabel.setObjectName("cameraFocusDistanceLabel")
        self.cameraFocusDistanceLabel.setGeometry(QRect(520, 10, 181, 31))
        
        self.cameraFocusDistanceSpinBox = QSpinBox(self.missionParameterTab2)
        self.cameraFocusDistanceSpinBox.setObjectName("cameraFocusDistanceSpinBox")
        self.cameraFocusDistanceSpinBox.setGeometry(QRect(720, 10, 48, 27))
        
        self.cameraViewHeightLabel = QLabel(self.missionParameterTab2)
        self.cameraViewHeightLabel.setObjectName("cameraViewHeightLabel")
        self.cameraViewHeightLabel.setGeometry(QRect(520, 40, 191, 31))
        
        self.cameraViewHeightSpinBox = QSpinBox(self.missionParameterTab2)
        self.cameraViewHeightSpinBox.setObjectName("cameraViewHeightSpinBox")
        self.cameraViewHeightSpinBox.setGeometry(QRect(720, 40, 48, 27))
        
        self.cameraViewWidthLabel = QLabel(self.missionParameterTab2)
        self.cameraViewWidthLabel.setObjectName("cameraViewWidthLabel")
        self.cameraViewWidthLabel.setGeometry(QRect(520, 70, 191, 31))
        
        self.cameraViewWidthSpinBox = QSpinBox(self.missionParameterTab2)
        self.cameraViewWidthSpinBox.setObjectName("cameraViewWidthSpinBox")
        self.cameraViewWidthSpinBox.setGeometry(QRect(720, 70, 48, 27))

        self.surveillanceTimeLabel = QLabel(self.missionParameterTab2)
        self.surveillanceTimeLabel.setObjectName("surveillanceTimeLabel")
        self.surveillanceTimeLabel.setGeometry(QRect(290, 70, 181, 31))

        self.formationDistanceLabel = QLabel(self.missionParameterTab2)
        self.formationDistanceLabel.setObjectName("formationDistanceLabel")
        self.formationDistanceLabel.setGeometry(QRect(6, 40, 181, 31))

        # self.formationStopLabel = QLabel(self.missionParameterTab2) 
        # self.formationStopLabel.setObjectName("formationTimeLabel") 
        # self.formationStopLabel.setGeometry(QRect(290, 40, 161, 31))    
            
        self.formationStopButton = QPushButton(self.missionParameterTab2) 
        self.formationStopButton.setObjectName("formationTimeSpinBox") 
        self.formationStopButton.setGeometry(QRect(290, 40, 200, 27))   
        #self.formationStopButton.clicked.connect(self.endFormation)
        self.formationStopButton.setEnabled(False)

        self.missionRepeatNumberLabel = QLabel(self.missionParameterTab2)
        self.missionRepeatNumberLabel.setObjectName("missionRepeatNumberLabel")
        self.missionRepeatNumberLabel.setGeometry(QRect(6, 70, 151, 31))

        self.surveillanceTargetLabel = QLabel(self.missionParameterTab2)    
        self.surveillanceTargetLabel.setObjectName("surveillanceTargetLabel")   
        self.surveillanceTargetLabel.setGeometry(QRect(290, 10, 100, 22))   
    
        #self.surveillanceTargetComboBox = CheckableComboBox(self.missionParameterTab2)  
        #self.surveillanceTargetComboBox.setObjectName("surveillanceTargetComboBox") 
        #self.surveillanceTargetComboBox.setGeometry(QRect(400, 10, 100, 27))

        self.surveillanceSelectRemoveAllButton = QPushButton(self.missionParameterTab2)
        self.surveillanceSelectRemoveAllButton.setObjectName("surveillanceSelectRemoveAllButton")
        self.surveillanceSelectRemoveAllButton.setGeometry(QRect(520, 10, 181, 31))
        self.surveillanceSelectRemoveAllButton.clicked.connect(lambda: self.selectRemoveAll(self.surveillanceTargetComboBox))

        self.surveillanceTimeSpinBox = QSpinBox(self.missionParameterTab2)
        self.surveillanceTimeSpinBox.setObjectName("surveillanceTimeSpinBox")
        self.surveillanceTimeSpinBox.setGeometry(QRect(450, 70, 48, 27))    
        #self.surveillanceTimeSpinBox.setValue(globals()["defaultSurveillanceTime"]) 
        #self.surveillanceTimeSpinBox.valueChanged.connect(self.changeSurveillanceTime)

        self.surveillanceTargetButton = QPushButton(self.missionParameterTab2)
        self.surveillanceTargetButton.setObjectName("surveillanceTargetButton")
        self.surveillanceTargetButton.setGeometry(QRect(6, 50, 250, 27))
        #self.surveillanceTargetButton.clicked.connect(self.selectSurveillanceTarget)

        self.formationTargetButton = QPushButton(self.missionParameterTab2)
        self.formationTargetButton.setObjectName("formationTargetButton")
        self.formationTargetButton.setGeometry(QRect(290, 10, 200, 27))
        #self.formationTargetButton.clicked.connect(self.selectFormationTarget)

        self.formationDistanceSpinBox = QSpinBox(self.missionParameterTab2)
        self.formationDistanceSpinBox.setObjectName("formationDistanceSpinBox")
        self.formationDistanceSpinBox.setGeometry(QRect(200, 40, 48, 27))
        self.formationDistanceSpinBox.setMinimum(15)    
        #self.formationDistanceSpinBox.setValue(globals()["defaultFormationDistance"])

        self.formationShapeLabel = QLabel(self.missionParameterTab2)
        self.formationShapeLabel.setObjectName("scanPatternLabel")
        self.formationShapeLabel.setGeometry(QRect(6, 70, 121, 31))
        
        self.formationShapeComboBox = QComboBox(self.missionParameterTab2)
        self.formationShapeComboBox.setObjectName("scanPatternComboBox")
        self.formationShapeComboBox.setGeometry(QRect(140, 70, 111, 27))

        self.formationUAVComboBox = QComboBox(self.missionParameterTab2)
        self.formationUAVComboBox.setObjectName("formationUAVComboBox")
        self.formationUAVComboBox.setGeometry(QRect(700, 70, 111, 27))

        self.missionRepeatNumberSpinBox = QSpinBox(self.missionParameterTab2)
        self.missionRepeatNumberSpinBox.setObjectName("missionRepeatNumberSpinBox")
        self.missionRepeatNumberSpinBox.setGeometry(QRect(170, 70, 48, 27))

        self.verticalSpeedLabel = QLabel(self.missionParameterTab2)
        self.verticalSpeedLabel.setObjectName("verticalSpeedLabel")
        self.verticalSpeedLabel.setGeometry(QRect(320, 70, 101, 31))

        self.horizontalSpeedSpinBox = QSpinBox(self.missionParameterTab2)
        self.horizontalSpeedSpinBox.setObjectName("horizontalSpeedSpinBox")
        self.horizontalSpeedSpinBox.setGeometry(QRect(430, 40, 48, 27))
        self.horizontalSpeedSpinBox.setStyleSheet("")
        
        self.horizontalSpeedLabel = QLabel(self.missionParameterTab2)
        self.horizontalSpeedLabel.setObjectName("horizontalSpeedLabel")
        self.horizontalSpeedLabel.setGeometry(QRect(320, 40, 101, 31))

        self.verticalSpeedSpinBox = QSpinBox(self.missionParameterTab2)
        self.verticalSpeedSpinBox.setObjectName("verticalSpeedSpinBox")
        self.verticalSpeedSpinBox.setGeometry(QRect(430, 70, 48, 27))

        self.scanHeightLabel = QLabel(self.missionParameterTab2)
        self.scanHeightLabel.setObjectName("scanHeightLabel")
        self.scanHeightLabel.setGeometry(QRect(290, 10, 131, 31))
        
        self.scanHeightSpinBox = QSpinBox(self.missionParameterTab2)
        self.scanHeightSpinBox.setObjectName("scanHeightSpinBox")
        self.scanHeightSpinBox.setGeometry(QRect(430, 10, 48, 27))

        self.separator_3 = QLabel(self.missionParameterTab2)
        self.separator_3.setObjectName("separator_3")
        self.separator_3.setGeometry(QRect(270, 0, 1, 118))
        self.separator_3.setStyleSheet("QLabel {background-color: #FF17365D; padding: 0; margin: 0; border-bottom: 1 solid gray; border-top: 1 solid gray;}")
        
        self.separator_4 = QLabel(self.missionParameterTab2)
        self.separator_4.setObjectName("separator_4")
        self.separator_4.setGeometry(QRect(500, 0, 1, 118))
        self.separator_4.setStyleSheet("QLabel {background-color: #FF17365D; padding: 0; margin: 0; border-bottom: 1 solid gray; border-top: 1 solid gray;}")
        
        self.missionTabWidget.addTab(self.missionParameterTab2, "")

        self.missionControlTab = QWidget()
        self.missionControlTab.setObjectName("missionControlTab")

        self.pauseContinueMissionButton = QPushButton(self.missionControlTab)
        self.pauseContinueMissionButton.setObjectName("pauseContinueMissionButton")
        self.pauseContinueMissionButton.setGeometry(QRect(550, 70, 161, 30))
        #self.pauseContinueMissionButton.clicked.connect(self.pauseContinueMission)
        self.pauseContinueMissionButton.setEnabled(False)

        self.cancelMissionButton = QPushButton(self.missionControlTab)
        self.cancelMissionButton.setObjectName("cancelMissionButton")
        self.cancelMissionButton.setGeometry(QRect(550, 40, 161, 30))
        #self.cancelMissionButton.clicked.connect(self.cancelMission)
        self.cancelMissionButton.setEnabled(False)

        
        self.loadMissionParameterButton = QPushButton(self.missionControlTab)
        self.loadMissionParameterButton.setObjectName("loadMissionParameterButton")
        self.loadMissionParameterButton.setGeometry(QRect(250, 10, 271, 30))
        #self.loadMissionParameterButton.clicked.connect(self.loadMissionParameters)
        self.loadMissionParameterButton.setEnabled(False)

        
        self.readMissionParameterButton = QPushButton(self.missionControlTab)
        self.readMissionParameterButton.setObjectName("readMissionParameterButton")
        self.readMissionParameterButton.setGeometry(QRect(250, 40, 271, 30))
        #self.readMissionParameterButton.clicked.connect(self.readMissionParameters)
        self.readMissionParameterButton.setEnabled(False)
        
        self.startMissionButton = QPushButton(self.missionControlTab)
        self.startMissionButton.setObjectName("startMissionButton")
        self.startMissionButton.setGeometry(QRect(550, 10, 161, 30))
        #self.startMissionButton.clicked.connect(self.startMission)
        self.startMissionButton.setEnabled(False)

        self.connectButton = QPushButton(self.missionControlTab)
        self.connectButton.setObjectName("connectButton")
        self.connectButton.setGeometry(QRect(50, 10, 181, 30))
        #self.connectButton.clicked.connect(self.connect)
        
        self.deleteMissionParameterButton = QPushButton(self.missionControlTab)
        self.deleteMissionParameterButton.setObjectName("deleteMissionParameterButton")
        self.deleteMissionParameterButton.setGeometry(QRect(250, 70, 271, 30))
        #self.deleteMissionParameterButton.clicked.connect(self.deleteMissionParameters)
        self.deleteMissionParameterButton.setEnabled(False)
        
        self.missionTabWidget.addTab(self.missionControlTab, "")


        self.consoleBox = QGroupBox(self.centralwidget)
        self.consoleBox.setObjectName("consoleBox")
        self.consoleBox.setGeometry(QRect(1160, 710, 421, 131))
        self.consoleBox.setStyleSheet("QGroupBox#consoleBox { \
                                            border: 1px solid gray;\
                                            border-color: #FF17365D;\
                                            font-size: 14px;\
                                            border-radius: 9px; }\
                                        QGroupBox:title {\
                                            color: rgb(255,255,255);\
                                            background-color: rgb(1, 130, 153);\
                                            subcontrol-origin: margin;\
                                            subcontrol-position: top center;\
                                            padding-left: 350px;\
                                            padding-right: 350px;  \
                                            border-radius: 9px; \
                                        }")

        self.console = QTextEdit(self.consoleBox)
        self.console.setObjectName("console")
        self.console.setGeometry(10, 20, 401, 101)
        self.console.setStyleSheet("color: white; background-color: rgb(0, 0, 0);")
        self.console.setReadOnly(True)

        self.cameraBox = QGroupBox(self.centralwidget)
        self.cameraBox.setObjectName("cameraBox")
        self.cameraBox.setGeometry(QRect(760, 520, 391, 321))
        self.cameraBox.setStyleSheet("QGroupBox#cameraBox { \
                                        border: 1px solid gray;\
                                        border-color: #FF17365D;\
                                        font-size: 14px;\
                                        border-radius: 9px; }\
                                    QGroupBox:title {\
                                        color: rgb(255,255,255);\
                                        background-color: rgb(1, 130, 153);\
                                        subcontrol-origin: margin;\
                                        subcontrol-position: top center;\
                                        padding-left: 350px;\
                                        padding-right: 350px;  \
                                        border-radius: 9px;\
                                    }")

        self.uavCameraNumberLabel = QLabel(self.cameraBox)
        self.uavCameraNumberLabel.setObjectName("uavCameraNumberLabel")
        self.uavCameraNumberLabel.setGeometry(QRect(100, 30, 111, 31))

        self.uavCameraNumberSpinBox = QSpinBox(self.cameraBox)
        self.uavCameraNumberSpinBox.setObjectName("uavCameraNumberSpinBox")
        self.uavCameraNumberSpinBox.setGeometry(QRect(210, 30, 48, 27))
        self.uavCameraNumberSpinBox.setMinimum(1)
        self.uavCameraNumberSpinBox.setMaximum(1)



        self.freeControlBox = QGroupBox(self.centralwidget)
        self.freeControlBox.setObjectName("freeControlBox")
        self.freeControlBox.setGeometry(QRect(1160, 520, 421, 181))
        self.freeControlBox.setStyleSheet("QGroupBox#freeControlBox { \
                                                border: 1px solid gray;\
                                                border-color: #FF17365D;\
                                                font-size: 14px;\
                                                border-radius: 9px; }\
                                            QGroupBox:title {\
                                                color: rgb(255,255,255);\
                                                background-color: rgb(1, 130, 153);\
                                                subcontrol-origin: margin;\
                                                subcontrol-position: top center;\
                                                padding-left: 350px;\
                                                padding-right: 350px;  \
                                                border-radius: 9px;\
                                            }")

        self.freeControlTabWidget = QTabWidget(self.freeControlBox)
        self.freeControlTabWidget.setObjectName("freeControlTabWidget")
        self.freeControlTabWidget.setGeometry(QRect(10, 20, 401, 151))

        self.freeControlUavSelectTab = QWidget()
        self.freeControlUavSelectTab.setObjectName("freeControlUavSelectTab")

        

        self.freeControlUavLabel = QLabel(self.freeControlUavSelectTab)
        self.freeControlUavLabel.setObjectName("freeControlUavLabel")
        self.freeControlUavLabel.setGeometry(QRect(10, 30, 100, 22))

        self.fcSelectRemoveAllButton = QPushButton(self.freeControlUavSelectTab)
        self.fcSelectRemoveAllButton.setObjectName("fcSelectRemoveAllButton")
        self.fcSelectRemoveAllButton.setGeometry(QRect(10, 65, 181, 27))
        self.fcSelectRemoveAllButton.clicked.connect(lambda: self.selectRemoveAll(self.freeControlUavComboBox))

        self.disarmButton = QPushButton(self.freeControlUavSelectTab)
        self.disarmButton.setObjectName("disarmButton")
        self.disarmButton.setGeometry(QRect(280, 65, 99, 30))
        #self.disarmButton.clicked.connect(disarmCallback)
        self.disarmButton.setEnabled(False)

        self.armButton = QPushButton(self.freeControlUavSelectTab)
        self.armButton.setObjectName("armButton")
        self.armButton.setGeometry(QRect(280, 30, 99, 30))
        #self.armButton.clicked.connect(self.arm)
        self.armButton.setEnabled(False)        

        self.freeControlTabWidget.addTab(self.freeControlUavSelectTab, "")
        
        self.freeControlCommandTab = QWidget()
        self.freeControlCommandTab.setObjectName("freeControlCommandTab")
        
        self.takeoffButton = QPushButton(self.freeControlCommandTab)
        self.takeoffButton.setObjectName("takeoffButton")
        self.takeoffButton.setGeometry(QRect(10, 10, 99, 30))
        #self.takeoffButton.clicked.connect(self.takeoff)
        self.takeoffButton.setEnabled(False)        
        
        self.landButton = QPushButton(self.freeControlCommandTab)
        self.landButton.setObjectName("landButton")
        self.landButton.setGeometry(QRect(10, 45, 99, 30))
        #self.landButton.clicked.connect(self.land)
        self.landButton.setEnabled(False)        
        
        self.emergencyLandButton = QPushButton(self.freeControlCommandTab)
        self.emergencyLandButton.setObjectName("emergencyLandButton")
        self.emergencyLandButton.setGeometry(QRect(120, 10, 99, 30))
        #self.emergencyLandButton.clicked.connect(self.emergencyLand)
        self.emergencyLandButton.setEnabled(False)        
        
        self.smartLandButton = QPushButton(self.freeControlCommandTab)
        self.smartLandButton.setObjectName("smartLandButton")
        self.smartLandButton.setGeometry(QRect(230, 10, 151, 30))
        #self.smartLandButton.clicked.connect(self.smartLand)
        self.smartLandButton.setEnabled(False)        
        
        self.hoverButton = QPushButton(self.freeControlCommandTab)
        self.hoverButton.setObjectName("hoverButton")
        self.hoverButton.setGeometry(QRect(120, 45, 99, 30))
        #self.hoverButton.clicked.connect(self.hover)
        self.hoverButton.setEnabled(False)        
        
        self.gotoButton = QPushButton(self.freeControlCommandTab)
        self.gotoButton.setObjectName("gotoButton")
        self.gotoButton.setGeometry(QRect(230, 80, 151, 30))
        #self.gotoButton.clicked.connect(self.selectGoToTarget)
        self.gotoButton.setEnabled(False)        
        
        self.gotoHorizontalSpeedSpinBox = QSpinBox(self.freeControlCommandTab)
        self.gotoHorizontalSpeedSpinBox.setObjectName("gotoHorizontalSpeedSpinBox")
        self.gotoHorizontalSpeedSpinBox.setGeometry(QRect(140, 81, 48, 27))
        
        self.gotoHorizontalSpeedLabel = QLabel(self.freeControlCommandTab)
        self.gotoHorizontalSpeedLabel.setObjectName("gotoHorizontalSpeedLabel")
        self.gotoHorizontalSpeedLabel.setGeometry(QRect(30, 80, 101, 31))
        
        self.freeControlTabWidget.addTab(self.freeControlCommandTab, "")

        self.puvBox = QGroupBox(self.centralwidget)
        self.puvBox.setObjectName("puvBox")
        self.puvBox.setGeometry(QRect(760, 220, 821, 291))
        self.puvBox.setStyleSheet("QGroupBox#puvBox{ \
                                                border: 1px solid gray;\
                                                border-color: #FF17365D;\
                                                font-size: 14px;\
                                                border-radius: 9px; }\
                                            QGroupBox:title {\
                                                color: rgb(255,255,255);\
                                                background-color: rgb(1, 130, 153);\
                                                subcontrol-origin: margin;\
                                                subcontrol-position: top center;\
                                                padding-left: 400px;\
                                                padding-right: 400px;  \
                                                border-radius: 9px;\
                                            }")


        self.puvTable = QTableWidget(self.puvBox)
        self.puvTable.setObjectName("puvTable")
        self.puvTable.setGeometry(QRect(10, 20, 801, 261))
        self.puvTable.setStyleSheet("QTableWidget#puvTable { \
                                        border: 1px solid gray;\
                                        border-color: #FF17365D;\
                                        font-size: 14px;\
                                        border-radius: 9px; }\
                                        ")
        self.puvTable.setRowCount(2)
        self.puvTable.setColumnCount(17)
        self.puvTable.setItem(0,0, QTableWidgetItem("Modul No"))
        self.puvTable.setItem(0,1, QTableWidgetItem("Batarya Doluluk Orani"))
        self.puvTable.setItem(0,2, QTableWidgetItem("Batarya Voltaji"))
        self.puvTable.setItem(0,3, QTableWidgetItem("Bataryadan Cekilen Akim"))
        self.puvTable.setItem(0,4, QTableWidgetItem("Batarya Toplam Tuketimi"))
        self.puvTable.setItem(0,5, QTableWidgetItem("Modul Durumu"))
        self.puvTable.setItem(0,6, QTableWidgetItem("Hata Durumu"))
        self.puvTable.setItem(0,7, QTableWidgetItem("Otopilot Durumu"))
        self.puvTable.setItem(0,8, QTableWidgetItem("Irtifa"))
        self.puvTable.setItem(0,9, QTableWidgetItem("Yatay/Dikey Hiz"))
        self.puvTable.setItem(0,10, QTableWidgetItem("Konum"))
        self.puvTable.setItem(0,11, QTableWidgetItem("Anlik Uydu Sayisi"))
        self.puvTable.setItem(0,12, QTableWidgetItem("Yatay/Dikey Navigasyon Dogrulugu"))
        self.puvTable.setItem(0,13, QTableWidgetItem("YKI'ye Olan Uzaklik"))
        self.puvTable.setItem(0,14, QTableWidgetItem("Goreve Olan Uzaklik"))
        self.puvTable.setItem(0,15, QTableWidgetItem("Toplam Ucus Suresi"))
        self.puvTable.setItem(0,16, QTableWidgetItem("RSSI"))

        self.setCentralWidget(self.centralwidget)
        
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1600, 25))
        self.menuScenario = QMenu(self.menubar)
        self.menuScenario.setObjectName("menuScenario")
        self.menuScenarioType = QMenu(self.menuScenario)
        self.menuScenarioType.setObjectName("menuScenarioType")
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuScenario.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())


        self.missionTabWidget.setCurrentIndex(0)
        self.freeControlTabWidget.setCurrentIndex(0)

if __name__ == '__main__':

    # rospy.init_node("gui")

    app = QApplication( sys.argv )

    GCSGui = GCSGui()
    #app.lastWindowClosed.connect(GCSGui.onTerminate)
    # initiateDialog()
    GCSGui.show()

    app.exec_()