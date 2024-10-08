﻿# Screen Streaming with Cursor Overlay

This Python project streams the computer's screen along with the mouse cursor to a connected client device over a network using sockets. It captures the screen using the `mss` library and overlays the mouse cursor in real-time. The images are compressed and sent via a socket to a client for display.

## Features

- **Real-time screen capture**: Uses `mss` for fast and efficient screen capturing.
- **Mouse cursor overlay**: The mouse cursor is captured and overlaid on the screenshot using `ctypes`.
- **Optimized JPEG compression**: The captured screen is compressed into JPEG format with adjustable quality to balance speed and image quality.
- **Custom framerate**: Adjusts the sleep time dynamically to maintain a specified framerate.
- **Automatic reconnection**: Attempts to reconnect for 2 minutes if the connection is lost.
  
## Requirements

To run this project, you need to install the following Python libraries:

```bash
pip install mss pillow
```
## How It Works

1. Screen Capture: The `mss` library captures the screen in real-time. You can adjust which monitor to capture by changing the monitor index.
2. Mouse Cursor Overlay: The mouse cursor position is retrieved using `ctypes` and then a custom cursor image (e.g., `cursor.png`) is overlaid on the screen capture.
3. Socket Connection: The screen and cursor data are sent over a socket to a client device. The program tries to connect to the client for up to 2 minutes before giving up.
4. Framerate Control: The program is designed to maintain a target framerate (default is 40 FPS) by dynamically adjusting the sleep time between frames.

## How to Use
1. Set up the client: Make sure the client device is ready to receive the screen stream over a socket on port `8888`.
2. Modify the IP address: Replace `'Device IP'` in the code with the IP address of the client device.
3. Run the script:

```bash
python screen_stream.py
```
The program will start capturing the screen, overlay the cursor, and send it to the client device.

**Cursor Image**

Ensure that you have a cursor.png file in the same directory as the script. This image will be used as the custom mouse cursor overlay.

## Customization

- Adjust the framerate: You can modify the `target_fps` variable to increase or decrease the frames per second (FPS).
- Change image quality: Adjust the `quality` parameter in the `img.save()` function to change the JPEG compression level.
- Resize the image: You can uncomment the `img.resize()` line to downscale the captured image for faster transmission if needed.

## Example Output
When the connection is established, you'll see:

```
Connection established
```

If the connection fails, it will retry for 2 minutes, displaying messages such as:

```
Connection failed: [error message]. Retrying...
```

## Work in Progress

1. Android app where you can view your casting.
2. rewriting the code in `C` or `C++` for better performance.
