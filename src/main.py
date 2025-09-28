# Importação dp proprio repo
from algorithms.grafo import grafo_base
from algorithms.a_star import executar_e_plotar_a_star 
from algorithms.cvrptw import executar_cvrptw

#------------------
# dados fixossssss
#------------------
astar_alagoas_coordenadas = {
    'Maragogi (Norte)': (-8.7504, -35.2289), 
    'Penedo (Sul)': (-10.3015, -36.1416),
    'Arapiraca (Oeste)': (-9.7344, -36.6577),
    'Maceió (Capital)': (-9.6653, -35.7337)
}

cvrptw_maceio_coordenadas = [
    (-9.6653, -35.7337), # Ponto 0: Depósito (Praça Sete Coqueiros)
    (-9.6645, -35.7380), # Ponto 1: Cliente 1 (Praia de Pajuçara)
    (-9.6580, -35.7190), # Ponto 2: Cliente 2 (Jatiúca)
    (-9.6450, -35.7050), # Ponto 3: Cliente 3 (Maceió Shopping)
]

cvrptw_maceio_parametros = {
    'nomes_clientes': ['Depósito', 'Cliente 1', 'Cliente 2', 'Cliente 3'],
    'demands': [0, 1, 2, 1],
    'time_windows': [
        (0, 5000), (100, 300), (400, 600), (700, 900),
    ],
    'vehicle_capacities': [4, 4],
    'num_vehicles': 2,
    'depot': 0
}

def selecionar_local_por_menu(predefinidos, nome_ponto):
    opcoes = list(predefinidos.keys())
    
    print(f"\n--- Selecione o {nome_ponto} ---")
    for i, nome in enumerate(opcoes):
        print(f"[{i + 1}] {nome}")
    
    while True:
        try:
            num = int(input(f"Digite o número para o {nome_ponto}: ")) - 1
            if 0 <= num < len(opcoes):
                num_escolhido = opcoes[num]
                print(f"-> Selecionado: {num_escolhido}\n")
                return predefinidos[num_escolhido]
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite apenas o número.")

def main():
    
    print("=" * 60)
    print(" "*10 + "ROTAS ALAGOAS (e cvrptw de maceió)")
    print("=" * 60)
    
    grafo_alagoas = "Alagoas, Brazil"
    peso_do_grafo = 'travel_time' 
    
    origem_a_star = selecionar_local_por_menu(astar_alagoas_coordenadas, "Ponto de Origem (A*)")
    destino_a_star = selecionar_local_por_menu(astar_alagoas_coordenadas, "Ponto de Destino (A*)")
    
    grafo_alagoas, weight_type = grafo_base(place_name=grafo_alagoas, weight_type=peso_do_grafo)

    executar_e_plotar_a_star(
        grafo_alagoas, 
        weight_type, 
        origem_a_star, 
        destino_a_star, 
        grafo_alagoas
    )
    
    local_grafo_maceio = "Maceió, Alagoas, Brazil"
    
    grafo_maceio, _ = grafo_base(place_name=local_grafo_maceio, weight_type=peso_do_grafo)

    executar_cvrptw(
        grafo_maceio, 
        cvrptw_maceio_parametros, 
        cvrptw_maceio_coordenadas
    )
    
    print("\nProcesso concluído.")

if __name__ == '__main__':
    main()