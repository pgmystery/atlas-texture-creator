from pydantic import BaseSettings


class AtlasManagerConfigType(BaseSettings):
    save_dir: str
