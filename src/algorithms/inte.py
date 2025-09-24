# integracao_vrp.py

import osmnx as ox
import sys
import os

# Adicione o diretório pai ao path para encontrar os módulos
# Esta linha pode ser ajustada dependendo da sua estrutura de diretórios
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importe as funções e classes dos arquivos separados
from grafo import grafo_base, grafo_mapear
from a_star import Grafo_A_Star_Base, a_star_opi
from cvrptw import CVRPTWSolver

def gerar_matriz_tempos(G, pontos_de_interesse):
    """
    Calcula a matriz de tempos de viagem entre todos os pontos de interesse
    usando o algoritmo A*.
    """
    num_pontos = len(pontos_de_interesse)
    matriz_tempos = [[0] * num_pontos for _ in range(num_pontos)]
    
    # Mapear coordenadas para os nós mais próximos no grafo
    nodes_map = [ox.nearest_nodes(G, X=lon, Y=lat) for lat, lon in pontos_de_interesse]
    
    # Instancia a classe A* apenas uma vez para o grafo
    grafo_a_star = Grafo_A_Star_Base(G)
    
    for i in range(num_pontos):
        for j in range(num_pontos):
            if i == j:
                continue
                
            origem = nodes_map[i]
            destino = nodes_map[j]
            
            # Executa o A* e obtém o custo total (g_score)
            # A chamada da função a_star_opi agora está correta
            g_score, _, _ = a_star_opi(grafo_a_star, origem, destino)
            tempo_viagem = g_score.get(destino, float('inf'))
            
            if tempo_viagem == float('inf'):
                tempo_viagem = 99999  # Valor alto para rotas inacessíveis
            
            matriz_tempos[i][j] = int(tempo_viagem)
            
    return matriz_tempos

def main():
    """
    Função principal para executar o protótipo.
    """
    # 1. Dados de entrada: pontos de interesse, demandas e janelas de tempo
    pontos_de_interesse = [
        (-10.9161, -37.0716),  # Depósito
        (-10.9250, -37.0780),  # Cliente 1
        (-10.9300, -37.0850),  # Cliente 2
        (-10.9050, -37.0650),  # Cliente 3
    ]

    nomes_clientes = ['Depósito', 'Cliente 1', 'Cliente 2', 'Cliente 3']
    demands = [0, 1, 2, 1]
    
    # Janelas de tempo em segundos, compatíveis com o tempo de viagem do OSMnx
    time_windows = [
        (0, 5000),   
        (100, 300), 
        (400, 600),
        (700, 900),
    ]
    
    vehicle_capacities = [4, 4]
    num_vehicles = 2
    depot = 0

    # 2. Carregar o grafo da rede de ruas
    cidade = "Aracaju, Sergipe, Brasil"
    # Usa a função do seu arquivo grafo.py
    grafo_rede, peso = grafo_base(place_name=cidade, weight_type='travel_time')
    
    if not grafo_rede:
        print("Erro: Não foi possível carregar o grafo.")
        return

    # 3. Gerar a matriz de tempos de viagem
    print("\nCalculando a matriz de tempos de viagem com A*...")
    time_matrix = gerar_matriz_tempos(grafo_rede, pontos_de_interesse)
    print("Matriz de tempos gerada:")
    for row in time_matrix:
        print(row)
    
    # Verificação de consistência dos dados
    num_pontos = len(pontos_de_interesse)
    assert len(nomes_clientes) == num_pontos
    assert len(demands) == num_pontos
    assert len(time_windows) == num_pontos
    assert len(time_matrix) == num_pontos and all(len(row) == num_pontos for row in time_matrix)
    print("Verificação de consistência de dados: OK ✅")
        
    # 4. Resolver o problema CVRPTW
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
        print("Nenhuma solução foi encontrada. Verifique as restrições.")
        
if __name__ == '__main__':
    main()