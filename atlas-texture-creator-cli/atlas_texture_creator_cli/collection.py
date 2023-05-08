import typer
from atlas_texture_creator import atlas_manager


app = typer.Typer()

@app.command()
def list():
    atlas_manager.
