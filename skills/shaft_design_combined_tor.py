Here's a Python function that calculates the safety factor for a shaft design based on the combined torsion and bending fatigue failure criterion, following the Soderberg and Goodman methods:

```python
import numpy as np

def shaft_safety_factor(M_t, M_b, J, I_yy, sigma_y, sigma_t, sigma_b, phi=0.9):
    """
    Calculate the safety factor for a shaft under combined torsion and bending.
    
    Parameters:
    - M_t: Maximum torque in Newton-meters (Nm)
    - M_b: Maximum bending moment in Newton-meters (Nm)
    - J: Polar moment of inertia of the shaft cross-section in meters^4 (m^4)
    - I_yy: Second moment of area about the y-axis in meters^4 (m^4)
    - sigma_y: Yield strength of the shaft material in Pascals (Pa)
    - sigma_t: Torsion stress in Pascals (Pa)
    - sigma_b: Bending stress in Pascals (Pa)
    - phi: Factor of safety (default is 0.9)
    
    Returns:
    - Safety factor (SF) for the shaft design
    """
    
    # Calculate the combined torsion and bending stress
    sigma_combined = np.sqrt(sigma_t**2 + sigma_b**2)
    
    # Soderberg failure criterion
    sigma_max_soderberg = sigma_y / phi
    
    # Goodman failure criterion
    sigma_max_goodman = 0.5 * (sigma_y - sigma_combined) / phi
    
    # Calculate safety factors using both criteria
    SF_soderberg = sigma_max_soderberg / sigma_combined
    SF_goodman = sigma_max_goodman / sigma_combined
    
    # The overall safety factor is the minimum of the two
    SF = min(SF_soderberg, SF_goodman)
    
    return SF

# Example usage:
# M_t = 1000  # Maximum torque in Nm
# M_b = 500   # Maximum bending moment in Nm
# J = 1.5e-6  # Polar moment of inertia in m^4
# I_yy = 2e-6 # Second moment of area about the y-axis in m^4
# sigma_y = 500e6  # Yield strength in Pa
# sigma_t = 100e6  # Torsion stress in Pa
# sigma_b = 200e6  # Bending stress in Pa

# SF = shaft_safety_factor(M_t, M_b, J, I_yy, sigma_y, sigma_t, sigma_b)
# print(f"Safety Factor: {SF}")
```

This function takes the maximum torque (`M_t`), maximum bending moment (`M_b`), polar moment of inertia (`J`), second moment of area about the y-axis (`I_yy`), yield strength (`sigma_y`), torsion stress (`sigma_t`), and bending stress (`sigma_b`) as inputs, along with an optional safety factor (`phi`). It calculates the safety factor based on both the Soderberg and Goodman failure criteria and returns the minimum of the two. This ensures that the shaft design meets both criteria simultaneously.