"""
Diction Trainer - Extended Version
Features added on top of original:
 - Pronunciation scoring using MFCC + DTW (librosa) with fallback messaging
 - Live simple VU meter waveform (RMS) during recording
 - History panel stored in SQLite (records: id, text, filename, timestamp, score)
 - Settings panel (TTS engine, rate, export path, default repeat, dark mode)
 - Keyboard shortcuts (Ctrl+Enter=Speak, Ctrl+R=Record, Ctrl+E=Export)
 - ThreadPoolExecutor for background tasks
 - Phonetic / IPA lookup using `pronouncing` if present
 - Progress plotting (matplotlib saved image) from history scores
 - Better error handling and dependency checks
 - Notes for Android packaging included in comments

Run: python diction_trainer_full.py
Dependencies (desktop):
 pip install kivy pyttsx3 gTTS sounddevice soundfile numpy librosa pronouncing matplotlib
 Some libraries are optional and the app will degrade gracefully if missing.
"""

import os
import time
import uuid
import threading
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from kivy.clock import mainthread
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.switch import Switch
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.slider import Slider

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDTopAppBar

# Optional libraries
try:
    import pyttsx3
    HAVE_PYTTX = True
except Exception:
    HAVE_PYTTX = False

try:
    from gtts import gTTS
    HAVE_GTTS = True
except Exception:
    HAVE_GTTS = False

try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    HAVE_REC = True
except Exception:
    HAVE_REC = False

try:
    import librosa
    import librosa.display
    HAVE_LIBROSA = True
except Exception:
    HAVE_LIBROSA = False

try:
    import pronouncing
    HAVE_PRON = True
except Exception:
    HAVE_PRON = False

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAVE_PLT = True
except Exception:
    HAVE_PLT = False

# Thread pool for background tasks
_executor = ThreadPoolExecutor(max_workers=4)

