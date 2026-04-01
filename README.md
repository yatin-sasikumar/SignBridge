# SignBridge — Two-Way Communication System

SignBridge is a real-time assistive system that bridges communication between speech and sign language users using Computer Vision, Machine Learning, and Natural Language Processing.

---

## Features

*  **Speech to Text**

  * Real-time speech recognition
  * Silence detection based recording
  * Live UI feedback

* **Sign Language to Text**

  * Hand tracking using MediaPipe
  * Gesture classification using ML model
  * Buffered prediction for stability

* **NLP Enhancement**

  * Converts raw gesture words into natural sentences
  * API-based + fallback system

* **Interactive UI**

  * Built with CustomTkinter
  * Real-time status updates
  * Clean and responsive design

---

##  Tech Stack

* Python
* OpenCV
* MediaPipe
* scikit-learn
* CustomTkinter
* Cohere API (with fallback)
* SpeechRecognition
* pyttsx3

---

##  System Flow

###  Speech Mode

User Speech → Audio Processing → Speech-to-Text → UI Output

###  Gesture Mode

Camera Input → Hand Landmarks → ML Model → Word Sequence
→ NLP Processing → Final Sentence → UI Output

---

##  Key Concepts Used

* Computer Vision (Hand Tracking)
* Machine Learning (Gesture Classification)
* Natural Language Processing (Sentence Correction)
* Multithreading (Non-blocking UI)
* API Integration with fallback handling

---

##  How to Run

```bash
pip install -r requirements.txt
python main.py
```

---

##  Environment Setup

Create a `.env` file:

```
COHERE_API_KEY=your_api_key_here
```

---

##  Notes

* Ensure proper lighting for gesture detection
* Press `Q` to stop gesture input
* API fallback ensures system works even without internet

---

## Future Improvements

* Mobile App Deployment (Android)
* Continuous sign sentence recognition
* Multi-language support
* Voice output for gesture mode
* Improved ML model accuracy

---

## Acknowledgements

* MediaPipe by Google
* Cohere API
* OpenCV community
