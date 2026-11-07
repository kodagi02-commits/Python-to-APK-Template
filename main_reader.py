from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.camera import Camera
import cv2
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from kivy.clock import Clock

class HitsterReaderApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.status_label = MDLabel(text="Irányítsd a kamerát a QR kódra", halign="center", font_style="H6", size_hint_y=None, height=50)
        layout.add_widget(self.status_label)
        
        # Élő kamera kép
        self.camera = Camera(play=True, size_hint=(1, 0.7))
        layout.add_widget(self.camera)
        
        # Stop gomb
        self.btn_stop = MDRaisedButton(text="⏹️ ZENE LEÁLLÍTÁSA (STOP)", size_hint=(1, None), height=70, md_bg_color=(1, 0.2, 0.2, 1))
        self.btn_stop.bind(on_release=self.stop_music)
        layout.add_widget(self.btn_stop)
        
        # Spotify inicializálás (Itt fixen be kell égetned a kódjaidat az offline működéshez)
        self.CLIENT_ID = "IDE_ÍRD_A_CLIENT_ID_T"
        self.CLIENT_SECRET = "IDE_ÍRD_A_CLIENT_SECRET_ET"
        self.REDIRECT_URI = "http://localhost:8888/callback"
        
        self.sp = None
        self.connect_spotify()
        
        # Kamera kép folyamatos szkennelése QR kód után (másodpercenként 2-szer)
        Clock.schedule_interval(self.scan_qr, 0.5)
        
        return layout

    def connect_spotify(self):
        try:
            sp_oauth = SpotifyOAuth(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET, redirect_uri=self.REDIRECT_URI, scope="user-modify-playback-state user-read-playback-state")
            self.sp = spotipy.Spotify(auth_manager=sp_oauth)
        except:
            self.status_label.text = "⚠️ Spotify kapcsolódási hiba!"

    def scan_qr(self, dt):
        if not self.camera.texture: return
        
        # Kivy kamera textúra átalakítása OpenCV formátumba
        texture = self.camera.texture
        size = texture.size
        pixels = texture.pixels
        pil_img = np.frombuffer(pixels, dtype=np.uint8).reshape(size[1], size[0], 4)
        cv2_img = cv2.cvtColor(pil_img, cv2.COLOR_RGBA2BGR)
        
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(cv2_img)
        
        if data and "://spotify.com" in data:
            self.play_track(data)

    def play_track(self, track_link):
        if not self.sp: return
        try:
            track_id = track_link.split("track/").split("?")
            track_uri = f"spotify:track:{track_id}"
            devices = self.sp.devices()
            if devices['devices']:
                self.sp.start_playback(device_id=devices['devices']['id'], uris=[track_uri])
                self.status_label.text = "▶️ Dal elindítva!"
        except:
            pass

    def stop_music(self, instance):
        if not self.sp: return
        try:
            self.sp.pause_playback()
            self.status_label.text = "⏹️ Zene leállítva!"
        except:
            pass

if __name__ == '__main__':
    HitsterReaderApp().run()
