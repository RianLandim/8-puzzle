import heapq
import copy

def is_solvable(puzzle):
    """
    Verifica se o puzzle é solucionável.
    Conta o número de inversões; se for par, é solucionável.
    """
    inversion_count = 0
    puzzle = [tile for tile in puzzle if tile != 0]
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] > puzzle[j]:
                inversion_count += 1
    return inversion_count % 2 == 0

def manhattan_distance(state, goal):
    """
    Calcula a distância de Manhattan entre o estado atual e o objetivo.
    """
    distance = 0
    for num in range(1, 9):
        current_index = state.index(num)
        goal_index = goal.index(num)
        current_row, current_col = divmod(current_index, 3)
        goal_row, goal_col = divmod(goal_index, 3)
        distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def get_neighbors(state):
    """
    Gera todos os estados vizinhos a partir do estado atual.
    """
    neighbors = []
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)
    moves = []

    if row > 0: moves.append(-3)  # Up
    if row < 2: moves.append(3)   # Down
    if col > 0: moves.append(-1)  # Left
    if col < 2: moves.append(1)   # Right

    for move in moves:
        new_index = zero_index + move
        new_state = list(state)
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        neighbors.append(tuple(new_state))

    return neighbors

def reconstruct_path(came_from, current):
    """
    Reconstrói o caminho do estado inicial até o objetivo.
    """
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def solve_puzzle(start, goal):
    """
    Resolve o 8-puzzle utilizando o Algoritmo A*.
    Retorna a sequência de estados do início ao objetivo.
    """
    if not is_solvable(start):
        return None

    open_set = []
    heapq.heappush(open_set, (0 + manhattan_distance(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current):
            tentative_g_score = current_g + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + manhattan_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))

    return None

def print_puzzle(state):
    """
    Imprime o estado do puzzle de forma formatada.
    """
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

if __name__ == "__main__":
    # Definição do estado inicial e objetivo
    start_state = (7, 8, 4,
                   6, 3, 5,
                   2, 1, 0)

    goal_state = (1, 2, 3,
                  4, 5, 6,
                  7, 8, 0)

    print("Estado Inicial:")
    print_puzzle(start_state)

    print("Estado Objetivo:")
    print_puzzle(goal_state)

    solution = solve_puzzle(start_state, goal_state)

    if solution:
        print(f"Solução encontrada em {len(solution)-1} movimentos:")
        for step in solution:
            print_puzzle(step)
    else:
        print("Nenhuma solução existe para o puzzle fornecido.")
