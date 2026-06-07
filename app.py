import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

# Configuração da página para ficar mais larga e com título
st.set_page_config(page_title="Otimização: A Rede da Cantina", layout="wide")

# Inicializando o "Session State" para guardar os palpites da turma sem apagar a tabela
if 'historico' not in st.session_state:
    st.session_state.historico = pd.DataFrame(columns=['Palpite (a)', 'Valor de b (m)', 'Distância da Rede (m)'])

# BARRA LATERAL (Controle da Professora)
st.sidebar.title("Roteiro da Aula")
etapa = st.sidebar.radio(
    "Navegação:",
    ["1. O Problema", 
     "2. Modelagem", 
     "3. Testes", 
     "4. Resultado"]
)

st.sidebar.markdown("---")

# ETAPA 1: A MISSÃO
if etapa == "1. O Problema":
    st.title("🏐 Salvando as Janelas da Cantina")
    st.markdown("""
   
    No recreio, durante os jogos no pátio da escola, a bola frequentemente voa e atinge as janelas da cantina. 
    
    Para resolver isso, pretende-se instalar uma **rede de proteção em linha reta**. Existe um poste de iluminação no meio da área, 
    localizado no ponto **P(1, 2)**, e a rede precisa passar exatamente apoiada nele para não ceder com o vento.
    
    A rede é vendida por metro. Para que o grêmio consiga pagar, **como devemos posicioná-la para usar o menor comprimento possível?**
    """)

    from PIL import Image
    
    img = Image.open("diagrama.jpg")
    st.image(img, caption="Esquema da quadra e a rede de proteção.", width=500)

    st.warning(" Mova o ponto **A** no simulador abaixo e verifique o que acontece com o tamanho da rede se amarrarmos a ponta muito longe da esquina.")


    st.subheader("Simulador")
    # AQUI VOCÊ COLOCA O LINK DE INCORPORAÇÃO DO SEU GEOGEBRA
    # Substitua a string abaixo pelo link gerado no site do GeoGebra (Compartilhar > Incorporar)
    geogebra_url = "https://www.geogebra.org/material/iframe/id/fpy3pppp/width/800/height/500/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/true/rc/false/ld/false/sdz/true/ctl/false" 
    components.iframe(geogebra_url, width=800, height=500)
    
    

