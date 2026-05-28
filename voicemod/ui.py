"""GUI using PyQt6"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QPushButton, QComboBox, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .audio_engine import AudioEngine


class VoiceModApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceMod Linux - Voice Modification")
        self.setGeometry(100, 100, 500, 600)
        self.audio_engine = AudioEngine()
        self.init_ui()
        self.load_devices()
    
    def init_ui(self):
        """Initialize user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        title = QLabel("VoiceMod Linux")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        main_layout.addWidget(title)
        
        # Audio Devices
        devices_group = QGroupBox("Audio Devices")
        devices_layout = QGridLayout()
        devices_layout.addWidget(QLabel("Input Device:"), 0, 0)
        self.input_device_combo = QComboBox()
        devices_layout.addWidget(self.input_device_combo, 0, 1)
        devices_layout.addWidget(QLabel("Output Device:"), 1, 0)
        self.output_device_combo = QComboBox()
        devices_layout.addWidget(self.output_device_combo, 1, 1)
        devices_group.setLayout(devices_layout)
        main_layout.addWidget(devices_group)
        
        # Effects
        effects_group = QGroupBox("Voice Effects")
        effects_layout = QVBoxLayout()
        effects_layout.addWidget(QLabel("Select Effect:"))
        self.effect_combo = QComboBox()
        self.effect_combo.addItems(["None", "Deep Voice", "High Pitch", "Robot", "Alien", "Echo", "Reverb"])
        self.effect_combo.currentTextChanged.connect(self.on_effect_changed)
        effects_layout.addWidget(self.effect_combo)
        effects_group.setLayout(effects_layout)
        main_layout.addWidget(effects_group)
        
        # Pitch Shift
        pitch_group = QGroupBox("Pitch Shift")
        pitch_layout = QHBoxLayout()
        pitch_layout.addWidget(QLabel("Semitones:"))
        self.pitch_slider = QSlider(Qt.Orientation.Horizontal)
        self.pitch_slider.setRange(-12, 12)
        self.pitch_slider.setValue(0)
        self.pitch_slider.sliderMoved.connect(self.on_pitch_changed)
        pitch_layout.addWidget(self.pitch_slider)
        self.pitch_label = QLabel("0")
        pitch_layout.addWidget(self.pitch_label)
        pitch_group.setLayout(pitch_layout)
        main_layout.addWidget(pitch_group)
        
        # Volume
        volume_group = QGroupBox("Volume")
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Gain (dB):"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(-20, 20)
        self.volume_slider.setValue(0)
        self.volume_slider.sliderMoved.connect(self.on_volume_changed)
        volume_layout.addWidget(self.volume_slider)
        self.volume_label = QLabel("0")
        volume_layout.addWidget(self.volume_label)
        volume_group.setLayout(volume_layout)
        main_layout.addWidget(volume_group)
        
        # Controls
        button_group = QGroupBox("Controls")
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.on_start)
        button_layout.addWidget(self.start_button)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.on_stop)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        button_group.setLayout(button_layout)
        main_layout.addWidget(button_group)
        
        self.status_label = QLabel("Status: Stopped")
        main_layout.addWidget(self.status_label)
        main_layout.addStretch()
        central_widget.setLayout(main_layout)
    
    def load_devices(self):
        """Load available audio devices"""
        input_devices = self.audio_engine.get_input_devices()
        output_devices = self.audio_engine.get_output_devices()
        for device_id, device_name in input_devices:
            self.input_device_combo.addItem(device_name, device_id)
        for device_id, device_name in output_devices:
            self.output_device_combo.addItem(device_name, device_id)
    
    def on_effect_changed(self, effect_name):
        effect_map = {
            "None": None, "Deep Voice": "deep", "High Pitch": "high",
            "Robot": "robot", "Alien": "alien", "Echo": "echo", "Reverb": "reverb"
        }
        self.audio_engine.set_effect(effect_map.get(effect_name))
    
    def on_pitch_changed(self, value):
        self.pitch_label.setText(str(value))
        self.audio_engine.set_pitch_shift(value)
    
    def on_volume_changed(self, value):
        self.volume_label.setText(str(value))
        self.audio_engine.set_volume_gain(value)
    
    def on_start(self):
        input_device = self.input_device_combo.currentData()
        output_device = self.output_device_combo.currentData()
        self.audio_engine.set_input_device(input_device)
        self.audio_engine.set_output_device(output_device)
        self.audio_engine.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("Status: Running")
    
    def on_stop(self):
        self.audio_engine.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("Status: Stopped")
    
    def closeEvent(self, event):
        if self.audio_engine.is_running:
            self.audio_engine.stop()
        event.accept()
