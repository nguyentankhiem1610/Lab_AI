import random


def count_conflicts(board):
    n = len(board)
    conflicts = 0

    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                conflicts += 1
            elif abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def fitness(board):
    n = len(board)
    max_pairs = n * (n - 1) // 2
    return max_pairs - count_conflicts(board)


def create_individual(n):
    board = list(range(1, n + 1))
    random.shuffle(board)
    return board


def create_population(population_size, n):
    return [
        create_individual(n)
        for _ in range(population_size)
    ]


def selection(population):
    tournament_size = 3

    candidates = random.sample(
        population,
        min(tournament_size, len(population))
    )

    return max(candidates, key=fitness).copy()


def crossover(parent1, parent2):

    n = len(parent1)

    start, end = sorted(
        random.sample(range(n), 2)
    )

    child = [None] * n

    # Copy một đoạn từ parent1
    child[start:end + 1] = parent1[start:end + 1]

    # Điền các gene còn thiếu từ parent2
    remaining = [
        gene for gene in parent2
        if gene not in child
    ]

    index = 0

    for i in range(n):
        if child[i] is None:
            child[i] = remaining[index]
            index += 1

    return child


def mutation(board, mutation_rate=0.1):
    board = board.copy()

    if random.random() < mutation_rate:

        i, j = random.sample(
            range(len(board)),
            2
        )

        board[i], board[j] = (
            board[j],
            board[i]
        )

    return board


def genetic_algorithm(
    n,
    population_size=100,
    generations=1000,
    mutation_rate=0.1
):

    population = create_population(
        population_size,
        n
    )

    max_fitness = n * (n - 1) // 2

    for generation in range(generations):

        best = max(
            population,
            key=fitness
        )

        if fitness(best) == max_fitness:

            print("Đã tìm thấy nghiệm!")
            print("Generation:", generation)
            print("Board:", best)
            print("Fitness:", fitness(best))

            return best

        new_population = []

        # Giữ cá thể tốt nhất
        new_population.append(
            best.copy()
        )

        while len(new_population) < population_size:

            parent1 = selection(population)
            parent2 = selection(population)

            child = crossover(
                parent1,
                parent2
            )

            child = mutation(
                child,
                mutation_rate
            )

            new_population.append(child)

        population = new_population

    best = max(
        population,
        key=fitness
    )

    print("Không tìm thấy nghiệm tối ưu.")
    print("Board:", best)
    print("Fitness:", fitness(best))
    print("Conflicts:", count_conflicts(best))

    return best


def print_board(board):

    n = len(board)

    print("\nBàn cờ:")

    for row in range(1, n + 1):

        for col in range(n):

            if board[col] == row:
                print(" Q ", end="")
            else:
                print(" . ", end="")

        print()

if __name__ == "__main__":

    print("=" * 50)
    print("BÀI 1: N-QUEENS + GENETIC ALGORITHM")
    print("=" * 50)

    N = 8

    solution = genetic_algorithm(
        n=N,
        population_size=100,
        generations=1000,
        mutation_rate=0.1
    )

    print_board(solution)