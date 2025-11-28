"""
Sistema de gestión de sonidos para el juego
Genera sonidos sintéticos usando pygame y wave (sin numpy)
"""

import pygame
import math
import os
import wave
import struct
import tempfile
from pathlib import Path

class GestorSonidos:
    def __init__(self):
        """Inicializa el gestor de sonidos"""
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        self.carpeta_sonidos = Path(__file__).parent.parent / "Sonidos"
        self.carpeta_sonidos.mkdir(exist_ok=True)
        
        self.volumen_efectos = 0.5
        self.volumen_musica = 0.3
        
        self.sonidos = {}
        self.musica_actual = None
        
        self._generar_sonidos()
    
    def _generar_sonidos(self):
        """Genera sonidos sintéticos usando pygame"""
        frecuencia = 22050
        
        self.sonidos['movimiento'] = self._generar_beep(400, 0.05, frecuencia)
        self.sonidos['trampa_colocada'] = self._generar_beep(300, 0.15, frecuencia)
        self.sonidos['trampa_activada'] = self._generar_beep(600, 0.2, frecuencia)
        self.sonidos['enemigo_atrapado'] = self._generar_beep(500, 0.3, frecuencia)
        self.sonidos['victoria'] = self._generar_melodia_victoria(frecuencia)
        self.sonidos['derrota'] = self._generar_beep(200, 0.5, frecuencia)
        self.sonidos['menu_click'] = self._generar_beep(600, 0.1, frecuencia)
        self.sonidos['energia_recuperada'] = self._generar_beep(800, 0.1, frecuencia)
        self.sonidos['enemigo_escapo'] = self._generar_beep(250, 0.3, frecuencia)
        self.sonidos['vida_perdida'] = self._generar_beep(150, 0.4, frecuencia)
        self.sonidos['correr'] = self._generar_beep(700, 0.2, frecuencia)
    
    def _generar_beep(self, frecuencia, duracion, sample_rate):
        """Genera un beep simple creando un archivo WAV temporal"""
        frames = int(duracion * sample_rate)
        max_sample = 2**(16 - 1) - 1
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        with wave.open(temp_file.name, 'w') as wav_file:
            wav_file.setnchannels(2)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(frames):
                t = float(i) / sample_rate
                wave_value = math.sin(2 * math.pi * frecuencia * t)
                if i < frames * 0.1:
                    envelope = 1.0
                else:
                    envelope = 1.0 - (i - frames * 0.1) / (frames * 0.9)
                
                sample = int(wave_value * max_sample * envelope * 0.3)
                sample = max(-32768, min(32767, sample))
                wav_file.writeframes(struct.pack('<hh', sample, sample))
        
        sound = pygame.mixer.Sound(temp_file.name)
        
        try:
            os.unlink(temp_file.name)
        except:
            pass
        
        return sound
    
    def _generar_melodia_victoria(self, sample_rate):
        """Genera una melodia de victoria (3 notas ascendentes)"""
        notas = [523, 659, 784]
        duracion_nota = 0.2
        frames_total = int((len(notas) * duracion_nota) * sample_rate)
        max_sample = 2**(16 - 1) - 1
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        with wave.open(temp_file.name, 'w') as wav_file:
            wav_file.setnchannels(2)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            frame_actual = 0
            for nota in notas:
                frames_nota = int(duracion_nota * sample_rate)
                for i in range(frames_nota):
                    if frame_actual < frames_total:
                        t = float(i) / sample_rate
                        wave_value = math.sin(2 * math.pi * nota * t)
                        if i < frames_nota * 0.1:
                            envelope = 1.0
                        else:
                            envelope = 1.0 - (i - frames_nota * 0.1) / (frames_nota * 0.9)
                        sample = int(wave_value * max_sample * envelope * 0.4)
                        sample = max(-32768, min(32767, sample))
                        wav_file.writeframes(struct.pack('<hh', sample, sample))
                        frame_actual += 1
        
        sound = pygame.mixer.Sound(temp_file.name)
        
        try:
            os.unlink(temp_file.name)
        except:
            pass
        
        return sound
    
    def reproducir_sonido(self, nombre, volumen=None):
        """Reproduce un efecto de sonido"""
        if nombre in self.sonidos:
            sonido = self.sonidos[nombre]
            if volumen is None:
                volumen = self.volumen_efectos
            sonido.set_volume(volumen)
            sonido.play()
    
    def reproducir_musica(self, loop=True):
        """Reproduce música de fondo (generada sintéticamente)"""
        if self.musica_actual is None:
            self.musica_actual = self._generar_musica_fondo()
        
        self.musica_actual.set_volume(self.volumen_musica)
        if loop:
            self.musica_actual.play(-1)
        else:
            self.musica_actual.play(1)
    
    def _generar_musica_fondo(self):
        """Genera música de fondo sintética"""
        sample_rate = 22050
        duracion = 4.0
        frames = int(duracion * sample_rate)
        max_sample = 2**(16 - 1) - 1
        
        notas = [261, 329, 392]
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        with wave.open(temp_file.name, 'w') as wav_file:
            wav_file.setnchannels(2)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(frames):
                t = float(i) / sample_rate
                wave_value = 0
                for nota in notas:
                    wave_value += math.sin(2 * math.pi * nota * t) * 0.15
                wave_value += math.sin(2 * math.pi * 110 * t) * 0.1
                
                envelope = 0.5 + 0.3 * math.sin(2 * math.pi * 0.5 * t)
                sample = int(wave_value * max_sample * envelope * 0.2)
                sample = max(-32768, min(32767, sample))
                wav_file.writeframes(struct.pack('<hh', sample, sample))
        
        sound = pygame.mixer.Sound(temp_file.name)
        
        try:
            os.unlink(temp_file.name)
        except:
            pass
        
        return sound
    
    def detener_musica(self):
        """Detiene la música de fondo"""
        if self.musica_actual:
            self.musica_actual.stop()
    
    def set_volumen_efectos(self, volumen):
        """Establece el volumen de los efectos (0.0 a 1.0)"""
        self.volumen_efectos = max(0.0, min(1.0, volumen))
    
    def set_volumen_musica(self, volumen):
        """Establece el volumen de la música (0.0 a 1.0)"""
        self.volumen_musica = max(0.0, min(1.0, volumen))
        if self.musica_actual:
            self.musica_actual.set_volume(self.volumen_musica)

