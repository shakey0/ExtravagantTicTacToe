# Extravagant Tic Tac Toe

## Introduction
My journey into the world of coding began with this intricate CLI Tic Tac Toe game, which I undertook just three weeks after I started learning Python. At that point, I hadn't ventured into concepts like OOP, nor was I familiar with the workings of GitHub, explaining the absence of a commit history. Instead of wading in shallow waters, I've always preferred diving deep when learning, and this project encapsulates that approach. While this might not reflect my most sophisticated work, it's a testament to my starting point, and I'm proud to showcase it on my GitHub portfolio.

## Features

- Players can choose their winning shapes/patterns (lines, squares, diamonds, L-shapes, T-shapes, lightning-shapes, horseshoes, etc.)
- Players can choose the game type:
    - Standard - <em>one line or shape wins.</em>
    - As Many As You Can - <em>when the board is full, the player with the most lines/shapes wins.</em>
    - Cards - <em>following the principles of 'As Many As You Can' but where players draw cards every 5 rounds. Cards do things such as let the user strike out their opponents Xs or Os, or let the player clear out a vertical or horizontal line of spaces on the board, or release a stink bomb on the board.</em>
- Players can choose blank types (2 examples below):
    - Electrical Storm - <em>Electricity that randomly moves around the board makes some spaces unavailable.</em>
    - Cattle Farm - <em>Cows make some spaces unavailable and bulls charge around the board knocking out players' Xs or Os.</em>
    - And more!
- Creative messages when the user makes a line or shape:
    - X hung a terrifyingly vertical line of 4!
    - O got the magic corners of the board!
    - X got the majestically rotating corners of the board!
    - O made a perfect representation of the letter L!
    - X came across an indescribably funny shape in its apparently most odd form!
- Code to deal with situations where a player makes more than one of the same shape in a turn:
    - O found 2 upside down horseshoes!
    (The code to handle this can be seen in [initialshapedata.py](initialshapedata.py))

## Installation & Setup

Run the following command to clone the repo:
```bash
git clone https://github.com/shakey0/ExtravagantTicTacToe
cd ExtravagantTicTacToe
```

Run the app in the CLI:
```bash
python main.py
```