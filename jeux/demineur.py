import pygame
import os
from random import randint

class Tile:
    def __init__(self, coordonatesGrid : tuple[int,int], size:int) -> None:
        self.coordonatesGrid : tuple[int,int] = coordonatesGrid

        self.size : int = size
        self.coordonates : tuple[int,int] = (self.coordonatesGrid[0]*self.size, self.coordonatesGrid[1]*self.size)

        self.surounding : set[Tile] = set()
        self.suroundingMines : int = 0
        self.suroundingFlags : int = 0

        self.__tileSheet : list[list[pygame.Surface]]
        self.__numberSheet : list[pygame.Surface]
        self.tileSheet : list[list[pygame.Surface]]
        self.numberSheet : list[pygame.Surface]
        self.load_textures()

        self.revealed : bool = False
        self.isMine : bool = False
        self.showMine : bool = False
        self.flag : int = 0 # 0 = no flag, 1 = flag, 2 = question mark

    def change_size(self, size:int) -> None:
        self.size = size
        self.coordonates = (self.coordonatesGrid[0]*self.size, self.coordonatesGrid[1]*self.size)
        self.update_textures()

    def load_textures(self) -> None:
        PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'assets/ressourcesActives/textures/demineur')
        tileSheet = pygame.image.load(os.path.join(PATH, 'tilesheet.png'))
        numberSheet = pygame.image.load(os.path.join(PATH, 'numbersheet.png'))

        self.__tileSheet = [[],[]]
        self.__numberSheet = []

        x,y = tileSheet.get_size()
        for i in range(2):
            x,y = tileSheet.get_size()
            for j in range(0,x,x//6):
                self.__tileSheet[i] += [tileSheet.subsurface(j,i*y//2,x//6,y//2)]

        x,y = numberSheet.get_size()
        for i in range(0,x,x//9):
            self.__numberSheet += [numberSheet.subsurface(i,0,x//9,y)]

        self.update_textures()

    def update_textures(self) -> None:
        self.tileSheet = [[pygame.transform.scale(tile, (self.size, self.size)) for tile in row] for row in self.__tileSheet]
        self.numberSheet = [pygame.transform.scale(number, (self.size, self.size)) for number in self.__numberSheet]

    def __str__(self) -> str:
        return f'{4*' '}Tile at {self.coordonatesGrid=} and {self.coordonates=} is {self.revealed=} and {self.flag=}'

    def is_touched(self, pos : tuple[int,int]) -> bool:
        x,y = pos
        if (self.coordonates[0] < x <= self.coordonates[0]+self.size) and (self.coordonates[1] < y <= self.coordonates[1]+self.size):
            return True
        else:
            return False
        
    def toggle_flag(self) -> None:
        if self.revealed:
            print('Tile already revealed')
            return
        
        if self.flag == 1:
            for tile in self.surounding:
                tile.suroundingFlags -= 1

        self.flag = (self.flag+1)%3

        if self.flag == 1:
            for tile in self.surounding:
                tile.suroundingFlags += 1

    def reveal(self) -> None:
        if self.revealed:
            print(f'{self.suroundingMines=}, {self.suroundingFlags=}')
            if self.suroundingFlags == self.suroundingMines:
                for tile in self.surounding:
                    verify = tile.reveal()
                    if not verify:
                        return False
                
            return True
        

        if self.flag == 1:
            return True
        
        self.revealed = True

        if self.isMine:
            return False
        elif self.suroundingMines == 0:
            for tile in self.surounding:
                if not tile.revealed and tile.flag != 1:
                    if not tile.reveal():
                        return False
                    
        return True
    
    def add_surounding(self, tile) -> None:
        self.surounding.add(tile)
        if tile.isMine:
            self.suroundingMines += 1
        if tile.flag == 1:
            self.suroundingFlags += 1
        
    def draw(self, screen : pygame.Surface) -> None:
        line : int = (self.coordonatesGrid[0]+self.coordonatesGrid[1])%2
        if self.revealed:
            if self.isMine:
                screen.blit(self.tileSheet[line][5], self.coordonates)
            else:
                screen.blit(self.tileSheet[line][4], self.coordonates)
                screen.blit(self.numberSheet[self.suroundingMines], self.coordonates)

        else:
            if self.showMine and self.isMine:
                
                screen.blit(self.tileSheet[line][3], self.coordonates)
            else:
                screen.blit(self.tileSheet[line][self.flag], self.coordonates)

class Demineur:
    def __init__(self, screen : pygame.Surface, gridSize : tuple[int,int], nbMines : int) -> None:

        self.screen : pygame.Surface = screen

        self.window_pos : tuple[int,int] = (0,0)
        self.window_screen : pygame.Surface = pygame.Surface(self.screen.get_size())

        self.mines_not_generated : bool = True
        

        self.gridSize : tuple[int,int] = gridSize
        self.nbMines : int = nbMines
        self.flagsLeft : int = self.nbMines
        
        x,y = self.window_screen.get_size()
        self.tile_size : int = y // self.gridSize[1]
        if self.tile_size * self.gridSize[0] > x:
            self.tile_size = x // self.gridSize[0]


        self.tiles : set[Tile] = set()
        for i in range(self.gridSize[0]):
            for j in range(self.gridSize[1]):
                self.tiles.add(Tile((i,j), self.tile_size))

    def generate_mines(self, tile_centered : Tile) -> None:
        self.mines_not_generated = False
        tiles : list[Tile] = list(self.tiles.copy())
        temporary : set[Tile] = set()
        for tile in tiles:
            if (tile_centered.coordonatesGrid[0] + 1 >= tile.coordonatesGrid[0] >= tile_centered.coordonatesGrid[0] - 1) and \
               (tile_centered.coordonatesGrid[1] + 1 >= tile.coordonatesGrid[1] >= tile_centered.coordonatesGrid[1] - 1):
                temporary.add(tile)
        for tile in temporary:
            tiles.remove(tile)
        
        mines : int = self.nbMines
        n = len(tiles)
        while mines > 0 and n > 0:
            x = randint(0, n-1)
            for tile in self.tiles:
                if tile == tiles[x]:
                    tile.isMine = True
                    mines -= 1
                    break

            tiles.remove(tile)
            n -= 1

        for tile in self.tiles:
            for tile2 in self.tiles:
                if (tile.coordonatesGrid[0] + 1 >= tile2.coordonatesGrid[0] >= tile.coordonatesGrid[0] - 1) and \
                   (tile.coordonatesGrid[1] + 1 >= tile2.coordonatesGrid[1] >= tile.coordonatesGrid[1] - 1) and \
                   tile != tile2:
                    tile.add_surounding(tile2)

    def update(self, events) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.dict['button'] == 1:
                    for tile in self.tiles:
                        if tile.is_touched((event.dict['pos'][0]-self.window_pos[0], event.dict['pos'][1]-self.window_pos[1])):
                            if self.mines_not_generated:
                                self.generate_mines(tile)
                                self.mines_not_generated = False
                            if not tile.reveal():
                                for tile in self.tiles:
                                    tile.showMine = True

                elif event.dict['button'] == 3:
                    for tile in self.tiles:
                        if tile.is_touched((event.dict['pos'][0]-self.window_pos[0], event.dict['pos'][1]-self.window_pos[1])):
                            tile.toggle_flag()
        for tile in self.tiles:
            tile.draw(self.window_screen)

        self.screen.blit(self.window_screen, self.window_pos)
