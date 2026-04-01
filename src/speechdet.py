import speech_recognition as sr
import numpy as np
import struct
import time

r = sr.Recognizer()

def get_audio_energy(audio):
    audio_data = audio.get_raw_data()
    audio_samples = np.array(struct.unpack("<" + "h" * (len(audio_data) // 2), audio_data))
    rms = np.sqrt(np.mean(np.square(audio_samples)))
    return rms


def record_and_transcribe(callback=None):

    silence_threshold = 200
    silence_duration = 1

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)

        if callback:
            callback("Speak now...")
        else:
            print("Speak now...")

        speech_audio = []
        speaking = False
        last_spoke_time = time.time()

        while True:
            try:
                audio = r.listen(source, phrase_time_limit=3)
            except:
                continue

            energy = get_audio_energy(audio)

            if energy > silence_threshold:
                if not speaking:
                    speaking = True
                    speech_audio = [audio]

                    if callback:
                        callback("Recording...")
                    else:
                        print("Recording...")
                else:
                    speech_audio.append(audio)

                last_spoke_time = time.time()

            else:
                if speaking and (time.time() - last_spoke_time > silence_duration):

                    if callback:
                        callback("Processing...")
                    else:
                        print("Processing...")

                    raw_audio = b"".join(chunk.get_raw_data() for chunk in speech_audio)
                    full_audio = sr.AudioData(raw_audio, source.SAMPLE_RATE, source.SAMPLE_WIDTH)

                    try:
                        text = r.recognize_google(full_audio)
                        return text
                    except:
                        return ""