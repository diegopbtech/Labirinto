import pygame
import numpy as np
import csv
import random
import threading

class Maze:

    '''
    O labirinto é representado por uma matriz binária em arquivo. Onde
    o valor 0 representa um quadrado da parede do labirinto, e o valor 1 representa 
    um quadrado do corredor do labirinto.
    
    O labirinto em memória é representado por uma matriz inteira, indicando para cada
    quadrado se o mesmo é uma parede, um corredor, o prêmio ou o jogador.
    '''
    
    WALL = 0
    HALL = 1
    PLAYER = 2
    PRIZE = 3

    # ESSA VARIÁVEL É UM INCREMENTO AO CÓDIGO - EXIBIR UMA MENSAGEM DE QUE O PRÊMIO FOI ENCONTRADO NA TELA
    WINNER = False
    
    def __init__(self):
        '''
        Inicializa a matriz de inteiros M que representa a lógica do labirinto

        '''
        self.M = None #matriz que representa o labirinto
        pygame.init()

    
    def load_from_csv(self, file_path : str):
        '''
        Função para carregar a matriz de um arquivo CSV  

        Parameters
        ----------
        file_path : str
            Nome do arquivo contendo a matriz binária que descreve o labirinto.

        '''
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.M = np.array([list(map(int, row)) for row in reader])
            
    def init_player(self):
        '''
        Coloca o prêmio (quadrado amarelo) e o jogador (quadrado azul)
        em posições aleatórias no corredor do labirinto.

        '''
        #escolhendo a posição aleatória do player em um corredor
        while True:
            posx = random.randint(2, 39)
            posy = random.randint(2, 39)
            if self.M[posx, posy] == Maze.HALL:
                self.init_pos_player = (posx, posy)
                self.M[posx, posy] = Maze.PLAYER
                break
        
        #escolhendo a posição aleatória do premio em um corredor
        while True:
            posx = random.randint(2, 39)
            posy = random.randint(2, 39)
            if self.M[posx, posy] == Maze.HALL:
                self.M[posx, posy] = Maze.PRIZE
                break

    def find_prize(self, pos : (int, int)) -> bool:
        '''
        O tabuleiro é dividio 
        Recebe uma posição (x,y) do tabuleiro e indica se o prêmio está contido
        naquela posição.

        Parameters
        ----------
        pos : (int, int)
            Posição do quadrado na matriz do labirinto que se deseja testar se 
            foi encontrado prêmio

        Returns
        -------
        bool
            Retorna True se o quadrado do labirinto na posição 'pos' contiver o prêmio, 
            retorna False em caso contrário.

        '''
        if self.M[pos[0], pos[1]] == Maze.PRIZE:
            self.WINNER = True
            return True
        else:
            return False
        
    def is_free(self, pos : (int, int)) -> bool:
        '''
        Indica se a posição fornecida está livre para o jogador acessar, ou seja, 
        se for corredor ou prêmio.

        Parameters
        ----------
        pos : (int, int)
            Posição do quadrado na matriz do labirinto que se deseja testar se 
            está livre.


        Returns
        -------
        bool
            Retorna True.

        '''
        if self.M[pos[0], pos[1]] in [Maze.HALL, Maze.PRIZE]:
            return True
        else:
            return False
        
        
    def mov_player(self, pos : (int, int)) -> None:
        '''
        Move o jogador para uma nova posição do labirinto desde que ela seja uma
        posição corredor na matriz M.

        Parameters
        ----------
        pos : (int, int)
            Nova posição (x,y) no labiritno em que o jogador será movido.

        '''
        if self.M[pos[0], pos[1]] == Maze.HALL:
            self.M[pos[0], pos[1]] = Maze.PLAYER
        

    def get_init_pos_player(self) -> (int, int):
        '''
        Indica a posição inicial do jogador dentro do labirinto que foi gerada 
        de forma aleatória.

        Returns
        -------
        (int, int)
            Posição inicial (x,y) do jogador no labirinto.

        '''
        
        return self.init_pos_player
            
    def run(self):
        '''
        Thread responsável pela atualização da visualização do labirinto.

        '''
        th = threading.Thread(target=self._display)
        th.start()
    
    def _display(self, cell_size=15):
        '''
        Método privado para exibir o labirinto na tela mapeando os valores lógicos
        atribuídos em cada casa da matriz M, seguindo as constantes definidas na classe.

        
        '''
        rows, cols = self.M.shape
        width, height = cols * cell_size, rows * cell_size
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Labirinto")
    
        # Cores
        BLACK = (0, 0, 0)
        GRAY = (192, 192, 192)
        BLUE = (0, 0, 255)
        GOLD = (255, 215, 0)
        WHITE = (255, 255, 255)
    
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
    
            screen.fill(BLACK)
    
            # Desenhar o labirinto
            for y in range(rows):
                for x in range(cols):
                    if self.M[y, x] ==  Maze.WALL:
                        color = BLACK
                    elif self.M[y, x] == Maze.HALL:
                        color = GRAY
                    elif self.M[y, x] == Maze.PLAYER:
                        color = BLUE
                    elif self.M[y, x] == Maze.PRIZE:
                        color = GOLD

                    pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

            # INCREMENTO AO CÓDIGO - EXIBIR UMA MENSAGEM DE QUE O PRÊMIO FOI ENCONTRADO NA TELA
            if self.WINNER:
                    font = pygame.font.SysFont('Arial', 30) 
                    text = font.render("Prêmio encontrado!", True, WHITE) 
                    
                    text_width = text.get_width()
                    text_height = text.get_height()
                    rectangle_width = text_width + 20 
                    rectangle_height = text_height + 20 
                    rectangle_x = (width // 2 - text_width // 2) - 10
                    rectangle_y = (height // 2 - text_height // 2)  + 10

                    pygame.draw.rect(screen, BLACK, 
                                    (rectangle_x, rectangle_y, rectangle_width, rectangle_height))

                    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))

            pygame.display.flip()
