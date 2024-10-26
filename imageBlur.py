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
    imageSize = screen.get_size()
    level0 = pygame.Surface.subsurface(screen, ((imageSize/3,imageSize/3),(2*imageSize/3,2*imageSize/3))).copy()
    level1 = pygame.Surface.subsurface(screen, ((imageSize/6,imageSize/6),(5*imageSize/6,5*imageSize/6))).copy()
    level2 = pygame.Surface.subsurface(screen, ((imageSize/12,imageSize/12),(11*imageSize/12,11*imageSize/12))).copy()
    level3 = screen.copy()
    level3 = gaussian(level3, 3)
    level2 = gaussian(level2, 2)
    level1 = gaussian(level1, 1)
    return (level0,level1,level2,level3)
    
    
