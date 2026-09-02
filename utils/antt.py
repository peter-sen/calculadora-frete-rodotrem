def calculate_antt_minimum(distance_km, axles=9):
    """
    Calculates a simplified ANTT minimum freight floor for a 9-axle vehicle.
    Based on typical general cargo rates, the value per km per axle varies
    depending on the distance, but for long distances it's often modeled as a linear function plus fixed loading/unloading rate.

    This is a simplified model for the purpose of the application.
    Current typical ANTT tables might dictate roughly R$ 1.00 to R$ 1.50 per km per loaded axle,
    or a coefficient based on distance.
    Let's use an average simplified coefficient for 9-axle rodotrem (7 to 9 axles range).

    Carga Geral - Lotação
    Fixed cost for load/unload (CCD): ~ R$ 400.00
    Cost per km (CC): ~ R$ 6.50 / km for 9 axles

    Formula: Minimum Freight = (Distance * CC) + CCD
    """

    # Simplified ANTT coefficients for a 9-axle rodotrem (General Cargo / Bulk)
    cost_per_km = 6.50
    fixed_loading_cost = 400.00

    min_freight = (distance_km * cost_per_km) + fixed_loading_cost

    return min_freight