# ETAPA 2: MODELAGEM
elif etapa == "2. Modelagem":
    st.title("📐 Revisão")
    st.markdown("Vamos fazer uma breve revisão sobre equação da reta antes de seguirmos para a análise do problema.")

    import matplotlib.pyplot as plt
    import numpy as np

    # =====================================================
    # FUNÇÕES AUXILIARES DE GRÁFICOS
    # =====================================================
    def setup_plot(ax, title=""):
        """Configura o visual padrão dos gráficos para manter o design limpo."""
        ax.axhline(0, color='black', linewidth=1.2)
        ax.axvline(0, color='black', linewidth=1.2)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_title(title, fontsize=11, fontweight='bold')
        return ax

    def plot_sarrus(matriz, legendas_azul, legendas_vermelha):
        """Função para desenhar a Regra de Sarrus igual ao material didático (TikZ)."""
        fig, ax = plt.subplots(figsize=(10, 3.5))
        ax.axis('off')
        ax.set_xlim(-4.5, 8.5)
        ax.set_ylim(-0.8, 2.8)

        # Textos da matriz
        for i in range(3):
            for j in range(5):
                ax.text(j, 2-i, f"${matriz[i][j]}$", ha='center', va='center', fontsize=16)

        # Barras do determinante
        ax.plot([-0.5, -0.5], [-0.5, 2.5], color='black', linewidth=2)
        ax.plot([2.5, 2.5], [-0.5, 2.5], color='black', linewidth=2)

        # Setas Azuis (Principais)
        for col in range(3):
            ax.annotate("", xy=(col+2.3, -0.3), xytext=(col-0.3, 2.3),
                        arrowprops=dict(arrowstyle="->", color="blue", alpha=0.3, lw=3))

        # Setas Vermelhas (Secundárias)
        for col in range(2, 5):
            ax.annotate("", xy=(col-2.3, -0.3), xytext=(col+0.3, 2.3),
                        arrowprops=dict(arrowstyle="->", color="red", alpha=0.3, lw=3))

        # Legendas
        for i in range(3):
            ax.text(4.5, 2-i, f"${legendas_azul[i]}$", color='blue', va='center', fontsize=12)
            ax.text(-1.0, 2-i, f"${legendas_vermelha[i]}$", color='red', ha='right', va='center', fontsize=12)

        plt.tight_layout()
        return fig

    # =====================================================
    # DIVISÃO 1: REVISÃO TEÓRICA PROGRESSIVA
    # =====================================================
    st.header("📚 Parte 1: Revisão Teórica")
    st.markdown("Vamos lembrar como as equações da reta são deduzidas e aplicadas geometricamente.")

    # --- 1. EQUAÇÃO GERAL ---
    with st.expander("1️⃣ A Equação Geral: $Ax + By + C = 0$", expanded=False):
        st.markdown("A **Equação Geral** é a representação mais abrangente. Todo ponto $P(x,y)$ que satisfaz a igualdade pertence à reta.")
        
        # ==========================================
        # 1. DEDUÇÃO GEOMÉTRICA
        # ==========================================
        st.markdown("#### 📐 Dedução Geométrica (Semelhança de Triângulos)")
        st.markdown("Para que os pontos $A(x_A, y_A)$, $B(x_B, y_B)$ e um ponto genérico $P(x, y)$ formem uma reta, eles devem ser colineares. Ao projetá-los, formamos triângulos retângulos semelhantes:")
        
        # Gráfico da Dedução Geométrica
        fig_geom, ax_geom = plt.subplots(figsize=(7, 4))
        ax_geom.set_xlim(0, 6); ax_geom.set_ylim(0, 5)
        
        # Reta principal
        ax_geom.plot([0.2, 6], [0.75 * 0.2 + 0.25, 0.75 * 6 + 0.25], color="black", linewidth=1.5)
        
        # Pontos A, B, P
        A, B, P = (1, 1), (3, 2.5), (5, 4)
        ax_geom.scatter([A[0], B[0], P[0]], [A[1], B[1], P[1]], color="black", zorder=5)
        ax_geom.text(A[0]-0.3, A[1]+0.2, "A", fontsize=12)
        ax_geom.text(B[0]-0.3, B[1]+0.2, "B", fontsize=12)
        ax_geom.text(P[0]-0.4, P[1]+0.2, "P(x,y)", fontsize=12)
        
        # Triângulos
        ax_geom.plot([A[0], B[0]], [A[1], A[1]], 'b-', lw=2.5) # Base 1
        ax_geom.plot([B[0], B[0]], [A[1], B[1]], 'b-', lw=2.5) # Altura 1
        ax_geom.plot([B[0], P[0]], [B[1], B[1]], color='teal', lw=2.5) # Base 2
        ax_geom.plot([P[0], P[0]], [B[1], P[1]], color='teal', lw=2.5) # Altura 2
        
        # Projeções nos eixos
        kwargs_proj = {'color': 'gray', 'linestyle': '--', 'alpha': 0.5}
        ax_geom.plot([A[0], 0], [A[1], A[1]], **kwargs_proj); ax_geom.plot([A[0], A[0]], [A[1], 0], **kwargs_proj)
        ax_geom.plot([B[0], 0], [B[1], B[1]], **kwargs_proj); ax_geom.plot([B[0], B[0]], [B[1], 0], **kwargs_proj)
        ax_geom.plot([P[0], 0], [P[1], P[1]], **kwargs_proj); ax_geom.plot([P[0], P[0]], [P[1], 0], **kwargs_proj)
        
        # Ajuste dos Eixos
        ax_geom.set_xticks([A[0], B[0], P[0]]); ax_geom.set_xticklabels(['$x_A$', '$x_B$', '$x$'], fontsize=12)
        ax_geom.set_yticks([A[1], B[1], P[1]]); ax_geom.set_yticklabels(['$y_A$', '$y_B$', '$y$'], fontsize=12)
        ax_geom.spines['top'].set_visible(False); ax_geom.spines['right'].set_visible(False)
        
        st.pyplot(fig_geom, use_container_width=True)
        
        st.markdown("Pela proporção entre as bases e alturas dos triângulos destacados, temos:")
        st.latex(r"\frac{x_B - x_A}{x - x_B} = \frac{y_B - y_A}{y - y_B}")
        st.markdown("Multiplicando cruzado e agrupando os termos de $x$ e $y$, obtemos a seguinte equação:")
        st.latex(r"x(y_A - y_B) + y(x_B - x_A) + (x_A y_B - x_B y_A) = 0")

        st.markdown("---")

        # ==========================================
        # 2. DEDUÇÃO POR DETERMINANTE
        # ==========================================
        st.markdown("#### 🔢 Dedução Algébrica (Matrizes)")
        st.markdown("A Álgebra Linear nos dá um 'atalho' para essa mesma conta. Para que três pontos estejam alinhados, o determinante de suas coordenadas deve ser zero. Aplicando a **Regra de Sarrus**:")
        
        matriz_gen = [['x', 'y', '1', 'x', 'y'], 
                      ['x_A', 'y_A', '1', 'x_A', 'y_A'], 
                      ['x_B', 'y_B', '1', 'x_B', 'y_B']]
        leg_azul_gen = [r'+ (x \cdot y_A \cdot 1) = +x y_A', 
                        r'+ (y \cdot 1 \cdot x_B) = +x_B y', 
                        r'+ (1 \cdot x_A \cdot y_B) = +x_A y_B']
        leg_verm_gen = [r'- (1 \cdot y_A \cdot x_B) = -x_B y_A', 
                        r'- (x \cdot 1 \cdot y_B) = -x y_B', 
                        r'- (y \cdot x_A \cdot 1) = -x_A y']
        st.pyplot(plot_sarrus(matriz_gen, leg_azul_gen, leg_verm_gen), use_container_width=True)
        st.latex(r"x(y_A-y_B) + y(x_B-x_A) + (x_Ay_B-x_By_A) = 0")

        st.markdown("---")
        
        # ==========================================
        # 3. EXEMPLO PRÁTICO
        # ==========================================
        st.markdown("#### ✍️ Exemplo Prático em um Caso Real")
        st.markdown("Qual a equação da reta que passa por **A(0,2)** e **B(3,0)**:")
        
        matriz_num = [['x', 'y', '1', 'x', 'y'], 
                      ['0', '2', '1', '0', '2'], 
                      ['3', '0', '1', '3', '0']]
        leg_azul_num = [r'+ (x \cdot 2 \cdot 1) = +2x', 
                        r'+ (y \cdot 1 \cdot 3) = +3y', 
                        r'+ (1 \cdot 0 \cdot 0) = 0']
        leg_verm_num = [r'- (1 \cdot 2 \cdot 3) = -6', 
                        r'- (x \cdot 1 \cdot 0) = 0', 
                        r'- (y \cdot 0 \cdot 1) = 0']
        st.pyplot(plot_sarrus(matriz_num, leg_azul_num, leg_verm_num), use_container_width=True)
        st.success("Somando os termos: $(2x + 3y + 0) - (6 + 0 + 0) = 0 \implies \mathbf{2x + 3y - 6 = 0}$")

    # --- 2. EQUAÇÃO REDUZIDA ---
    with st.expander("2️⃣ A Equação Reduzida: $y = mx + q$", expanded=False):
        st.markdown("Expressa a reta como função explícita de $x$.")
        st.markdown("#### 🔍 Dedução Algébrica")
        st.markdown("Isolando a variável dependente $y$ na Equação Geral ($Ax + By + C = 0$):")
        st.latex(r"By = -Ax - C \implies y = \left(-\frac{A}{B}\right)x + \left(-\frac{C}{B}\right)")
        st.markdown("Definimos então o **coeficiente angular** $m = -A/B$ e o **coeficiente linear** $q = -C/B$.")

        st.markdown("---")
        st.markdown("#### ✍️ O Coeficiente Angular ($m$)")
        st.markdown("A inclinação ($m = \\tan \\theta$) dita se a reta sobe, desce ou é constante:")
        
        fig2, axs2 = plt.subplots(1, 4, figsize=(12, 3))
        setup_plot(axs2[0], "1. Crescente (m > 0)"); axs2[0].set_xlim(-2, 2); axs2[0].set_ylim(-2, 2); axs2[0].plot([-2, 2], [-2, 2], color='blue', linewidth=2.5)
        setup_plot(axs2[1], "2. Decrescente (m < 0)"); axs2[1].set_xlim(-2, 2); axs2[1].set_ylim(-2, 2); axs2[1].plot([-2, 2], [2, -2], color='red', linewidth=2.5)
        setup_plot(axs2[2], "3. Constante (m = 0)"); axs2[2].set_xlim(-2, 2); axs2[2].set_ylim(-2, 2); axs2[2].plot([-2, 2], [1, 1], color='green', linewidth=2.5)
        setup_plot(axs2[3], "4. Vertical (Indefinida)"); axs2[3].set_xlim(-2, 2); axs2[3].set_ylim(-2, 2); axs2[3].axvline(1, color='orange', linewidth=2.5)
        for ax in axs2: ax.set_xticklabels([]); ax.set_yticklabels([])
        st.pyplot(fig2, use_container_width=True)

    # --- 3. EQUAÇÃO SEGMENTÁRIA ---
    with st.expander("3️⃣ A Equação Segmentária: $\\frac{x}{p} + \\frac{y}{q} = 1$", expanded=False):
        st.markdown("Esta forma é permite ver os exatos pontos onde a reta intercepta os eixos.")
        st.markdown("#### 🔍 Dedução Algébrica")
        st.markdown("Partindo de $Ax + By = -C$, dividimos toda a equação pela constante $-C$ para igualar a 1:")
        st.latex(r"\frac{Ax}{-C} + \frac{By}{-C} = \frac{-C}{-C} \implies \frac{x}{(-C/A)} + \frac{y}{(-C/B)} = 1 \implies \frac{x}{p} + \frac{y}{q} = 1")
        
        st.markdown("---")
        st.markdown("#### ✍️ Exemplo Prático e Cálculo de Área")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("Dada a reta: **$\\frac{x}{-2} + \\frac{y}{4} = 1$**")
            st.markdown("""
            - O denominador do $x$ ($p=-2$) é o intercepto horizontal.
            - O denominador do $y$ ($q=4$) é o intercepto vertical.
            """)
            st.success(r"A área do triângulo formado sob a reta é calculada imediatamente: $\text{Área} = \frac{|p \cdot q|}{2} = \frac{|-2 \cdot 4|}{2} = 4 \text{ u.a.}$")
        with col2:
            fig3, ax3 = plt.subplots(figsize=(5, 3.5))
            setup_plot(ax3, r"Interceptos e Área (4 u.a.)")
            ax3.set_xlim(-4, 2); ax3.set_ylim(-1, 5)
            x_vals = np.linspace(-4, 2, 100); y_vals = 4 * (1 - x_vals/(-2))
            ax3.plot(x_vals, y_vals, color='orange', linewidth=2.5)
            ax3.plot(-2, 0, 'ro', markersize=8, zorder=4); ax3.plot(0, 4, 'ro', markersize=8, zorder=4)
            ax3.text(-3.2, -0.6, "p = -2", color='red', fontweight='bold'); ax3.text(0.2, 4.1, "q = 4", color='red', fontweight='bold')
            ax3.fill_between([-2, 0], [0, 4], color='orange', alpha=0.2)
            st.pyplot(fig3, use_container_width=True)

    # --- 4. EQUAÇÃO PARAMÉTRICA ---
    with st.expander("4️⃣ A Equação Paramétrica: $x(t), y(t)$", expanded=False):
        st.markdown("Enquanto as outras formas mostram a reta estática, a paramétrica pode descrever a **trajetória** e o movimento ao longo do tempo ($t$).")
        st.markdown("#### 🔍 Dedução Algébrica")
        st.markdown("Dado um sistema paramétrico, isolamos o tempo $t$ em ambas as equações para encontrar a relação direta entre $x$ e $y$:")
        st.latex(r"\begin{cases} x = 3t + 4 \implies t = \frac{x-4}{3} \\ y = 2 - 3t \implies t = \frac{2-y}{3} \end{cases} \implies \frac{x-4}{3} = \frac{2-y}{3} \implies \mathbf{x + y - 6 = 0}")

        st.markdown("---")
        st.markdown("#### ✍️ Exemplo Prático: O Robô Entregador")
        st.markdown("""
        Um robô parte do ponto $(1, 1)$ e caminha em linha reta. Suas coordenadas variam conforme o tempo $t$ (em segundos):
        """)
        st.latex(r"\begin{cases} x(t) = 1 + 2t \\ y(t) = 1 + t \end{cases}")
        
        st.markdown("Veja onde ele está a cada segundo:")
        
        fig4, ax4 = plt.subplots(figsize=(8, 3))
        setup_plot(ax4, "Trajetória do Robô entregador")
        ax4.set_xlim(0, 7); ax4.set_ylim(0, 4)
        
        # Desenha a linha da trajetória
        ax4.plot([1, 7], [1, 4], color='gray', linestyle='--', alpha=0.5)
        
        # Desenha os pontos do robô em cada segundo
        tempos = [0, 1, 2, 3]
        cores = ['green', 'yellowgreen', 'orange', 'red']
        for i, t in enumerate(tempos):
            x_t = 1 + 2*t
            y_t = 1 + t
            ax4.plot(x_t, y_t, marker='s', color=cores[i], markersize=10, label=f"t={t}s")
            ax4.annotate(f' t={t}s\n({x_t},{y_t})', (x_t, y_t+0.2), fontsize=9, fontweight='bold', ha='center')
        
        st.pyplot(fig4, use_container_width=True)
        st.caption("Cada quadrado colorido é a posição do robô em um segundo. Note como a cada passo, ele anda 2 unidades em X e 1 unidade em Y.")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # =====================================================
    # DIVISÃO 2: MODELAGEM DO PROBLEMA (INVESTIGAÇÃO)
    # =====================================================
    st.header("🎯 Parte 2: O Problema")
    st.markdown("Agora que revisamos, vamos analisar o nosso problema.")

    # --- PASSO 1 ---

    from PIL import Image
    
    img = Image.open("diagrama.jpg")
    st.image(img, caption="", width=500)

    st.info("🤔 **Pergunta 1:** Se adotarmos o canto dos muros como a origem $(0,0)$ do nosso plano cartesiano, sabemos que a rede de proteção vai cruzar o muro horizontal numa distância **$a$** e o muro vertical numa distância **$b$**. Baseado na nossa revisão, qual é a equação da reta para descrever uma reta quando conhecemos exatamente onde ela 'corta' os eixos?")

    with st.expander("👉 A equação é... ", expanded=False):
        st.success("Se você pensou na **Equação Segmentária da Reta**, acertou na mosca! 🎯")
        st.markdown("Neste caso, os nossos interceptos (os pontos de corte nos eixos) são exatamente as distâncias $p=a$ e $q=b$. A equação da nossa rede será:")
        st.latex(r"\frac{x}{a} + \frac{y}{b} = 1")
        st.markdown("Mas lembre que a rede, a nossa, reta, pode ser amarrada de qualquer jeito...")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- PASSO 2 ---
    st.info("🤔 **Pergunta 2:** A rede deve obrigatoriamente encostar no **poste de sustentação**, que está fixado exatamente na coordenada $P(1,2)$. Geometricamente, se sabemos que um ponto pertence a uma reta, o que podemos fazer com a equação dela?")

    with st.expander("👉 Podemos...", expanded=False):
        st.success("Nós podemos **substituir** as coordenadas do poste ($x=1, y=2$) direto na equação da reta! 🎯")
        st.markdown("Ao fazer isso, obrigamos a rede a passar pelo poste:")
        st.latex(r"\frac{1}{a} + \frac{2}{b} = 1")
        
        st.markdown("Para facilitar a nossa vida na hora de otimizar, precisamos trabalhar com uma variável só. Vamos isolar a letra $b$ para descobrir como a posição de amarração no muro vertical depende da escolha que fizermos para o muro horizontal:")
        st.latex(r"\frac{2}{b} = 1 - \frac{1}{a} \implies \frac{2}{b} = \frac{a - 1}{a}")
        st.markdown("Invertendo as frações e multiplicando cruzado, chegamos à restrição física:")
        st.latex(r"\mathbf{b = \frac{2a}{a - 1}}")
        st.markdown("⚠️ **Isso é incrível:** Acabamos de provar que a posição onde vamos amarrar a rede na parede vertical ($b$) está totalmente 'amarrada' pela matemática à escolha que fizermos para a parede horizontal ($a$).")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- PASSO 3 ---
    st.info("🤔 **Pergunta 3:** O objetivo principal do grêmio é minimizar gastos, logo, precisamos calcular o **comprimento total da rede esticada**. Olhando de cima para o canto do muro, a parede e a rede, que figura geométrica se forma? Qual teorema famoso nos dá o comprimento da parte mais longa dessa figura?")

    with st.expander("👉 Revelar a Resposta: A Função do Comprimento", expanded=False):
        st.success("Forma-se um **Triângulo Retângulo** e nós usaremos o **Teorema de Pitágoras** (fórmula da distância)! 🎯")
        st.markdown("A rede nada mais é do que a hipotenusa desse triângulo. Portanto, o comprimento total $L$ será:")
        st.latex(r"L = \sqrt{(x_B - x_A)^2 + (y_B - y_A)^2} \implies L = \sqrt{(0 - a)^2 + (b - 0)^2} \implies L = \sqrt{a^2 + b^2}")
        
        st.markdown("Mas espere! No passo anterior, nós descobrimos exatamente quem é o $b$. Vamos substituir essa informação dentro do nosso Pitágoras para fundir tudo em uma letra só:")
        
        st.latex(r"\mathbf{L(a) = \sqrt{a^2 + \left(\frac{2a}{a - 1}\right)^2}}")
        
        st.markdown("🎉 **Conseguimos!** Acabamos de converter um problema físico de engenharia escolar em uma pura função analítica. Essa é a nossa **Função Objetivo**.")
        st.markdown("O nosso trabalho investigativo aqui terminou. **Prossiga para a Etapa 3 (Laboratório de Testes) no menu lateral** para jogarmos os valores nessa equação e descobrir qual o menor tamanho possível da rede!")
