# Lines of Actions

## Installation and prerequisite

1. Install Python3, see [official website](https://www.python.org/downloads/)
2. After installing Python3, install `pygame` Library, run:

```shell
pip install pygame
```

or

```shell
pip3 install pygame
```

## How to run

Using the Command Line, for Windows users, inside the `/src` directory:

```shell
python main.py <WhitePlayer> <BlackPlayer> [NGames]
```

Using the Command Line, for Linux or MacOS users, inside the `/src` directory:

```shell
python3 main.py <WhitePlayer> <BlackPlayer> [NGames]
```


Options:
```

        <WhitePlayer> and <BlackPlayer> options: 
                -h : For Human Player 
                -l1 : For Bot Player Easy Level, 
                -l2 : For Bot Player Medium Level, 
                -l3 : For Bot Player Hard Level

        [NGames] options: 
                [1-1000] default=1 : Number of games to play, OPTIONAL

        
        For Example: 

            python main.py -l1 -h 30   # 30 Games with White being Easy Bot
                                       # and Black being Human Player

```

## How to play

- Each turn a player moves one of their pieces on the board (starting with Black);
- For Human Players:
    - Click and select a piece to move;
    - After selecting a piece, it will appear green dots on the board, which are the moves that this piece can make;
    - Click on the square with a green dot to move the selected piece onto that specific square;
- Once game over is detected, the game result will be printed
- If `[NGames]` is given and set greater than 1, then the board will automatically reset for the next game (`[NGames]` times);