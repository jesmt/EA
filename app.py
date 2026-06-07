import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Otimização: A Rede da Cantina", layout="wide")

if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame(columns=['Palpite (a)', 'Valor de b (m)', 'Distância da Rede (m)'])

# BARRA LATERAL
st.sidebar.title("Roteiro da Aula")
etapa = st.sidebar.radio(
    "Navegação:",
    ["1. O Problema", 
     "2. Modelagem", 
     "3. Testes", 
     "4. Resultado"]
)
st.sidebar.markdown("---")

# =====================================================================
# ETAPA 1: O PROBLEMA (Adaptado para P(2,2))
# =====================================================================
if etapa == "1. O Problema":
    st.title("🏐 Salvando as Janelas da Cantina")
    st.markdown("""
    No recreio, durante os jogos no pátio da escola, a bola frequentemente voa e atinge as janelas da cantina. 
    
    Para resolver isso, pretende-se instalar uma **rede de proteção em linha reta**. Existe um poste de iluminação no meio da área, 
    localizado exatamente na coordenada **P(2, 2)** (ou seja, a 2 metros de distância de cada muro). A rede precisa passar exatamente apoiada nele para não ceder com o vento.
    
    A rede é vendida por metro. Para que o grêmio consiga pagar, **como devemos posicioná-la nos muros para usar o menor comprimento possível?**
    """)
    
    try:
        img = Image.open("diagrama.jpg")
        st.image(img, caption="Esquema da quadra e a rede de proteção.", width=500)
    except:
        st.info("(Professor: Certifique-se de que a imagem diagrama.jpg está na mesma pasta)")
    
    st.subheader("Simulador Interativo")
    geogebra_url = "https://www.geogebra.org/material/iframe/id/fpy3pppp/width/800/height/500/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/true/rc/false/ld/false/sdz/true/ctl/false" 
    components.iframe(geogebra_url, width=800, height=500)
    
    st.warning("O que acontece com o tamanho da rede se amarrarmos a ponta muito longe da esquina?")

# =====================================================================
# ETAPA 2: MODELAGEM (Matemática adaptada para o P(2,2))
# =====================================================================
elif etapa == "2. Modelagem":
    st.title("📐 A Modelagem Matemática (Investigação)")
    st.markdown("Vamos construir a solução passo a passo. **Tente responder mentalmente às perguntas antes de clicar para revelar!**")

    # --- PASSO 1 ---
    st.info("🤔 **Pergunta 1:** Se adotarmos o canto dos muros como a origem $(0,0)$, sabemos que a rede cruza o muro horizontal em uma distância **$a$** e o muro vertical em **$b$**. Baseado no que estudamos, qual é a ferramenta matemática perfeita para descrever uma reta conhecendo seus interceptos?")

    with st.expander("👉 Revelar a Resposta: Escolhendo o Modelo Espacial", expanded=False):
        st.success("A **Equação Segmentária da Reta**! 🎯")
        st.markdown("Os interceptos são exatamente $a$ e $b$. A equação da nossa rede será:")
        st.latex(r"\frac{x}{a} + \frac{y}{b} = 1")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- PASSO 2 ---
    st.info("🤔 **Pergunta 2:** A rede tem que obrigatoriamente encostar no **poste**, que está em **P(2,2)**. Geometricamente, se um ponto pertence a uma reta, o que fazemos com a equação?")

    with st.expander("👉 Revelar a Resposta: A Restrição do Poste", expanded=False):
        st.success("Nós **substituímos** as coordenadas do poste na equação da reta! 🎯")
        st.markdown("Trocando $x=2$ e $y=2$:")
        st.latex(r"\frac{2}{a} + \frac{2}{b} = 1")
        
        st.markdown("Para otimizar, precisamos isolar o $b$ e ver como o muro vertical depende do horizontal:")
        st.latex(r"\frac{2}{b} = 1 - \frac{2}{a} \implies \frac{2}{b} = \frac{a - 2}{a}")
        st.markdown("Multiplicando cruzado:")
        st.latex(r"\mathbf{b = \frac{2a}{a - 2}}")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- PASSO 3 ---
    st.info("🤔 **Pergunta 3:** O objetivo é minimizar o **comprimento da rede**. Olhando de cima para os muros e a rede, qual figura se forma e como calculamos o lado maior?")

    with st.expander("👉 Revelar a Resposta: A Função do Comprimento", expanded=False):
        st.success("Forma-se um **Triângulo Retângulo** e usamos o **Teorema de Pitágoras**! 🎯")
        st.latex(r"L = \sqrt{a^2 + b^2}")
        
        st.markdown("Substituindo o $b$ que isolamos no passo anterior, fundimos tudo em uma Função Objetivo:")
        st.latex(r"\mathbf{L(a) = \sqrt{a^2 + \left(\frac{2a}{a - 2}\right)^2}}")
        st.markdown("Prossiga para a Etapa 3 para testar os valores!")

