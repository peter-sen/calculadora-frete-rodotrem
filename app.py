import streamlit as st
from utils.ocr import extract_mileage
from utils.costs import calculate_costs
from utils.antt import calculate_antt_minimum

def main():
    st.set_page_config(page_title="Calculadora de Frete - Rodotrem", layout="wide")
    st.title("🚛 Calculadora de Frete - Rodotrem 9 Eixos")
    st.markdown("### Balsas-MA | Volvo FH 540 | Carga Útil Padrão: 47.200 kg (47,20 t)")

    st.sidebar.header("Extrair Quilometragem (Opcional)")
    if "ocr_distance" not in st.session_state:
        st.session_state.ocr_distance = 0.0

    uploaded_file = st.sidebar.file_uploader("Envie um print do Google Maps", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        if st.sidebar.button("Extrair KM da Imagem"):
            with st.spinner("Analisando imagem..."):
                extracted_km = extract_mileage(uploaded_file.getvalue())
                if extracted_km:
                    st.sidebar.success(f"Distância encontrada: {extracted_km} km")
                    st.session_state.ida_carregado = float(extracted_km)
                else:
                    st.sidebar.error("Não foi possível extrair a quilometragem da imagem. Insira manualmente.")

    st.write("---")

    col_ida, col_volta = st.columns(2)

    with col_ida:
        st.header("BLOCO 1: OPERAÇÃO DE IDA (Obrigatório)")
        st.write("Deslocamento inicial e transporte da carga principal (ex: grãos).")

        ida_km_vazio = st.number_input("KM Rodado Vazio (Deslocamento até a carga)", min_value=0.0, value=0.0, step=10.0, key="ida_vazio")
        ida_km_carregado = st.number_input("KM Rodado Carregado (Viagem com grãos)", min_value=0.0, step=10.0, key="ida_carregado")
        ida_valor_tonelada = st.number_input("Valor do Frete de Ida (R$ por tonelada)", min_value=0.0, value=0.0, step=10.0, key="ida_ton")

    with col_volta:
        st.header("BLOCO 2: OPERAÇÃO DE VOLTA (Opcional)")
        adicionar_retorno = st.checkbox("Adicionar Frete de Retorno (Calcário/Insumos)", value=False)

        if adicionar_retorno:
            st.write("Detalhes da viagem de retorno carregado.")
            volta_km_vazio = st.number_input("KM Vazio de Reposicionamento", min_value=0.0, value=0.0, step=10.0, key="volta_vazio")
            volta_km_carregado = st.number_input("KM Carregado de Volta", min_value=0.0, value=0.0, step=10.0, key="volta_carregado")
            volta_valor_tonelada = st.number_input("Valor do Frete de Volta (R$ por tonelada)", min_value=0.0, value=0.0, step=10.0, key="volta_ton")
        else:
            st.info("Retorno será calculado automaticamente como VAZIO para a origem.")
            volta_km_vazio = ida_km_vazio + ida_km_carregado
            st.write(f"**KM Vazio de Retorno Automático:** {volta_km_vazio} km")
            volta_km_carregado = 0.0
            volta_valor_tonelada = 0.0

    st.write("---")

    total_km_carregado = ida_km_carregado + volta_km_carregado
    total_km_vazio = ida_km_vazio + volta_km_vazio
    total_km = total_km_carregado + total_km_vazio

    # 47.2 tons is the fixed payload
    receita_ida = ida_valor_tonelada * 47.2
    receita_volta = volta_valor_tonelada * 47.2
    total_revenue = receita_ida + receita_volta

    if total_km > 0:
        # Calcular Custos
        costs = calculate_costs(total_km_carregado, total_km_vazio)
        total_costs = costs["total_cost"]

        # Calcular Piso ANTT
        antt_minimum = calculate_antt_minimum(total_km_carregado, total_km_vazio)

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

        st.subheader("Detalhamento Operacional e de Custos")

        c1, c2, c3, c4 = st.columns(4)
        c1.write(f"**KM Total:** {total_km} km")
        c1.write(f"- Carregado: {total_km_carregado} km")
        c1.write(f"- Vazio: {total_km_vazio} km")

        c2.write(f"**Diesel + Arla:** R$ {costs['fuel_cost']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        c3.write(f"**Pneus e Manutenção:** R$ {(costs['tires_cost'] + costs['maintenance_cost']):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        c4.write(f"**Pedágios (Est.):** R$ {costs['tolls_cost']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        st.write("---")
        st.write(f"*Custo Variável Total:* R$ {costs['total_variable_cost']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.write(f"*Custo Fixo Total (Rateado):* R$ {costs['total_fixed_cost']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.write(f"*Custo Médio por KM:* R$ {costs['cost_per_km']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        if total_revenue < antt_minimum:
            st.error("⚠️ Rota Inviável segundo a ANTT: O valor total do frete está abaixo do piso mínimo.")
        elif net_profit < 0:
            st.warning("⚠️ Rota operando em prejuízo, apesar de possível viabilidade legal.")
        else:
            st.success("✅ Rota Viável e dentro do piso mínimo da ANTT.")

    else:
        st.info("Insira as quilometragens para visualizar os cálculos da viagem.")

if __name__ == "__main__":
    main()
