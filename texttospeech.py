import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gtts import gTTS
import os

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Application")
        
        # Input
        self.text_input = tk.Text(self.root, height=10, width=50)  
        self.text_input.pack(pady=10)
        
        # Language Selection
        self.language_label = tk.Label(self.root, text="Select Language:")
        self.language_label.pack()
        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(self.root, textvariable=self.language_var)
        self.language_dropdown['values'] = ['English (en)', 'Spanish (es)', 'Hindi (hi)']
        self.language_dropdown.pack()
        
        # Gender Selection
        self.gender_label = tk.Label(self.root, text="Select Gender:")
        self.gender_label.pack()
        self.gender_var = tk.StringVar()
        self.gender_dropdown = ttk.Combobox(self.root, textvariable=self.gender_var)
        self.gender_dropdown['values'] = ['Male', 'Female']
        self.gender_dropdown.pack()
        
        # Rate Adjustment
        self.rate_label = tk.Label(self.root, text="Rate:")
        self.rate_label.pack()
        self.rate_scale = tk.Scale(self.root, from_=50, to=200, orient=tk.HORIZONTAL)
        self.rate_scale.pack()
        
        # Pitch Adjustment
        self.pitch_label = tk.Label(self.root, text="Pitch:")
        self.pitch_label.pack()
        self.pitch_scale = tk.Scale(self.root, from_=0, to=20, orient=tk.HORIZONTAL)
        self.pitch_scale.pack()
        
        # Volume Adjustment
        self.volume_label = tk.Label(self.root, text="Volume:")
        self.volume_label.pack()
        self.volume_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL)
        self.volume_scale.pack()
        
        # Playback Controls
        self.play_button = tk.Button(self.root, text="Play", command=self.play)
        self.play_button.pack(side=tk.LEFT, padx=10)
        
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        self.replay_button = tk.Button(self.root, text="Replay", command=self.replay)
        self.replay_button.pack(side=tk.LEFT, padx=10)
        
        self.save_button = tk.Button(self.root, text="Save Audio", command=self.save_audio)
        self.save_button.pack(side=tk.LEFT, padx=10)
        
        self.close_button = tk.Button(self.root, text="Close", command=self.root.destroy)
        self.close_button.pack(side=tk.BOTTOM, anchor="center", pady=50)  
        
    def play(self):
        text = self.text_input.get("1.0", tk.END)
        language = self.language_var.get()
        gender = self.gender_var.get()
        
        language_code = {
            'English (en)': 'en',
            'Spanish (es)': 'es',
            'Hindi (hi)': 'hi'
        }
        
        voice_id = self.get_voice_id(language_code[language], gender)
        
        tts = gTTS(text, lang=language_code[language], tld='com', slow=False, lang_check=False)
        tts.save("output.mp3")
        os.system("output.mp3")
    
    def pause(self):
        os.system("TASKKILL /F /IM vlc.exe")
    
    def stop(self):
        os.system("TASKKILL /F /IM vlc.exe")
    
    def replay(self):
        self.play()
    
    def save_audio(self):
        text = self.text_input.get("1.0", tk.END)
        language = self.language_var.get()
        
        language_code = {
            'English (en)': 'en',
            'Spanish (es)': 'es',
            'Hindi (hi)': 'hi'
        }
        
        tts = gTTS(text, lang=language_code[language])
        filename = "speech_output.mp3"
        tts.save(filename)
        messagebox.showinfo("Save Audio", f"Audio saved as '{filename}'")
        
    def get_voice_id(self, language_code, gender):
        if language_code == 'en':  # English
            if gender == 'Male':
                return 'en-us'
            elif gender == 'Female':
                return 'en-uk'
        elif language_code == 'es':  # Spanish
            if gender == 'Male':
                return 'es-es'
            elif gender == 'Female':
                return 'es-us'
        elif language_code == 'hi':  # Hindi
            if gender == 'Male':
                return 'hi-in'
            elif gender == 'Female':
                return 'hi-in'
        return None  

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
















