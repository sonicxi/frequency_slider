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

    def add_slider(self):
        slider_frame = ttk.Frame(self.slider_container)
        slider_frame.pack(side=tk.LEFT, padx=10)

        max_freq = 20000
        slider = tk.Scale(slider_frame, from_=max_freq, to=0, orient=tk.VERTICAL, length=200, command=self.update_frequency)
        slider.pack(side=tk.TOP)

        frequency_entry = tk.Entry(slider_frame, width=8)
        frequency_entry.insert(tk.END, "0")
        frequency_entry.bind("<Return>", self.set_frequency)
        frequency_entry.pack(side=tk.TOP)

        self.sliders.append(slider)
        self.frequency_entries.append(frequency_entry)

    def update_frequency(self, value):
        for i, slider in enumerate(self.sliders):
            freq = int(slider.get())
            self.frequency_entries[i].delete(0, tk.END)
            self.frequency_entries[i].insert(tk.END, str(freq))

    def set_frequency(self, event):
        for i, entry in enumerate(self.frequency_entries):
            freq = int(entry.get())
            self.sliders[i].set(freq)

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
        t = np.linspace(0, 1, 44100, False)
        signal = np.zeros_like(t)

        for freq in frequencies:
            if freq > 0:
                signal += np.sin(freq * 2 * np.pi * t)

        signal /= len(frequencies)
        signal = signal.astype(np.float32)
        return (signal.tobytes(), pyaudio.paContinue)

    def on_closing(self):
        self.stop_audio()
        self.audio.terminate()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
