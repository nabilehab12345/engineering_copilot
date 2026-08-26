import math

def design_motor_feeder_circuit(motor_power_kw: float, voltage_v: float = 380, power_factor: float = 0.85, efficiency: float = 0.9) -> dict:
    """
    حساب وتصميم دائرة تغذية محرك كهربائي ثلاثي الأطوار وفق معايير IEC:
    - تيار التشغيل المقنن (Full Load Current - FLC)
    - سعة القاطع الأوتوماتيكي (Circuit Breaker / MCB)
    - سعة الكونتاكتور (Contactor AC-3)
    - ضبط الأوفرلود الحراري (Thermal Overload Relay)
    - مساحة مقطع الكابل الموصى بها (Cable Cross-Section mm2)
    """
    # تيار التشغيل المقنن I = P / (sqrt(3) * V * pf * eff)
    current_flc = (motor_power_kw * 1000) / (math.sqrt(3) * voltage_v * power_factor * efficiency)
    
    # اختيار القاطع (Circuit Breaker) بحد أمان 1.3 إلى 1.4 للبدء المباشر
    cb_rating = current_flc * 1.4
    
    # اختيار الكونتاكتور لفئة AC-3 (حمل محركات)
    contactor_rating = current_flc * 1.25
    
    # ضبط الأوفرلود (Thermal Overload Relay)
    overload_min = round(current_flc * 0.9, 2)
    overload_max = round(current_flc * 1.15, 2)
    
    # تقدير مساحة مقطع الكابل النحاسي
    cable_mm2 = max(1.5, round(current_flc / 4.5, 1))
    
    return {
        "motor_power_kw": motor_power_kw,
        "operating_voltage_v": voltage_v,
        "full_load_current_flc_amps": round(current_flc, 2),
        "recommended_breaker_mcb_amps": math.ceil(cb_rating),
        "recommended_contactor_ac3_amps": math.ceil(contactor_rating),
        "overload_relay_setting_range_amps": f"{overload_min}A - {overload_max}A (Set at {round(current_flc, 2)}A)",
        "recommended_copper_cable_mm2": f"{cable_mm2} mm²",
        "standard": "IEC 60947 / IEC 60204-1"
    }