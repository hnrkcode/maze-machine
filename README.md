# Maze generator

> Generate a maze with the hunt-and-kill algorithm

![maze demo](maze.gif)

## Setup

```sh
pipenv install
pipenv shell
python3 run.py
```

## Usage

| key | description |
|:-----|-------|
| `Enter` | Run algorithm |
| `R`     | Reset |
| `S`     | Solve the maze |
| `SCROLL` | Change cell size |
| hold `W` & `SCROLL` | Change grid width |
| hold `H` & `SCROLL` | Change grid height |
| `ESC`   | Exit program |

## Development

```sh
pipenv install --dev
```

## Run tests

```sh
pytest
```

## Test coverage

```sh
pytest --cov=maze tests
```