import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

# Configuração da página para ficar mais larga e com título
st.set_page_config(page_title="Otimização: A Rede da Cantina", layout="wide")

# Inicializando o "Session State" para guardar os palpites da turma sem apagar a tabela
if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame(columns=['Palpite (a)', 'Valor de b (m)', 'Distância da Rede (m)'])

# BARRA LATERAL (Controle da Professora)
st.sidebar.title("Roteiro da Aula")
etapa = st.sidebar.radio(
    "Navegação:",
    ["1. A Missão (O Problema)", 
     "2. A Lousa Digital (Modelagem)", 
     "3. Mão na Massa (Testes)", 
     "4. A Mágica do Cálculo"]
)

st.sidebar.markdown("---")
st.sidebar.info("Dica para a prof: Use as setas do teclado para avançar pelas etapas sem precisar clicar no menu durante o Meet.")

# ETAPA 1: A MISSÃO
if etapa == "1. A Missão (O Problema)":
    st.title("🏐 Salvando as Janelas da Cantina")
    st.markdown("""
    A quadra de esportes da escola fica numa área onde duas muretas se encontram (formando nossos eixos $x$ e $y$). 
    Durante os jogos, a bola frequentemente voa e atinge as janelas da cantina. 
    
    Para resolver isso, vamos instalar uma **rede de proteção em linha reta**. Existe um poste de iluminação no meio da área, 
    localizado no ponto **P(1, 2)**, e a rede precisa passar exatamente apoiada nele para não ceder com o vento.
    
    A rede é vendida por metro. Para que o grêmio consiga pagar, **como devemos posicioná-la para usar o menor comprimento possível?**
    """)
    
    st.subheader("Simulador Interativo")
    # AQUI VOCÊ COLOCA O LINK DE INCORPORAÇÃO DO SEU GEOGEBRA
    # Substitua a string abaixo pelo link gerado no site do GeoGebra (Compartilhar > Incorporar)
    geogebra_url = "https://www.geogebra.org/material/iframe/id/fpy3pppp/width/800/height/500/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/true/rc/false/ld/false/sdz/true/ctl/false" 
    components.iframe(geogebra_url, width=800, height=500)
    
    st.warning("Pergunte no chat do Meet: O que acontece com o tamanho da rede se amarrarmos a ponta muito longe da esquina?")

# ETAPA 2: MODELAGEM
elif etapa == "2. A Lousa Digital (Modelagem)":
    st.title("📐 Colocando no Papel")
    st.markdown("Para descobrir o valor exato sem ficar apenas no 'olhômetro', precisamos de uma equação que garanta que a rede (reta) encoste no poste $P(1,2)$.")
    
    if st.button("Passo 1: A Equação da Reta"):
        st.latex(r"\frac{x}{a} + \frac{y}{b} = 1")
        st.markdown("Sabemos que a reta corta os muros nos pontos $A(a,0)$ e $B(0,b)$.")

    if st.button("Passo 2: Passando pelo poste P(1,2)"):
        st.latex(r"\frac{1}{a} + \frac{2}{b} = 1")
        st.markdown("Substituímos o $x$ por 1 e o $y$ por 2. Isolando o $b$, descobrimos que a posição no muro vertical depende do muro horizontal:")
        st.latex(r"b = \frac{2a}{a - 1}")

    if st.button("Passo 3: A Fórmula da Distância"):
        st.markdown("Pelo Teorema de Pitágoras, o comprimento total da rede ($AB$) será:")
        st.latex(r"AB = \sqrt{a^2 + b^2} \implies AB = \sqrt{a^2 + \left(\frac{2a}{a - 1}\right)^2}")

# ETAPA 3: TESTES
elif etapa == "3. Mão na Massa (Testes)":
    st.title("🧪 Laboratório de Testes Numéricos")
    st.markdown("Agora é com vocês! Mandem no chat valores para $a$ (posição no muro horizontal, deve ser maior que 1). Vamos ver onde a rede fica menor!")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Entrada de dados
        palpite_a = st.number_input("Digite um valor para 'a':", min_value=1.1, max_value=15.0, value=2.0, step=0.1)
        
        if st.button("Testar Palpite"):
            # Cálculos
            b = (2 * palpite_a) / (palpite_a - 1)
            distancia = np.sqrt(palpite_a**2 + b**2)
            
            # Criando um novo registro
            novo_dado = pd.DataFrame({
                'Palpite (a)': [round(palpite_a, 2)],
                'Valor de b (m)': [round(b, 2)],
                'Distância da Rede (m)': [round(distancia, 2)]
            })
            
            # Adicionando ao histórico do session_state
            st.session_state.historico = pd.concat([st.session_state.historico, novo_dado], ignore_index=True)
            # Ordenando a tabela pelo valor de 'a' para o gráfico ficar bonito
            st.session_state.historico = st.session_state.historico.sort_values(by='Palpite (a)')
            
    with col2:
        st.subheader("Tabela de Resultados")
        st.dataframe(st.session_state.historico, use_container_width=True)
        
    st.markdown("---")
    if not st.session_state.historico.empty:
        st.subheader("Comportamento da Distância (Gráfico)")
        # Plotando a curva baseada nos testes
        chart_data = st.session_state.historico.set_index('Palpite (a)')['Distância da Rede (m)']
        st.line_chart(chart_data)

# ETAPA 4: A MÁGICA DO CÁLCULO
elif etapa == "4. A Mágica do Cálculo":
    st.title("✨ A Mágica do Cálculo Diferencial")
    st.markdown("""
    Vocês perceberam que, testando valores na tabela, a distância diminui, chega num "fundo do poço" e depois volta a subir. 
    Fazer isso por tentativa e erro é o que chamamos de **Força Bruta**.
    
    Mas a Matemática Superior tem uma ferramenta chamada **Derivada**. Ela funciona como um radar que encontra esse "fundo do poço" instantaneamente!
    """)
    
    if st.button("Revelar o Valor Exato"):
        st.success("O valor exato descoberto pelo Cálculo é: **a ≈ 2,587**")
        
        b_exato = (2 * 2.587) / (2.587 - 1)
        dist_exato = np.sqrt(2.587**2 + b_exato**2)
        
        col1, col2 = st.columns(2)
        col1.metric("Posição em A (muro horizontal)", "2.587 m")
        col2.metric("Posição em B (muro vertical)", f"{b_exato:.2f} m")
        
        st.info(f"🏆 O comprimento MÍNIMO possível para a rede é de **{dist_exato:.2f} metros**!")
        st.markdown("*(Volte ao GeoGebra na Etapa 1, coloque 'a = 2.59' e confirme visualmente que é ali que a rede fica mais esticada e curta!)*")