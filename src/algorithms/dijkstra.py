import heapq

class Grafo_Dij_Base:
    def __init__(self, G_ox, weight_type='travel_time'):
        self.vizinhos = {}
        self.todos_os_nos = list(G_ox.nodes()) 
        for u, n, data in G_ox.edges(data=True):
            peso = data.get(weight_type, data.get('length', 1)) 
            
            if u not in self.vizinhos:
                self.vizinhos[u] = []
            if n not in self.vizinhos:
                self.vizinhos[n] = []
                
            # O OSMnx é um grafo direcional (MultiDiGraph), então só adicionamos u -> n
            self.vizinhos[u].append((n, peso))

def dij_Opi(grafo_dij, inicial): 
    pais = {n: None for n in grafo_dij.todos_os_nos}
    distancia = {n: float('inf') for n in grafo_dij.todos_os_nos}
    distancia[inicial] = 0

    filaPrioridade = []
    heapq.heappush(filaPrioridade, (0, inicial))
    
    #conta os nós para comparar com o bendito do A*
    contador_nos_dij = 0

    while filaPrioridade:
        distancia_removida, removido = heapq.heappop(filaPrioridade)

        if distancia_removida > distancia[removido]: 
            continue

        
        contador_nos_dij += 1
        
        for vizinho, peso in grafo_dij.vizinhos.get(removido, []): 
            novaDistancia = distancia_removida + peso
            
            if novaDistancia < distancia[vizinho]:
                distancia[vizinho] = novaDistancia
                pais[vizinho] = removido 
                heapq.heappush(filaPrioridade, (novaDistancia, vizinho))

    return distancia, pais, contador_nos_dij