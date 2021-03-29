
import os.path as path

from Process.AutoUpdate.autoupdate import Autoupdate
from decouple import config


@Autoupdate(name="Autoupdate WISROVI", project=config('project', default=''), root_path=path.dirname(path.realpath(__file__)))
def main_demo_autoupdate():
    print("update library")


if __name__ == "__main__":
    main_demo_autoupdate()
