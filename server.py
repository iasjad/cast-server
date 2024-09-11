import socket
import io
import threading
import mss
import ctypes
from PIL import Image
import time

# Function to get the mouse cursor position using ctypes (on Windows)
def get_cursor_position():
    cursor = ctypes.windll.user32.GetCursorPos
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt = POINT()
    cursor(ctypes.byref(pt))
    return pt.x, pt.y

def send_screenshot():
    # Retry connection for 2 minutes (120 seconds)
    timeout_duration = 120  # 2 minutes
    start_time = time.time()
    client_socket = None

    # Keep trying to connect within the timeout duration
    while time.time() - start_time < timeout_duration:
        try:
            # Attempt to connect to the device via socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('Device IP', 8888))  # Replace with your Device's IP
            
            # Disable Nagle's algorithm for lower latency
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            print("Connection established")
            break  # Connection successful, exit the loop

        except socket.error as e:
            print(f"Connection failed: {e}. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying

    # If after 2 minutes we could not establish a connection
    if client_socket is None:
        print("No clients found. Exiting...")
        return

    def send_image():
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Capture the first monitor

            try:
                while True:
                    start_frame_time = time.time()  # Start frame timing

                    # Capture the screen using mss
                    screenshot = sct.grab(monitor)

                    # Convert the screenshot to a Pillow image
                    img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)

                    # Get the cursor position using ctypes
                    cursor_x, cursor_y = get_cursor_position()

                    # Load and overlay the cursor image on the screenshot
                    cursor_img = Image.open('cursor.png')  # Load a custom cursor image
                    if cursor_img.mode != 'RGBA':
                        cursor_img = cursor_img.convert('RGBA')  # Ensure the cursor image is in RGBA format

                    # Overlay the cursor image at the captured cursor position
                    img.paste(cursor_img, (cursor_x, cursor_y), cursor_img)

                    # Resize the image for faster transmission (optional, adjust to your needs)
                    # img = img.resize((screenshot.width // 2, screenshot.height // 2))

                    # Convert the final image with the cursor back to bytes
                    byte_io = io.BytesIO()
                    img.save(byte_io, format='JPEG', quality=70)  # Lower the quality for higher speed
                    image_data = byte_io.getvalue()

                    # Send image size before sending the image itself
                    image_size = len(image_data).to_bytes(4, 'big')  # Image size in 4 bytes (big-endian)
                    client_socket.sendall(image_size + image_data)

                    # Calculate time taken for the frame and adjust the sleep time to maintain a higher framerate
                    frame_time = time.time() - start_frame_time
                    target_fps = 40  # Target FPS (frames per second)
                    time_per_frame = 1 / target_fps

                    # Sleep only if frame processing was faster than the target frame time
                    if frame_time < time_per_frame:
                        time.sleep(time_per_frame - frame_time)

            except Exception as e:
                print(f"Error: {e}")
            finally:
                client_socket.close()

    # Run the sending function in a separate thread
    send_thread = threading.Thread(target=send_image)
    send_thread.start()

try:
    send_screenshot()
except KeyboardInterrupt:
    print("Stopped by user")
