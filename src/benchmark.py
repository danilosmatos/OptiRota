# Importações avulsas
import os
import random
import numpy as np
import osmnx as ox
import matplotlib.pyplot as plt
import time
# Importações do próprio projeto, todos tem que vir do algorithms
from algorithms.grafo import grafo_base, grafo_mapear, grafo_teste
from algorithms.dijkstra import Grafo_Dij_Base, dij_Opi 
from algorithms.a_star import Grafo_A_Star_Base, a_star_opi

def comparacao_bruta(local_do_grafo, peso_do_grafo, origem_a_star, destino_a_star):
    # Construção do grafo, é sensível à acentuação e precisa ser capitalizado. OBS: aracaju é em sergipe
    # peso_do_grafo pode ser travel_time e lenght, mas se usar distância provavelmente vai dar erro no cvrptw
    print("\n" + "― "*32)
    print(" "*20 + "EXECUÇÃO DO A* E DIJKSTRA")
    print("― "*32 + "\n")
    print(f"Local do Grafo: {local_do_grafo}")
    print(f"Origem: {origem_a_star}")
    print(f"Destino: {destino_a_star}")

    grafo, weight_type = grafo_base(place_name=local_do_grafo, weight_type=peso_do_grafo)
    if not grafo:
        print("Erro: Grafo não pôde ser carregado.")
        return

    origem_node, destino_node = grafo_mapear(grafo, origem_a_star, destino_a_star)
    
    if origem_node is None or destino_node is None:
        print("Erro: Nós de origem ou destino não encontrados no grafo.")
        return
    
    #
    # Execução A*
    #
    
    print("\nExecutando A*")
    G_astar = Grafo_A_Star_Base(grafo, weight_type=weight_type)
    tempo_inicio_astar = time.time()
    distancias_a, pais_a, nos_a = a_star_opi(G_astar, origem_node, destino_node)
    tempo_fim_astar = time.time()
    tempo_total_astar = tempo_fim_astar - tempo_inicio_astar

    #
    # Execução Dijkstra
    #

    print("Executando Dijkstra")
    tempo_inicio_dijkstra = time.time()
    G_dijkstra = Grafo_Dij_Base(grafo, weight_type=weight_type) 
    distancias_d, pais_d, nos_d = dij_Opi(G_dijkstra, origem_node)
    tempo_fim_dijkstra = time.time()
    tempo_total_dijkstra = tempo_fim_dijkstra - tempo_inicio_dijkstra
    
    #
    # Manda os dados no terminal
    #
    
    if destino_node in distancias_a:
        print("\n" + "="*35)
        print(" "*5 + "COMPARAÇÃO DE DESEMPENHO")
        print("="*35)
        print("\n[Métricas]")
        print("-" * 60)
        print(f"{'Algoritmo':<10} | {'Tempo (ms)':>15} | {'Nós Explorados':>15}")
        print("-" * 60)
        print(f"{'Dijkstra':<10} | {tempo_total_dijkstra*1000:15.3f} | {nos_d:15}")
        print(f"{'A*':<10} | {tempo_total_astar*1000:15.3f} | {nos_a:15}")
        print("-" * 60)
        
        #
        # Gráficos
        #
        
        nome_arquivo = f"comp_time_{local_do_grafo.replace(', ', '_').lower()}.png"
        
        DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
        PASTA_GRAFICOS = os.path.join(DIRETORIO_ATUAL, 'graph')
        if not os.path.exists(PASTA_GRAFICOS):
             os.makedirs(PASTA_GRAFICOS)
        CAMINHO_COMPLETO = os.path.join(PASTA_GRAFICOS, nome_arquivo)
        
        algoritmos = ['Dijkstra', 'A*']
        tempos_ms = [tempo_total_dijkstra * 1000, tempo_total_astar * 1000]
        nos_explorados = [nos_d, nos_a]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(f'Comparação de Desempenho entre Algoritmos em {local_do_grafo}', fontsize=16)

        ax1.bar(algoritmos, tempos_ms, color=['darkorange', 'dodgerblue'])
        ax1.set_title('Tempo de Execução')
        ax1.set_ylabel('Tempo (milissegundos)')
        ax1.set_xlabel('Algoritmo')
        for i, v in enumerate(tempos_ms):
            ax1.text(i, v + max(tempos_ms)*0.05, f'{v:.2f}', ha='center', color='black', fontweight='bold')
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        ax2.bar(algoritmos, nos_explorados, color=['darkorange', 'dodgerblue'])
        ax2.set_title('Nós do Grafo Explorados')
        ax2.set_ylabel('Quantidade de Nós')
        ax2.set_xlabel('Algoritmo')
        for i, v in enumerate(nos_explorados):
            ax2.text(i, v + max(nos_explorados)*0.05, f'{v}', ha='center', color='black', fontweight='bold')
        ax2.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        plt.savefig(CAMINHO_COMPLETO)
        plt.show()
        plt.close(fig)

    else:
        print("Caminho A* não encontrado. Verifique as coordenadas.")
        print("\n"+"― "*30+"\n")

