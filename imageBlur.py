import pygame
from PIL import Image, ImageFilter

def gaussian(img: pygame.Surface, distance: int) -> pygame.Surface:
    """For blurring based on distance."""
    blurImg = Image.frombytes("RGBA", img.get_size(), pygame.image.tobytes(img, "RGBA")).filter(ImageFilter.GaussianBlur(radius=distance))
    im = pygame.image.frombytes(blurImg.tobytes(), img.get_size(), "RGBA")
    return im
# 1/3 normal
# 1/6 slightly more
# 1/12 much more
# 1/12 loads more
def blurScreen(screen: pygame.Surface) -> (pygame.Surface,pygame.Surface,pygame.Surface,pygame.Surface):
    """For blurring based on peripheral vision in 3 levels. Returns a tuple (level0,level1,level2,level3). Level0 is the innermost, level3 the outermost."""
    imageHeight = screen.get_height()
    imageWidth = screen.get_width()
    level0 = pygame.Surface.subsurface(screen, ((imageWidth/3,imageHeight/3),(imageWidth/3,imageHeight/3))).copy()
    level1 = pygame.Surface.subsurface(screen, ((imageWidth/6,imageHeight/6),(4*imageWidth/6,4*imageHeight/6))).copy()
    level2 = pygame.Surface.subsurface(screen, ((imageWidth/12,imageHeight/12),(10*imageWidth/12,10*imageHeight/12))).copy()
    level3 = screen.copy()
    level3 = gaussian(level3, 5)
    level2 = gaussian(level2, 4)
    level1 = gaussian(level1, 3)
    level0 = gaussian(level0, 2)
    return (level0,level1,level2,level3)
    
    
