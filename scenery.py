import config
from pygame import Color, Surface, SurfaceType, image



class Skybox:
    def __init__(self, world_name:str = config.WORLD_NAMES[0]):
        """Initialise une skybox avec des couleurs d'altitudes prédéfinis."""
        # Background Data Fetching and preparation
        background_data =  config.BACKGROUND_WORLDS_DATA[world_name]
        self.bdry_name = background_data["BDRY_NAME"]
        self.bdry_alti = background_data["BDRY_ALTI"]
        self.bdry_color = background_data["BDRY_COLOR"]

        # Initialisation of positional variable
        self.alti = self.bdry_alti[0]
        self.layer = 0
        self.max_layer = len(self.bdry_alti) - 2 # layer(0,1,2,3) for 5 boundary
        self.prev_bdry = self.bdry_alti[self.layer]
        self.next_bdry = self.bdry_alti[self.layer+1]
        # Initialisation of color variable
        self.curr_bdry_color = self.bdry_color[self.layer]
        self.next_bdry_color = self.bdry_color[self.layer+1]
        self.color = Color(self.bdry_color[self.layer])

    def skybox_color(self) -> Color:
        """ Give the color to use for sky depending of altitude

        pseudo-code
        alti_gradient: proximité to next bdry agaisnt current bdry
		= (closest_higher_boundary_alti - alti) / (clos_higher - clos_lower)
        color_gradient: rgb previous bdry colour,  RGB next bdry colour
        current_colour= (r, g, b) + alti_gradient*(R-r, G-g, B-b)
        """
        alti_gradient = 1 - ((self.next_bdry-self.alti) / (self.next_bdry - self.prev_bdry))
        prev_c = self.curr_bdry_color
        next_c = self.next_bdry_color
        current_c = [0,0,0]
        for i in (0,1,2):
            current_c[i] = prev_c[i] + int(alti_gradient * (next_c[i]-prev_c[i]))
        return Color(current_c)


    def update(self, altitude:float) -> None:
        """ Update the skybox with the new altitude

        update current layer first if needed,
        then the sky color if not in last layer"""
        self.alti = altitude
        while self.alti > self.next_bdry:
            self.layer += 1
            self.prev_bdry = self.next_bdry
            self.next_bdry = self.bdry_alti[self.layer+1]
        if self.layer < self.max_layer:
            self.color.update(self.skybox_color())

    def render(self, surf: SurfaceType) -> None:
        """Fill screen(background) with current color

        it fill the background if called before other rendering"""
        surf.fill(self.color)


class MovingBackground:
    """Gestion de l'image d'arrière-plan, mouvement et "wrapping" """

    def __init__(self, img_path:str="images/bg-plaine.jpg") -> None:
        """"Initialisation of scrollable background"""
        self.img = image.load(img_path)
        self.img = Surface.convert(self.img) # For perfomance and screen compatibility
        self.width = self.img.get_width()
        self.height = self.img.get_height()


        # In pygame, origin (ie: 0,0) is on top left on screen,
        # screen end on bottom right at (scr.width, scr.height).
        # (Rectangular) object are placed by
        # giving the position of their top left corner the same way.
        #
        # Starting position of the "anchor"/the base surface.
        self.posx, self.posy = 0, 0
        # Position of its 3 clone circling its bottom right corner.
        self.xpos_clonex = self.posx + self.width
        self.ypos_cloney = self.posy + self.height

    def update(self, deltax:int=0, deltay:int=0) -> None:
        """"update background with possible movement,
        as if you moved delta in a direction, now with wrapping !
        """
        # Modulo to avoid crash a crash (on Pierre pc), and avoid ginourmous nb
        deltax %= self.width * (1 if deltax>=0 else -1)
        deltay %= self.height* (1 if deltay>=0 else -1)
        self.posx -= deltax;     self.xpos_clonex -= deltax
        self.posy -= deltay;     self.ypos_cloney -= deltay

        # if the anchor leave the origin, it is swapped with the opposites clones from the origin
        # Circling back on the horizontal
        if self.posx > 0:
            self.xpos_clonex = self.posx
            self.posx -= self.width
        elif self.xpos_clonex <= 0:
            self.posx = self.xpos_clonex
            self.xpos_clonex += self.width
        # Circling back on the vertical
        if self.posy > 0:
            self.ypos_cloney = self.posy
            self.posy -= self.height
        elif self.ypos_cloney <= 0:
            self.posy = self.ypos_cloney
            self.ypos_cloney += self.height

    def render(self, surf: SurfaceType) -> None:
        """Put the four identical surface,
        starting from the one always on screen (always under the origin)"""
        surf.blit(self.img, dest=(self.posx, self.posy))                  # anchor
        surf.blit(self.img, dest=(self.posx, self.ypos_cloney))           # clone on the right
        surf.blit(self.img, dest=(self.xpos_clonex, self.posy))           # clone under
        surf.blit(self.img, dest=(self.xpos_clonex, self.ypos_cloney))    # clone under and on the right (in the corner)

