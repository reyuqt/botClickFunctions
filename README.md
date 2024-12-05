# WebDriver Click Functions

## Overview
The WebDriver Click Functions project provides a set of utilities for performing advanced mouse and element interactions using both Selenium and PyAutoGUI. It is designed to simulate human-like interactions with web elements and screen coordinates, enhancing automation scripts with more natural movements.

## Features
- **Bezier Curve Mouse Movements**: Generate and use cubic Bezier curves for smooth, human-like mouse movements.
- **Image Recognition and Clicking**: Locate images on the screen and click within them using configurable confidence levels and retries.
- **Selenium Element Interactions**: Retrieve, save, and click on web elements using Selenium with enhanced accuracy.
- **Utility Functions**: Includes various helper functions for logging and element handling.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/reyuqt/webdriverClickFunctions.git
   ```
2. Navigate to the project directory:
   ```bash
   cd webdriverClickFunctions
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- **Bezier Curve Mouse Movements**: Use the `click_with_bezier` function to move the mouse to a target location and click.
- **Image Recognition**: Use `locate_image` and `click_image` functions to interact with screen elements based on image recognition.
- **Selenium Interactions**: Use `get_element`, `save_element`, and `click_this_element` to interact with web elements.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, please contact Lauren at reyuqt01@gmail.com.
