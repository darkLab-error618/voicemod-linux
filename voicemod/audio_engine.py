"""Real-time audio engine"""

import numpy as np
import sounddevice as sd
from .audio_processor import AudioProcessor


class AudioEngine:
    """Manages real-time audio stream"""
    
    def __init__(self, sample_rate=44100, block_size=2048):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.processor = AudioProcessor(sample_rate)
        self.stream = None
        self.is_running = False
        self.current_effect = None
        self.pitch_shift = 0
        self.volume_gain = 0
        self.input_device = None
        self.output_device = None
        
    def get_input_devices(self):
        """Get list of input devices"""
        devices = sd.query_devices()
        input_devices = []
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                input_devices.append((i, device['name']))
        return input_devices
    
    def get_output_devices(self):
        """Get list of output devices"""
        devices = sd.query_devices()
        output_devices = []
        for i, device in enumerate(devices):
            if device['max_output_channels'] > 0:
                output_devices.append((i, device['name']))
        return output_devices
    
    def set_input_device(self, device_id):
        self.input_device = device_id
    
    def set_output_device(self, device_id):
        self.output_device = device_id
    
    def set_pitch_shift(self, semitones):
        self.pitch_shift = semitones
    
    def set_volume_gain(self, db):
        self.volume_gain = db
    
    def set_effect(self, effect_name):
        self.current_effect = effect_name
    
    def start(self):
        """Start audio stream"""
        if self.is_running:
            return
        self.is_running = True
        self.stream = sd.Stream(
            device=(self.input_device, self.output_device),
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            channels=1,
            callback=self._audio_callback,
            latency='low'
        )
        self.stream.start()
    
    def stop(self):
        """Stop audio stream"""
        if not self.is_running:
            return
        self.is_running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
    
    def _audio_callback(self, indata, outdata, frames, time_info, status):
        """Audio callback for processing"""
        if status:
            print(f"Audio status: {status}")
        
        try:
            audio = indata[:, 0].copy()
            
            if self.current_effect == "robot":
                audio = self.processor.apply_robot_effect(audio)
            elif self.current_effect == "alien":
                audio = self.processor.apply_alien_effect(audio)
            elif self.current_effect == "echo":
                audio = self.processor.apply_echo_effect(audio)
            elif self.current_effect == "reverb":
                audio = self.processor.apply_reverb_effect(audio)
            elif self.current_effect == "deep":
                audio = self.processor.apply_deep_effect(audio)
            elif self.current_effect == "high":
                audio = self.processor.apply_high_effect(audio)
            
            if self.pitch_shift != 0:
                audio = self.processor.apply_pitch_shift(audio, self.pitch_shift)
            
            if self.volume_gain != 0:
                audio = self.processor.apply_volume(audio, self.volume_gain)
            
            outdata[:, 0] = audio
        except Exception as e:
            print(f"Error in audio callback: {e}")
            outdata.fill(0)
