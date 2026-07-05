from ast import literal_eval
import os
import inspect
from typing import Any, get_args

from lcollections.list_node import ListNode
from lcollections.tree_node import TreeNode


class Tester:
    # ========================================================
    # MAGIC METHODS
    # ========================================================
    def __init__(self, AnyClass: type, input_file_path: str, expected_file_path: str) -> None:
        if not isinstance(AnyClass, type):
            raise TypeError(f"`AnyClass` must be a class, not an instance.")

        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"{input_file_path}")

        if not os.path.exists(expected_file_path):
            raise FileNotFoundError(f"{expected_file_path}")

        self.IS_DESIGN_PROBLEM = AnyClass.__name__ != "Solution"
        self.AnyClass = AnyClass

        if self.IS_DESIGN_PROBLEM:
            self.__init_design_problem(input_file_path, expected_file_path)
        else:
            self.__init_solution_problem(input_file_path, expected_file_path)

    # ========================================================
    # PUBLIC METHODS
    # ========================================================
    def run_all(self):
        if self.IS_DESIGN_PROBLEM:
            self.__run_all_design()
        else:
            self.__run_all_solution()

    def run_at(self, test_number: int):
        if self.IS_DESIGN_PROBLEM:
            self.__run_at_design(test_number)
        else:
            self.__run_at_solution(test_number)

    # ========================================================
    # PRIVATE METHODS
    # ========================================================
    def __init_design_problem(self, input_file_path: str, expected_file_path: str):
        self.raw_inputs, self.raw_outputs = [], []

        with open(input_file_path) as in_file:
            raw_inputs = in_file.readlines()

            for i in range(0, len(raw_inputs), 2):
                raw_input = []

                methods = literal_eval(self.__clean_raw_string(raw_inputs[i]))
                args_list = literal_eval(self.__clean_raw_string(raw_inputs[i + 1]))

                for method, args in zip(methods, args_list):
                    raw_input.append((method, args))
                self.raw_inputs.append(raw_input)

        with open(expected_file_path) as out_file:
            for raw_output in out_file:
                raw_output = raw_output \
                    .replace('null', 'None') \
                    .replace('true', 'True') \
                    .replace('false', 'False')
                self.raw_outputs.append(literal_eval(raw_output))

    def __init_solution_problem(self, input_file_path: str, expected_file_path: str):
        self.solution = self.AnyClass()
        self.solution_func = self.__get_first_public_method(self.solution)
        self.in_annotation, self.out_annotation = self.__extract_annotation(self.solution_func)
        self.raw_inputs, self.raw_outputs = [], []

        with open(input_file_path) as in_file:
            raw_inputs = in_file.readlines()
            in_arg_count = len(self.in_annotation)
            for i in range(0, len(raw_inputs), in_arg_count):
                self.raw_inputs.append(raw_inputs[i: i + in_arg_count])

        with open(expected_file_path) as out_file:
            self.raw_outputs = out_file.readlines()

    def __get_first_public_method(self, solution: Any) -> Any:
        for method_name in dir(solution):
            func = getattr(solution, method_name)
            if callable(func) and method_name.find('__') == -1:
                return func
        raise AttributeError(f"Class '{type(self.solution).__name__}' does not have any public method.")

    def __extract_annotation(self, func):
        sig = inspect.signature(func)

        params = sig.parameters

        input_annotation = [
            val.annotation
            for val in params.values()
            if val.annotation is not inspect.Parameter.empty
        ]
        return_annotation = sig.return_annotation

        return input_annotation, return_annotation

    def __run_all_design(self):
        for i in range(len(self.raw_outputs)):
            self.__run_at_design(i + 1)

    def __run_all_solution(self):
        for i in range(len(self.raw_outputs)):
            self.__run_at_solution(i + 1)

    def __run_at_design(self, test_number: int):
        # Get raw
        raw_input = self.raw_inputs[test_number - 1]
        raw_output = self.raw_outputs[test_number - 1]

        instance = None
        actual_output = []
        for method, args in raw_input:
            if self.AnyClass.__name__ == method:
                instance = self.AnyClass(*args)
                actual_output.append(None)
            elif instance:
                result = getattr(instance, method)(*args)
                actual_output.append(result)

        if actual_output == raw_output:
            self.__printGreen(f"Case {test_number}: PASSED")
        else:
            self.__printRed(f"Case {test_number}: WRONG ANSWER")
            self.__printRed(f"\tOutput: {actual_output}")
            self.__printRed(f"\tExpected: {raw_output}")

    def __run_at_solution(self, test_number: int):
        # Get raw
        raw_input_strings = self.raw_inputs[test_number - 1]
        raw_output_string = self.raw_outputs[test_number - 1]

        # Parse input
        parsed_inputs = []
        for i, current_type in enumerate(self.in_annotation):
            val = literal_eval(self.__clean_raw_string(raw_input_strings[i]))

            if current_type is TreeNode or TreeNode in get_args(current_type):
                val = TreeNode.deserialize(val)
            elif current_type is ListNode or ListNode in get_args(current_type):
                val = ListNode.deserialize(val)

            parsed_inputs.append(val)

        # Parse output
        expected_output = literal_eval(self.__clean_raw_string(raw_output_string))

        if self.out_annotation == TreeNode or TreeNode in get_args(self.out_annotation):
            expected_output = TreeNode.deserialize(expected_output)
        elif self.out_annotation == ListNode or ListNode in get_args(self.out_annotation):
            expected_output = ListNode.deserialize(expected_output)

        # Excute function
        actual_output = self.solution_func(*parsed_inputs)
        if actual_output == expected_output:
            self.__printGreen(f"Case {test_number}: PASSED")
        else:
            self.__printRed(f"Case {test_number}: WRONG ANSWER")
            self.__printRed(f"\tOutput: {actual_output}")
            self.__printRed(f"\tExpected: {expected_output}")

    def __clean_raw_string(self, s: str) -> str:
        return s.replace('null', 'None').replace('true', 'True').replace('false', 'False')

    def __printGreen(self, skk):
        print("\033[92m{}\033[00m" .format(skk))

    def __printRed(self, skk):
        print("\033[91m{}\033[00m" .format(skk))