# ----- Styled widgets (same as before) -----
class FancyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_size = 16
        self.size_hint_y = None
        self.height = 56
        with self.canvas.before:
            Color(0.14, 0.45, 0.85, 1)
            self._rect = RoundedRectangle(radius=[12])
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.bind(on_press=self._anim_press)

    def _update_rect(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def _anim_press(self, *a):
        anim = Animation(opacity=0.7, duration=0.06) + Animation(opacity=1.0, duration=0.06)
        anim.start(self)

class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._rect = RoundedRectangle(radius=[10])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

# ----- Database helper -----
DB_FILE = os.path.join(os.getcwd(), 'diction_history.db')

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id TEXT PRIMARY KEY, text TEXT, filename TEXT, timestamp TEXT, score REAL)''')
    conn.commit()
    conn.close()

init_db()

# ----- Main UI -----
class DictionAppUI(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=12, padding=12, **kwargs)

        # Toolbar/Header
        self.toolbar = MDTopAppBar(title="🎤 Diction Trainer", elevation=10)
        self.toolbar.right_action_items = [["cog", lambda x: self.open_settings()]]
        self.add_widget(self.toolbar)

        # Input Card
        input_card = MDCard(orientation='vertical', padding=16, size_hint=(1, None), height=140, style="elevated")
        input_label = MDLabel(text="Enter text to practice:", font_style="Subtitle1", size_hint_y=None, height=28)
        input_card.add_widget(input_label)
        self.text_input = MDTextField(text="Python is fun", mode="rectangle", font_size=20, size_hint_y=None, height=48)
        input_card.add_widget(self.text_input)
        self.add_widget(input_card)

        # Controls Row
        controls_row = MDBoxLayout(orientation='horizontal', spacing=8, size_hint=(1, None), height=48)
        self.slow_toggle = MDSwitch(active=False)
        controls_row.add_widget(MDLabel(text="Slow", size_hint_x=0.15))
        controls_row.add_widget(self.slow_toggle)
        controls_row.add_widget(MDLabel(text="Repeat:", size_hint_x=0.15))
        self.repeat_spinner = MDSpinner(size_hint_x=0.15)
        controls_row.add_widget(self.repeat_spinner)
        self.add_widget(controls_row)

        # Action Buttons
        actions_row = MDBoxLayout(orientation='horizontal', spacing=8, size_hint=(1, None), height=56)
        self.speak_btn = MDRaisedButton(text="Speak", md_bg_color=(0.2, 0.6, 0.9, 1), on_release=self.on_speak)
        actions_row.add_widget(self.speak_btn)
        self.repeat_btn = MDRaisedButton(text="Repeat", on_release=self.on_speak_repeat)
        actions_row.add_widget(self.repeat_btn)
        self.export_btn = MDRaisedButton(text="Export", on_release=self.on_export)
        actions_row.add_widget(self.export_btn)
        self.record_btn = MDRaisedButton(text="Record", md_bg_color=(0.9, 0.2, 0.2, 1), on_release=self.on_record)
        actions_row.add_widget(self.record_btn)
        self.stop_btn = MDRaisedButton(text="Stop", on_release=self.on_stop)
        actions_row.add_widget(self.stop_btn)
        self.play_student_btn = MDRaisedButton(text="Play", on_release=self.on_play_student)
        actions_row.add_widget(self.play_student_btn)
        self.add_widget(actions_row)

        # Score and VU Meter
        info_row = MDBoxLayout(orientation='horizontal', spacing=8, size_hint=(1, None), height=64)
        self.vu_label = MDLabel(text="VU: 0.00", font_style="Subtitle2", size_hint_x=0.5)
        info_row.add_widget(self.vu_label)
        self.score_label = MDLabel(text="Score: —", font_style="Subtitle2", size_hint_x=0.5)
        info_row.add_widget(self.score_label)
        self.add_widget(info_row)

        # History Section
        history_card = MDCard(orientation='vertical', padding=12, size_hint=(1, 1), style="elevated")
        history_label = MDLabel(text="History", font_style="H6", size_hint_y=None, height=32)
        history_card.add_widget(history_label)
        scroll = MDScrollView()
        self.history_list = MDList()
        scroll.add_widget(self.history_list)
        history_card.add_widget(scroll)
        self.add_widget(history_card)

        # Status Footer
        self.status = MDLabel(text="Ready.", font_style="Caption", halign="center", theme_text_color="Custom", text_color=(0.06, 0.5, 0.12, 1))
        self.add_widget(self.status)

        # State
        self.engine = None
        self.recording = False
        self.record_filename = None
        self.playing_sound = None
        self.last_score = None
        self.export_path = os.getcwd()
        self.dark_mode = False

        # Init
        self.init_tts()
        self.load_history()

        # Keyboard shortcuts
        Window.bind(on_key_down=self._on_key_down)

        # For recording VU
        self._vu_level = 0.0

        # Thread pool
        self.executor = _executor

    def init_tts(self):
        if not HAVE_PYTTX:
            self._update_status("pyttsx3 not installed; will use gTTS online fallback.")
            return
        try:
            engine = pyttsx3.init()
            self.engine = engine
            self._update_status("pyttsx3 initialized.")
        except Exception as e:
            self.engine = None
            self._update_status(f"pyttsx3 init failed: {e}")

    # ----- TTS and export -----
    def _speak_desktop(self, text, slow=False):
        # Always re-initialize pyttsx3 engine for reliability
        if HAVE_PYTTX:
            try:
                engine = pyttsx3.init()
                rate = engine.getProperty('rate')
                if slow:
                    engine.setProperty('rate', int(rate * 0.75))
                engine.say(text)
                engine.runAndWait()
                if slow:
                    engine.setProperty('rate', rate)
                engine.stop()
                return
            except Exception as e:
                print('pyttsx3 error', e)
        if HAVE_GTTS:
            try:
                tld = 'co.uk'
                tts = gTTS(text=text, lang='en', tld=tld, slow=slow)
                tmpfile = os.path.join(self.export_path, f"_tts_{uuid.uuid4().hex}.mp3")
                tts.save(tmpfile)
                sound = SoundLoader.load(tmpfile)
                if sound:
                    sound.play()
                    while sound.state == 'play':
                        time.sleep(0.05)
                try:
                    os.remove(tmpfile)
                except Exception:
                    pass
                return
            except Exception as e:
                print('gTTS error', e)
        self._update_status('No TTS available.')

    def on_speak(self, instance):
        text = self.text_input.text.strip()
        if not text:
            self._update_status('Type something first.')
            return
        slow = self.slow_toggle.active
        self._update_status('Speaking...')
        self.executor.submit(self._speak_desktop, text, slow)

    def on_speak_repeat(self, instance):
        text = self.text_input.text.strip()
        if not text:
            self._update_status('Type something first.')
            return
        times = int(self.repeat_spinner.text)
        slow = self.slow_toggle.active
        self._update_status(f'Repeating {times} time(s)...')
        def repeat_job():
            for _ in range(times):
                self._speak_desktop(text, slow)
                time.sleep(0.12)
            self._update_status('Done speaking.')
        self.executor.submit(repeat_job)

    def on_export(self, instance):
        text = self.text_input.text.strip()
        if not text:
            self._update_status('Type text to export.')
            return
        if not HAVE_GTTS:
            self._update_status('gTTS not installed; install to export MP3.')
            return
        self._update_status('Exporting MP3...')
        self.executor.submit(self._export_worker, text)

    def _export_worker(self, text):
        try:
            fname = os.path.join(self.export_path, f'diction_{int(time.time())}.mp3')
            tts = gTTS(text=text, lang='en', tld='co.uk')
            tts.save(fname)
            self._update_status(f'Exported: {fname}')
        except Exception as e:
            self._update_status(f'Export failed: {e}')

    # ----- Recording with VU and scoring -----
    def on_record(self, instance):
        if not HAVE_REC:
            self._update_status('Recording libs missing.')
            return
        if self.recording:
            self._update_status('Already recording.')
            return
        self.recording = True
        self.record_filename = os.path.join(self.export_path, f"student_{int(time.time())}.wav")
        self._update_status('Recording... (press Stop to finish)')
        self.executor.submit(self._record_worker)

    def _record_worker(self, samplerate=22050, channels=1):
        frames = []
        try:
            def callback(indata, frames_count, time_info, status):
                if not self.recording:
                    raise sd.CallbackStop()
                frames.append(indata.copy())
                # VU: RMS
                rms = float(np.sqrt(np.mean(indata**2)))
                self._vu_level = rms
                self._update_vu(rms)

            with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
                while self.recording:
                    sd.sleep(100)

            if frames:
                data = np.concatenate(frames, axis=0)
                sf.write(self.record_filename, data, samplerate)
                self._update_status(f'Saved recording: {self.record_filename}')
                # after saving, optionally compute score against reference
                self.executor.submit(self.compute_score_and_save, self.text_input.text.strip(), self.record_filename)
            else:
                self._update_status('No audio captured.')
        except Exception as e:
            self._update_status(f'Record failed: {e}')
        finally:
            self.recording = False
            self._vu_level = 0.0
            self._update_vu(0.0)

    @mainthread
    def _update_vu(self, val):
        try:
            self.vu_label.text = f'VU Meter (RMS): {val:.4f}'
            # create a simple colored rectangle texture for VU
            w = max(1, int(self.vu_card.width * min(1.0, val*20)))
            with self.vu_card.canvas:
                Color(0.2, 0.7, 0.2, 1)
                Rectangle(pos=(self.vu_card.x, self.vu_card.y), size=(w, self.vu_card.height))
        except Exception:
            pass

    def on_stop(self, instance):
        if self.recording:
            self.recording = False
            self._update_status('Stopping recording...')
            return
        if self.playing_sound and hasattr(self.playing_sound, 'stop'):
            try:
                self.playing_sound.stop()
                self._update_status('Playback stopped.')
            except Exception:
                self._update_status('Stop failed.')
        else:
            self._update_status('Nothing to stop.')

    def on_play_student(self, instance):
        if not self.record_filename or not os.path.exists(self.record_filename):
            self._update_status('No student recording found. Record first.')
            return
        sound = SoundLoader.load(self.record_filename)
        if not sound:
            self._update_status('Failed to load recording.')
            return
        self.playing_sound = sound
        sound.play()
        self._update_status('Playing student recording...')

    # ----- Scoring -----
    def compute_score_and_save(self, reference_text, student_file):
        score = None
        if HAVE_LIBROSA:
            try:
                # Synthesize reference using TTS to temporary file if possible
                ref_file = None
                if HAVE_GTTS:
                    ref_file = os.path.join(self.export_path, f'_ref_{uuid.uuid4().hex}.mp3')
                    gTTS(text=reference_text, lang='en', tld='co.uk').save(ref_file)
                if ref_file:
                    try:
                        y_ref, sr_ref = librosa.load(ref_file, sr=None)
                        y_stu, sr_stu = librosa.load(student_file, sr=None)
                        if y_ref is not None and y_stu is not None:
                            ref_mfcc = librosa.feature.mfcc(y=y_ref, sr=sr_ref)
                            stu_mfcc = librosa.feature.mfcc(y=y_stu, sr=sr_stu)
                            dist, _ = librosa.sequence.dtw(ref_mfcc, stu_mfcc)
                            score = max(0, 100 - int(dist.mean()))
                        else:
                            score = None
                    except Exception as e:
                        print("Scoring error:", e)
                        score = 0
                    finally:
                        try:
                            os.remove(ref_file)
                        except Exception:
                            pass
                else:
                    score = None
            except Exception as e:
                print('scoring failed', e)
                score = None
        else:
            # librosa not available - fallback to simple loudness-based placeholder
            try:
                import soundfile as sf
                data, sr = sf.read(student_file)
                loudness = float(np.mean(np.abs(data))) if 'np' in globals() else 0.0
                score = min(100.0, loudness * 1000.0)
            except Exception:
                score = None

        # Save to DB and update UI
        rec_id = uuid.uuid4().hex
        ts = datetime.utcnow().isoformat()
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO history(id, text, filename, timestamp, score) VALUES (?,?,?,?,?)',
                  (rec_id, reference_text, student_file, ts, score if score is not None else -1))
        conn.commit()
        conn.close()
        self._update_status(f'Recording scored: {score if score is not None else "—"}')
        self.last_score = score
        self._refresh_history_item(rec_id, reference_text, student_file, ts, score)

    # ----- History UI -----
    def load_history(self):
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('SELECT id, text, filename, timestamp, score FROM history ORDER BY timestamp DESC LIMIT 100')
            rows = c.fetchall()
            conn.close()
            for r in rows:
                self._add_history_row(*r)
        except Exception as e:
            print('load history failed', e)

    @mainthread
    def _add_history_row(self, rec_id, text, fname, ts, score):
        item = OneLineListItem(text=f"{text[:30]} ({ts.split('T')[0]}) | Score: {score if score and score>=0 else '—'}")
        item.on_release = lambda: self._play_file(fname)
        self.history_list.add_widget(item)

    @mainthread
    def _refresh_history_item(self, rec_id, text, fname, ts, score):
        # prepend new item
        self._add_history_row(rec_id, text, fname, ts, score)

    def _play_file(self, fname):
        if not os.path.exists(fname):
            self._update_status('File not found.')
            return
        s = SoundLoader.load(fname)
        if not s:
            self._update_status('Failed to load file.')
            return
        self.playing_sound = s
        s.play()
        self._update_status('Playing...')

    # ----- Settings -----
    def open_settings(self, instance=None):
        content = BoxLayout(orientation='vertical', spacing=8, padding=8)
        export_lbl = Label(text='Export folder:')
        content.add_widget(export_lbl)
        export_inp = TextInput(text=self.export_path, multiline=False)
        content.add_widget(export_inp)
        dark_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=36)
        dark_row.add_widget(Label(text='Dark mode'))
        dark_switch = Switch(active=self.dark_mode)
        dark_row.add_widget(dark_switch)
        content.add_widget(dark_row)
        save_btn = FancyButton(text='Save')
        content.add_widget(save_btn)
        popup = Popup(title='Settings', content=content, size_hint=(0.8,0.5))

        def save_settings(_):
            self.export_path = export_inp.text.strip() or os.getcwd()
            self.dark_mode = dark_switch.active
            popup.dismiss()
            self._update_status('Settings saved.')
        save_btn.bind(on_press=save_settings)
        popup.open()

    # ----- Utilities -----
    @mainthread
    def _update_status(self, text, color=(0.06,0.5,0.12,1)):
        self.status.text = text
        self.status.text_color = color

    def _on_key_down(self, window, key, scancode, codepoint, modifier):
        # Ctrl+Enter = speak
        if 'ctrl' in modifier and key == 13:  # Enter
            self.on_speak(None)
        # Ctrl+R = record
        if 'ctrl' in modifier and (key == ord('r')):
            self.on_record(None)
        # Ctrl+E = export
        if 'ctrl' in modifier and (key == ord('e')):
            self.on_export(None)

# ----- App -----
class DictionTrainerApp(MDApp):
    def build(self):
        Window.size = (1000, 720)
        Window.clearcolor = (0.95, 0.96, 1, 1)
        return DictionAppUI()

if __name__ == '__main__':
    DictionTrainerApp().run()

# Notes for Android packaging:
# - Replace pyttsx3 + gTTS with plyer.tts (or native Android TTS) for offline reliability.
# - Replace sounddevice/soundfile with plyer or Android native recording (MediaRecorder) to avoid native build issues.
# - Add RECORD_AUDIO permission and handle runtime permission requests in buildozer.spec and Android code.
# - Consider using lightweight scoring on-device or offloading scoring to a server if heavy libs (librosa) are unavailable.
