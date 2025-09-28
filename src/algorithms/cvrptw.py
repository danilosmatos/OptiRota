from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import osmnx as ox
import matplotlib.pyplot as plt

# A* e Grafo devem ser importados para gerar a matriz de tempos
# Assumindo que a_star.py e grafo.py estão acessíveis
from .a_star import Grafo_A_Star_Base, a_star_opi 

class CVRPTWSolver:
    # ... (O restante da classe CVRPTWSolver permanece inalterado) ...
    def __init__(self, nomes_clientes, time_matrix, time_windows, demands, vehicle_capacities, num_vehicles, depot=0):
        self.data = {
            'nomes_clientes': nomes_clientes,
            'time_matrix': time_matrix,
            'time_windows': time_windows,
            'demands': demands,
            'vehicle_capacities': vehicle_capacities,
            'num_vehicles': num_vehicles,
            'depot': depot
        }
        self.manager = None
        self.routing = None
        self.solution = None

    def _create_callbacks(self):
        def time_callback(from_index, to_index):
            from_node = self.manager.IndexToNode(from_index)
            to_node = self.manager.IndexToNode(to_index)
            return self.data['time_matrix'][from_node][to_node]

        def demand_callback(from_index):
            from_node = self.manager.IndexToNode(from_index)
            return self.data['demands'][from_node]

        return time_callback, demand_callback

    def setup_model(self):
        self.manager = pywrapcp.RoutingIndexManager(
            len(self.data['time_matrix']), self.data['num_vehicles'], self.data['depot']
        )
        self.routing = pywrapcp.RoutingModel(self.manager)

        time_callback, demand_callback = self._create_callbacks()
        transit_callback_index = self.routing.RegisterTransitCallback(time_callback)
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        demand_callback_index = self.routing.RegisterUnaryTransitCallback(demand_callback)
        self.routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0, # sem folga para a capacidade
            self.data['vehicle_capacities'],
            True, # começa do zero
            'Capacity',
        )

        # Adiciona a restrição de janelas de tempo, com folga maior para encontrar solução
        self.routing.AddDimension(
            transit_callback_index,
            3000, # folga máxima
            3000, # tempo máximo por rota
            False, # não zera a cada início de rota
            'Time',
        )
        time_dimension = self.routing.GetDimensionOrDie('Time')

        # Adiciona as janelas de tempo aos nós
        for location_idx, time_window in enumerate(self.data['time_windows']):
            if location_idx == self.data['depot']:
                continue
            index = self.manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    def solve(self):
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        self.solution = self.routing.SolveWithParameters(search_parameters)
        return self.solution

    def save_solution(self):
        if not self.solution:
            return []

        solucoes = []
        time_dimension = self.routing.GetDimensionOrDie('Time')

        for vehicle_id in range(self.data['num_vehicles']):
            rota_atual = []
            index = self.routing.Start(vehicle_id)
            route_load = 0

            while not self.routing.IsEnd(index):
                node_index = self.manager.IndexToNode(index)
                time_var = time_dimension.CumulVar(index)
                route_load += self.data['demands'][node_index]

                ponto_parada = {
                    'node_id': node_index,
                    'cliente': self.data['nomes_clientes'][node_index],
                    'arrive_time': self.solution.Min(time_var),
                    'depart_time': self.solution.Max(time_var),
                    'load': route_load
                }
                rota_atual.append(ponto_parada)
                index = self.solution.Value(self.routing.NextVar(index))

            # Adicionar o depósito final (End)
            node_index = self.manager.IndexToNode(index)
            time_var = time_dimension.CumulVar(index)
            ponto_parada = {
                'node_id': node_index,
                'cliente': self.data['nomes_clientes'][node_index],
                'arrive_time': self.solution.Min(time_var),
                'depart_time': self.solution.Max(time_var),
                'load': route_load
            }
            rota_atual.append(ponto_parada)
            solucoes.append({'vehicle_id': vehicle_id, 'rota': rota_atual})

        return solucoes

    def print_saved_solution(self, saved_solutions):
        if saved_solutions:
            for solucao_veiculo in saved_solutions:
                print(f"--- Rota do Veículo {solucao_veiculo['vehicle_id'] + 1} ---")
                for ponto in solucao_veiculo['rota']:
                    print(f"Nó: {ponto['node_id']} | Cliente: {ponto['cliente']} | Chegada: {ponto['arrive_time']}s | Partida: {ponto['depart_time']}s | Carga: {ponto['load']}")
                print("-" * 30)
        else:
            print('Nenhuma solução encontrada.')

