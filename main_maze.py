# -*- coding: utf-8 -*-
import time
from maze import Maze
from collections import deque

s = deque()


maze_csv_path = "labirinto1.txt"  # Substitua pelo caminho correto
maze = Maze() 

maze.load_from_csv(maze_csv_path)

# Exibir o lab
maze.run()
maze.init_player()
s.append(maze.get_init_pos_player())

# MOVIMENTAÇÃO DO JOGADOR - LOOP PARA RODAR ENQUANTO A PILHA NÃO ESTIVER VAZIA 
while s:
    # VARIÁVEL DE CONTROLE PARA AVISAR QUE O JOGADOR PRECISA DESEMPILHAR ATÉ ENCONTRAR JOGADAS POSSÍVEIS
    moved = False

    current = s[-1]  # PEGA O TOPO DA PILHA

    # ADICIONA AS POSIÇÕES QUE ESTÃO NO TOPO A VARIÁVEIS QUE SERÃO RESPONSÁVEIS PELA MOVIMENTAÇÃO DO JOGADOR
    x, y = current 

    # VERIFICA SE O VIZINHO À DIREITA ESTÁ LIVRE (PRÊMIO OU CORREDOR)
    if maze.is_free((x, y + 1)):
        new_pos = (x, y + 1)
        maze.mov_player(new_pos)
        s.append(new_pos)  # ADICIONA A POSIÇÃO PERCORRIDA A PILHA
        moved = True # RETORNA VERDADEIRO POIS ENCONTROU UMA POSIÇÃO VÁLIDA
    
    # VERIFICA SE O VIZINHO À ESQUERDA ESTÁ LIVRE (PRÊMIO OU CORREDOR)
    elif maze.is_free((x, y - 1)):
        new_pos = (x, y - 1)
        maze.mov_player(new_pos)
        s.append(new_pos)  # ADICIONA A POSIÇÃO PERCORRIDA A PILHA
        moved = True # RETORNA VERDADEIRO POIS ENCONTROU UMA POSIÇÃO VÁLIDA

    # VERIFICA SE O VIZINHO DE CIMA ESTÁ LIVRE (PRÊMIO OU CORREDOR)
    elif maze.is_free((x + 1, y)):
        new_pos = (x + 1, y)
        maze.mov_player(new_pos)
        s.append(new_pos)   # ADICIONA A POSIÇÃO PERCORRIDA A PILHA
        moved = True # RETORNA VERDADEIRO POIS ENCONTROU UMA POSIÇÃO VÁLIDA

    # VERIFICA SE O VIZINHO DE BAIXO ESTÁ LIVRE (PRÊMIO OU CORREDOR)
    elif maze.is_free((x - 1, y)): 
        new_pos = (x - 1, y)
        maze.mov_player(new_pos) 
        s.append(new_pos) # ADICIONA A POSIÇÃO PERCORRIDA A PILHA
        moved = True # RETORNA VERDADEIRO POIS ENCONTROU UMA POSIÇÃO VÁLIDA

    # NÃO HOUVE NENHUM VIZINHO DISPONÍVEL > 'MOVED' = FALSO
    if not moved:
        s.pop() # DESEMPILHA E RETORNA PRA POSIÇÃO ANTERIOR

    # TIME PARA SIMULAR O PREENCHIMENTO DOS CORREDORES
    time.sleep(0.005)

    # QUANDO O PRÊMIO FOR ENCONTRADO
    if maze.find_prize(current):
        print("Prêmio encontrado!")
        break