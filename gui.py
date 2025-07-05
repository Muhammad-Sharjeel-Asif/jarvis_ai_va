import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import main
import threading
import asyncio

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis Virual Assistant")
        self.root.geometry("600x700")
        self.root.configure(bg="#f5f6fa")
        self.root.minsize(500, 600)  # Minimum size for responsiveness
        
        # Load environment variables
        load_dotenv()
        
        # Initialize speech recognizer and text-to-speech
        try:
            self.recognizer = sr.Recognizer()
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 170)
            self.engine.setProperty('volume', 0.9)
        except Exception as e:
            self.show_error(f"Initialization failed: {str(e)}")
            return
        
        # Listening state and thread control
        self.listening = False
        self.listen_thread = None
        
        # Create GUI elements
        self.create_gui()
        
        # Speak initialization message
        try:
            self.speak("Initializing Jarvis... How can I help you")
        except Exception as e:
            self.show_error(f"Speech initialization failed: {str(e)}")
            
    def create_gui(self):
        try:
            # Main frame
            main_frame = tk.Frame(self.root, bg="#f5f6fa")
            main_frame.pack(padx=20, pady=20, fill="both", expand=True)
            
            # Title
            title_label = tk.Label(
                main_frame, text="Jarvis Voice Assistant", font=("Helvetica", 24, "bold"),
                bg="#f5f6fa", fg="#2ecc71", pady=10
            )
            title_label.pack()
            
            # Control frame
            control_frame = tk.Frame(main_frame, bg="#f5f6fa")
            control_frame.pack(pady=10, fill="x")
            
            # Start Listening button
            self.start_button = tk.Button(
                control_frame, text="Start Listening", font=("Helvetica", 16, "bold"),
                command=self.start_listening, bg="#2ecc71", fg="white",
                activebackground="#27ae60", width=20, height=2, bd=0,
                relief="flat"
            )
            self.start_button.pack(side="left", padx=5)
            
            # Stop Listening button
            self.stop_button = tk.Button(
                control_frame, text=" Stop Listening", font=("Helvetica", 16, "bold"),
                command=self.stop_listening, bg="#e74c3c", fg="white",
                activebackground="#c0392b", width=20, height=2, bd=0,
                relief="flat", state="disabled"
            )
            self.stop_button.pack(side="left", padx=5)
            
            # Command display
            self.command_var = tk.StringVar()
            command_frame = tk.Frame(main_frame, bg="#f5f6fa")
            command_frame.pack(pady=10, fill="x")
            command_label = tk.Label(
                command_frame, textvariable=self.command_var, font=("Helvetica", 14),
                bg="#ffffff", fg="#34495e", wraplength=560, padx=10, pady=10,
                relief="groove", borderwidth=2
            )
            command_label.pack(fill="x")
            
            # Suggestions frame
            suggestions_frame = tk.LabelFrame(
                main_frame, text="Command Suggestions", font=("Helvetica", 14, "bold"),
                bg="#f5f6fa", fg="#2ecc71", padx=10, pady=5
            )
            suggestions_frame.pack(pady=10, fill="x")
            
            suggestions = [
                "Open Google", "Open YouTube", "Open Facebook", "Open LinkedIn", "Open Instagram", "Open Twitter", "Open Chatgpt", "News",
                "What is artificial intelligence?", "Exit"
            ]
            
            for suggestion in suggestions:
                suggestion_label = tk.Label(
                    suggestions_frame, text=suggestion, font=("Helvetica", 12),
                    bg="#ffffff", fg="#34495e", cursor="hand2", padx=10, pady=5
                )
                suggestion_label.pack(anchor="w", fill="x")
                suggestion_label.bind("<Button-1>", lambda e, s=suggestion: self.process_command(s))
            
            # Output log
            self.output_text = scrolledtext.ScrolledText(
                main_frame, height=15, font=("Helvetica", 12),
                bg="#ffffff", fg="#34495e", wrap=tk.WORD
            )
            self.output_text.pack(pady=10, fill="both", expand=True)
            self.output_text.config(state="disabled")
            
            # Status bar
            self.status_var = tk.StringVar(value="Ready")
            status_label = tk.Label(
                main_frame, textvariable=self.status_var, font=("Helvetica", 10),
                bg="#ecf0f1", fg="#2ecc71", anchor="w", padx=10, pady=5
            )
            status_label.pack(side="bottom", fill="x")
            
        except Exception as e:
            self.show_error(f"GUI creation failed: {str(e)}")
            
    def update_command(self, text):
        self.command_var.set(text)
        self.root.update()
        
    def append_output(self, text):
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state="disabled")
        self.root.update()
        
    def show_error(self, text):
        self.append_output(f"Error: {text}")
        
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        
    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_var.set("Listening...")
            self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
            self.listen_thread.start()
            
    def stop_listening(self):
        if self.listening:
            self.listening = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_var.set("Stopped")
            if self.listen_thread:
                self.listen_thread.join(timeout=1)
                
    def listen_loop(self):
        try:
            while self.listening:
                with sr.Microphone() as source:
                    self.update_command("Listening...")
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                    
                    try:
                        command = self.recognizer.recognize_google(audio)
                        self.update_command(f"Recognized: {command}")
                        
                        if "jarvis" in command.lower():
                            self.speak("Ya")
                            self.update_command("Waiting for command...")
                            with sr.Microphone() as source:
                                self.recognizer.adjust_for_ambient_noise(source)
                                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                                command = self.recognizer.recognize_google(audio)
                                self.update_command(f"Command: {command}")
                                loop = asyncio.new_event_loop()
                                asyncio.set_event_loop(loop)
                                try:
                                    self.process_command(command)
                                finally:
                                    loop.close()
                        elif "exit" in command.lower():
                            self.speak("Goodbye")
                            self.append_output("Jarvis: Goodbye")
                            self.stop_listening()
                            self.root.quit()
                        else:
                            self.update_command("Say 'Jarvis' to activate")
                            
                    except sr.UnknownValueError:
                        self.update_command("Could not understand audio")
                        self.speak("Sorry, I couldn't understand that.")
                    except sr.RequestError as e:
                        self.update_command(f"Error: {str(e)}")
                        self.speak("Sorry, there was an error with the speech recognition service.")
                        
        except Exception as e:
            self.update_command(f"Error: {str(e)}")
            self.speak("An error occurred while listening.")
            
    def process_command(self, command):
        def custom_speak(text):
            self.speak(text)
            self.append_output(f"Jarvis: {text}")
            
        original_speak = main.speak
        main.speak = custom_speak
        
        try:
            main.processCommand(command)
            if command.lower() == "exit":
                self.speak("Goodbye")
                self.append_output("Jarvis: Goodbye")
                self.root.quit()
        except Exception as e:
            self.show_error(f"Command processing failed: {str(e)}")
        finally:
            main.speak = original_speak
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisGUI(root)
    app.run()