def comparacao_big_o(locais_para_teste, peso_do_grafo):
    print("\n" + "― "*30)
    print(" "*10 + "BIG O: DIJKSTRA E A*")
    print("― "*30 + "\n")
    
    tamanhos_nos_dij = []
    tempos_dij = []
    tamanhos_nos_a = []
    tempos_a = []

    for local, nome_tamanho in locais_para_teste:
        print(f"Fazendo Grafo: {nome_tamanho} ({local})")
        
        grafo, weight_type = grafo_base(place_name=local, weight_type=peso_do_grafo)
        
        num_nos = grafo.number_of_nodes()
        
        todos_os_nos = list(grafo.nodes)
        
        origem_node = random.choice(todos_os_nos)
        destino_node = random.choice(todos_os_nos)
        
        while origem_node == destino_node:
            destino_node = random.choice(todos_os_nos)
        #
        # Dijkstra
        #
        grafo_dijkstra = Grafo_Dij_Base(grafo, weight_type=weight_type) 
        tempo_inicio_d = time.time()
        x, x, nos_d = dij_Opi(grafo_dijkstra, origem_node) 
        tempo_final_d = time.time()
        tempo_dijkstra = tempo_final_d - tempo_inicio_d
        
        #
        # A*
        #
        grafo_a_star = Grafo_A_Star_Base(grafo, weight_type=weight_type)
        tempo_inicio_a_star = time.time()
        x, x, nos_a_star = a_star_opi(grafo_a_star, origem_node, destino_node) 
        tempo_final_a_star = time.time()
        tempo_a_star = tempo_final_a_star - tempo_inicio_a_star
        
        tamanhos_nos_dij.append(num_nos)
        tempos_dij.append(tempo_dijkstra * 1000)
        tamanhos_nos_a.append(num_nos)
        tempos_a.append(tempo_a_star * 1000)
        
        print(f"\n    Nós: {num_nos:5d}")
        print(f"    | Tempo D: {tempo_dijkstra*1000:7.2f}ms | Percorreu: {nos_d:5d}")
        print(f"    | Tempo A*: {tempo_a_star*1000:7.2f}ms | Percorreu: {nos_a_star:5d}")
        print("\n")
    
    plt.figure(figsize=(10, 6))
    
    # Esse bloco é da linha do grafico dos algoritmos
    plt.plot(tamanhos_nos_dij, tempos_dij, 'o-', label='Dijkstra', color='darkorange')
    plt.plot(tamanhos_nos_a, tempos_a, 's-', label='A*', color='dodgerblue')

    # Esse bloco faz a curva teórica do BigO n log n do dijkstra, pois tem muita váriaveis tipo
    # a máquoinma usada e etc. Para manter consistente precisa ser feita toda vez.
    maior_n = tamanhos_nos_dij[-1]
    maior_tempo_d = tempos_dij[-1]
    C = maior_tempo_d / (maior_n * np.log(maior_n + 1))
    n_lin = np.linspace(min(tamanhos_nos_dij), max(tamanhos_nos_dij), 100)
    teorico_n_log_n = C * n_lin * np.log(n_lin + 1)
    plt.plot(n_lin, teorico_n_log_n, '--', label=r'n log n', color='red', alpha=0.6)
    
    #
    #   Grafico e salva o arquivo
    #
    plt.title('Complexidade Big O')
    plt.xlabel('Quantidade de Nós)')
    plt.ylabel('Tempo de Execução ms')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
    PASTA_GRAFICOS = os.path.join(DIRETORIO_ATUAL, 'graph')
    if not os.path.exists(PASTA_GRAFICOS):
         os.makedirs(PASTA_GRAFICOS)
    CAMINHO_COMPLETO = os.path.join(PASTA_GRAFICOS, "comp_bigO_alagoas.png")
    
    plt.savefig(CAMINHO_COMPLETO)
    plt.show()
    plt.close()

def main():
    
    local_do_grafo = "Alagoas, Brazil"
    peso_do_grafo = 'travel_time' 
    
    while True:
        try:
            pass
            print("\nQual Teste Deseja Fazer?\n")
            print("[1] Comparação de tempo bruto\n[2] Comparação Big O (Tempo/Tamanho)\n[3] Grafo\n[4] Sair")
            escolha = int(input())
            
            if escolha == 1:
                print("Digite a latitude e longitude da origem e do destino")
                #Maragogi (Norte):  (-8.7504, -35.2289)
                #Penedo (Sul):      (-10.3015, -36.1416)
                #Arapiraca (Oeste): (-9.7344, -36.6577)
                #Maceió:            (-9.6653, -35.7337)
                
                x = float(input())
                y = float(input())
                xx = float(input())
                yy = float(input())
                
                origem_a_star = (x, y) 
                destino_a_star = (xx, yy)
                
                comparacao_bruta(local_do_grafo,peso_do_grafo,origem_a_star,destino_a_star)
                
            elif escolha == 2:
                locais_big_o = [
                ("São Miguel dos Milagres, Alagoas, Brazil", "Municipio"),
                ("Marechal Deodoro, Alagoas, Brazil", "Cidade Pequena"),
                ("Arapiraca, Alagoas, Brazil", "Cidade Média"),
                ("Maceió, Alagoas, Brazil", "Cidade Grande"),
                ("Alagoas, Brazil", "Enorme (Estado)")] 
                
                comparacao_big_o(locais_big_o,peso_do_grafo)
            
            elif escolha == 3:
                loc = input("Digite a cidade/estado que deseja ver o grafo: ")
                grafo_teste(loc = loc,peso = peso_do_grafo)
            
            else:
                break    
                
                
        except ValueError:
            print("Digite um número adequado.")

if __name__ == '__main__':
    main()