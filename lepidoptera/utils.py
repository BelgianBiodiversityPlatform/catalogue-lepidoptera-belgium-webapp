import subprocess


def get_source_version_info():
    return subprocess.run(['git', 'log', "--pretty=format:%h (%ai)", '-n 1'],  # nosec
                          stdout=subprocess.PIPE).stdout.decode('utf-8')  # nosec
