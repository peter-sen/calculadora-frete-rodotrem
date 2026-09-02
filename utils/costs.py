def calculate_costs(km_loaded, km_empty, payload_tons=47.2):
    """
    Calculates fixed and variable costs for a Volvo FH 540 (9 axles) in Balsas-MA,
    differentiating between loaded and empty segments.

    Variables (Estimates for 2023/2024):
    - Diesel price in Balsas-MA region: ~ R$ 6.20 / liter
    - Average fuel consumption loaded: ~ 1.8 km/liter
    - Average fuel consumption empty: ~ 2.8 km/liter
    - Arla 32 consumption: ~ 5% of diesel consumption, price ~ R$ 4.00 / liter
    - Tires (34 tires on a 9-axle rodotrem): ~ R$ 0.45 / km total wear cost (simplification, applies to total km)
    - Maintenance (Preventive + Corrective): ~ R$ 0.35 / km
    - Tolls: ~ R$ 0.40 / km average

    Fixed Costs:
    - Assuming 10,000 km / month -> Fixed cost ~ R$ 2.00 / km
    """

    total_km = km_loaded + km_empty
    diesel_price = 6.20
    arla_price = 4.00

    # Fuel calculations
    liters_loaded = km_loaded / 1.8 if km_loaded > 0 else 0
    liters_empty = km_empty / 2.8 if km_empty > 0 else 0
    total_liters = liters_loaded + liters_empty

    fuel_cost = total_liters * diesel_price
    arla_cost = (total_liters * 0.05) * arla_price

    # Other variable costs based on total km
    tires_cost = total_km * 0.45
    maintenance_cost = total_km * 0.35
    tolls_cost = total_km * 0.40

    total_variable_cost = fuel_cost + arla_cost + tires_cost + maintenance_cost + tolls_cost

    # Fixed costs
    fixed_cost_per_km = 2.00
    total_fixed_cost = total_km * fixed_cost_per_km

    total_cost = total_variable_cost + total_fixed_cost

    cost_per_km = total_cost / total_km if total_km > 0 else 0

    return {
        "total_km": total_km,
        "km_loaded": km_loaded,
        "km_empty": km_empty,
        "payload_tons": payload_tons,
        "fuel_cost": fuel_cost + arla_cost,  # Combining Diesel + Arla for display
        "tires_cost": tires_cost,
        "maintenance_cost": maintenance_cost,
        "tolls_cost": tolls_cost,
        "total_variable_cost": total_variable_cost,
        "total_fixed_cost": total_fixed_cost,
        "total_cost": total_cost,
        "cost_per_km": cost_per_km
    }
