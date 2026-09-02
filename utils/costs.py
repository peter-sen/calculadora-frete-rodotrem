def calculate_costs(distance_km, payload_tons=47.2):
    """
    Calculates fixed and variable costs for a Volvo FH 540 (9 axles) in Balsas-MA.

    Variables (Estimates for 2023/2024):
    - Diesel price in Balsas-MA region: ~ R$ 6.20 / liter
    - Average fuel consumption (Volvo FH 540 loaded with 47.2t): ~ 1.8 km/liter
    - Arla 32 consumption: ~ 5% of diesel consumption, price ~ R$ 4.00 / liter
    - Tires (34 tires on a 9-axle rodotrem): ~ R$ 0.45 / km total wear cost
    - Maintenance (Preventive + Corrective): ~ R$ 0.35 / km
    - Tolls: Estimate ~ R$ 0.25 / km per axle (for 9 axles = 2.25/km, but let's assume an average R$ 0.50/km overall if not fully tolled, we will use a simplified average of R$ 0.40/km)

    Fixed Costs (Monthly apportioned per trip based on days, or per km):
    - Driver salary + taxes: ~ R$ 8000 / month
    - Insurance, IPVA, Depreciation, Tracking: ~ R$ 12000 / month
    - Assuming 10,000 km / month -> Fixed cost ~ R$ 2.00 / km

    Returns a dictionary with cost breakdown.
    """

    # Cost per km parameters
    diesel_price = 6.20
    consumption_kml = 1.8
    fuel_cost_per_km = diesel_price / consumption_kml

    arla_cost_per_km = (fuel_cost_per_km * 0.05) * (4.00 / 6.20) # Approximation
    tires_cost_per_km = 0.45
    maintenance_cost_per_km = 0.35
    tolls_per_km = 0.40

    variable_cost_per_km = fuel_cost_per_km + arla_cost_per_km + tires_cost_per_km + maintenance_cost_per_km + tolls_per_km

    fixed_cost_per_km = 2.00

    total_variable_cost = variable_cost_per_km * distance_km
    total_fixed_cost = fixed_cost_per_km * distance_km
    total_cost = total_variable_cost + total_fixed_cost

    return {
        "distance_km": distance_km,
        "payload_tons": payload_tons,
        "fuel_cost": fuel_cost_per_km * distance_km,
        "tires_cost": tires_cost_per_km * distance_km,
        "maintenance_cost": maintenance_cost_per_km * distance_km,
        "tolls_cost": tolls_per_km * distance_km,
        "total_variable_cost": total_variable_cost,
        "total_fixed_cost": total_fixed_cost,
        "total_cost": total_cost,
        "cost_per_km": variable_cost_per_km + fixed_cost_per_km
    }
