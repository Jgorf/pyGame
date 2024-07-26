# pyWordle - A Wordle Clone using Pygame

## Project Overview

&nbsp;&nbsp; `pyWordle` is an engaging and interactive clone of the popular word-guessing game Wordle, implemented using Python's Pygame library. The game challenges players to guess a hidden word within a limited number of attempts, providing visual feedback through color-coded tiles. This project showcases not only a fun and challenging game but also serves as a demonstration of Python and Pygame's capabilities in creating interactive graphical applications.

## What the Application Does
&nbsp;&nbsp; In `pyWordle`, players must guess a hidden word by inputting letters on their keyboard. The game provides immediate feedback by coloring the tiles: 
- **Green** for correct letters in the correct position,
- **Yellow** for correct letters in the wrong position,
- **Gray** for letters not in the word at all.
    
&nbsp;&nbsp; Players can select the length of the hidden word, making the game customizable and challenging for different skill levels. The goal is to guess the word within six attempts, with an option to replay and improve your guessing skills.

## Skills acquired
- Learned to use pygame to create graphical applications
- Implemented an interactive user interface and visual feedback system
- Developed logic for game mechanics, including word guessing and feedback through colors and alerts

## Achievements
- Successfully created a functional Wordle clone with interactive gameplay
- Implemented a customizable game experience by allowing players to select the length of the hidden word
- Generated tiles according to the user-selected word length, adapting the game setup to different word lengths.


## Challenges Faced 
- Managing the game state and transitions, such as handling alerts and switching between game states
- Creating a responsive and user-friendly interface, including the virtual keyboard, settings menu and the tile generation

## Potential Future Improvements
- Make the keyboard that indicates which letters are in the word interactive, so users can input their guess by using their mouse to interact with the virtual keyboard
- Add delete and enter key to the keyboard so that users are able to submit their guess if they chose to use the virtual keyboard
- Improve alert system
- Use API to get words of various lengths rather than getting a random word of the correct length from the list of words compiled

## How to Install/Run Project

There are two ways to get up and running with `pyWordle`:

### Option 1: Download the Pre-built Executable

The simplest way to start playing `pyWordle` is to download the pre-built executable file. This option does not require Python or any additional libraries. 

1. **Download the .exe File**: 
   - Visit the [GitHub repository for pyWordle](https://github.com/Jgorf/pyWordle) and press the code button.
   - Download as a `.zip` file, which contains the `pyWordle.exe`.

2. **Extract and Run the Executable**:
   - Extract the contents of the `.zip` file to a directory on your computer.
   - Double-click the `pyWordle.exe` file to run the game.

### Option 2: Run the Code on Local Machine

If you prefer to run the code yourself, follow these steps. This option requires Python and the Pygame library.

1. **Install Python**:
   - Download and install Python from the [official Python website](https://www.python.org/downloads/).

2. **Install Pygame**:
   - Open your command line interface (CLI) and install Pygame using pip:
     ```bash
     pip install pygame
     ```

3. **Clone the Repository**:
   - Clone the repository to your local machine from the [GitHub repository](https://github.com/Jgorf/pyWordle).
   - Or use your command line interface and enter:
    ```bash
     git clone https://github.com/Jgorf/pyWordle.git
     ``` 

4. **Run the Game**:
   - Navigate to the directory containing the `pyWordle` source code in your CLI:
     ```bash
     cd pyWordle
     ```
   - Run the game by executing:
     ```bash
     python pyWordle.py
     ```
