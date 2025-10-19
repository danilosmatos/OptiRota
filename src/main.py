# Importação dp proprio repo
from algorithms.grafo import grafo_base, grafo_teste
from algorithms.a_star import plotagem_a_star 
from algorithms.cvrptw import plotagem_cvrptw

#------------------
# dados predefinidos para caso não queira digitar 20 inputs
#------------------
a_star_coords_pred = {
    'Maragogi (Norte)': (-8.7504, -35.2289), 
    'Penedo (Sul)': (-10.3015, -36.1416),
    'Arapiraca (Oeste)': (-9.7344, -36.6577),
    'Maceió': (-9.6653, -35.7337)
}

cvrptw_coords_pred = [
    (-9.6653, -35.7337), # Depósito (Praça Sete Coqueiros)
    (-9.6645, -35.7380), # Cliente 1 (Praia de Pajuçara)
    (-9.6580, -35.7190), # Cliente 2 (Jatiúca)
    (-9.6450, -35.7050), # Cliente 3 (Maceió Shopping)
]

cvrptw_param_pred = {
    'nomes_clientes': ['Depósito', 'Cliente 1', 'Cliente 2', 'Cliente 3'],
    'demands': [0, 1, 2, 1],
    'time_windows': [
        (0, 5000), (100, 300), (400, 600), (700, 900),
    ],
    'vehicle_capacities': [4, 4],
    'num_vehicles': 2,
    'depot': 0
}

def config_a_star(dicionario_coords, sentido):
    opcoes = list(dicionario_coords.keys())
    op = len(opcoes)
    print(f"\n--- Selecione o {sentido} ---")
    n = 0
    for i, nome in enumerate(opcoes):
        n +=1
        print(f"[{n}] {nome}")
    print(f"[{n+1}] Customizavel")
    
    while True:
        
        try:
            num = int(input(f"Digite o número para o {sentido}: "))
            if 1 <= num <= op:
                num_escolhido = opcoes[num-1]
                print(f"-> Selecionado: {num_escolhido}\n")
                return dicionario_coords[num_escolhido]
            
            elif num == op+1:
                customizavel1 = float(input("\nEscreva as coordenadas desejadas: "))
                customizavel2 = float(input("Escreva as coordenadas desejadas: "))
                customizavel = (customizavel1,customizavel2)
                return customizavel
        
            else:
                print("Opção inválida. Tente novamente.")
        
        except ValueError:
            print("Entrada inválida. Digite apenas o número.")

def config_cvrptw(parametros, coordenadas):
    
    print("\n" + "=" * 50)
    print("      CONFIGURAÇÃO DO CVRP")
    print("=" * 50)

    #   Escolha Inicial
    while True:
        escolha_modo = input("\nUsar dados fixos de maceió ou customizar eles? (C/F)").lower()
        if escolha_modo == 'f':
            print("Usando dados fixos de Maceió.")
            return parametros, coordenadas
        elif escolha_modo == 'c':
            break
        else:
            print("Opção inválida.")

    #   Número de Pontos
    while True:
        try:
            num_pontos = int(input("\nTotal de pontos (Depósito + Clientes): "))
            if num_pontos < 2:
                print("O CVRP deve ter pelo menos 2 pontos (Deposito + Cliente).")
            else:
                break
        except ValueError:
            print("Entrada inválida. Digite um número adequado.") #ou morra
            
    #   Coordenadas
    coordenadas = []
    print("\nInserindo Coordenadas (Latitude, Longitude)")
    for i in range(num_pontos):
        nome = "Depósito (Ponto 0)" if i == 0 else f"Cliente {i}"
        while True:
            try:
                lat = float(input(f"  {nome} - Latitude: "))
                lon = float(input(f"  {nome} - Longitude: "))
                coordenadas.append((lat, lon))
                break
            except ValueError:
                print("Entrada inválida. Digite um número adequado.") 

    #   Demandas
    print("\nInserindo Demandas (Carga)")
    demandas = [0]
    for i in range(1, num_pontos):
        while True:
            try:
                dem = int(input(f"  Demanda do Cliente {i}: "))
                if dem < 0:
                    print("Demanda não pode ser negativa.")
                else:
                    demandas.append(dem)
                    break
            except ValueError:
                print("Entrada inválida. Digite um número adequado.")

    #   Janelas de Tempo (Time Windows)
    time_windows = []
    print("\nInserindo Janelas de Tempo")
    
    print(f"  Depósito (Ponto 0): Sugestão (Entre 0 e 5000)")
    for i in range(num_pontos):
        nome = "Depósito (Ponto 0)" if i == 0 else f"Cliente {i}"
        while True:
            try:
                start = int(input(f"  {nome} - Início da Janela (s): "))
                end = int(input(f"  {nome} - Fim da Janela (s): "))
                if start >= end or start < 0:
                    print("O Início deve ser menor que o Fim e não-negativo.")
                else:
                    time_windows.append((start, end))
                    break
            except ValueError:
                print("Entrada inválida. Digite um número adequado.")

    #   Veículos
    print("\n--- Configuração de Veículos ---")
    while True:
        try:
            capacidade = int(input("Capacidade de Carga de Cada Veículo: "))
            num_veiculos = int(input("Número de Veículos Disponíveis: "))
            if capacidade <= 0 or num_veiculos <= 0:
                print("Capacidade e número de veículos devem ser positivos.")
            else:
                break
        except ValueError:
            print("Entrada inválida. Digite um número adequado.")

    #   Dicionario
    parametros = {
        'nomes_clientes': [f'Ponto {i}' for i in range(num_pontos)],
        'demands': demandas,
        'time_windows': time_windows,
        'vehicle_capacities': [capacidade] * num_veiculos,
        'num_vehicles': num_veiculos,
        'depot': 0
    }
    
    print("\nConfiguração CVRPTW finalizada.")
    return parametros, coordenadas 

