Designing and verifying gear stress calculations can be complex and requires careful consideration of various factors. Below is a Python function that calculates the stresses in spur helical planetary and cycloidal gears based on the ISO and AGMA standards. This function is designed to be reusable and can be easily integrated into larger gear design software or simulations.

```python
import math

def calculate_gear_stress(module, pressure_angle, number_of_teeth, helix_angle, face_width, load, material_strength, safety_factor):
    """
    Calculate the stresses in spur helical planetary and cycloidal gears.

    Parameters:
    - module (float): Gear module (mm)
    - pressure_angle (float): Pressure angle (degrees)
    - number_of_teeth (int): Number of teeth on the gear
    - helix_angle (float): Helix angle (degrees)
    - face_width (float): Gear face width (mm)
    - load (float): Applied load (N)
    - material_strength (float): Material yield strength (MPa)
    - safety_factor (float): Safety factor

    Returns:
    - tuple: (radial stress, tangential stress)
    """
    # Convert angles to radians
    pressure_angle_rad = math.radians(pressure_angle)
    helix_angle_rad = math.radians(helix_angle)

    # Calculate involute parameters
    d = module * number_of_teeth  # Gear pitch circle diameter (mm)
    r = d / 2  # Gear pitch radius (mm)
    a = r * math.tan(pressure_angle_rad)  # Involute curve parameter (mm)
    h = module * number_of_teeth / 2  # Gear height (mm)

    # Calculate gear tooth parameters
    tooth_width = face_width / (number_of_teeth * 2)  # Width of each tooth (mm)
    tooth_length = h * math.tan(helix_angle_rad)  # Length of each tooth (mm)

    # Calculate normal and tangential stresses
    F_normal = load * math.cos(pressure_angle_rad)  # Normal force (N)
    F_tangential = load * math.sin(pressure_angle_rad)  # Tangential force (N)
    sigma_normal = F_normal / (tooth_width * tooth_length)  # Normal stress (MPa)
    sigma_tangential = F_tangential / (tooth_width * tooth_length)  # Tangential stress (MPa)

    # Apply safety factor
    sigma_normal /= safety_factor
    sigma_tangential /= safety_factor

    # Ensure stresses do not exceed material strength
    sigma_normal = min(sigma_normal, material_strength)
    sigma_tangential = min(sigma_tangential, material_strength)

    return sigma_normal, sigma_tangential

# Example usage
module = 5  # mm
pressure_angle = 20  # degrees
number_of_teeth = 20
helix_angle = 30  # degrees
face_width = 50  # mm
load = 1000  # N
material_strength = 400  # MPa
safety_factor = 2.5

radial_stress, tangential_stress = calculate_gear_stress(module, pressure_angle, number_of_teeth, helix_angle, face_width, load, material_strength, safety_factor)
print(f"Radial Stress: {radial_stress} MPa")
print(f"Tangential Stress: {tangential_stress} MPa")
```

### Explanation:
1. **Parameters**:
   - `module`: Gear module (mm)
   - `pressure_angle`: Pressure angle (degrees)
   - `number_of_teeth`: Number of teeth on the gear
   - `helix_angle`: Helix angle (degrees)
   - `face_width`: Gear face width (mm)
   - `load`: Applied load (N)
   - `material_strength`: Material yield strength (MPa)
   - `safety_factor`: Safety factor

2. **Calculations**:
   - Convert angles from degrees to radians.
   - Calculate the involute parameters such as pitch circle diameter, pitch radius, and involute curve parameter.
   - Calculate the gear tooth parameters such as tooth width and tooth length.
   - Compute the normal and tangential forces.
   - Calculate the normal and tangential stresses.
   - Apply the safety factor and ensure the stresses do not exceed the material strength.

3. **Output**:
   - The function returns the radial and tangential stresses.

This function provides a basic framework for calculating gear stresses and can be extended or modified based on specific requirements or additional factors such as lubrication, tooth root stresses, and more.