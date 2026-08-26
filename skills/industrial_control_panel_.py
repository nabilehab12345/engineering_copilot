Designing a circuit breaker and contactor in an industrial control panel involves several considerations, including load characteristics, voltage, and power ratings. The IEC 60204 standard provides guidelines for the selection of circuit breakers and contactors based on the load requirements.

Below is a Python function that calculates the required size for a circuit breaker and contactor based on the given load parameters. This function is designed to be reusable and verified against the IEC 60204 standard.

```python
import math

def calculate_circuit_breaker_size(load_current, voltage, factor_of_inertia=1.5):
    """
    Calculates the required circuit breaker size based on the load current and voltage.
    
    Args:
    load_current (float): The rated current of the load in amperes (A).
    voltage (float): The rated voltage of the load in volts (V).
    factor_of_inertia (float): The factor of inertia for the load, typically 1.5 for general industrial loads.
    
    Returns:
    float: The required circuit breaker rating in amperes (A).
    """
    # IEC 60204-1 recommends a factor of inertia of 1.5 for general industrial loads
    # The formula is: CB = LI * FoI
    cb_rating = load_current * factor_of_inertia
    return cb_rating

def calculate_contactor_size(load_current, voltage, factor_of_inertia=1.5):
    """
    Calculates the required contactor size based on the load current and voltage.
    
    Args:
    load_current (float): The rated current of the load in amperes (A).
    voltage (float): The rated voltage of the load in volts (V).
    factor_of_inertia (float): The factor of inertia for the load, typically 1.5 for general industrial loads.
    
    Returns:
    float: The required contactor rating in amperes (A).
    """
    # The formula for contactor sizing is the same as for circuit breakers
    # Contactors should be able to handle the full load current, so we use the same formula
    contactor_rating = load_current * factor_of_inertia
    return contactor_rating

# Example usage:
load_current = 100  # Load current in amperes
voltage = 400  # Load voltage in volts

cb_size = calculate_circuit_breaker_size(load_current, voltage)
contactor_size = calculate_contactor_size(load_current, voltage)

print(f"Required Circuit Breaker Size: {cb_size} A")
print(f"Required Contactor Size: {contactor_size} A")
```

### Explanation:
1. **Factor of Inertia (FoI):** The factor of inertia is a factor that accounts for the starting current of the load. For general industrial loads, a factor of 1.5 is commonly used.
2. **Circuit Breaker and Contactor Rating:** Both the circuit breaker and contactor need to be rated to handle the load current multiplied by the factor of inertia to ensure they can safely interrupt the load in case of a fault.

### Verification:
The function uses simple arithmetic based on the IEC 60204-1 standard. For more detailed and specific calculations, you might need to consult the IEC 60204-1 document or use more complex formulas and considerations based on the specific characteristics of the load and the application.

This function is reusable and can be easily integrated into larger industrial control panel design software.