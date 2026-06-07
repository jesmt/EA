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
# ETAPA 4: A MÁGICA DA ÁLGEBRA (Otimização sem Derivadas)
# =====================================================================
elif etapa == "4. Resultado":
    st.title("✨ A Prova Matemática: Otimização com Álgebra")
    st.markdown("""
    Nós observamos na tabela que o menor valor parece ocorrer quando $a=4$ e $b=4$. Mas em matemática, não podemos confiar apenas no "olhômetro" ou na intuição de que "por ser simétrico, deve ser igual". Precisamos provar!
    
    A grande sacada aqui é que podemos encontrar esse ponto de mínimo absoluto sem usar nenhuma matemática de faculdade (Cálculo). Vamos usar apenas o que aprendemos no **1º Ano do Ensino Médio**: Equação do 2º Grau!
    """)
    
    st.markdown("---")

    # --- PASSO 1: SOMA E PRODUTO ---
    st.info("🤔 **Investigação 1:** Vamos voltar à equação da nossa restrição (o poste). Se multiplicarmos toda a equação pelo MMC ($ab$), o que acontece com a relação entre $a$ e $b$?")
    
    with st.expander("👉 Revelar a Dedução: Soma e Produto", expanded=False):
        st.markdown("A partir da nossa restrição do poste, vamos manipular a fração:")
        st.latex(r"\frac{2}{a} + \frac{2}{b} = 1")
        st.markdown("Multiplicando todos os termos por $ab$ (para sumir com os denominadores):")
        st.latex(r"2b + 2a = ab \implies \mathbf{ab = 2(a + b)}")
        
        st.markdown("""
        Olhe com atenção para essa última equação. Ela nos diz que a **multiplicação** de $a$ e $b$ é igual ao dobro da **soma** deles! 
        Se chamarmos a soma de **$S$** ($S = a+b$) e o produto de **$P$** ($P = ab$), acabamos de descobrir que:
        """)
        st.latex(r"\mathbf{P = 2S}")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- PASSO 2: A EQUAÇÃO DO 2º GRAU ---
    st.info("🤔 **Investigação 2:** Na álgebra, se conhecemos a Soma ($S$) e o Produto ($P$) de dois números, sabemos que eles são as raízes de uma equação do 2º grau: $x^2 - Sx + P = 0$. O que acontece se trocarmos o $P$ por $2S$ nessa equação?")
    
    with st.expander("👉 Revelar a Dedução: O Delta de Bhaskara", expanded=False):
        st.markdown("Substituindo $P = 2S$ na equação genérica, descobrimos que os nossos pedaços de muro ($a$ e $b$) são as raízes desta exata equação:")
        st.latex(r"x^2 - Sx + 2S = 0")
        
        st.markdown("""
        Para que os muros $a$ e $b$ existam no mundo real (como distâncias físicas), essa equação **precisa ter raízes reais**. 
        Qual é a regra de Bhaskara para que existam raízes reais? O discriminante (Delta) tem que ser maior ou igual a zero! ($\Delta \ge 0$)
        """)
        
        st.latex(r"\Delta = (-S)^2 - 4 \cdot 1 \cdot (2S) \ge 0")
        st.latex(r"\mathbf{S^2 - 8S \ge 0}")
        
        st.markdown("Como as distâncias são positivas ($S > 0$), podemos dividir por $S$:")
        st.latex(r"S - 8 \ge 0 \implies \mathbf{S \ge 8}")
        
        st.success("🚨 **Descoberta Incrível:** Nós acabamos de provar matematicamente que a **menor soma possível** para os dois pedaços de rede amarrados no muro ($a+b$) é 8 metros!")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- PASSO 3: O GOLPE FINAL ---
    st.info("🤔 **Investigação 3:** Nós queremos a situação de menor gasto possível, ou seja, o limite extremo onde a soma é mínima ($S = 8$). Mas lembre-se da aula de Bhaskara: o que acontece com as duas raízes de uma equação quando o Delta é exatamente ZERO?")
    
    with st.expander("👉 Revelar a Prova Final: Por que a = b?", expanded=False):
        st.markdown("Se escolhermos a soma mínima ($S = 8$), o nosso cálculo do passo anterior fica:")
        st.latex(r"\Delta = 8^2 - 8(8) = 64 - 64 = 0")
        
        st.markdown("""
        Quando $\Delta = 0$, a fórmula de Bhaskara nos dá **duas raízes idênticas** ($x_1 = x_2$). 
        Como as nossas raízes são $a$ e $b$, isso PROVA, sem sombra de dúvidas, que no ponto de menor custo, obrigatoriamente:
        """)
        st.latex(r"\mathbf{a = b}")
        
        st.markdown("Se a soma deles é 8 ($a + b = 8$) e eles são iguais:")
        st.latex(r"\mathbf{a = 4 \quad \text{e} \quad b = 4}")
        
        st.success("🎉 **Vencemos a Otimização!** Provamos de forma irrefutável que a configuração mais econômica exige $a=4$ e $b=4$.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- CONCLUSÃO E GRÁFICO ---
    st.markdown("### 🏆 O Resultado Final para o Grêmio")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("Agora que temos a prova algébrica de que $a=4$ e $b=4$, basta jogar na fórmula original de Pitágoras para descobrirmos o tamanho exato da rede de proteção a ser comprada:")
        st.latex(r"L = \sqrt{a^2 + b^2}")
        st.latex(r"L = \sqrt{4^2 + 4^2}")
        st.latex(r"L = \sqrt{16 + 16} = \sqrt{32}")
        st.latex(r"\mathbf{L \approx 5.65 \text{ metros}}")
        st.info("Parabéns! Vocês acabaram de resolver um problema complexo de otimização de engenharia utilizando apenas as propriedades da parábola do 1º ano do Ensino Médio!")
        
    with col2:
        # Gráfico final da rede posicionada
        import matplotlib.pyplot as plt
        import numpy as np
        fig_final, ax_final = plt.subplots(figsize=(5, 4))
        
        ax_final.axhline(0, color='black', linewidth=1)
        ax_final.axvline(0, color='black', linewidth=1)
        ax_final.set_xlim(-1, 6)
        ax_final.set_ylim(-1, 6)
        ax_final.grid(True, linestyle='--', alpha=0.5)
        
        # Muros
        ax_final.plot([0, 5], [0, 0], color='gray', linewidth=4, label="Muro Horizontal")
        ax_final.plot([0, 0], [0, 5], color='gray', linewidth=4, label="Muro Vertical")
        
        # A rede ótima
        ax_final.plot([4, 0], [0, 4], color='magenta', linewidth=3, label="Rede de Proteção Ótima")
        
        # Poste e pontos
        ax_final.plot(2, 2, 'ko', markersize=8)
        ax_final.text(2.2, 2.2, "Poste P(2,2)", fontweight='bold')
        ax_final.plot(4, 0, 'mo', markersize=6)
        ax_final.text(3.5, 0.3, "a = 4")
        ax_final.plot(0, 4, 'mo', markersize=6)
        ax_final.text(0.2, 4.2, "b = 4")
        
        ax_final.set_title("O Posicionamento Perfeito", fontweight='bold')
        ax_final.legend(loc='upper right', fontsize=8)
        
        st.pyplot(fig_final, use_container_width=True)
