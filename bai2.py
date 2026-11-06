import random

N = 5

def is_safe(assignment, variable, value):

    for other_variable, other_value in assignment.items():

        # Không cùng hàng
        if value == other_value:
            return False

        # Không cùng đường chéo
        if abs(value - other_value) == abs(
            variable - other_variable
        ):
            return False

    return True


def get_legal_values(assignment, variable):

    values = []

    for value in range(1, N + 1):

        if is_safe(
            assignment,
            variable,
            value
        ):
            values.append(value)

    return values

def backtracking_basic(assignment=None):

    if assignment is None:
        assignment = {}

    # Đã gán hết biến
    if len(assignment) == N:
        return assignment.copy()

    # Chọn biến theo thứ tự X1 -> X5
    variable = len(assignment)

    for value in range(1, N + 1):

        if is_safe(
            assignment,
            variable,
            value
        ):

            assignment[variable] = value

            result = backtracking_basic(
                assignment
            )

            if result is not None:
                return result

            # Backtrack
            del assignment[variable]

    return None

def select_variable_mrv(assignment):

    unassigned = [
        variable
        for variable in range(N)
        if variable not in assignment
    ]

    best_variable = None
    best_size = float("inf")

    for variable in unassigned:

        legal_values = get_legal_values(
            assignment,
            variable
        )

        if len(legal_values) < best_size:

            best_size = len(legal_values)
            best_variable = variable

    return best_variable


def backtracking_mrv(assignment=None):

    if assignment is None:
        assignment = {}

    if len(assignment) == N:
        return assignment.copy()

    # Chọn biến bằng MRV
    variable = select_variable_mrv(
        assignment
    )

    values = get_legal_values(
        assignment,
        variable
    )

    for value in values:

        assignment[variable] = value

        result = backtracking_mrv(
            assignment
        )

        if result is not None:
            return result

        # Backtrack
        del assignment[variable]

    return None

def count_future_options(
    assignment,
    variable,
    value
):

    temporary = assignment.copy()

    temporary[variable] = value

    total = 0

    for other_variable in range(N):

        if other_variable not in temporary:

            legal_values = get_legal_values(
                temporary,
                other_variable
            )

            total += len(legal_values)

    return total


def order_values_lcv(
    assignment,
    variable
):

    values = get_legal_values(
        assignment,
        variable
    )

    # Giá trị để lại nhiều lựa chọn nhất
    # cho các biến khác được ưu tiên
    values.sort(
        key=lambda value:
        count_future_options(
            assignment,
            variable,
            value
        ),
        reverse=True
    )

    return values


def backtracking_lcv(assignment=None):

    if assignment is None:
        assignment = {}

    if len(assignment) == N:
        return assignment.copy()

    # Biến vẫn chọn theo thứ tự
    variable = len(assignment)

    # Nhưng giá trị chọn theo LCV
    values = order_values_lcv(
        assignment,
        variable
    )

    for value in values:

        assignment[variable] = value

        result = backtracking_lcv(
            assignment
        )

        if result is not None:
            return result

        # Backtrack
        del assignment[variable]

    return None

def count_conflicts(board):

    conflicts = 0

    for i in range(N):
        for j in range(i + 1, N):

            if board[i] == board[j]:
                conflicts += 1

            elif abs(
                board[i] - board[j]
            ) == abs(i - j):

                conflicts += 1

    return conflicts


def fitness(board):

    max_pairs = N * (N - 1) // 2

    return max_pairs - count_conflicts(board)


def create_individual():

    board = list(range(1, N + 1))
    random.shuffle(board)

    return board


def create_population(size):

    return [
        create_individual()
        for _ in range(size)
    ]


def selection(population):

    candidates = random.sample(
        population,
        min(3, len(population))
    )

    return max(
        candidates,
        key=fitness
    ).copy()


def crossover(parent1, parent2):

    start, end = sorted(
        random.sample(range(N), 2)
    )

    child = [None] * N

    # Copy từ parent1
    child[start:end + 1] = (
        parent1[start:end + 1]
    )

    # Gene còn thiếu từ parent2
    remaining = [
        gene
        for gene in parent2
        if gene not in child
    ]

    index = 0

    for i in range(N):

        if child[i] is None:

            child[i] = remaining[index]
            index += 1

    return child


def mutation(
    board,
    mutation_rate=0.1
):

    board = board.copy()

    if random.random() < mutation_rate:

        i, j = random.sample(
            range(N),
            2
        )

        board[i], board[j] = (
            board[j],
            board[i]
        )

    return board


def genetic_algorithm(
    population_size=100,
    generations=1000,
    mutation_rate=0.1
):

    population = create_population(
        population_size
    )

    max_fitness = N * (N - 1) // 2

    for generation in range(generations):

        best = max(
            population,
            key=fitness
        )

        if fitness(best) == max_fitness:

            return best

        new_population = []

        # Elitism
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

    return max(
        population,
        key=fitness
    )

def print_board(solution):

    if solution is None:

        print("Không tìm thấy nghiệm.")
        return

    print("Nghiệm:", solution)

    print("\nBàn cờ:")

    for row in range(1, N + 1):

        for col in range(N):

            if solution[col] == row:
                print(" Q ", end="")
            else:
                print(" . ", end="")

        print()

if __name__ == "__main__":

    print("=" * 50)
    print("BÀI 2: CSP - 5 QUEENS")
    print("=" * 50)

    print("\n--- 2.1 BACKTRACKING CƠ BẢN ---")

    solution = backtracking_basic()

    print_board(solution)

    print("\n--- 2.2 VARIABLE ORDERING - MRV ---")

    solution = backtracking_mrv()

    print_board(solution)

    print("\n--- 2.3 VALUE ORDERING - LCV ---")

    solution = backtracking_lcv()

    print_board(solution)

    print(
        "\n--- 2.4 CSP -> SEARCH -> GENETIC ALGORITHM ---"
    )

    solution = genetic_algorithm(
        population_size=100,
        generations=1000,
        mutation_rate=0.1
    )

    print_board(solution)