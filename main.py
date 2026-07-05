import inspect

from lcollections import Tester
import solution


def get_first_public_class():
    for name in dir(solution):
        if name.startswith('__'):
            continue

        obj = getattr(solution, name)
        if inspect.isclass(obj) and obj.__module__ == "solution":
            return obj

    raise ValueError("Not found any user-defined class in solution.py!")


def main():
    target_class = get_first_public_class()
    tester = Tester(target_class, "./data/input.txt", "./data/expected.txt")
    tester.run_all()


if __name__ == "__main__":
    main()
