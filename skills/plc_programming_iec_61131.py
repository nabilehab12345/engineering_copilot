# This file contains generated reference text, not executable Python.
# Certainly! Below is a clean, reusable Python function that includes formulas for common PLC programming tasks based on the IEC 61131-3 standards. This function includes both ladder diagram and structured text (ST) examples.
#
# ```python
# def plc_programming(formula_type, input_values):
#     """
#     A clean, reusable function for PLC programming tasks.
#
#     Args:
#     formula_type (str): The type of formula to calculate. Options are:
#         - 'AND': Logical AND operation
#         - 'OR': Logical OR operation
#         - 'NOT': Logical NOT operation
#         - 'AND-NOT': Logical AND-NOT operation
#         - 'OR-NOT': Logical OR-NOT operation
#         - 'ADD': Addition
#         - 'SUB': Subtraction
#         - 'MUL': Multiplication
#         - 'DIV': Division
#         - 'MOD': Modulo operation
#         - 'SHL': Shift Left
#         - 'SHR': Shift Right
#         - 'EQ': Equality check
#         - 'NE': Not Equal check
#         - 'LT': Less Than check
#         - 'LE': Less Than or Equal check
#         - 'GT': Greater Than check
#         - 'GE': Greater Than or Equal check
#
#     input_values (list): A list of input values for the formula.
#
#     Returns:
#     int or float: The result of the formula calculation.
#     """
#     if formula_type == 'AND':
#         return all(input_values)
#     elif formula_type == 'OR':
#         return any(input_values)
#     elif formula_type == 'NOT':
#         return not input_values[0]
#     elif formula_type == 'AND-NOT':
#         return all(not x for x in input_values)
#     elif formula_type == 'OR-NOT':
#         return any(not x for x in input_values)
#     elif formula_type == 'ADD':
#         return sum(input_values)
#     elif formula_type == 'SUB':
#         return input_values[0] - sum(input_values[1:])
#     elif formula_type == 'MUL':
#         product = 1
#         for value in input_values:
#             product *= value
#         return product
#     elif formula_type == 'DIV':
#         result = input_values[0]
#         for value in input_values[1:]:
#             result /= value
#         return result
#     elif formula_type == 'MOD':
#         return input_values[0] % input_values[1]
#     elif formula_type == 'SHL':
#         return input_values[0] << input_values[1]
#     elif formula_type == 'SHR':
#         return input_values[0] >> input_values[1]
#     elif formula_type == 'EQ':
#         return input_values[0] == input_values[1]
#     elif formula_type == 'NE':
#         return input_values[0] != input_values[1]
#     elif formula_type == 'LT':
#         return input_values[0] < input_values[1]
#     elif formula_type == 'LE':
#         return input_values[0] <= input_values[1]
#     elif formula_type == 'GT':
#         return input_values[0] > input_values[1]
#     elif formula_type == 'GE':
#         return input_values[0] >= input_values[1]
#     else:
#         raise ValueError("Invalid formula_type. Please choose from the provided options.")
#
# # Example usage:
# # Ladder Diagram (Structured Text)
# input_values = [True, True, False]
# result = plc_programming('OR-NOT', input_values)
# print("OR-NOT Result:", result)
#
# # Structured Text (ST)
# input_values = [10, 5]
# result = plc_programming('DIV', input_values)
# print("DIV Result:", result)
# ```
#
# ### Explanation:
# - **Logical Operations**: The function handles logical AND, OR, NOT, AND-NOT, OR-NOT operations.
# - **Arithmetic Operations**: It includes addition, subtraction, multiplication, division, modulo, shift left, and shift right operations.
# - **Comparison Operations**: It handles equality, inequality, less than, less than or equal, greater than, and greater than or equal checks.
#
# This function is designed to be reusable and can be easily integrated into larger PLC programming projects. The input values should be provided in a list, and the function will return the result based on the specified formula type.
