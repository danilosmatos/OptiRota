# Importação dp proprio repo
from algorithms.grafo import grafo_base
from algorithms.a_star import plotagem_a_star 
from algorithms.cvrptw import plotagem_cvrptw

#------------------
# dados fixossssss
#------------------
a_star_alagoas_coordenadas = {
    'Maragogi (Norte)': (-8.7504, -35.2289), 
    'Penedo (Sul)': (-10.3015, -36.1416),
    'Arapiraca (Oeste)': (-9.7344, -36.6577),
    'Maceió': (-9.6653, -35.7337)
}

cvrptw_maceio_coordenadas = [
    (-9.6653, -35.7337), # Depósito (Praça Sete Coqueiros)
    (-9.6645, -35.7380), # Cliente 1 (Praia de Pajuçara)
    (-9.6580, -35.7190), # Cliente 2 (Jatiúca)
    (-9.6450, -35.7050), # Cliente 3 (Maceió Shopping)
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

def menu_a_star(predefinidos, nome_ponto):
    opcoes = list(predefinidos.keys())
    op = len(opcoes)
    print(f"\n--- Selecione o {nome_ponto} ---")
    n = 0
    for i, nome in enumerate(opcoes):
        n +=1
        print(f"[{n}] {nome}")
    print(f"[{n+1}] Customizavel")
    
    
    while True:
        
        try:
            num = int(input(f"Digite o número para o {nome_ponto}: "))
            if 0 <= num < op:
                num_escolhido = opcoes[num-1]
                print(f"-> Selecionado: {num_escolhido}\n")
                return predefinidos[num_escolhido]
            
            elif num == op+1:
                customizavel1 = float(input("\nEscreva as coordenadas desejadas: "))
                customizavel2 = float(input("Escreva as coordenadas desejadas: "))
                customizavel = (customizavel1,customizavel2)
                return customizavel
        
            else:
                print("Opção inválida. Tente novamente.")
        
        except ValueError:
            print("Entrada inválida. Digite apenas o número.")

def config_cvrptw(coordenadas_fixas, parametros_fixos):
    """
    Coleta todos os parâmetros do CVRP-TW de forma interativa, 
    permitindo ao usuário definir número de pontos, demandas, janelas 
    de tempo e configurações de veículo.
    """
    
    print("\n" + "=" * 50)
    print("      CONFIGURAÇÃO DETALHADA DO CVRP-TW")
    print("=" * 50)

    # 1. Opção de usar dados fixos ou customizar
    while True:
        escolha_modo = input("\nUsar (F)ixos de Maceió ou (C)ustomizar totalmente? (F/C): ").lower()
        if escolha_modo == 'f':
            print("-> Usando dados fixos de Maceió.")
            return parametros_fixos, coordenadas_fixas
        elif escolha_modo == 'c':
            break
        else:
            print("Opção inválida. Digite 'F' ou 'C'.")


    # 2. Número de Pontos
    while True:
        try:
            num_pontos = int(input("\nTotal de pontos (Depósito + Clientes): "))
            if num_pontos < 2:
                print("O CVRP-TW deve ter pelo menos 2 pontos (Depósito + 1 Cliente).")
            else:
                break
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
            
    # 3. Coordenadas
    coordenadas = []
    print("\n--- Inserindo Coordenadas (Latitude, Longitude) ---")
    for i in range(num_pontos):
        nome = "Depósito (Ponto 0)" if i == 0 else f"Cliente {i}"
        while True:
            try:
                lat = float(input(f"  {nome} - Latitude: "))
                lon = float(input(f"  {nome} - Longitude: "))
                coordenadas.append((lat, lon))
                break
            except ValueError:
                print("Coordenada inválida. Digite um número real.")

    # 4. Demandas
    demands = [0] * num_pontos 
    print("\n--- Inserindo Demandas (Carga) ---")
    print(f"  Depósito (Ponto 0): Demanda fixada em 0.")
    for i in range(1, num_pontos):
        while True:
            try:
                demanda = int(input(f"  Demanda do Cliente {i}: "))
                if demanda < 0:
                    print("Demanda deve ser não-negativa.")
                else:
                    demands[i] = demanda
                    break
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")

    # 5. Janelas de Tempo (Time Windows)
    time_windows = []
    print("\n--- Inserindo Janelas de Tempo (Início, Fim) ---")
    # Para o depósito, a janela de tempo inicial deve ser muito ampla
    print(f"  Depósito (Ponto 0): Sugestão (0, 5000)")
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
                print("Entrada inválida. Digite um número inteiro.")

    # 6. Parâmetros do Veículo
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
            print("Entrada inválida. Digite um número inteiro.")

    # 7. Montar o Dicionário de Parâmetros
    parametros = {
        'nomes_clientes': [f'Ponto {i}' for i in range(num_pontos)],
        'demands': demands,
        'time_windows': time_windows,
        'vehicle_capacities': [capacidade] * num_veiculos,
        'num_vehicles': num_veiculos,
        'depot': 0
    }
    
    print("\nConfiguração CVRP-TW customizada finalizada.")
    return parametros, coordenadas 

def menu_cvrptw(parametros_fixos, coordenadas_fixas):
    print("\n" + "=" * 40)
    print("  CONFIGURAÇÃO DO CVRP-TW")
    print("=" * 40)

    # 1. Coletar Capacidade e Número de Veículos
    while True:
        try:
            # Note a inclusão de int() para garantir que a entrada é tratada como número.
            # Se o usuário apertar Enter sem nada, pode dar ValueError.
            capacidade_str = input(f"Capacidade do Veículo (atual: {parametros_fixos['vehicle_capacities'][0]}): ")
            num_veiculos_str = input(f"Número de Veículos (atual: {parametros_fixos['num_vehicles']}): ")
            
            # Tenta converter
            capacidade = int(capacidade_str)
            num_veiculos = int(num_veiculos_str)
            
            if capacidade > 0 and num_veiculos > 0:
                break
            else:
                print("Capacidade e número de veículos devem ser maiores que zero.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    # Criar a nova lista de capacidades baseada no número de veículos
    nova_capacidade = [capacidade] * num_veiculos
    
    # 2. Pergunta sobre as coordenadas
    novas_coordenadas = coordenadas_fixas # Define um valor padrão seguro
    while True:
        escolha_coord = input("\nUsar as Coordenadas de Maceió fixas (y/n)? ").lower()
        if escolha_coord in ['y', 's']:
            novas_coordenadas = coordenadas_fixas
            print(f"-> Coordenadas fixas de {len(coordenadas_fixas)} pontos selecionadas.")
            break
        elif escolha_coord in ['n']:
            print("Você precisará editar o código ou implementar uma função de inserção de coordenadas para customizar.")
            print("Usando as coordenadas fixas como fallback para manter a execução.")
            novas_coordenadas = coordenadas_fixas
            break
        else:
            print("Opção inválida. Digite 'y' ou 'n'.")

    # 3. Retorna o novo dicionário de parâmetros
    novos_parametros = parametros_fixos.copy()
    novos_parametros['vehicle_capacities'] = nova_capacidade
    novos_parametros['num_vehicles'] = num_veiculos
    
    print("\n-> CVRP-TW configurado com sucesso!")
    print(f"   Capacidade: {capacidade}, Veículos: {num_veiculos}, Pontos: {len(novas_coordenadas)}")
    
    # GARANTIA DE RETORNO NO FINAL DA FUNÇÃO
    return novos_parametros, novas_coordenadas
def main():
    
    print("=" * 60)
    print(" "*10 + "ROTAS ALAGOAS (e cvrptw de maceió)")
    print("=" * 60)
    
    grafo_alagoas = "Alagoas, Brazil"
    peso_do_grafo = 'travel_time' 
    
    origem_a_star = menu_a_star(a_star_alagoas_coordenadas, "Origem (A*)")
    destino_a_star = menu_a_star(a_star_alagoas_coordenadas, "Destino (A*)")
    
    grafo_alagoas, weight_type = grafo_base(place_name=grafo_alagoas, weight_type=peso_do_grafo)

    plotagem_a_star(
        grafo_alagoas, 
        weight_type, 
        origem_a_star, 
        destino_a_star, 
        grafo_alagoas
    )
    
    local_grafo_maceio = "Maceió, Alagoas, Brazil"
    
    cvrptw_parametros_interativos, cvrptw_coordenadas_interativas = menu_cvrptw(
        cvrptw_maceio_parametros, 
        cvrptw_maceio_coordenadas
    )
    
    grafo_maceio, xzxzxzxzxz = grafo_base(place_name=local_grafo_maceio, weight_type=peso_do_grafo)

    

    plotagem_cvrptw(
        grafo_maceio, 
        cvrptw_parametros_interativos, 
        cvrptw_coordenadas_interativas
    )

if __name__ == '__main__':
    main()