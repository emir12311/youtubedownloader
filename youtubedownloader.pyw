from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from yt_dlp import YoutubeDL
from youtubedownloader_ui import Ui_MainWindow
import sys, requests, qtmodern.styles

API_KEY = "YOUR_API_KEY" # gotta be a youtube data api v3

class DownloaderWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.u = Ui_MainWindow()
        self.u.setupUi(self)
        self.labels = [self.u.thumbnail1, self.u.thumbnail2, self.u.thumbnail3, self.u.thumbnail4]
        self.label_buttons = [self.u.thumbnail1download, self.u.thumbnail2download, self.u.thumbnail3download, self.u.thumbnail4download]
        self.label_texts = [self.u.label_5, self.u.label_6, self.u.label_7, self.u.label_8]
        self.file_action_list = [self.u.actionOnly_Video, self.u.actionOnly_Audio, self.u.actionVideo_Audio]
        self.format_menu_list = [self.u.menuVideo, self.u.menuAudio, self.u.menuVideo_Audio]
        self.video_menu_subaction_list = [self.u.action_mp4, self.u.action_webm]
        self.audio_menu_subaction_list = [self.u.action_mp3, self.u.action_opus]
        self.video_audio_menu_subaction_list = [self.u.action_mp4_2, self.u.action_webm_2]
        self.video_ids = []
        self.setupui()

    def setupui(self):
        for button in self.label_buttons:
            button.hide()
        self.u.searchbutton.pressed.connect(self.search_videos)
        self.u.thumbnail1download.pressed.connect(self.download_video)
        self.u.thumbnail2download.pressed.connect(self.download_video)
        self.u.thumbnail3download.pressed.connect(self.download_video)
        self.u.thumbnail4download.pressed.connect(self.download_video)
        self.u.actionOnly_Audio.triggered.connect(self.keep_action_and_menu_in_check)
        self.u.actionOnly_Video.triggered.connect(self.keep_action_and_menu_in_check)
        self.u.actionVideo_Audio.triggered.connect(self.keep_action_and_menu_in_check)
        self.u.action_mp4.triggered.connect(self.keep_subaction_in_check)
        self.u.action_mp3.triggered.connect(self.keep_subaction_in_check)
        self.u.action_mp4_2.triggered.connect(self.keep_subaction_in_check)
        self.u.action_webm.triggered.connect(self.keep_subaction_in_check)
        self.u.action_webm_2.triggered.connect(self.keep_subaction_in_check)
        self.u.action_opus.triggered.connect(self.keep_subaction_in_check)
    

    def search_videos(self):
        self.query = self.u.searchbar.text()
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=4&q={self.query}&key={API_KEY}"
        try:
            self.response = requests.get(url).json()
        except:
            QMessageBox.warning(self, "Error", "Couldnt get response")
            return
        self.videos = []
        for item in self.response.get("items", []):
            vid_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            thumb_url = item["snippet"]["thumbnails"]["medium"]["url"]
            self.videos.append((vid_id, title, thumb_url))
        self.display_videos(self.videos)

    def display_videos(self, videos):
        self.video_ids = []
        for label, label_text, video in zip(self.labels, self.label_texts, videos):
            vid_id, title, thumb_url = video
            try:
                self.r = requests.get(thumb_url, timeout=5)
                pixmap = QPixmap()
                pixmap.loadFromData(self.r.content)
                label.setPixmap(pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            except:
                label.setText("No image")
            self.video_ids.append(vid_id)
            label_text.setText(title)
        for button in self.label_buttons:
            button.show()
    
    def download_video(self):
        for index, menu in enumerate(self.format_menu_list):
            if menu.isEnabled():
                self.chosen_menu = index
                break
        if self.chosen_menu == 0:
            ydl_opts = {
                "format": "bestvideo",
                "quiet": True,
                "no_warnings": True,
            }
            for subaction in self.video_menu_subaction_list:
                if subaction.isChecked():
                    ydl_opts["format"] = f"bestvideo[ext={subaction.text().split(".")[1]}]"
        elif self.chosen_menu == 1:
            ydl_opts = {
                "format": "bestaudio/best",
                "quiet": True,
                "no_warnings": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3"
                }, {
                    "key": "EmbedThumbnail"
                }],
                "writethumbnail": True
            }
            for subaction in self.audio_menu_subaction_list:
                if subaction.isChecked():
                    ydl_opts["postprocessors"][0]["preferredcodec"] = subaction.text().split(".")[1]
        else:
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "quiet": True,
                "no_warnings": True,
                "merge_output_format": "mp4",
                "keepvideo": False,
                "postprocessor_args": ["-y"]
            }
            for subaction in self.video_audio_menu_subaction_list:
                if subaction.isChecked():
                    ydl_opts["merge_output_format"] = subaction.text().split(".")[1]
        
        def download(videoid):
            YoutubeDL(ydl_opts).download([f"https://www.youtube.com/watch?v={videoid}"])
  
        self.sender_button = self.sender()
        if self.sender_button == self.u.thumbnail1download:
            download(self.video_ids[0])
        elif self.sender_button == self.u.thumbnail2download:
            download(self.video_ids[1])
        elif self.sender_button == self.u.thumbnail3download:
            download(self.video_ids[2])
        else:
            download(self.video_ids[3])
    
    def keep_action_and_menu_in_check(self):
        self.sender_action_file = self.sender()
        self.nonsender_index_numbers = []
        self.all_index_numbers = []
        for index, file_action in enumerate(self.file_action_list):  
            if self.sender_action_file.isChecked():
                if file_action != self.sender_action_file:
                    file_action.setChecked(False)
                    self.nonsender_index_numbers.append(index)
        for index in range(0, len(self.format_menu_list)):
            self.all_index_numbers.append(index)
        for index in self.nonsender_index_numbers:
            self.format_menu_list[index].setEnabled(False)
        for index in list(set(self.all_index_numbers) - set(self.nonsender_index_numbers)):
            self.format_menu_list[index].setEnabled(True)

    def keep_subaction_in_check(self):
        self.subaction_sender = self.sender()
        for subaction_list in [self.video_menu_subaction_list, self.audio_menu_subaction_list, self.video_audio_menu_subaction_list]:    
            if self.subaction_sender in subaction_list:
                for action in subaction_list:
                    if action == self.subaction_sender:
                        action.setChecked(True)
                    else:
                        action.setChecked(False)

app = QApplication(sys.argv)
qtmodern.styles.dark(app)
window = DownloaderWindow()
window.show()
sys.exit(app.exec_())