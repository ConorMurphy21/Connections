import subprocess

from src.fileUtils import DATA_PATH

def _ensure_submodule():
    subprocess.call(['git', 'submodule', 'update', '--init', '-q'], cwd=DATA_PATH)
    subprocess.call(['git', 'checkout', 'master', '-q'], cwd=DATA_PATH)
    


def pull_master():
    _ensure_submodule()
    subprocess.call(['git', 'pull', '--rebase', '--autostash', '-q'], cwd=DATA_PATH)


def save_to_git(args, user_config, file):
    if args.no_git:
        return
    print('syncing game files to the cloud...')
    _ensure_submodule()
    subprocess.call(['git', 'pull', '--rebase', '--autostash', '-q'], cwd=DATA_PATH)
    subprocess.call(['git', 'add', file], cwd=DATA_PATH)
    if args.generate:
        subprocess.call(['git', 'commit', '-q', '-m', f'{user_config.username} generated new game!'], cwd=DATA_PATH)
    else:
        subprocess.call(['git', 'commit', '-q', '-m', f'{user_config.username} played a game!'], cwd=DATA_PATH)

    subprocess.run(['git', 'push'], cwd=DATA_PATH)
    result = subprocess.run(['git', 'status'], cwd=DATA_PATH, capture_output=True, text=True).stdout
    if 'nothing to commit' not in result:
        print('Something went wrong syncing with the cloud :(')
        print('Make sure conor gave you access to the repo')

