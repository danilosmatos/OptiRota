# Importações avulsas
import osmnx as ox
import matplotlib.pyplot as plt
import time
# Importações do próprio projeto, todos tem que vir do algorithms
from algorithms.grafo import grafo_base, grafo_mapear
from algorithms.dijkstra import Grafo_Dij_Base, dij_Opi 
from algorithms.a_star import Grafo_A_Star_Base, a_star_opi, reconstruir_caminho
from algorithms.cvrptw import executar_cvrptw

# Dijkstra e A* armazenam só o nó pai, ao invés de armazenar uma lista inteira de nós do caminho inteiro 
# que fizeram, assim economiza memória e deixa facil de atualizar (substituir o pai) e n precisa iterar 
# uma lista inteira

def main():

    # Construção do grafo, é sensível à acentuação e precisa ser capitalizado. OBS: aracaju é em sergipe
    # peso_do_grafo pode ser travel_time e lenght, mas se usar distância provavelmente vai dar erro no cvrptw
    local_do_grafo = "Alagoas, Brazil"
    peso_do_grafo = 'travel_time' 
    
    #Maragogi: -8.7504, -35.2289
    #Penedo: -10.3015, -36.1416
    origem_a_star = (-8.7504, -35.2289) 
    destino_a_star = (-10.3015, -36.1416)
    
    # Configura as cordenadas do cvrptw, cuidado para não usar latitude e longitude fora de maceió, 
    # isso aqui consome bastante e pode causar erro se for muito calculo
    coordenadas_cvrptw = [
        (-9.6653, -35.7337),# Depósito (Praça Sete Coqueiros)
        (-9.6645, -35.7380),# Cliente 1 (Praia de Pajuçara)
        (-9.6580, -35.7190),# Cliente 2 (Jatiúca)
        (-9.6450, -35.7050),# Cliente 3 (Maceió Shopping)
    ]
    
    # Parametros do cvrptw mais gerais, numero de veiculos, capacidades e etc. 
    cvrptw_params = {
        'nomes_clientes': ['Depósito', 'Cliente 1', 'Cliente 2', 'Cliente 3'],
        'demands': [0, 1, 2, 1],
        'time_windows': [
            (0, 5000),
            (100, 300), 
            (400, 600),
            (700, 900),
        ],
        'vehicle_capacities': [4, 4],
        'num_vehicles': 2,
        'depot': 0
    }
    
    # Execução do setup para fazer o A* e o gráfico correspondente,
    print("\n" + "― "*32)
    print(" "*20 + "EXECUÇÃO E GRÁFICO A*")
    print("― "*32 + "\n")
    print(f"Local do Grafo: {local_do_grafo}")
    print(f"Origem: {origem_a_star}")
    print(f"Destino: {destino_a_star}")

    # Usa do grafo.py para retornar o grafo
    grafo, weight_type = grafo_base(place_name=local_do_grafo, weight_type=peso_do_grafo)
    if not grafo:
        print("Erro: Grafo não pôde ser carregado.")
        return

    origem_node, destino_node = grafo_mapear(grafo, origem_a_star, destino_a_star)
    
    if origem_node is None or destino_node is None:
        print("Erro: Nós de origem ou destino não encontrados no grafo.")
        return
    
    # Execução do A*
    G_astar = Grafo_A_Star_Base(grafo, weight_type=weight_type)

    print("\nExecutando A*")
    tempo_inicio_astar = time.time()
    distancias_a, pais_a, nos_a = a_star_opi(G_astar, origem_node, destino_node)
    tempo_fim_astar = time.time()
    
    path_a_star = reconstruir_caminho(pais_a, destino_node, origem_node)
    tempo_total_astar = tempo_fim_astar - tempo_inicio_astar

    print("Executando Dijkstra")
    tempo_inicio_dijkstra = time.time()
    G_dijkstra = Grafo_Dij_Base(grafo, weight_type=weight_type) 
    distancias_d, pais_d, nos_d = dij_Opi(G_dijkstra, origem_node)
    tempo_fim_dijkstra = time.time()
    path_dijkstra = reconstruir_caminho(pais_d, destino_node, origem_node)
    tempo_total_dijkstra = tempo_fim_dijkstra - tempo_inicio_dijkstra

    
    if path_a_star:
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
        
        print("\nDesenhando a rota A* de ponta a ponta do estado...")
        fig, ax = ox.plot_graph_route(
            grafo, path_a_star, route_color='r', route_linewidth=3, route_alpha=1.0, 
            node_size=1, bgcolor='w', 
            show=False, close=False
        )
        
        plt.title(f"Rota A* em {local_do_grafo}")
        plt.show()    
        
    else:
        print("Caminho A* não encontrado. Verifique as coordenadas.")
        print("\n"+"― "*30+"\n")
    
    executar_cvrptw(grafo, cvrptw_params, coordenadas_cvrptw)
    
if __name__ == '__main__':
    main()