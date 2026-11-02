from simpleai.search import SearchProblem
from simpleai.search.utils import FifoList, BoundedPriorityQueue, LifoList
from simpleai.search.models import (
    SearchNode,
    SearchNodeHeuristicOrdered,
    SearchNodeStarOrdered,
    SearchNodeCostOrdered,
)


INITIAL = (
    (2, 1, 0),
    (3, 4, 5),
    (7, 8, 6),
)

GOAL = (
    (1, 2, 3),
    (8, 0, 4),
    (7, 6, 5),
)

# Hướng di chuyển của ô trống 0
DIRECTIONS = (
    ("UP", -1, 0),
    ("DOWN", 1, 0),
    ("LEFT", 0, -1),
    ("RIGHT", 0, 1),
)

GOAL_POSITIONS = {
    GOAL[r][c]: (r, c)
    for r in range(3)
    for c in range(3)
}


def find_zero(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

    raise ValueError("Trạng thái phải có ô trống 0")


def h1(state):
    """Số ô sai vị trí, bỏ qua ô trống 0."""
    return sum(
        state[r][c] != 0 and state[r][c] != GOAL[r][c]
        for r in range(3)
        for c in range(3)
    )


def h2(state):
    """Tổng khoảng cách Manhattan, bỏ qua ô trống 0."""
    total = 0

    for r in range(3):
        for c in range(3):
            tile = state[r][c]

            if tile != 0:
                goal_r, goal_c = GOAL_POSITIONS[tile]
                total += abs(r - goal_r) + abs(c - goal_c)

    return total


class EightPuzzleProblem(SearchProblem):
    def __init__(self, initial_state=INITIAL, heuristic_type="h2"):
        super().__init__(initial_state=initial_state)

        self.heuristic_type = heuristic_type
        self.expanded = 0
        self.generated = 0
        self.cutoff = False

    def actions(self, state):
        """Các hướng di chuyển hợp lệ của ô trống."""
        r, c = find_zero(state)

        return [
            name
            for name, dr, dc in DIRECTIONS
            if 0 <= r + dr < 3 and 0 <= c + dc < 3
        ]

    def result(self, state, action):
        """Trạng thái mới sau khi di chuyển ô trống."""
        r, c = find_zero(state)

        dr, dc = next(
            (dr, dc)
            for name, dr, dc in DIRECTIONS
            if name == action
        )

        nr, nc = r + dr, c + dc
        board = [list(row) for row in state]

        board[r][c], board[nr][nc] = board[nr][nc], board[r][c]

        return tuple(tuple(row) for row in board)

    def is_goal(self, state):
        return state == GOAL

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        if self.heuristic_type == "h1":
            return h1(state)

        if self.heuristic_type == "h2":
            return h2(state)

        raise ValueError("Heuristic phải là h1 hoặc h2")



# 1. BFS
def breadth_first(problem, graph_search=False, viewer=None):
    return _search(
        problem,
        FifoList(),
        graph_search=graph_search,
        viewer=viewer,
    )


# 2. DFS
def depth_first(problem, graph_search=False, viewer=None):
    return _search(
        problem,
        LifoList(),
        graph_search=graph_search,
        viewer=viewer,
    )


# 3. DLS
def limited_depth_first(
    problem, depth_limit, graph_search=False, viewer=None
):
    return _search(
        problem,
        LifoList(),
        graph_search=graph_search,
        depth_limit=depth_limit,
        viewer=viewer,
    )


# 4. IDS
def iterative_limited_depth_first(
    problem, graph_search=False, viewer=None, max_depth=30
):
    for limit in range(max_depth + 1):
        solution = limited_depth_first(
            problem,
            limit,
            graph_search=graph_search,
            viewer=viewer,
        )

        if solution is not None:
            return solution

        # Không bị cắt ở giới hạn và đã xét hết cây tìm kiếm
        if not problem.cutoff:
            return None

    return None


# 5. UCS
def uniform_cost(problem, graph_search=False, viewer=None):
    return _search(
        problem,
        BoundedPriorityQueue(),
        graph_search=graph_search,
        node_factory=SearchNodeCostOrdered,
        graph_replace_when_better=True,
        viewer=viewer,
    )


# 6. Greedy
def greedy(problem, graph_search=False, viewer=None):
    return _search(
        problem,
        BoundedPriorityQueue(),
        graph_search=graph_search,
        node_factory=SearchNodeHeuristicOrdered,
        graph_replace_when_better=True,
        viewer=viewer,
    )


# 7. A*
def astar(problem, graph_search=False, viewer=None):
    return _search(
        problem,
        BoundedPriorityQueue(),
        graph_search=graph_search,
        node_factory=SearchNodeStarOrdered,
        graph_replace_when_better=True,
        viewer=viewer,
    )



def _search(
    problem,
    fringe,
    graph_search=False,
    depth_limit=None,
    node_factory=SearchNode,
    graph_replace_when_better=False,
    viewer=None,
):
    if viewer:
        viewer.event("started")

    memory = set()

    # Tra cứu nút đang trong fringe theo trạng thái
    frontier_by_state = {}
    problem.cutoff = False

    initial_node = node_factory(
        state=problem.initial_state,
        problem=problem,
    )

    fringe.append(initial_node)
    problem.generated += 1

    if graph_search:
        frontier_by_state[initial_node.state] = initial_node

    while fringe:
        if viewer:
            viewer.event("new_iteration", fringe.sorted())

        node = fringe.pop()

        if graph_search:
            frontier_by_state.pop(node.state, None)

        # Kiểm tra đích trước khi mở rộng
        if problem.is_goal(node.state):
            if viewer:
                viewer.event("chosen_node", node, True)
                viewer.event(
                    "finished", fringe.sorted(), node, "goal found"
                )

            return node

        if viewer:
            viewer.event("chosen_node", node, False)

        memory.add(node.state)

        # DLS: không mở rộng nút đã chạm giới hạn
        if depth_limit is not None and node.depth >= depth_limit:
            problem.cutoff = True
            continue

        problem.expanded += 1

        # Sử dụng phương thức expand() của SimpleAI
        expanded = node.expand()
        problem.generated += len(expanded)

        if viewer:
            viewer.event("expanded", [node], [expanded])

        for n in expanded:

            # DLS/IDS: tránh chu trình trên đường đi hiện tại
            if depth_limit is not None:
                ancestor = node

                while (
                    ancestor is not None
                    and ancestor.state != n.state
                ):
                    ancestor = ancestor.parent

                if ancestor is not None:
                    continue

            if graph_search:
                other = frontier_by_state.get(n.state)

                if n.state not in memory and other is None:
                    fringe.append(n)
                    frontier_by_state[n.state] = n

                elif (
                    graph_replace_when_better
                    and other is not None
                    and n < other
                ):
                    fringe.remove(other)
                    fringe.append(n)
                    frontier_by_state[n.state] = n

            else:
                fringe.append(n)

    if viewer:
        viewer.event(
            "finished", fringe.sorted(), None, "goal not found"
        )

    return None


def inversion_count(state):
    tiles = [
        tile
        for row in state
        for tile in row
        if tile != 0
    ]

    return sum(
        tiles[i] > tiles[j]
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
    )



def main():
    if inversion_count(INITIAL) % 2 != inversion_count(GOAL) % 2:
        print("INITIAL không thể chuyển đến GOAL.")
        return

    print("h1(INITIAL) =", h1(INITIAL))
    print("h2(INITIAL) =", h2(INITIAL))

    # Mỗi cấu hình dùng một đối tượng bài toán mới để đếm riêng
    cases = [
        (
            "BFS", "h2",
            lambda p: breadth_first(p, graph_search=True)
        ),
        (
            "DFS", "h2",
            lambda p: depth_first(p, graph_search=True)
        ),
        (
            "DLS", "h2",
            lambda p: limited_depth_first(p, 20)
        ),
        (
            "IDS", "h2",
            lambda p: iterative_limited_depth_first(p, max_depth=30)
        ),
        (
            "UCS", "h2",
            lambda p: uniform_cost(p, graph_search=True)
        ),
        (
            "Greedy-h1", "h1",
            lambda p: greedy(p, graph_search=True)
        ),
        (
            "Greedy-h2", "h2",
            lambda p: greedy(p, graph_search=True)
        ),
        (
            "A*-h1", "h1",
            lambda p: astar(p, graph_search=True)
        ),
        (
            "A*-h2", "h2",
            lambda p: astar(p, graph_search=True)
        ),
    ]

    print(
        f"\n{'Thuật toán':<14}"
        f"{'Số bước':>10}"
        f"{'Chi phí':>10}"
        f"{'Expanded':>12}"
    )
    print("-" * 46)

    optimal_result = None

    for name, heuristic_type, algorithm in cases:
        problem = EightPuzzleProblem(INITIAL, heuristic_type)
        result = algorithm(problem)

        if result is None:
            status = (
                "Hết giới hạn"
                if problem.cutoff
                else "Không có lời giải"
            )

            print(
                f"{name:<14}"
                f"{status:>20}"
                f"{problem.expanded:>12}"
            )
            continue

        print(
            f"{name:<14}"
            f"{result.depth:>10}"
            f"{result.cost:>10}"
            f"{problem.expanded:>12}"
        )

        if name == "A*-h2":
            optimal_result = result

    # In đường đi tìm được bởi A* dùng h2
    if optimal_result is not None:
        print("\nLỜI GIẢI A*-h2 — hướng di chuyển của ô trống:")

        for step, (action, state) in enumerate(
            optimal_result.path()
        ):
            print(f"\nBước {step}: {action or 'START'}")
            print(
                f"g={step}; "
                f"h1={h1(state)}; "
                f"h2={h2(state)}"
            )

            for row in state:
                print(*row)


if __name__ == "__main__":
    main()
