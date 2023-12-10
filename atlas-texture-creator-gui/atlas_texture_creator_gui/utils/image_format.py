def get_supported_image_formats() -> str:
    supported_image_formats = (
        "png",
        "jpg",
        "jpeg",
        "bmp",
        "tga",
    )

    return " ".join(f"*.{format}" for format in supported_image_formats)
