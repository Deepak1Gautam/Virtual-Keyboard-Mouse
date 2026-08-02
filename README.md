<p align="center">
  <img src="assets/banner.gif" alt="Virtual Keyboard & Mouse" width="100%">
</p>

<p align="center">

  <a href="https://github.com/Deepak1Gautam/Virtual-Keyboard-Mouse">
    <img src="https://img.shields.io/badge/💻%20GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>

  <a href="YOUR_LINKEDIN_POST_LINK">
    <img src="https://img.shields.io/badge/💼%20LinkedIn-View%20Post-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>

</p>

<h1 align="center">🖐️ Virtual Keyboard & Mouse</h1>

<p align="center">
  <b>Control your computer using hand gestures — no physical keyboard or mouse required.</b>
</p>

<p align="center">
  A real-time computer vision project built with Python, OpenCV, MediaPipe and PyAutoGUI.
</p>

---

## 📌 About The Project

**Virtual Keyboard & Mouse** is a computer-vision-based human-computer interaction project that allows users to control their computer using hand gestures.

The system uses **MediaPipe hand landmark detection** to track the user's hand and **OpenCV** to process the webcam feed in real time.

The project provides two main modes:

- 🖱️ **Virtual Mouse**
- ⌨️ **Virtual Keyboard**

Users can switch between these modes using simple hand gestures.

---

## ✨ Features

### 🖱️ Virtual Mouse

Control your computer mouse using simple hand gestures.

- ☝️ **Index Finger** → Move cursor
- 🤏 **Index + Thumb Pinch** → Left click
- ✊ **Hold Pinch** → Drag & drop
- 🤏 **Thumb + Middle Finger Pinch** → Right click
- ↕️ **Index + Middle Fingers Apart** → Scroll
- ⚡ Smooth and responsive cursor movement

---

### ⌨️ Virtual Keyboard

Type on your computer without touching a physical keyboard.

- ☝️ **Index Finger** → Hover over a key
- 🤏 **Thumb + Index Pinch** → Press key
- 🔠 **CAPS** → Toggle uppercase
- ⇧ **SHIFT** → Temporary uppercase
- ␣ **SPACE** → Insert space
- ⌫ **BACKSPACE** → Delete character
- ↵ **ENTER** → Press Enter
- 🧹 **CLEAR** → Clear typed text

---

### 🎯 Smart Interaction

- 🔄 Mouse ↔ Keyboard mode switching
- 🖐️ Real-time hand landmark tracking
- 📊 Real-time FPS counter
- 🟢 Live gesture status
- 📋 Current action display
- 🎨 Transparent UI panels
- ⏱️ Gesture hold detection
- ⚡ Click and keypress cooldown system
- 🎯 Cursor smoothing

## 🧠 Gesture Controls

| Gesture | Action | Mode |
|---|---|---|
| ☝️ Index Finger | Move cursor | 🖱️ Mouse |
| 🤏 Index + Thumb Pinch | Left Click | 🖱️ Mouse |
| ✊ Hold Pinch | Drag & Drop | 🖱️ Mouse |
| 🤏 Thumb + Middle Pinch | Right Click | 🖱️ Mouse |
| ↕️ Index + Middle Apart | Scroll | 🖱️ Mouse |
| ✌️ Index + Middle Hold | Switch to Keyboard | 🔄 Switch |
| ☝️ Index Finger Hover | Select Key | ⌨️ Keyboard |
| 🤏 Thumb + Index Pinch | Type Key | ⌨️ Keyboard |
| 🔠 CAPS | Toggle Uppercase | ⌨️ Keyboard |
| ⇧ SHIFT | Temporary Uppercase | ⌨️ Keyboard |
| ␣ SPACE | Insert Space | ⌨️ Keyboard |
| ⌫ BACKSPACE | Delete Character | ⌨️ Keyboard |
| ↵ ENTER | Press Enter | ⌨️ Keyboard |
| 🧹 CLEAR | Clear Text | ⌨️ Keyboard |
| ☝️ Index Finger Hold | Switch to Mouse | 🔄 Switch |

> 💡 **Tip:** Hold the required gesture for a short moment to prevent accidental actions.

---

## ⚙️ How To Run

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Deepak1Gautam/Virtual-Keyboard-Mouse.git

```markdown
Move into the project folder:
cd Virtual-Keyboard-Mouse

### 2️⃣ Create a Virtual Environment

Windows:

```bash
python -m venv venv

Activate the virtual environment:

```powershell
venv\Scripts\activate