# ETAPA 3: TESTES
elif etapa == "3. Testes":
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
            # Cálculos já com arredondamento na matemática
            b = round((2 * palpite_a) / (palpite_a - 1), 2)
            distancia = round(np.sqrt(palpite_a**2 + b**2), 2)
            
            # --- NOVIDADE: MOSTRANDO A SUBSTITUIÇÃO NA TELA ---
            st.success(rf"""
            Veja o cálculo para o palpite **a = {palpite_a:.2f}**:
            
            $b = \frac{{2 \cdot {palpite_a:.2f}}}{{{palpite_a:.2f} - 1}} = {b} \text{{ m}}$
            
            $AB = \sqrt{{{palpite_a:.2f}^2 + {b}^2}} = {distancia} \text{{ m}}$
            """)
            st.markdown("---")
            
            # Criando um novo registro já com os números "limpos"
            novo_dado = pd.DataFrame({
                'Palpite (a)': [round(palpite_a, 2)],
                'Valor de b (m)': [b],
                'Distância da Rede (m)': [distancia]
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
        
        # Plotando a curva usando Matplotlib
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Vamos buscar os dados ao histórico
        eixo_x = st.session_state.historico['Palpite (a)']
        eixo_y = st.session_state.historico['Distância da Rede (m)']
        
        # Desenhamos a linha e os pontos
        ax.plot(eixo_x, eixo_y, marker='o', color='royalblue', linestyle='-')
        ax.set_title('Tamanho da Rede x Posição no Muro Horizontal', fontsize=12)
        ax.set_xlabel('Valor de a (metros)')
        ax.set_ylabel('Comprimento da Rede (metros)')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Exibe o gráfico no ecrã
        st.pyplot(fig)

# ETAPA 4: A MÁGICA DO CÁLCULO
elif etapa == "4. Resultado":
    st.title("✨ A Mágica do Cálculo")
    st.markdown("""
    Nós encontramos o "fundo do poço" (o menor gasto de rede possível) tateando no escuro, testando números na tabela. 
    Mas, afinal, será que não dava para usar uma daquelas fórmulas mágicas que aprendemos na escola?
    """)
    
    # Criando o adendo interativo (caixa sanfona)
    with st.expander("🤔 Adendo: Por que não usar a fórmula do Vértice da Parábola?"):
        st.markdown("""
        No 1º ano do Ensino Médio, nós aprendemos que o ponto mais baixo (mínimo) ou mais alto (máximo) de uma parábola pode ser encontrado rapidinho com a fórmula do **Vértice** ($x_v = \\frac{-b}{2a}$).
        
        **Exemplo Rápido:** Se o lucro da cantina fosse calculado por uma equação do 2º grau simples como $L(x) = -x^2 + 10x$, o lucro máximo ocorreria em $x = \\frac{-10}{2(-1)} = 5$. Resolvido em segundos!
        
        **Qual é o nosso problema então?** A curva que a nossa rede formou **não é uma equação do 2º grau**. Se tentarmos resolver a nossa fórmula da distância algebricamente, ela vira um "monstro" de 4º grau, e a resposta exata exige extrair uma raiz cúbica. A matemática tradicional do Ensino Médio bate num muro aqui e simplesmente não tem ferramentas para resolver isso de forma direta.
        """)
        
    st.markdown("""
    Para não termos que ficar testando números pelo resto da vida toda vez que formos construir um prédio, uma ponte ou instalar uma rede, os matemáticos inventaram uma ferramenta superior chamada **Derivada** (que vocês estudarão na faculdade!).
    
    A Derivada funciona como um radar infalível. Ela consegue achar o ponto mínimo de **qualquer** curva, por mais torta e complexa que ela seja, num piscar de olhos, cortando todo o trabalho braçal!
    """)
    
    if st.button("Revelar o Valor Exato com o Radar do Cálculo"):
        st.success("O Cálculo Diferencial cravou o valor exato: **a = 1 + \sqrt[3]{4} ≈ 2,587**")
        
        b_exato = (2 * 2.587) / (2.587 - 1)
        dist_exato = np.sqrt(2.587**2 + b_exato**2)
        
        col1, col2 = st.columns(2)
        col1.metric("Posição exata no muro horizontal (a)", "2.587 m")
        col2.metric("Posição exata no muro vertical (b)", f"{b_exato:.2f} m")
        
        st.info(f"🏆 O comprimento MÍNIMO possível para poupar o dinheiro do grêmio é de **{dist_exato:.2f} metros**!")
        st.markdown("*(Dica: Voltem ao GeoGebra na Etapa 1, coloquem o controle em 'a = 2.59' e confirmem com os próprios olhos que é nessa posição que a rede fica mais esticada e curta!)*")
