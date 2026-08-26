The topic "Mechanical vibration resonance, damping, and modal analysis in machine structures" involves several key concepts. Resonance occurs when a system is driven at a frequency close to its natural frequency, leading to large oscillations. Damping is the force that reduces the amplitude of oscillations over time, while modal analysis helps in understanding the natural frequencies and modes of vibration of a structure.

Here's a Python function that calculates the natural frequency, damping ratio, and modal damping for a simple mechanical system. This function assumes a single-degree-of-freedom system.

```python
import numpy as np

def mechanical_vibration_analysis(m, k, c):
    """
    Calculates the natural frequency, damping ratio, and modal damping for a single-degree-of-freedom system.
    
    Parameters:
    m (float): Mass of the system (kg)
    k (float): Stiffness of the system (N/m)
    c (float): Damping coefficient of the system (Ns/m)
    
    Returns:
    tuple: (natural_frequency, damping_ratio, modal_damping)
    """
    # Calculate the natural frequency
    natural_frequency = np.sqrt(k / m)
    
    # Calculate the damping ratio
    damping_ratio = c / (2 * np.sqrt(m * k))
    
    # Calculate the modal damping
    modal_damping = c
    
    return natural_frequency, damping_ratio, modal_damping

# Example usage:
m = 10  # mass in kg
k = 100  # stiffness in N/m
c = 20  # damping coefficient in Ns/m

natural_frequency, damping_ratio, modal_damping = mechanical_vibration_analysis(m, k, c)
print(f"Natural Frequency: {natural_frequency} Hz")
print(f"Damping Ratio: {damping_ratio}")
print(f"Modal Damping: {modal_damping} Ns/m")
```

### Explanation:
1. **Natural Frequency (ω_n)**:
   \[
   \omega_n = \sqrt{\frac{k}{m}}
   \]
   This is the frequency at which the system naturally oscillates without any external force.

2. **Damping Ratio (ζ)**:
   \[
   \zeta = \frac{c}{2 \sqrt{m k}}
   \]
   The damping ratio indicates how quickly the system's oscillations die out. A higher damping ratio means more rapid damping.

3. **Modal Damping (c)**:
   Modal damping is simply the damping coefficient of the system.

### Assumptions:
- The function assumes a single-degree-of-freedom system.
- The damping is proportional to the velocity (viscous damping).

### Considerations:
- For more complex multi-degree-of-freedom systems, additional analysis techniques like eigenvalue analysis or finite element analysis (FEA) are required.
- The damping coefficient (c) can be derived from tests or empirical data.

This function provides a basic framework for calculating key parameters related to the vibration behavior of a mechanical system.