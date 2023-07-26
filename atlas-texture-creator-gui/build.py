import os
import PyInstaller.__main__


def build():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dist_path = os.path.join(dir_path, "dist", "atlas-texture-creator")

    if not os.path.exists(dist_path):
        os.makedirs(dist_path)

    resource_path = os.path.join("atlas_texture_creator_gui", "resources")
    resource_path_images = os.path.join(resource_path, "images", "*")
    resource_path_icon = os.path.join(resource_path, "icons", "atlas_texture_creator.ico")

    PyInstaller.__main__.run([
        "--name",
        "Atlas Texture Creator",
        "--onefile",
        "--noconsole",
        "--distpath",
        dist_path,
        "run.py",
        "--clean",
        "--debug=all",
        f"--icon={resource_path_icon}",
        f"--add-data={resource_path_images}{os.pathsep}images/",
    ])


if __name__ == "__main__":
    build()
