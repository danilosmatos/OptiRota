# cvrptw.py

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class CVRPTWSolver:
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