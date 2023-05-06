import tkinter as tk
from tkinter import ttk
import numpy as np
import pyaudio

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Frequency Slider")
        
        self.sliders = []
        self.frequency_entries = []

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_playing = False

        self.add_slider_button = tk.Button(self.root, text="Add Slider", command=self.add_slider)
        self.add_slider_button.pack(side=tk.TOP)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_audio)
        self.play_button.pack(side=tk.TOP)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_audio)
        self.stop_button.pack(side=tk.TOP)

        self.slider_container = ttk.Frame(self.root)
        self.slider_container.pack(side=tk.TOP)

    def slider_value_to_freq(self, value):
        if value < 500:
            return value
        elif value < 1000:
            return 500 + (value - 500) * 2
        else:
            return 1500 + (value - 1000) * 18.5

    def freq_to_slider_value(self, freq):
        if freq < 500:
            return freq
        elif freq < 1500:
            return 500 + (freq - 500) / 2
        else:
            return 1000 + (freq - 1500) / 18.5

    def add_slider(self):
        slider_frame = ttk.Frame(self.slider_container)
        slider_frame.pack(side=tk.LEFT, padx=10)

        max_value = 20000
        slider = tk.Scale(slider_frame, from_=self.freq_to_slider_value(max_value), to=self.freq_to_slider_value(1), orient=tk.VERTICAL, length=400, command=self.update_frequency, resolution=0.01, tickinterval=0, sliderlength=30, showvalue=0)
        slider.pack(side=tk.TOP)

        frequency_entry = tk.Entry(slider_frame, width=8)
        frequency_entry.insert(tk.END, "0")
        frequency_entry.bind("<Return>", self.set_frequency)
        frequency_entry.pack(side=tk.TOP)

        self.sliders.append(slider)
        self.frequency_entries.append(frequency_entry)

    def update_frequency(self, value):
        for i, slider in enumerate(self.sliders):
            freq = int(self.slider_value_to_freq(float(slider.get())))
            self.frequency_entries[i].delete(0, tk.END)
            self.frequency_entries[i].insert(tk.END, str(freq))

    def set_frequency(self, event):
        for i, entry in enumerate(self.frequency_entries):
            freq = int(entry.get())
            self.sliders[i].set(self.freq_to_slider_value(freq))

    def play_audio(self):
        if self.is_playing:
            return

        self.is_playing = True
        self.stream = self.audio.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True, stream_callback=self.audio_callback)

    def stop_audio(self):
        if not self.is_playing:
            return

        self.is_playing = False
        self.stream.stop_stream()
        self.stream.close()

    def audio_callback(self, in_data, frame_count, time_info, status):
        frequencies = [float(entry.get()) for entry in self.frequency_entries]
        t