def main():
    
    while True:
        try:
            print("\n"+"="*20+   " Bem vindo ao protótipo Optirota "+"="*20)
            print("\nEscolha o que deseja fazer:")
            print("[1] A*\n[2] CVRPTW\n[3] Grafos\n[4] Sair")
            
            local_grafo_cvrptw = "Maceió, Alagoas, Brazil"
            local_grafo_a_star = "Alagoas, Brazil"
            peso_do_grafo = 'travel_time' 
        
            escolha = int(input(""))
            print("")
            
            if escolha == 1:
                print("=" * 60)
                print(" "*10 + "ROTAS ALAGOAS (e cvrptw de maceió)")
                print("=" * 60)
                
                origem_a_star = config_a_star(a_star_coords_pred, "Origem (A*)")
                destino_a_star = config_a_star(a_star_coords_pred, "Destino (A*)")
                
                local_grafo_a_star, weight_type = grafo_base(place_name=local_grafo_a_star, weight_type=peso_do_grafo)
                
                plotagem_a_star(local_grafo_a_star, weight_type, origem_a_star, destino_a_star, local_grafo_a_star )
                
            elif escolha == 2:
                
                while True:
                    try:
                        cvrptw_parametros, cvrptw_coordenadas = config_cvrptw(cvrptw_param_pred, cvrptw_coords_pred)
                        
                        print("\nCriando Grafo base para cálculo de matriz de distâncias...")
                        grafo_cvrptw, _ = grafo_base(place_name=local_grafo_cvrptw, weight_type=peso_do_grafo)

                        print("\nTentando Resolver...\n")
                        plotagem_cvrptw(grafo_cvrptw, cvrptw_parametros, cvrptw_coordenadas)
                        print("\nCVRPTW resolvido com sucesso.\n")
                        break

                    except Exception as e:
                        # Na real, o maior causador de erros na minha parte foram coords erradas colocados por mim mesmo
                        # certifique se que você ta usando lat/long e que estão firmamente em maceió, pois o cvrptw laga
                        # bastante quando pede distâncias maiores então melhor prototipar só por aqui mesmo
                        print(f"\nERRO: {e}")
                        print("\nNão foi possível encontrar uma solução válida. ")
                        print("Por favor, tente novamente com novos parâmetros.")
                        
            elif escolha == 3:
                loc = input("\nDigite a cidade/estado que deseja ver o grafo: ")
                grafo_teste(loc = loc,peso = peso_do_grafo)
            else:
                print("Obrigado por testar!")
                print("Desenvolvido por Antônio Gabriel, Danilo Soares, Eudes Oliveira, Vinicius Augusto\n")
                break
        except ValueError:
            print("\nERRO: Digite um número adequado")

if __name__ == '__main__':
    main()