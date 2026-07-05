def parse_test_case(solution, input_file_path: str, expected_file_path: str):
    
    with open(input_file_path) as input_file, \
        open(expected_file_path) as expected_file:
            