def calculate_bom_and_weight_budget(components_list: list) -> dict:
    total_w = 0.0
    total_c = 0.0
    detailed = []
    for item in components_list:
        qty = item.get("qty", 1)
        w = item.get("weight_g", 0.0) * qty
        c = item.get("price_usd", 0.0) * qty
        total_w += w
        total_c += c
        detailed.append({
            "component": item.get("name", "Unknown"),
            "qty": qty,
            "weight_kg": round(w / 1000.0, 3),
            "cost_usd": round(c, 2)
        })
    return {
        "total_weight_kg": round(total_w / 1000.0, 3),
        "total_cost_usd": round(total_c, 2),
        "detailed_bom": detailed
    }