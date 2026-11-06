
DOMAIN = range(-10, 11)

def check_constraints(x, y):

    constraint_1 = (
        3 * x + 2 * y == 25
    )

    constraint_2 = (
        2 * x - y == 5
    )

    return (
        constraint_1
        and constraint_2
    )

def backtracking(
    assignment=None
):

    if assignment is None:
        assignment = {}

    if "x" in assignment and "y" in assignment:

        x = assignment["x"]
        y = assignment["y"]

        if check_constraints(x, y):

            return assignment.copy()

        return None

    if "x" not in assignment:

        variable = "x"

    else:

        variable = "y"

    for value in DOMAIN:

        assignment[variable] = value

        print(
            f"Thử {variable} = {value}"
        )

        if "x" in assignment and "y" in assignment:

            x = assignment["x"]
            y = assignment["y"]

            if check_constraints(x, y):

                print(
                    f"  -> Tìm thấy nghiệm: "
                    f"x = {x}, y = {y}"
                )

                return assignment.copy()

            else:

                # Vi phạm ràng buộc
                del assignment[variable]

                continue

        result = backtracking(
            assignment
        )

        if result is not None:

            return result

        if variable in assignment:

            del assignment[variable]


    return None

if __name__ == "__main__":

    print("=" * 50)
    print("BÀI 3: BACKTRACKING - HỆ PHƯƠNG TRÌNH")
    print("=" * 50)

    print("\nHệ phương trình:")

    print("3x + 2y = 25")
    print("2x - y  = 5")

    print("\nDomain:")

    print(
        "x, y ∈ [-10, 10]"
    )


    solution = backtracking()


    print("\n" + "=" * 50)
    print("KẾT QUẢ")
    print("=" * 50)


    if solution is not None:

        x = solution["x"]
        y = solution["y"]

        print(f"x = {x}")
        print(f"y = {y}")

        print("\nKiểm tra:")

        print(
            f"3x + 2y = "
            f"3({x}) + 2({y}) = "
            f"{3 * x + 2 * y}"
        )

        print(
            f"2x - y = "
            f"2({x}) - ({y}) = "
            f"{2 * x - y}"
        )

    else:

        print(
            "Không tìm thấy nghiệm."
        )