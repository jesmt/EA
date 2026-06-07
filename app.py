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
```python
# ETAPA 4: RESULTADO E INTERPRETAÇÃO
elif etapa == "4. Resultado":

    st.title("🏆 O Que a Matemática Nos Mostrou?")

    st.markdown("""
    Ao longo desta atividade, transformamos um problema real em um problema matemático.

    Nosso objetivo era descobrir qual posição da rede utiliza a menor quantidade possível de material.
    """)

    st.latex(r"L(a)=\sqrt{a^2+\left(\frac{2a}{a-1}\right)^2}")

    st.markdown("""
    Para encontrar essa posição, construímos tabelas, realizamos testes e analisamos o comportamento da função.
    """)

    # -------------------------------------------------------
    # GEOGEBRA
    # -------------------------------------------------------

    st.subheader("📈 O gráfico da função")

    geogebra_url = "https://www.geogebra.org/material/iframe/id/nypq2fcu/width/800/height/500/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/true/ctl/true"

    st.markdown(f"""
    <div style="width: 100%; max-width: 800px; margin: 0 auto;">
        <div style="position: relative; padding-bottom: 62.5%; height: 0;">
            <iframe src="{geogebra_url}"
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
                    allowfullscreen>
            </iframe>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("""
    Observe a curva vermelha.

    Ela representa os valores possíveis para o nosso problema.

    Antes de continuar, tente responder às perguntas abaixo apenas observando o gráfico.
    """)

    # -------------------------------------------------------
    # QUIZ INTERATIVO
    # -------------------------------------------------------

    resposta = st.radio(
        "Qual das afirmações descreve melhor o comportamento da curva?",
        [
            "O comprimento da rede só aumenta.",
            "O comprimento da rede só diminui.",
            "Existe um ponto onde o comprimento é mínimo.",
            "O gráfico representa uma reta."
        ]
    )

    if resposta == "Existe um ponto onde o comprimento é mínimo.":

        st.success("""
        Excelente!

        A curva primeiro desce, atinge um ponto mais baixo e depois volta a subir.

        Isso significa que existe uma posição ideal para instalar a rede.
        """)

    elif resposta:

        st.error("""
        Observe novamente a curva vermelha.

        Perceba que ela diminui, atinge um valor mínimo e depois volta a crescer.
        """)

    # -------------------------------------------------------
    # LEITURA DO GRÁFICO
    # -------------------------------------------------------

    st.subheader("🔍 O que o gráfico revela?")

    st.markdown("""
    Ao analisar a curva observamos três fatos importantes:

    **1️⃣ A rede fica cada vez menor**

    Quando aumentamos o valor de **a** logo após 1, o comprimento da rede diminui rapidamente.

    **2️⃣ Existe um ponto mais baixo**

    Em determinado momento a curva atinge seu menor valor.

    Esse é o ponto de mínimo da função.

    **3️⃣ Depois a rede volta a crescer**

    Continuar aumentando **a** não gera economia.

    Pelo contrário: a quantidade de material necessária volta a aumentar.
    """)

    # -------------------------------------------------------
    # CONEXÃO COM A TABELA
    # -------------------------------------------------------

    st.subheader("📊 Ligando o gráfico aos testes")

    st.success("""
    O mais interessante é que nós já havíamos percebido esse comportamento antes mesmo de visualizar o gráfico completo.

    A tabela construída durante a investigação mostrava exatamente a mesma tendência:

    ✔ os valores diminuíam;

    ✔ chegavam a uma região de mínimo;

    ✔ depois voltavam a crescer.

    O gráfico apenas tornou esse comportamento mais fácil de enxergar.
    """)

    # -------------------------------------------------------
    # O QUE APRENDEMOS
    # -------------------------------------------------------

    st.subheader("🎯 O que aprendemos?")

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
        ✔ Equação da reta

        ✔ Equação segmentária

        ✔ Distância entre pontos
        """)

    with col2:
        st.success("""
        ✔ Construção de tabelas

        ✔ Interpretação de gráficos

        ✔ Análise de mínimos
        """)

    st.info("""
    Utilizando apenas ferramentas do Ensino Médio, conseguimos determinar a forma mais econômica de instalar a rede.
    """)

    # -------------------------------------------------------
    # CURIOSIDADE MATEMÁTICA
    # -------------------------------------------------------

    with st.expander("✨ Curiosidade: existe uma resposta exata?"):

        st.markdown("""
        Nossa investigação localizou com bastante precisão a região onde ocorre o mínimo da função.

        Em cursos mais avançados existe uma ferramenta chamada **Cálculo Diferencial**, capaz de confirmar matematicamente esse resultado.
        """)

        a_exato = 1 + np.cbrt(4)
        b_exato = (2 * a_exato) / (a_exato - 1)
        dist_exato = np.sqrt(a_exato**2 + b_exato**2)

        st.latex(r"a = 1+\sqrt[3]{4}")

        st.metric(
            "Valor aproximado de a",
            f"{a_exato:.3f} m"
        )

        st.metric(
            "Comprimento mínimo da rede",
            f"{dist_exato:.2f} m"
        )

        st.success("""
        Observe que esse valor aparece exatamente na região identificada por nós através da análise da tabela e do gráfico.

        Ou seja: a investigação realizada pela turma chegou muito perto da solução matemática exata.
        """)
```
