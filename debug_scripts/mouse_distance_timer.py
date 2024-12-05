""" I used this during development to find ranges that felt human like """
from pynput import mouse
import time
import math

# Variables to store start and end positions and times
start_position = None
start_time = None
end_position = None
end_time = None


def calculate_distance(pos1, pos2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)


def on_click(x, y, button, pressed):
    """Handle mouse click events."""
    global start_position, start_time, end_position, end_time

    if pressed:
        # First click (start)
        if start_position is None:
            start_position = (x, y)
            start_time = time.time()
            print(f"Timer started at position {start_position}")
        # Second click (end)
        elif end_position is None:
            end_position = (x, y)
            end_time = time.time()
            print(f"Timer stopped at position {end_position}")

            # Calculate distance and time
            distance = calculate_distance(start_position, end_position)
            elapsed_time = end_time - start_time
            print(f"Mouse traveled a distance of {distance:.2f} pixels in {elapsed_time:.2f} seconds.")

            # Stop the listener
            return False


def main():
    print("Click anywhere to start the timer...")
    # Start listening for mouse events
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()  # Wait for the listener to stop


if __name__ == "__main__":
    main()
