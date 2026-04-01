import threading
import customtkinter as ctk
import tkinter as tk
import speechdet as speech
import signdet as sign
import nlp


class SignBridgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SignBridge")
        self.geometry("380x570")

        self.loading_frame = LoadingFrame(self)
        self.mode_frame = ModeFrame(self)

        self.show_frame("loading")

    def show_frame(self, name):
        for frame in (self.loading_frame, self.mode_frame):
            frame.pack_forget()

        if name == "loading":
            self.loading_frame.pack(fill="both", expand=True)
        elif name == "mode":
            self.mode_frame.pack(fill="both", expand=True)


class LoadingFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        ctk.CTkLabel(self, text="SignBridge", font=("Arial", 40, "bold"), text_color="#36719f").pack(pady=80)
        ctk.CTkLabel(self, text="Launching...", font=("Arial", 18)).pack(pady=10)

        bar = ctk.CTkProgressBar(self, mode="indeterminate")
        bar.pack(pady=20)
        bar.start()

        self.after(2500, lambda: self.parent.show_frame("mode"))


class ModeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Choose Mode", font=("Arial", 28, "bold")).pack(pady=40)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Speak Mode", command=self.speak_mode)\
            .grid(row=0, column=0, padx=20)

        ctk.CTkButton(button_frame, text="Gesture Mode", command=self.gesture_mode)\
            .grid(row=0, column=1, padx=20)

        # 🔥 SINGLE label (don’t recreate)
        self.output_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 18),
            wraplength=320,
            justify="left"
        )
        self.output_label.pack(pady=30)

    # ---------------- SPEECH ---------------- #
    def speak_mode(self):
        self.update_ui("Speak Now...")
        threading.Thread(target=self.run_speech, daemon=True).start()

    def run_speech(self):
        text = speech.record_and_transcribe(self.update_ui)

        if text.strip() == "":
            self.update_ui("No speech detected")
        else:
            self.update_ui(text)

    # ---------------- GESTURE ---------------- #
    def gesture_mode(self):
        self.update_ui("Opening camera...")
        threading.Thread(target=self.run_gesture, daemon=True).start()

    def run_gesture(self):
        # Step 1: Detect gestures
        self.update_ui("Detecting gestures... (Press Q to stop)")

        words = sign.run_sign_detection(self.update_ui)

        # Step 2: NLP processing
        self.update_ui("Processing sentence...")

        final_text = nlp.refine_text(words)

        # Step 3: Display final output
        if final_text.strip() == "":
            self.update_ui("No gesture detected")
        else:
            self.update_ui(final_text)

    # ---------------- UI SAFE UPDATE ---------------- #
    def update_ui(self, message):
        self.after(0, lambda: self.output_label.configure(text=message))


if __name__ == "__main__":
    app = SignBridgeApp()
    app.mainloop()