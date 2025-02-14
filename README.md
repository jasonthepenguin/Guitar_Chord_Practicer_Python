# Chord Practice App

A simple desktop application built with Python and Tkinter that helps musicians practice chord recognition through a customizable slideshow of chord diagrams.

## Features

- Displays chord diagrams in a randomized slideshow format
- Shows upcoming chord name to help with preparation
- Adjustable timing between chord changes
- Simple start/stop controls
- Window stays on top of other applications for easy viewing while practicing
- Centered window position on screen

## Prerequisites

- Python 3.x
- PIL (Python Imaging Library)
- Tkinter (usually comes with Python)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/chord-practice-app.git
cd chord-practice-app
```

2. Install required dependencies:
```bash
pip install Pillow
```

## Setup

1. Create a `Chords` folder in the same directory as `play.py`:
```bash
mkdir Chords
```

2. Add your chord diagram images to the `Chords` folder. Supported formats:
   - PNG
   - JPG/JPEG
   - GIF
   - BMP

The filename of each image will be displayed as the upcoming chord name, so name your files accordingly (e.g., `A_minor.png`, `C_major.png`, etc.).

## Usage

1. Run the application:
```bash
python play.py
```

2. The application window will appear with the following controls:
   - **Seconds per image**: Enter the number of seconds each chord should display
   - **Start**: Begin the slideshow
   - **Stop**: Pause the slideshow

3. The upcoming chord name will be displayed below the current chord diagram.

## Tips for Best Use

- Organize your chord images with clear, descriptive filenames
- Ensure all images are of similar dimensions for consistent display
- Adjust the timing to match your practice needs


## License

Lmfao

## Author

Jason Botterill