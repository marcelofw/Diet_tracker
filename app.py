import streamlit as st
import pandas as pd
import datetime

META_CALORIAS = 2400
META_PROTEINAS = 110
META_GORDURAS = 70

# Faz a leitura do banco de dados de alimento e do diário
def inicializar_dados():
    try:
        alimentos = pd.read_csv('alimentos.csv')
    except FileNotFoundError:
        dados = {'alimento': ['Arroz', 'Banana'],
                 'quantidade': [100, 100],
                 'energia (kcal)': [130, 109],
                 'carboidratos (g)': [30, 26.7],
                 'proteinas (g)': [2.38, 1.27],
                 'gorduras (g)': [0.41, 0.19]}
        alimentos = pd.DataFrame(dados)
        alimentos.to_csv('alimentos.csv', index=False)
    try:
        diario = pd.read_csv('diario.csv')
    except FileNotFoundError:
        diario = pd.DataFrame(columns=['data', 'tipo_refeicao', 'alimento','quantidade', 'energia (kcal)', 'carboidratos (g)', 'proteinas (g)', 'gorduras (g)'])
        diario.to_csv('diario.csv', index=False)

    return alimentos, diario

# Cadastra alimentos ao banco de dados de alimentos (alimentos.csv)
def cadastrar_alimento(nome_alimento, quant, cal, carb, prot, gord):
    alimentos, _ = inicializar_dados()

    novo_alimento = {
        'alimento': nome_alimento,
        'quantidade': quant,
        'energia (kcal)': cal,
        'carboidratos (g)': carb,
        'proteinas (g)': prot,
        'gorduras (g)': gord
    }

    alimentos = pd.concat([alimentos, pd.DataFrame([novo_alimento])], ignore_index=True)
    alimentos.to_csv('alimentos.csv', index=False)
    return "Alimento cadastrado com sucesso!"

# Adiciona alimentos ao diário
def add_alimento_ao_diario(tipo_refeicao, nome_alimento, quant):
    alimentos, diario = inicializar_dados()
    
    alimento_info = alimentos[alimentos['alimento'] == nome_alimento]
    if alimento_info.empty:
        return "Alimento não encontrado na base de dados!"

    alimento_info = alimento_info.iloc[0]
    quantidade_cadastrada = alimento_info['quantidade']

    fator = quant / quantidade_cadastrada

    nova_refeicao = {
        'data': datetime.date.today().strftime('%d/%m/%Y'),
        'tipo_refeicao': tipo_refeicao,
        'alimento': nome_alimento,
        'quantidade': quant,
        'energia (kcal)': round(alimento_info['energia (kcal)'] * fator, 2),
        'carboidratos (g)': round(alimento_info['carboidratos (g)'] * fator, 2),
        'proteinas (g)': round(alimento_info['proteinas (g)'] * fator, 2),
        'gorduras (g)': round(alimento_info['gorduras (g)'] * fator, 2)
    }

    diario = pd.concat([diario, pd.DataFrame([nova_refeicao])], ignore_index=True)

    diario.to_csv('diario.csv', index=False)

    return f"Sucesso! {nome_alimento} adicionado ao diário."

#Somatório dos alimentos consumidos no dia
def resumo_do_dia():
    _, diario = inicializar_dados()
    hoje = datetime.date.today().strftime('%d/%m/Y')
    diario_hoje = diario[diario['data'] == hoje]
    totais = diario_hoje[['energia (kcal)', 'carboidratos (g)', 'proteinas (g)', 'gorduras (g)']].sum()
    faltas = {
        'Calorias restantes': META_CALORIAS - totais['energia (kcal)'],
        'Proteínas restantes': META_PROTEINAS - totais['proteinas (g)'],
        'Gorduras restantes': META_GORDURAS - totais['gorduras (g)']
    }
    return totais, faltas

#Status diário
def exibir_status_diario():
    totais = resumo_do_dia()
    print(f"Calorias: {totais['energia (kcal)']} / {META_CALORIAS}")
    print(f"Proteinas: {totais['proteinas (g)']} / {META_PROTEINAS}")
    print(f"Gorduras: {totais['gorduras (g)']} / {META_GORDURAS}")

st.title('Diet tracker')

aba1, aba2 = st.tabs(['Diário', 'Cadastrar Alimento'])

with aba1:
    st.header('O que você comeu hoje?')
    alimentos, diario = inicializar_dados()

    col1, col2, col3 = st.columns(3)
    with col1:
        refeicao = st.selectbox('Refeição', ['Café da manhã', 'Almoço', 'Janta'])
    with col2:
        alimento = st.selectbox('Alimento', alimentos['alimento'].unique())
    with col3:
        quantidade = st.number_input('Quantidade', min_value = 1)

    if st.button('Lançar no Diário'):
        mensagem = add_alimento_ao_diario(refeicao, alimento, quantidade)
        st.success(mensagem)

with aba2:
    st.header('Novo Alimento no Cardápio')
    cadastrar_alimento()



















