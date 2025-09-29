A funcionalidade central do sistema de otimização de rotas foi entregue. Estes itens representam as capacidades do produto no nível de usuário e integração:

- [x] Modelagem de Mapa Urbano: O sistema utiliza dados reais do OpenStreetMap (via osmnx) para construir o grafo de ruas, garantindo que a base geográfica seja precisa e atualizada.

- [x] Cálculo de Custo Otimizado: O custo de cada rota é calculado com base no tempo de viagem (travel_time), o que é fundamental para encontrar as rotas mais rápidas na prática, e não apenas as mais curtas em distância.

- [x] Busca de Rota A* (Uniponto): Implementação funcional do algoritmo A-Estrela (a_star.py), que encontra a rota mais eficiente entre uma origem e um destino específico, utilizando a heurística para acelerar a busca.

- [x] Roteamento com Janelas de Tempo (VRPTW): A lógica de roteamento agora respeita os horários agendados. O motor garante que as entregas a clientes específicos sejam atendidas dentro das suas janelas de tempo pré-determinadas.

- [x] Integração do A* para Matriz de Tempo: Seu algoritmo A* é usado internamente para calcular a matriz de tempo de viagem exata (custo de rota) entre todos os clientes e o depósito. Isso garante que o motor de roteamento VRP utilize dados de custo de rota altamente precisos e realistas.

Time
    Product Owner (PO): Natalie

    Project Manager (PM): Danilo

    Desenvolvedores: Antônio (Dijkstra), Danilo (Geral), Eudes (A*)

    Engenheiro de QA: Samuel



