import pygame
from pygame import SurfaceType


class MovingBackground:
    """Gestion de l'image d'arrière-plan, mouvement et "wrapping"."""
    def __init__(self, img_path="images/bg-plaine.jpg"):
        """Initialisation of scrollable background."""
        self.img = pygame.image.load(img_path)
        self.img= pygame.Surface.convert(self.img)      # For performance and screen compatibility.
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        # Starting position of the "anchor"/the base surface.
        # In pygame, origin (ie: 0,0) is on top left on screen, screen end on bottom right at (scr.width, scr.height).
        # (rectangular) object are placed by giving the position of their top left corner the same way.
        self.posx, self.posy = 0,0
        # Position of its 3 clone circling its bottom right corner.
        self.xpos_clonex = self.posx + self.width   # clonex are for the 2 clones just on the right of the anchor.
        self.ypos_cloney = self.posy + self.height  # cloney are for the 2 clones just under the anchor.

    def update(self, deltax:int = 0, deltay:int = 0):
        """Update background with possible movement, as if you moved delta in a direction, now with wrapping !"""
        if deltax > 1000:       deltax = 1000   # Game crashes if deltax too big.
        self.posx -= deltax;     self.xpos_clonex -= deltax
        self.posy -= deltay;     self.ypos_cloney -= deltay

        # If the anchor leave the origin, it is swapped with the opposite clone from the origin.
        # Circling back on the horizontal.
        if self.posx > 0:
            self.xpos_clonex = self.posx
            self.posx -= self.width

        elif self.xpos_clonex <= 0:
            self.posx = self.xpos_clonex
            self.xpos_clonex += self.width

        # Circling back on the vertical.
        if self.posy > 0:
            self.ypos_cloney = self.posy
            self.posy -= self.height

        elif self.ypos_cloney <= 0:
            self.posy = self.ypos_cloney
            self.ypos_cloney += self.height


    def render(self, surf:SurfaceType):
        """Put the four identical surface, starting from the one always on screen (always under the origin)."""
        surf.blit(self.img, dest=(self.posx, self.posy))                  # Anchor.
        surf.blit(self.img, dest=(self.posx, self.ypos_cloney))           # Clone on the right.
        surf.blit(self.img, dest=(self.xpos_clonex, self.posy))           # Clone under.
        surf.blit(self.img, dest=(self.xpos_clonex, self.ypos_cloney))    # Clone under and on the right (in the corner).
