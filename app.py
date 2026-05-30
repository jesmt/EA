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

    st.image("diagrama.jpg", caption="Esquema da quadra e a rede de proteção.", width=500)
    
    st.subheader("Simulador Interativo")
    # AQUI VOCÊ COLOCA O LINK DE INCORPORAÇÃO DO SEU GEOGEBRA
    # Substitua a string abaixo pelo link gerado no site do GeoGebra (Compartilhar > Incorporar)
    geogebra_url = "https://www.geogebra.org/material/iframe/id/fpy3pppp/width/800/height/500/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/true/rc/false/ld/false/sdz/true/ctl/false" 
    components.iframe(geogebra_url, width=800, height=500)
    
    st.warning("O que acontece com o tamanho da rede se amarrarmos a ponta muito longe da esquina?")

# ETAPA 2: MODELAGEM
elif etapa == "2. A Lousa Digital (Modelagem)":
    st.title("📐 Colocando no Papel")
    st.markdown("Para descobrir o valor exato sem ficar apenas no 'olhômetro', precisamos traduzir o desenho da rede e dos muros para a linguagem da Matemática.")
    
    # Criamos uma "memória" para saber em qual passo da explicação a aula está
    if 'passo_aula' not in st.session_state:
        st.session_state.passo_aula = 0

    st.info("🤔 **Pergunta para a turma:** Se os muros formam um ângulo de 90 graus (como os eixos X e Y), e a rede é uma linha reta que cruza esses muros, alguém lembra de alguma equação que represente uma reta cortando os eixos?")

    # O botão avança o estado da aula para o passo 1
    if st.button("Revelar Passo 1: A Equação da Reta"):
        st.session_state.passo_aula = 1

    # Se o passo for 1 ou maior, mostra este bloco (assim ele não some mais!)
    if st.session_state.passo_aula >= 1:
        st.markdown("### Passo 1: A Forma Segmentária")
        st.markdown("""
        Como nós sabemos exatamente onde a rede encosta nos muros — nos pontos **A(a,0)** do muro horizontal e **B(0,b)** do muro vertical —, a maneira mais prática de descrever essa reta é usando a **Equação Segmentária da Reta**:
        """)
        st.latex(r"\frac{x}{a} + \frac{y}{b} = 1")
        
        st.warning("🗣️ **Discussão:** Muito bem, mas a rede não pode ser amarrada em qualquer lugar solta pelo pátio. Ela tem um obstáculo obrigatório. Qual é e como colocamos isso na fórmula?")

        if st.button("Revelar Passo 2: O Poste Central"):
            st.session_state.passo_aula = 2

    if st.session_state.passo_aula >= 2:
        st.markdown("### Passo 2: Passando pelo poste P(1,2)")
        st.markdown("A rede tem que encostar no poste central. Isso significa que o ponto $P(1,2)$ *pertence* à reta. Então, podemos substituir o $x$ por 1 e o $y$ por 2 na nossa equação:")
        st.latex(r"\frac{1}{a} + \frac{2}{b} = 1")
        st.markdown("Isolando o $b$, descobrimos que a posição em que a rede é amarrada no muro vertical ($b$) depende diretamente da posição do muro horizontal ($a$):")
        st.latex(r"b = \frac{2a}{a - 1}")

        st.error("💡 **Pergunta Final:** Agora sabemos onde ficam as pontas da rede. Mas o nosso problema é o orçamento! Precisamos saber o *comprimento* da rede. Que figura geométrica o chão, os muros e a rede formam?")

        if st.button("Revelar Passo 3: O Comprimento da Rede"):
            st.session_state.passo_aula = 3

    if st.session_state.passo_aula >= 3:
        st.markdown("### Passo 3: Pitágoras e a Fórmula da Distância")
        st.markdown("Eles formam um Triângulo Retângulo! Pelo Teorema de Pitágoras, o comprimento total da rede (que é a nossa hipotenusa $AB$) será:")
        st.latex(r"AB = \sqrt{a^2 + b^2}")
        st.markdown("Como nós já sabemos lá do Passo 2 que o $b$ vale $\\frac{2a}{a-1}$, nós substituímos para ter uma fórmula com uma única variável:")
        st.latex(r"AB(a) = \sqrt{a^2 + \left(\frac{2a}{a - 1}\right)^2}")
        
        st.success("Pronto! Agora temos a modelagem matemática completa. Podemos ir para a próxima etapa testar os valores!")
        
        # Botão opcional para o professor esconder tudo e começar de novo se precisar
        if st.button("🔄 Reiniciar Lousa"):
            st.session_state.passo_aula = 0
            st.rerun() # Atualiza a tela imediatamente

