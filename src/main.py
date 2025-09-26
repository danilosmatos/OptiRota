import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import time
import sys
import os

# Importe todos os módulos necessários de uma vez só
from algorithms.grafo import grafo_base, grafo_mapear
from algorithms.dijkstra import Grafo_Dij_Base, dij_Opi
from algorithms.a_star import Grafo_A_Star_Base, a_star_opi
from algorithms.cvrptw import CVRPTWSolver

def reconstruir_caminho(pais, destino, inicio):
    caminho = []
    atual = destino
    while atual is not None and atual != inicio:
        caminho.append(atual)
        atual = pais.get(atual)

    if atual == inicio:
        caminho.append(inicio)
        return caminho[::-1]
    return None

def gerar_matriz_tempos(G, pontos_de_interesse):
    """
    Calcula a matriz de tempos de viagem entre todos os pontos de interesse
    usando o algoritmo A*.
    """
    num_pontos = len(pontos_de_interesse)
    matriz_tempos = [[0] * num_pontos for _ in range(num_pontos)]
    
    nodes_map = [ox.nearest_nodes(G, X=lon, Y=lat) for lat, lon in pontos_de_interesse]
    
    grafo_a_star = Grafo_A_Star_Base(G)
    
    for i in range(num_pontos):
        for j in range(num_pontos):
            if i == j:
                continue
                
            origem = nodes_map[i]
            destino = nodes_map[j]
            
            g_score, _, _ = a_star_opi(grafo_a_star, origem, destino)
            tempo_viagem = g_score.get(destino, float('inf'))
            
            if tempo_viagem == float('inf'):
                tempo_viagem = 99999
            
            matriz_tempos[i][j] = int(tempo_viagem)
            
    return matriz_tempos

def executar_cvrptw(grafo_rede):
    """
    Função para resolver o problema CVRPTW.
    """
    print("\n" + "="*35)
    print("     SOLVER CVRPTW")
    print("="*35)
    
    # Coordenadas de exemplo em Maceió
    pontos_de_interesse = [
        (-9.6653, -35.7337),  # Depósito (Ex: Praça Sete Coqueiros)
        (-9.6645, -35.7380),  # Cliente 1 (Ex: Próximo à praia de Pajuçara)
        (-9.6580, -35.7190),  # Cliente 2 (Ex: Próximo ao bairro de Jatiúca)
        (-9.6450, -35.7050),  # Cliente 3 (Ex: Próximo ao Maceió Shopping)
    ]
    nomes_clientes = ['Depósito', 'Cliente 1', 'Cliente 2', 'Cliente 3']
    demands = [0, 1, 2, 1]
    time_windows = [
        (0, 5000),   
        (100, 300), 
        (400, 600),
        (700, 900),
    ]
    vehicle_capacities = [4, 4]
    num_vehicles = 2
    depot = 0
    
    print("\nCalculando a matriz de tempos de viagem com A*...")
    time_matrix = gerar_matriz_tempos(grafo_rede, pontos_de_interesse)
    print("Matriz de tempos gerada:")
    for row in time_matrix:
        print(row)
    
    print("\nIniciando o solver CVRPTW...")
    solver = CVRPTWSolver(
        nomes_clientes=nomes_clientes,
        time_matrix=time_matrix,
        time_windows=time_windows,
        demands=demands,
        vehicle_capacities=vehicle_capacities,
        num_vehicles=num_vehicles,
        depot=depot
    )
    
    solver.setup_model()
    solution = solver.solve()
    
    if solution:
        print("Solução encontrada:")
        solucoes_salvas = solver.save_solution()
        solver.print_saved_solution(solucoes_salvas)
    else:
        print("Nenhuma solução foi encontrada. Verifique as restrições (capacidades, janelas de tempo).")


def main():
    """
    Função principal que executa a comparação de algoritmos e o solver VRP.
    """
    # Adicione o diretório pai ao path para encontrar os módulos
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    print("\n"+"― "*30+"\n")
    print("     COMPARAÇÃO DIJKSTRA X A*")
    print("― "*30+"\n")

    # Altera o local para Alagoas, Brazil
    local = "Alagoas, Brazil"
    peso = 'travel_time' 
    # Coordenadas de origem e destino em Maceió (capital de AL)
    origem = (-9.6653, -35.7337)
    destino = (-9.6450, -35.7050)

    grafo, weight_type = grafo_base(place_name=local, weight_type=peso)
    if not grafo:
        print("Erro: Grafo não pôde ser carregado.")
        return

    origem_node, destino_node = grafo_mapear(grafo, origem, destino)
    
    if origem_node is None or destino_node is None:
        print("Erro: Nós de origem ou destino não encontrados no grafo.")
        return
    
    # Execução do Dijkstra
    G_dijkstra = Grafo_Dij_Base(grafo, weight_type=weight_type)
    
    print("\nExecutando Dijkstra...")
    tempo_inicio_dijkstra = time.time()
    distancias_d, pais_d, nos_d = dij_Opi(G_dijkstra, origem_node)
    tempo_fim_dijkstra = time.time()
    
    path_dijkstra = reconstruir_caminho(pais_d, destino_node, origem_node)
    tempo_total_dijkstra = tempo_fim_dijkstra - tempo_inicio_dijkstra

    # Execução do A*
    G_astar = Grafo_A_Star_Base(grafo, weight_type=weight_type)

    print("Executando A*...")
    tempo_inicio_astar = time.time()
    distancias_a, pais_a, nos_a = a_star_opi(G_astar, origem_node, destino_node)
    tempo_fim_astar = time.time()
    
    path_a_star = reconstruir_caminho(pais_a, destino_node, origem_node)
    tempo_total_astar = tempo_fim_astar - tempo_inicio_astar
    
    if path_dijkstra and path_a_star:
        print("\n" + "="*35)
        print("     COMPARAÇÃO DE DESEMPENHO")
        print("="*35)
        print("\n[Métricas]")
        print("-" * 60)
        print(f"{'Algoritmo':<10} | {'Tempo (ms)':>15} | {'Nós Explorados':>15}")
        print("-" * 60)
        print(f"{'Dijkstra':<10} | {tempo_total_dijkstra*1000:15.3f} | {nos_d:15}")
        print(f"{'A*':<10} | {tempo_total_astar*1000:15.3f} | {nos_a:15}")
        print("-" * 60)
        
        print("\nDesenhando a rota desejada...")
        print("\n"+"― "*30+"\n")
        fig, ax = ox.plot_graph_route(
            grafo, path_a_star,route_color='r', route_linewidth=3, route_alpha=1.0, 
            node_size=0, bgcolor='w', show=True, close=True
        )
    else:
        print("Caminho não encontrado. Verifique as coordenadas.")
        print("\n"+"― "*30+"\n")

    # Chama a nova função para executar o VRP
    executar_cvrptw(grafo)
    
if __name__ == '__main__':
    main()