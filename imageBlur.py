import pygame
from PIL import Image, ImageFilter

def gaussian(img: pygame.Surface, distance: int) -> Image:
    blurImg = Image.frombytes("RGBA", img.get_size(), pygame.image.tobytes(img, "RGBA")).filter(ImageFilter.GaussianBlur(radius=distance))
    im = pygame.image.frombytes(blurImg.tobytes(), img.get_size(), "RGBA")
    return im
