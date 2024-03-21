# -*- coding: utf-8 -*-
"""
# Vishal
"""
from pydub import AudioSegment
from pydub.generators import Sine
import numpy as np

# Set the parameters for the tone
duration_in_seconds = 5  # Duration of the tone in seconds
frequency = 440  # Frequency of the tone in Hz
volume = 0.3  # Volume level of the tone (0 to 1)

# Generate the sine wave tone
tone = Sine(frequency).to_audio_segment(duration=duration_in_seconds * 1000)

# Convert the audio data to a numpy array and scale it
audio_data = np.array(tone.get_array_of_samples())
audio_data = (audio_data * volume).astype(np.int16)

# Create an AudioSegment from the scaled audio data
tone = AudioSegment(audio_data.tobytes(), frame_rate=tone.frame_rate, sample_width=2, channels=1)

# Export the tone as a WAV file
tone.export("sound.wav", format="wav")




import tkinter as tk
import datetime
import threading
from pydub import AudioSegment
from pydub.playback import play

class AlarmClock:
    def __init__(self, master):
        self.master = master
        master.title("Alarm Clock")
        master.geometry("400x200")

        self.alarm_time = None
        self.alarm_triggered = False

        self.label = tk.Label(master, text="Alarm Clock", font=("Helvetica", 20, "bold"), fg="red")
        self.label.pack(pady=10)

        self.time_label = tk.Label(master, font=("Helvetica", 15, "bold"))
        self.time_label.pack()

        self.set_time_frame = tk.Frame(master)
        self.set_time_frame.pack()

        self.hour_label = tk.Label(self.set_time_frame, text="Hour:", font=("Helvetica", 12))
        self.hour_label.grid(row=0, column=0)
        self.hour_spinbox = tk.Spinbox(self.set_time_frame, from_=0, to=23, width=2)
        self.hour_spinbox.grid(row=0, column=1)

        self.minute_label = tk.Label(self.set_time_frame, text="Minute:", font=("Helvetica", 12))
        self.minute_label.grid(row=0, column=2)
        self.minute_spinbox = tk.Spinbox(self.set_time_frame, from_=0, to=59, width=2)
        self.minute_spinbox.grid(row=0, column=3)

        self.second_label = tk.Label(self.set_time_frame, text="Second:", font=("Helvetica", 12))
        self.second_label.grid(row=0, column=4)
        self.second_spinbox = tk.Spinbox(self.set_time_frame, from_=0, to=59, width=2)
        self.second_spinbox.grid(row=0, column=5)

        self.set_button = tk.Button(master, text="Set Alarm", font=("Helvetica", 15), command=self.set_alarm)
        self.set_button.pack(pady=20)

        self.update_time()

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.master.after(1000, self.update_time)

    def set_alarm(self):
        self.alarm_time = f"{self.hour_spinbox.get()}:{self.minute_spinbox.get()}:{self.second_spinbox.get()}"
        self.alarm_triggered = False
        threading.Thread(target=self.check_alarm).start()

    def check_alarm(self):
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            if current_time == self.alarm_time and not self.alarm_triggered:
                self.alarm_message()
                self.alarm_triggered = True
            elif current_time != self.alarm_time:
                self.alarm_triggered = False
            if not self.alarm_time:
                break

    def alarm_message(self):
        print("Time to Wake up")
        # Load and play the sound file using pydub
        alarm_sound = AudioSegment.from_wav("sound.wav")
        play(alarm_sound)

root = tk.Tk()
app = AlarmClock(root)
root.mainloop()