# =====================================================================
# ETAPA 3: TESTES (Ajustado o domínio para a > 2)
# =====================================================================
elif etapa == "3. Testes":
    st.title("🧪 Laboratório de Testes Numéricos")
    st.markdown("Mandem palpites para a distância **$a$** no muro horizontal. Como o poste está em 2m, a rede deve ir além dele, então **$a > 2$**.")
    
    col1, col2 = st.columns([1.2, 1.2])
    
    with col1:
        palpite_a = st.number_input("Digite um valor para 'a':", min_value=2.1, max_value=20.0, value=3.5, step=0.1)
        
        if st.button("Testar Palpite"):
            b = round((2 * palpite_a) / (palpite_a - 2), 2)
            distancia = round(np.sqrt(palpite_a**2 + b**2), 2)
            
            st.success(rf"""
            Veja o cálculo para **a = {palpite_a:.2f}**:
            $b = \frac{{2 \cdot {palpite_a:.2f}}}{{{palpite_a:.2f} - 2}} = {b} \text{{ m}}$
            $L = \sqrt{{{palpite_a:.2f}^2 + {b}^2}} = {distancia} \text{{ m}}$
            """)
            
            novo_dado = pd.DataFrame({'Palpite (a)': [round(palpite_a, 2)], 'Valor de b (m)': [b], 'Distância da Rede (m)': [distancia]})
            st.session_state.historico = pd.concat([st.session_state.historico, novo_dado], ignore_index=True)
            st.session_state.historico = st.session_state.historico.sort_values(by='Palpite (a)')
            
    with col2:
        st.subheader("Tabela de Resultados")
        st.dataframe(st.session_state.historico, use_container_width=True)
        
    st.markdown("---")
    
    quantidade_testes = len(st.session_state.historico)
    if quantidade_testes > 0 and quantidade_testes < 3:
        st.info("Façam pelo menos 3 testes diferentes para visualizarmos a curva!")
    elif quantidade_testes >= 3:
        st.subheader("📉 Rastreador de Tamanho (Gráfico)")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(st.session_state.historico['Palpite (a)'], st.session_state.historico['Distância da Rede (m)'], marker='o', color='royalblue')
        ax.set_title('Tamanho da Rede x Posição no Muro Horizontal', fontsize=12)
        ax.set_xlabel('Valor de a (metros)')
        ax.set_ylabel('Comprimento da Rede (metros)')
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)

# =====================================================================
# ETAPA 4: A MÁGICA PARA O ENSINO MÉDIO (Princípio da Simetria)
# =====================================================================
elif etapa == "4. Resultado":
    st.title("✨ A Matemática Resolve: O Segredo da Simetria")
    st.markdown("""
    Nós tentamos achar o "fundo do poço" testando números. Mas não precisamos de tentativa e erro, nem de Cálculo de faculdade! Podemos resolver isso usando pura lógica geométrica.
    """)
    
    st.info("🤔 **O Pulo do Gato:** Vocês repararam na coordenada do poste? Ele está em **$P(2,2)$**. O que isso significa em relação aos muros?")
    
    with st.expander("👉 Revelar o Raciocínio Geométrico (A Solução)", expanded=True):
        st.markdown("""
        O poste está **exatamente à mesma distância** do muro horizontal e do muro vertical (2 metros de cada). Isso significa que o nosso problema possui **Simetria Perfeita**.
        
        Na natureza e na matemática, quando as condições de um problema são perfeitamente simétricas, a configuração ótima (que gasta menos energia ou menor distância) também é simétrica!
        
        Logo, para o tamanho da rede ser o menor possível, a amarração nos muros deve ser igual:
        """)
        st.latex(r"\mathbf{a = b}")
        
        st.markdown("Voltando na nossa equação do Poste:")
        st.latex(r"\frac{2}{a} + \frac{2}{b} = 1")
        
        st.markdown("Como $a = b$, substituímos:")
        st.latex(r"\frac{2}{a} + \frac{2}{a} = 1 \implies \frac{4}{a} = 1 \implies \mathbf{a = 4}")
        
        st.success("Bingo! Se o menor caminho exige que $a=4$, consequentemente $b=4$.")
        
        st.markdown("Para descobrir a rede exata que o grêmio deve comprar, jogamos no nosso Pitágoras:")
        st.latex(r"L = \sqrt{4^2 + 4^2} = \sqrt{16 + 16} = \sqrt{32} \approx \mathbf{5.65 \text{ metros}}")
        
        st.markdown("*(Voltem à Tabela de Testes: Vejam se o palpite a=4 não foi exatamente o 'fundo do poço' da nossa montanha-russa!)*")
