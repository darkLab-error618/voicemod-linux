"""Audio processing module for voice modification"""

import numpy as np
from scipy import signal
from scipy.fft import fft, ifft


class AudioProcessor:
    """Handles audio effects and processing"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.buffer_size = 2048
        
    def apply_pitch_shift(self, audio, semitones):
        """
        Apply pitch shift using phase vocoder
        semitones: positive for higher pitch, negative for lower
        """
        if semitones == 0:
            return audio
            
        factor = 2 ** (semitones / 12.0)
        return self._time_stretch(audio, 1/factor)
    
    def apply_robot_effect(self, audio):
        """Apply robot/vocoder effect"""
        n_bands = 8
        bands = []
        
        for i in range(n_bands):
            low_freq = 100 * (2 ** i)
            high_freq = 100 * (2 ** (i + 1))
            
            if high_freq > self.sample_rate / 2:
                high_freq = self.sample_rate / 2 - 100
                
            if low_freq < high_freq:
                filtered = self._bandpass_filter(audio, low_freq, high_freq)
                envelope = np.abs(signal.hilbert(filtered))
                carrier = np.sin(2 * np.pi * low_freq * np.arange(len(audio)) / self.sample_rate)
                bands.append(envelope * carrier)
        
        result = np.sum(bands, axis=0) / len(bands) if bands else audio
        return np.clip(result, -1.0, 1.0)
    
    def apply_alien_effect(self, audio):
        """Apply alien/UFO-like effect"""
        pitch_shift = self.apply_pitch_shift(audio, 12)
        t = np.arange(len(audio)) / self.sample_rate
        modulation = 1 + 0.3 * np.sin(2 * np.pi * 3 * t)
        result = pitch_shift * modulation
        return np.clip(result, -1.0, 1.0)
    
    def apply_echo_effect(self, audio, delay_ms=500, decay=0.6):
        """Apply echo/delay effect"""
        delay_samples = int(delay_ms * self.sample_rate / 1000)
        output = np.copy(audio)
        if delay_samples < len(audio):
            output[delay_samples:] += audio[:-delay_samples] * decay
        return np.clip(output, -1.0, 1.0)
    
    def apply_reverb_effect(self, audio):
        """Simple reverb using convolution"""
        ir_length = int(0.5 * self.sample_rate)
        decay = np.exp(-np.arange(ir_length) / (0.1 * self.sample_rate))
        ir = np.random.randn(ir_length) * decay * 0.1
        ir[0] += 1.0
        result = signal.fftconvolve(audio, ir, mode='same')
        return np.clip(result / np.max(np.abs(result)), -1.0, 1.0)
    
    def apply_deep_effect(self, audio):
        """Make voice deeper (lower pitch)"""
        return self.apply_pitch_shift(audio, -5)
    
    def apply_high_effect(self, audio):
        """Make voice higher (higher pitch)"""
        return self.apply_pitch_shift(audio, 5)
    
    def apply_volume(self, audio, gain_db):
        """Apply volume gain"""
        if gain_db == 0:
            return audio
        gain_linear = 10 ** (gain_db / 20.0)
        result = audio * gain_linear
        return np.clip(result, -1.0, 1.0)
    
    def _bandpass_filter(self, audio, low_freq, high_freq, order=5):
        """Apply bandpass filter"""
        nyquist = self.sample_rate / 2
        low = low_freq / nyquist
        high = high_freq / nyquist
        low = max(0.001, min(low, 0.999))
        high = max(low + 0.001, min(high, 0.999))
        b, a = signal.butter(order, [low, high], btype='band')
        return signal.filtfilt(b, a, audio)
    
    def _time_stretch(self, audio, rate):
        """Simple time stretching"""
        if rate == 1.0:
            return audio
        original_length = len(audio)
        new_length = int(original_length / rate)
        indices = np.linspace(0, original_length - 1, new_length)
        stretched = np.interp(indices, np.arange(original_length), audio)
        return stretched