def gerar_matriz_tempos(G, pontos_de_interesse):
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

def plotagem_cvrptw(grafo_rede, cvrptw_params, coordenadas_cvrptw):
    print("="*40)
    print(" "*10 + "SOLVER CVRPTW")
    print("="*40)
    
    # Desempacotamento dos parametros silvio santos
    nomes_clientes = cvrptw_params['nomes_clientes']
    demands = cvrptw_params['demands']
    time_windows = cvrptw_params['time_windows']
    vehicle_capacities = cvrptw_params['vehicle_capacities']
    num_vehicles = cvrptw_params['num_vehicles']
    depot = cvrptw_params['depot']
    
    # Gera a matriz de tempos, agr oq é? boa pergunta
    print("\nCalculando a matriz de tempos de viagem com A*...")
    time_matrix = gerar_matriz_tempos(grafo_rede, coordenadas_cvrptw)
    print("Matriz de tempos gerada:")
    for row in time_matrix:
        print(row)
    
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
    
    if not solution:
        print("Nenhuma solução foi encontrada. Verifique as restrições (capacidades, janelas de tempo).")
        return

    print("Solução encontrada:")
    solucoes_salvas = solver.save_solution()
    solver.print_saved_solution(solucoes_salvas)

    print("\nDesenhando as rotas do CVRPTW em Maceió...")

    cores_veiculos = plt.cm.get_cmap('hsv', len(solucoes_salvas))
    
    # Nós mais próximos dos pontos de interesse, inverso do resto do programa por alguma razão satanica
    nodes_map = [ox.nearest_nodes(grafo_rede, X=lon, Y=lat) for lat, lon in coordenadas_cvrptw]

    fig, ax = ox.plot_graph(grafo_rede, show=False, close=False, node_size=0, edge_color='gray', bgcolor='w')

    for i, solucao_veiculo in enumerate(solucoes_salvas):
        rota_nodes_cliente_id = []
        
        for ponto in solucao_veiculo['rota']:
            if not rota_nodes_cliente_id or rota_nodes_cliente_id[-1] != ponto['node_id']:
                 rota_nodes_cliente_id.append(ponto['node_id'])
        
        nodes_do_caminho_osmnx = [nodes_map[idx] for idx in rota_nodes_cliente_id]

        if len(nodes_do_caminho_osmnx) > 1:
            try:
                caminho_completo = []
                
                for j in range(len(nodes_do_caminho_osmnx) - 1):
                    origem = nodes_do_caminho_osmnx[j]
                    destino = nodes_do_caminho_osmnx[j+1]
                    
                    caminho_segmento = ox.shortest_path(grafo_rede, origem, destino, weight='travel_time')
                    
                    if caminho_segmento:
                        caminho_completo.extend(caminho_segmento[:-1]) 
                
                caminho_completo.append(nodes_do_caminho_osmnx[-1]) # Adiciona o nó final (destino do último segmento)
                
                if caminho_completo:
                    ox.plot_graph_route(
                         grafo_rede, caminho_completo, route_color=cores_veiculos(i), route_linewidth=4, route_alpha=0.7, 
                         ax=ax, route_zorder=5, show=False, close=False, node_size=0
                    )
                
            except Exception as e:
                print(f"Não foi possível plotar a rota para o veículo {i+1}: {e}")

    lats = [coord[0] for coord in coordenadas_cvrptw]
    lons = [coord[1] for coord in coordenadas_cvrptw]
    
    ax.scatter(lons[0], lats[0], c='green', s=100, label='Depósito (D)', zorder=6) 
    ax.scatter(lons[1:], lats[1:], c='blue', s=80, label='Clientes', zorder=6) 
    
    for idx, (lat, lon) in enumerate(zip(lats, lons)):
        anotacao = f"D" if idx == 0 else f"{idx}"

        ax.annotate(
            anotacao, (lon, lat), xytext=(10, 10),textcoords="offset points", 
            color='black', fontsize=12, fontweight='bold', 
            bbox=dict(facecolor='yellow', alpha=0.6, edgecolor='none', pad=2), 
            zorder=7
        )

    plt.title('Rotas CVRPTW')
    plt.legend()
    plt.show()