# ETAPA 3: TESTES
elif etapa == "3. Mão na Massa (Testes)":
    st.title("🧪 Laboratório de Testes Numéricos")
    st.markdown("""
    Chegou a hora de tentar poupar o dinheiro do grêmio! 
    Mandem no chat valores para **$a$** (a distância no muro horizontal onde vamos amarrar a primeira ponta da rede). Lembrem-se que esse valor tem que ser maior que 1.
    
    Vamos observar a tabela com atenção: **o tamanho da rede está diminuindo ou aumentando?**
    """)
    
    col1, col2 = st.columns([1.2, 1.2])
    
    with col1:
        # Entrada de dados
        palpite_a = st.number_input("Digite um valor para 'a':", min_value=1.1, max_value=15.0, value=2.0, step=0.1)
        
        if st.button("Testar Palpite"):
            # Cálculos
            b = (2 * palpite_a) / (palpite_a - 1)
            distancia = np.sqrt(palpite_a**2 + b**2)
            
           # --- NOVIDADE: MOSTRANDO A SUBSTITUIÇÃO NA TELA ---
            st.success(rf"""
            Veja o cálculo para o palpite **a = {palpite_a}**:
            
            $b = \frac{{2 \cdot {palpite_a}}}{{{palpite_a} - 1}} = {b:.2f} \text{{ m}}$
            
            $AB = \sqrt{{{palpite_a}^2 + {b:.2f}^2}} = {distancia:.2f} \text{{ m}}$
            """)
            st.markdown("---")
            
            
            # Criando um novo registro
            novo_dado = pd.DataFrame({
                'Palpite (a)': [round(palpite_a, 2)],
                'Valor de b (m)': [round(b, 2)],
                'Distância da Rede (m)': [round(distancia, 2)]
            })
            
            # Adicionando ao histórico do session_state
            st.session_state.historico = pd.concat([st.session_state.historico, novo_dado], ignore_index=True)
            # Ordenando a tabela pelo valor de 'a' para fazer sentido na leitura
            st.session_state.historico = st.session_state.historico.sort_values(by='Palpite (a)')
            
    with col2:
        st.subheader("Tabela de Resultados")
        st.dataframe(st.session_state.historico, use_container_width=True)
        
    st.markdown("---")
    
    # O PULO DO GATO PEDAGÓGICO: O gráfico só aparece depois de 3 testes!
    quantidade_testes = len(st.session_state.historico)
    
    if quantidade_testes > 0 and quantidade_testes < 3:
        st.info(f"📌 Vocês já fizeram {quantidade_testes} teste(s). Continuem dando palpites! Precisamos de pelo menos 3 testes diferentes para conseguir visualizar o que está acontecendo com o tamanho da rede.")
        
    elif quantidade_testes >= 3:
        st.subheader("📉 Rastreador de Tamanho (Gráfico)")
        st.markdown("""
        Olhar apenas para números numa tabela pode ser confuso. Vamos colocar esses tamanhos que vocês descobriram num gráfico. 
        
        **Como ler esse gráfico:** Imaginem que isso é uma montanha-russa do nosso orçamento. Percebam que a linha desce (estamos economizando rede) até chegar num "fundo do poço", e depois volta a subir (estamos gastando mais de novo). 
        
        O nosso objetivo é encontrar exatamente os valores que nos deixam lá no ponto mais baixo!
        """)
        
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
