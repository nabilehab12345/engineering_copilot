import math

def calculate_shaft_diameter(torque_nm: float, bending_moment_nm: float, yield_strength_mpa: float, factor_of_safety: float = 2.0) -> dict:
    allowable_stress = (0.5 * yield_strength_mpa * 1e6) / factor_of_safety
    equivalent_torque = math.sqrt(torque_nm**2 + bending_moment_nm**2)
    diameter_m = ((16 * equivalent_torque) / (math.pi * allowable_stress)) ** (1/3)
    return {
        "recommended_diameter_mm": round(diameter_m * 1000, 2),
        "equivalent_torque_nm": round(equivalent_torque, 2),
        "allowable_shear_stress_mpa": round(allowable_stress / 1e6, 2),
        "factor_of_safety": factor_of_safety
    }

def calculate_gear_ratio_and_teeth(torque_input: float, desired_torque_output: float, pinion_teeth: int = 14) -> dict:
    ratio = desired_torque_output / torque_input
    gear_teeth = math.ceil(pinion_teeth * ratio)
    actual_ratio = gear_teeth / pinion_teeth
    return {
        "target_gear_ratio": round(ratio, 2),
        "actual_gear_ratio": round(actual_ratio, 2),
        "pinion_teeth": pinion_teeth,
        "gear_teeth": gear_teeth,
        "actual_output_torque_nm": round(torque_input * actual_ratio, 2)
    }