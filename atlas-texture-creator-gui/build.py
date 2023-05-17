import PyInstaller.__main__


def build():
    PyInstaller.__main__.run([
        "--name",
        "Atlas Texture Creator",
        "--onefile",
        "--noconsole",
        "run.py",
        "--clean",
    ])


if __name__ == "__main__":
    build()
