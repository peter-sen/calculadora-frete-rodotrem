import streamlit as st
from utils.ocr import extract_mileage
from utils.costs import calculate_costs
from utils.antt import calculate_antt_minimum

def main():
    st.set_page_config(page_title="Calculadora de Frete - Rodotrem", layout="wide")
    st.title("🚛 Calculadora de Frete - Rodotrem 9 Eixos")
    st.markdown("### Balsas-MA | Volvo FH 540 | Carga Útil: 47,20t")

    st.sidebar.header("Configurações da Viagem")

    if "distance_km" not in st.session_state:
        st.session_state.distance_km = 0.0

    # Upload da Imagem do Google Maps
    st.sidebar.subheader("1. Extrair Quilometragem")
    uploaded_file = st.sidebar.file_uploader("Envie um print do Google Maps", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        if st.sidebar.button("Extrair KM da Imagem"):
            with st.spinner("Analisando imagem..."):
                extracted_km = extract_mileage(uploaded_file.getvalue())
                if extracted_km:
                    st.sidebar.success(f"Distância encontrada: {extracted_km} km")
                    st.session_state.distance_km = extracted_km
                else:
                    st.sidebar.error("Não foi possível extrair a quilometragem da imagem. Insira manualmente.")

    distance_km = st.sidebar.number_input("Distância Total (km - Ida e Volta)", min_value=0.0, value=float(st.session_state.distance_km), step=10.0)

    st.sidebar.subheader("2. Receitas (Frete Casado)")
    freight_outward = st.sidebar.number_input("Valor do Frete de Ida (R$ - ex: Soja)", min_value=0.0, value=0.0, step=100.0)
    freight_return = st.sidebar.number_input("Valor do Frete de Volta (R$ - ex: Fertilizante)", min_value=0.0, value=0.0, step=100.0)

    total_revenue = freight_outward + freight_return

    if distance_km > 0:
        # Calcular Custos
        costs = calculate_costs(distance_km)
        total_costs = costs["total_cost"]

        # Calcular Piso ANTT
        antt_minimum = calculate_antt_minimum(distance_km)

        # Calcular Lucro e Margem
        net_profit = total_revenue - total_costs
        profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0

        st.header("Resumo Financeiro da Viagem")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Receita Total (R$)", f"R$ {total_revenue:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col2.metric("Custo Total (R$)", f"R$ {total_costs:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        # Highlight ANTT compliance
        antt_delta = total_revenue - antt_minimum
        col3.metric("Piso Mínimo ANTT (R$)", f"R$ {antt_minimum:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), delta=f"R$ {antt_delta:,.2f}", delta_color="normal")

        col4.metric("Margem de Lucro Líquida", f"{profit_margin:.2f}%".replace(".", ","), delta=f"R$ {net_profit:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        st.subheader("Detalhamento dos Custos")

        c1, c2, c3, c4 = st.columns(4)
        c1.write(f"**Diesel + Arla:** R$ {costs['fuel_cost'] + (costs['fuel_cost']*0.05*(4.0/6.2)):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        c2.write(f"**Pneus:** R$ {costs['tires_cost']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        c3.write(f"**Manutenção:** R$ {costs['maintenance_cost']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        c4.write(f"**Pedágios (Est.):** R$ {costs['tolls_cost']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        st.write("---")
        st.write(f"*Custo Variável Total:* R$ {costs['total_variable_cost']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.write(f"*Custo Fixo Total (Rateado):* R$ {costs['total_fixed_cost']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.write(f"*Custo por KM:* R$ {costs['cost_per_km']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        if total_revenue < antt_minimum:
            st.warning("⚠️ O valor total do frete está abaixo do piso mínimo exigido pela ANTT.")
        else:
            st.success("✅ O valor total do frete está de acordo com o piso mínimo da ANTT.")

    else:
        st.info("Insira a distância total da viagem (ida e volta) para visualizar os cálculos.")

if __name__ == "__main__":
    main()
