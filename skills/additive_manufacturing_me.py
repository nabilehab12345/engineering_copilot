# This file contains generated reference text, not executable Python.
# Certainly! Additive manufacturing (AM) techniques such as Direct Metal Laser Sintering (DMLS) and Selective Laser Sintering (SLS) are widely used in metal 3D printing. Below is a Python function that calculates the volume of a part designed using AM techniques. This function assumes that the part is a rectangular prism for simplicity, but it can be easily extended to other shapes such as cylinders or spheres.
#
# ```python
# def calculate_am_part_volume(length, width, height):
#     """
#     Calculate the volume of an additive manufactured part designed using DMLS or SLS.
#
#     Parameters:
#     - length (float): The length of the part.
#     - width (float): The width of the part.
#     - height (float): The height of the part.
#
#     Returns:
#     - float: The volume of the part.
#     """
#     if length <= 0 or width <= 0 or height <= 0:
#         raise ValueError("All dimensions must be positive numbers.")
#     
#     volume = length * width * height
#     return volume
#
# # Example usage:
# length = 10.0  # in mm
# width = 5.0    # in mm
# height = 2.0   # in mm
#
# part_volume = calculate_am_part_volume(length, width, height)
# print(f"The volume of the AM part is: {part_volume} cubic mm")
# ```
#
# ### Explanation:
# 1. **Function Definition**: The function `calculate_am_part_volume` takes three parameters: `length`, `width`, and `height`.
# 2. **Input Validation**: The function checks if any of the dimensions are non-positive and raises a `ValueError` if they are. This ensures that the dimensions are valid.
# 3. **Volume Calculation**: The volume of the rectangular prism is calculated using the formula \( \text{Volume} = \text{length} \times \text{width} \times \text{height} \).
# 4. **Return Value**: The function returns the calculated volume.
#
# ### Extending the Function:
# If you need to calculate the volume for other shapes (e.g., cylinders or spheres), you can create additional functions. Here’s an example for a cylindrical part:
#
# ```python
# import math
#
# def calculate_am_cylinder_volume(radius, height):
#     """
#     Calculate the volume of an additive manufactured cylindrical part designed using DMLS or SLS.
#
#     Parameters:
#     - radius (float): The radius of the cylinder.
#     - height (float): The height of the cylinder.
#
#     Returns:
#     - float: The volume of the cylinder.
#     """
#     if radius <= 0 or height <= 0:
#         raise ValueError("All dimensions must be positive numbers.")
#     
#     volume = math.pi * radius ** 2 * height
#     return volume
#
# # Example usage:
# radius = 3.0  # in mm
# height = 10.0  # in mm
#
# cylinder_volume = calculate_am_cylinder_volume(radius, height)
# print(f"The volume of the AM cylindrical part is: {cylinder_volume} cubic mm")
# ```
#
# This approach ensures that your code is clean, reusable, and easy to maintain. You can extend it further by adding more shapes and complex geometries as needed.
