import os
import PyInstaller.__main__


def build():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dist_path = os.path.join(dir_path, "dist", "atlas-texture-creator")

    if not os.path.exists(dist_path):
        os.makedirs(dist_path)


    PyInstaller.__main__.run([
        "--name",
        "Atlas Texture Creator",
        "--onefile",
        "--noconsole",
        "--distpath",
        dist_path,
        "run.py",
        "--clean",
    ])


if __name__ == "__main__":
    build()
