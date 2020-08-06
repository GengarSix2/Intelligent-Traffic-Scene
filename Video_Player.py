from PyQt5.QtGui import QIcon, QFont, QPainter, QPixmap
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from Traffic_Scene_Detection import VideoProcessing
import qtawesome as qta
import datetime
import os


class VideoPlayer(QWidget):

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # 创建标题文本
        self.Title = QLabel()
        self.Title.setText("智能交通场景识别")
        self.Title.setAlignment(Qt.AlignCenter)
        self.Title.setFont(QFont("黑体", 12))
        self.Title.setFixedHeight(30)

        # 创建视频控件
        self.videoWidget = QVideoWidget()
        self.videoWidget.setStyleSheet('''QVideoWidget{background: #FFFAF0;}''')

        # 创建处理视频按键
        pro_icon = qta.icon('fa5s.tools', color='#EEC900')
        self.proButton = QPushButton()
        self.proButton.setStatusTip("Processing Video")
        self.proButton.setFixedHeight(45)
        self.proButton.setIcon(pro_icon)  # 设置图标
        self.proButton.setIconSize(QSize(35, 35))
        self.proButton.clicked.connect(self.ProcessVideo)
        self.proButton.setStyleSheet('''QPushButton{background: #FFEFD5;}''')

        # 创建选择视频文件按钮
        open_icon = qta.icon('fa5s.folder', color='#EEC900')
        self.openButton = QPushButton()
        self.openButton.setStatusTip("Open Video File")
        self.openButton.setFixedHeight(45)
        self.openButton.setIcon(open_icon)  # 设置图标
        self.openButton.setIconSize(QSize(38, 38))
        self.openButton.clicked.connect(self.abrir)
        self.openButton.setStyleSheet('''QPushButton{background: #FFEFD5;}''')


        # 创建play按钮
        play_icon = qta.icon('fa5s.play')
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedHeight(45)
        self.playButton.setIcon(play_icon)
        self.playButton.setIconSize(QSize(38, 38))
        self.playButton.clicked.connect(self.play)
        self.playButton.setStyleSheet('''QPushButton{background: #FFEFD5;}''')


        # 创建进度条控件 进度条跑的时候 颜色改变 且不显示进度条文字
        self.progressBar = QProgressBar(self.videoWidget)
        self.progressBar.setRange(0, 100)
        self.progressBar.setFixedHeight(30)
        self.progressBar.setStyleSheet('''
                    QProgressBar::chunk {
                        background-color: green;
                    }
                ''')
        self.progressBar.setTextVisible(False)


        # 创建选择框
        self.cb_1 = QCheckBox("识别行人违规行为")
        self.cb_1.setFont(QFont("黑体", 12))
        self.cb_1.setChecked(True)

        self.cb_2 = QCheckBox("识别车牌")
        self.cb_2.setFont(QFont("黑体", 12))
        self.cb_2.setChecked(False)

        self.cb_3 = QCheckBox("检测车速")
        self.cb_3.setFont(QFont("黑体", 12))
        self.cb_3.setChecked(False)

        # 创建状态控件
        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("黑体", 12))
        self.statusBar.setFixedHeight(25)


        # 设置布局
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.proButton)
        controlLayout.addWidget(self.openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addSpacing(10)
        controlLayout.addWidget(self.progressBar)

        # 设置选择框布局
        CheckBox_layout = QHBoxLayout()
        CheckBox_layout.setContentsMargins(5, 5, 0, 0)
        CheckBox_layout.addWidget(self.cb_1)
        CheckBox_layout.addWidget(self.cb_2)
        CheckBox_layout.addWidget(self.cb_3)


        layout = QVBoxLayout()
        layout.addWidget(self.Title)
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout) # 选择框布局
        layout.addLayout(CheckBox_layout)
        layout.addWidget(self.statusBar)

        self.setLayout(layout)


        # 设置控件事件
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage("请点击上方工具图标并选择您想要处理的视频，处理完成后点击文件夹图标选择视频进行播放。")


    def ProcessVideo(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona los mediose",
                                                  ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")

        if fileName != '':
            self.statusBar.showMessage("视频处理中，请耐心等待。")
            today = datetime.date.today().strftime("%y%m%d")
            video = VideoProcessing()
            video.flags["video"] = fileName
            video.flags["output"] = "./Image&Video/" + today + "-result.avi"
            video.Traffic_Light_Recognition = self.cb_1.isChecked()
            video.License_Plate_Recognition = self.cb_2.isChecked()
            video.Estimate_Speed = self.cb_3.isChecked()
            video.Run()
            res_path = os.getcwd().replace('\\','/')+video.flags["output"]
            self.statusBar.showMessage("结果已存放于: {}".format(res_path))


    def abrir(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Selecciona los mediose",
                ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.statusBar.showMessage(fileName)
            self.play()


    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.progressBar.setValue(position)

    def durationChanged(self, duration):
        self.progressBar.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.setWindowTitle("VideoPlayer")
    player.resize(1000, 700)
    # 设置对象名称
    player.setObjectName("MainWindow")
    # 设置窗口背景色
    player.setStyleSheet("#MainWindow{background-color: #FAEBD7}")

    player.show()
    sys.exit(app.exec_())