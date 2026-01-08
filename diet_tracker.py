#%% 
import pandas as pd
import datetime

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
        diario = pd.DataFrame(columns=['data', 'tipo_refeicao', 'alimento',' quantidade', 'energia (kcal)', 'carboidratos (g)', 'proteinas (g)', 'gorduras (g)'])
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












# %%
