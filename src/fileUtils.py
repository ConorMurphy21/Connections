from pathlib import Path

BASE_PATH = Path(__file__).parent.parent

DATA_PATH = BASE_PATH / Path('data')

GAMES_FOLDER = DATA_PATH / Path('games')

RESULTS_FOLDER = DATA_PATH / Path('results')


def get_game_filename(author: str, number: int) -> Path:
    return GAMES_FOLDER / author / str(number)


def get_author_folder(author: str) -> Path:
    return GAMES_FOLDER / author


def get_logfile_dir(user: str, author: str, number: int) -> Path:
    return RESULTS_FOLDER / author / str(number) / user


def get_machine_logfile(user: str, author: str, number: int) -> Path:
    return RESULTS_FOLDER / author / str(number) / user / 'machine.jsonl'
