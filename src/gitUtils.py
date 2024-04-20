import subprocess

from src.fileUtils import DATA_PATH


def pull_master():
    subprocess.call(['git', 'pull', '--rebase', '--autostash'], cwd=DATA_PATH)


def save_to_git(args, user_config, file):
    if args.no_git:
        return
    subprocess.call(['git', 'pull', '--rebase', '--autostash'], cwd=DATA_PATH)
    subprocess.call(['git', 'add', file], cwd=DATA_PATH)
    if args.generate:
        subprocess.call(['git', 'commit', '-m', f'{user_config.username} generated new game!'], cwd=DATA_PATH)
    else:
        subprocess.call(['git', 'commit', '-m', f'{user_config.username} played a game!'], cwd=DATA_PATH)

    subprocess.call(['git', 'push'], cwd=DATA_PATH)
