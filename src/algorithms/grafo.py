import osmnx as ox
import networkx as nx
import os
import matplotlib.pyplot as plt

def grafo_base(
    # Localização e peso que vai ser usado para medir rotas
    place_name="",
    weight_type=""
    ):
    
    # Para não demorar muito, ele tem sistema de baixar e reusar grafos, primeiro ele procura agora e depois
    # se não achar baixa para poder usar depois
    
    print(f"Procurando grafo para: {place_name}...")
    data_dir = "src/data" 
    filename_base = place_name.replace(", ", "_").replace(" ", "_") + ".graphml"
    filepath = os.path.join(data_dir, filename_base)
    
    if os.path.exists(filepath):
        try:
            print(f"Grafo encontrado no disco em ({filepath})...\n")
            G = ox.load_graphml(filepath)
            G = ox.add_edge_speeds(G)
            G = ox.add_edge_travel_times(G)
            return G, weight_type
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}. Baixando novamente.")
            # Se falhar ao carregar, continua para baixar
            pass 
    
    # Aqui que acontece a mágica, se ele não achar no if, ele baixa o grafo
    print(f"Grafo não encontrado. Baixando e processando para: {place_name}...\n")
    
    G = ox.graph_from_place(place_name, network_type="drive")

    # Muitos lugares baixam sem velocidade médias definidas, então precisa desse fallback
    velocidades_medias = {
        'residential': 30, 'secondary': 40, 'tertiary': 50,
        'primary': 60, 'motorway': 80, 'trunk': 80
    }
    # Adiciona as velocidades
    G = ox.add_edge_speeds(G, hwy_speeds=velocidades_medias)
    
    # Calcula o tempo de viagem
    G = ox.add_edge_travel_times(G)
    
    # Verifica se o github baixou a pasta corretamente, frequentemente ele n cria
    if not os.path.exists(data_dir):
        # A flag 'exist_ok=True' evita erro caso a pasta já exista
        os.makedirs(data_dir, exist_ok=True)
    
    print(f"Grafo baixado e processado. Salvando em {filepath}...")
    ox.save_graphml(G, filepath=filepath)
    
    return G, weight_type

def grafo_mapear(G, coords_origem, coords_destino):
    # Aqui seta a origem e o destino para fazer o grafo com base nisso
    node_origem = ox.nearest_nodes(G, X=coords_origem[1], Y=coords_origem[0])
    node_destino = ox.nearest_nodes(G, X=coords_destino[1], Y=coords_destino[0])
    return node_origem, node_destino

def main():
    loc = "Aracaju, Sergipe, Brasil"
    peso = "travel_time"

    print(f"Tentando obter o grafo para: {loc}")
    grafo, z = grafo_base(place_name=loc, weight_type=peso)

    if grafo:
        print(f"Número de Interseções: {grafo.number_of_nodes()}")
        print(f"Número de Ruas: {grafo.number_of_edges()}")
        
        fig, ax = ox.plot_graph(
        grafo,
        filepath=None,
        node_size=0,
        edge_color="gray",
        bgcolor="w",
        save=False,
        show=False,
        close=False)
        plt.show()
        
    else:
        print("FALHA: O local provavelmente foi colocado incorretamente.")



if __name__ == '__main__':
    main()  