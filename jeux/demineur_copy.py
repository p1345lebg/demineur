import pygame
import os
from random import randint



class Demineur:
    def __init__(self, screen : pygame.surface.Surface, gridSize : tuple[int,int], mines : int, textures : dict) -> None:
        self.background_base : pygame.surface.Surface = textures["background"]

        self.grid = Grid(screen,gridSize, mines, textures)

        self.screen : pygame.surface.Surface
        self.update_screen(screen)

    
        #self.font : pygame.font.Font = textures["font"]

        self.gridSize : tuple[int,int] = gridSize

    def update_screen(self, screen : pygame.surface.Surface) -> None:
        self.screen  = screen
        screenSize : tuple[int,int] = screen.get_size()

        x, y = screenSize
        x1, y1 = self.background_base.get_size()
        resize_x = x/x1
        resize_y = y/y1

        self.background : pygame.surface.Surface
        self.background_pos : tuple[int,int]

        if resize_x > resize_y:
            self.background = pygame.transform.scale_by(self.background_base, resize_x)
            self.background_pos = (0, int((y - y1*resize_x) // 2))
        else:
            self.background  = pygame.transform.scale_by(self.background_base, resize_y)
            self.background_pos = (int((x - x1*resize_y)) // 2, 0)

        self.grid.update_screen(screen)
        

    
    def update(self) -> None:
        self.screen.blit(self.background, self.background_pos)
        self.grid.update()



class Grid:
    def __init__(self, screen : pygame.Surface, gridSize : tuple[int,int], mines : int, textures : dict[str,pygame.surface.Surface]) -> None:
        self.size : tuple[int,int] = gridSize
        self.mines : int = mines



        self.screen : pygame.surface.Surface = screen
        screenSize_x, screenSize_y = screen.get_size()

        self.tile_size : int = screenSize_y // self.size[1]
        if self.tile_size * self.size[0] > screenSize_x:
            self.tile_size = screenSize_x // self.size[0]

        self.size_x : int = self.size[0] * self.tile_size
        self.size_y : int = self.size[1] * self.tile_size




        self.tileSheet : list[pygame.surface.Surface] = [[],[]]
        self.numberSheet : list[pygame.surface.Surface] = []
        x,y = textures["tileSheet"].get_size()
        for i in range(0, 2):
            for j in range(0,x,x//6):
                self.tileSheet[i] += [textures["tileSheet"].subsurface(j,i*y//2,x//6,y//2)]

        self.numberSheet = []
        x,y = textures["numberSheet"].get_size()
        for i in range(0,x,x//9):
            self.tileSheet += [textures["numberSheet"].subsurface(i,0,x//9,y)]

        

        self.tiles : set[Tile] = set()
        for y in range(gridSize[1]):
            for x in range(gridSize[0]):
                self.tiles.add(Tile((x,y), self.tileSheet, self.numberSheet))


    def update_screen(self, screen : pygame.surface.Surface) -> None:
        self.screen = screen
        screenSize_x, screenSize_y = screen.get_size()

        self.tile_size = screenSize_y // self.size[1]
        if self.tile_size * self.size[0] > screenSize_x:
            self.tile_size = screenSize_x // self.size[0]

        self.size_x : int = self.size[0] * self.tile_size
        self.size_y : int = self.size[1] * self.tile_size

        for tile in self.tiles:
            tile.update_size(self.tile_size)
            tile.update_textures()

    def update_textures(self, textures : dict[str, pygame.surface.Surface]):
        self.tileSheet = [[],[]]
        x,y = textures["tileSheet"].get_size()
        for i in range(0, 2):
            for j in range(0,x,x//6):
                self.tileSheet[i] += [textures["tileSheet"].subsurface(j,i*y//2,x//6,y//2)]

        self.numberSheet = []
        x,y = textures["numberSheet"].get_size()
        for i in range(0,x,x//9):
            self.tileSheet += [textures["numberSheet"].subsurface(i,0,x//9,y)]

        for tile in self.tiles:
            tile.change_textures(self.tileSheet, self.numberSheet)
            tile.update_textures()

    def generate_tiles(self, gridSize):
        pass

    def generate_mines(self):
        pass

    def update(self):
        for tile in self.tiles:
            tile.draw(self.screen)

class Tile:
    def __init__(self, coordonates : tuple[int,int], tileSheet : list[list[pygame.Surface]], numberSheet : list[pygame.Surface]) -> None:
        self.coordonates : tuple[int,int] = coordonates 
        self.size : int = 1

        self.__tileSheet : list[list[pygame.Surface]] = tileSheet
        self.__numberSheet : list[pygame.Surface] = numberSheet

        self.tileSheet : list[list[pygame.Surface]]
        self.numberSheet : list[pygame.Surface]
        self.update_textures()



        self.surounding : set[Tile]
        self.revealed : bool = False
        self.flag : bool = False

    def surounding_add(self, tile) -> None:
        self.surounding.add(tile)


    def set_flag(self) -> None:
        self.flag = not self.flag

    def reveal(self) -> None:
        if self.flag:
            return
        
        if self.revealed:
            self.__reveal_around()
            return
        
        self.revealed = True

    def __reveal_around(self) -> None:
        for tile in self.surounding:
            tile.reveal()

    def change_textures(self, tileSheet : list[list[pygame.surface.Surface]], numberSheet : list[pygame.surface.Surface]) -> None:
        self.__tileSheet = tileSheet
        self.__numberSheet = numberSheet
        self.update_textures()

    def update_textures(self):
        self.tileSheet = [[],[]]
        for i in range(len(self.__tileSheet)):
            if type(self.__tileSheet[i]) == list:
                for j in range(len(self.__tileSheet[i])):
                    self.tileSheet[i] += [pygame.transform.scale(self.__tileSheet[i][j], (self.size, self.size))]



    def update_size(self, size : int) -> None:
        self.size = size
        self.update_textures()

    def draw(self, screen : pygame.surface.Surface) -> None:
        screen.blit(self.tileSheet[(self.coordonates[0]+self.coordonates[1])%2][0], (self.coordonates[0]*self.size, self.coordonates[1]*self.size))