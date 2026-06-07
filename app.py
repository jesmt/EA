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
    
    st.subheader("Simulador Interativo")
    # AQUI VOCÊ COLOCA O LINK DE INCORPORAÇÃO DO SEU GEOGEBRA
    # Substitua a string abaixo pelo link gerado no site do GeoGebra (Compartilhar > Incorporar)
    geogebra_url = "https://www.geogebra.org/material/iframe/id/fpy3pppp/width/800/height/500/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/true/rc/false/ld/false/sdz/true/ctl/false" 
    components.iframe(geogebra_url, width=800, height=500)
    
    st.warning("O que acontece com o tamanho da rede se amarrarmos a ponta muito longe da esquina?")

# ETAPA 2: MODELAGEM
elif etapa == "2. Modelagem":
    st.title("📐 Lousa Digital: A Matemática da Reta")
    st.markdown("Revisão detalhada baseada nos fundamentos da Geometria Analítica para equações da reta.")

    # Inicializa o passo da aula
    if 'passo_aula' not in st.session_state:
        st.session_state.passo_aula = 0

    import matplotlib.pyplot as plt
    import numpy as np

    def setup_plot(ax, title=""):
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_title(title, fontsize=10)
        return ax

    # Função Mágica para desenhar a Regra de Sarrus igual ao TikZ!
    def plot_sarrus(matriz, legendas_azul, legendas_vermelha):
        fig, ax = plt.subplots(figsize=(10, 3.5))
        ax.axis('off')
        ax.set_xlim(-4.5, 8.5)
        ax.set_ylim(-0.8, 2.8)

        # Plotar os textos da matriz
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

        # Legendas Azuis (Direita)
        for i in range(3):
            ax.text(4.5, 2-i, f"${legendas_azul[i]}$", color='blue', va='center', fontsize=12)

        # Legendas Vermelhas (Esquerda)
        for i in range(3):
            ax.text(-1.0, 2-i, f"${legendas_vermelha[i]}$", color='red', ha='right', va='center', fontsize=12)

        plt.tight_layout()
        return fig

    # --- REVISÃO TEÓRICA DETALHADA COM ABAS ---
    with st.expander("📚 Revisão Teórica: As Formas da Equação da Reta", expanded=True):
        t_geral, t_reduzida, t_seg, t_param = st.tabs([
            "1. Equação Geral", 
            "2. Equação Reduzida", 
            "3. Equação Segmentária", 
            "4. Equação Paramétrica"
        ])

        # TAB 1: EQUAÇÃO GERAL
        with t_geral:
            st.markdown("A **Equação Geral** é a representação mais abrangente da reta no plano cartesiano.")
            st.latex(r"Ax + By + C = 0")
            
            with st.expander("🔍 Dedução por Determinante (Regra de Sarrus)", expanded=True):
                st.markdown("Para que três pontos estejam alinhados, o determinante de suas coordenadas deve ser zero. Duplicando as duas primeiras colunas (Regra de Sarrus), temos:")
                
                # Desenhando a Sarrus Genérica
                matriz_gen = [['x', 'y', '1', 'x', 'y'], 
                              ['x_A', 'y_A', '1', 'x_A', 'y_A'], 
                              ['x_B', 'y_B', '1', 'x_B', 'y_B']]
                leg_azul_gen = [r'+ (x \cdot y_A \cdot 1) = +x y_A', 
                                r'+ (y \cdot 1 \cdot x_B) = +x_B y', 
                                r'+ (1 \cdot x_A \cdot y_B) = +x_A y_B']
                leg_verm_gen = [r'- (1 \cdot y_A \cdot x_B) = -x_B y_A', 
                                r'- (x \cdot 1 \cdot y_B) = -x y_B', 
                                r'- (y \cdot x_A \cdot 1) = -x_A y']
                
                fig_sarrus1 = plot_sarrus(matriz_gen, leg_azul_gen, leg_verm_gen)
                st.pyplot(fig_sarrus1, use_container_width=True)
                
                st.markdown("Somando os resultados obtidos pelas diagonais e igualando a zero:")
                st.latex(r"xy_A + x_By + x_Ay_B - x_By_A - xy_B - x_Ay = 0")
                st.latex(r"x(y_A-y_B) + y(x_B-x_A) + (x_Ay_B-x_By_A) = 0")

            with st.expander("✍️ Exemplo Prático com Sarrus", expanded=True):
                st.markdown("Vamos deduzir a reta que passa por **A(0,2)** e **B(3,0)**:")
                
                # Desenhando a Sarrus Numérica
                matriz_num = [['x', 'y', '1', 'x', 'y'], 
                              ['0', '2', '1', '0', '2'], 
                              ['3', '0', '1', '3', '0']]
                leg_azul_num = [r'+ (x \cdot 2 \cdot 1) = +2x', 
                                r'+ (y \cdot 1 \cdot 3) = +3y', 
                                r'+ (1 \cdot 0 \cdot 0) = 0']
                leg_verm_num = [r'- (1 \cdot 2 \cdot 3) = -6', 
                                r'- (x \cdot 1 \cdot 0) = 0', 
                                r'- (y \cdot 0 \cdot 1) = 0']
                
                fig_sarrus2 = plot_sarrus(matriz_num, leg_azul_num, leg_verm_num)
                st.pyplot(fig_sarrus2, use_container_width=True)
                
                st.latex(r"(2x + 3y + 0) - (6 + 0 + 0) = 0")
                st.success("Equação Geral: **2x + 3y - 6 = 0**")

        # TAB 2: EQUAÇÃO REDUZIDA
        with t_reduzida:
            st.markdown("Expressa a reta como função explícita de $x$. É a mais usada no Cálculo Diferencial.")
            st.latex(r"y = mx + q")
            st.markdown("Onde **$m$** é a inclinação (tangente do ângulo) e **$q$** é o corte no eixo y.")
            
            st.markdown("### Comportamento Geométrico do Coeficiente Angular ($m$)")
            fig, axs = plt.subplots(1, 4, figsize=(12, 3))
            
            setup_plot(axs[0], "1. Crescente (m > 0)")
            axs[0].set_xlim(-2, 2); axs[0].set_ylim(-2, 2)
            axs[0].plot([-2, 2], [-2, 2], color='blue', linewidth=2)
            
            setup_plot(axs[1], "2. Decrescente (m < 0)")
            axs[1].set_xlim(-2, 2); axs[1].set_ylim(-2, 2)
            axs[1].plot([-2, 2], [2, -2], color='red', linewidth=2)
            
            setup_plot(axs[2], "3. Constante (m = 0)")
            axs[2].set_xlim(-2, 2); axs[2].set_ylim(-2, 2)
            axs[2].plot([-2, 2], [1, 1], color='green', linewidth=2)
            
            setup_plot(axs[3], "4. Vertical (m Indef.)")
            axs[3].set_xlim(-2, 2); axs[3].set_ylim(-2, 2) 
            axs[3].axvline(1, color='orange', linewidth=2)
            
            for ax in axs: 
                ax.set_xticks([]); ax.set_yticks([])
            st.pyplot(fig, use_container_width=True)

        # TAB 3: EQUAÇÃO SEGMENTÁRIA
        with t_seg:
            st.markdown("Representação ideal para visualização imediata dos cortes nos eixos cartesianos.")
            st.latex(r"\frac{x}{p} + \frac{y}{q} = 1")
            
            st.markdown("### Visualização no Plano Cartesiano")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Exemplo 1 (Sinais Iguais):** $\\frac{x}{3} + \\frac{y}{2} = 1$")
                fig1, ax1 = plt.subplots(figsize=(4, 3))
                setup_plot(ax1)
                ax1.set_xlim(-1, 4); ax1.set_ylim(-1, 3)
                ax1.plot([-1.5, 4.5], [3, -1], color='teal', linewidth=2)
                ax1.plot(3, 0, 'ro'); ax1.annotate('p=3', (3, 0.2), color='red')
                ax1.plot(0, 2, 'ro'); ax1.annotate('q=2', (0.2, 2), color='red')
                st.pyplot(fig1, use_container_width=True)

            with col2:
                st.markdown("**Exemplo 2 (Sinais Distintos):** $\\frac{x}{-2} + \\frac{y}{4} = 1$")
                fig2, ax2 = plt.subplots(figsize=(4, 3))
                setup_plot(ax2)
                ax2.set_xlim(-3, 2); ax2.set_ylim(-1, 5)
                ax2.plot([-2.5, 0.5], [-1, 5], color='orange', linewidth=2)
                ax2.plot(-2, 0, 'ro'); ax2.annotate('p=-2', (-2, 0.2), color='red')
                ax2.plot(0, 4, 'ro'); ax2.annotate('q=4', (0.2, 4), color='red')
                st.pyplot(fig2, use_container_width=True)

        # TAB 4: EQUAÇÃO PARAMÉTRICA
        with t_param:
            st.markdown("Descreve a 'história' do ponto sobre a reta usando uma variável escalar (tempo $t$). É fundamental na cinemática.")
            st.latex(r"\begin{cases} x = 3t + 4 \\ y = 2 - 3t \end{cases}")
            
            st.markdown("### A Ideia de Trajetória e Tempo")
            fig3, ax3 = plt.subplots(figsize=(6, 3))
            setup_plot(ax3)
            ax3.set_xlim(0, 11); ax3.set_ylim(-5, 6)
            
            x_vals = np.linspace(0, 11, 100)
            y_vals = (6 - x_vals)
            ax3.plot(x_vals, y_vals, color='magenta', linestyle='--', alpha=0.5)
            
            tempos = [-1, 0, 1, 2]
            cores = ['#D8BFD8', '#DA70D6', '#BA55D3', '#800080']
            for i, t in enumerate(tempos):
                x_t = 3*t + 4
                y_t = 2 - 3*t
                ax3.plot(x_t, y_t, marker='o', color=cores[i], markersize=8)
                ax3.annotate(f' t={t}s\n ({x_t},{y_t})', (x_t+0.2, y_t), fontsize=9)
                
            ax3.set_title("O ponto se desloca ao longo da reta conforme o tempo (t) avança")
            st.pyplot(fig3, use_container_width=True)

    st.markdown("---")
    
    # --- FLUXO DO PROBLEMA DA REDE (Modelagem Acadêmica) ---
    st.markdown("### 🎯 A Modelagem Matemática do Problema")
    st.markdown("Para descobrir o comprimento exato da rede e minimizar o custo para a cantina, precisamos traduzir o espaço físico da escola para uma função matemática. Acompanhe a dedução lógica:")
    
    st.markdown("**1. A Equação da Rede de Proteção:**")
    st.markdown("Sabemos que a rede cruza os dois muros (eixos X e Y). Seja $A(a, 0)$ o ponto de fixação no muro horizontal e $B(0, b)$ no vertical. Como conhecemos os interceptos, a **Equação Segmentária** é a ferramenta ideal:")
    st.latex(r"\frac{x}{a} + \frac{y}{b} = 1")

    st.markdown("**2. A Restrição Física (O Poste Central):**")
    st.markdown("A rede deve obrigatoriamente se apoiar no poste localizado em $P(1,2)$. Substituindo na reta:")
    st.latex(r"\frac{1}{a} + \frac{2}{b} = 1")
    
    st.markdown("Isolando a variável $b$, obtemos a relação de dependência:")
    st.latex(r"b = \frac{2a}{a - 1}")

    st.markdown("**3. A Função Objetivo (O Comprimento da Rede):**")
    st.markdown("A rede esticada forma um triângulo retângulo com os muros. Pelo **Teorema de Pitágoras**, o comprimento total ($L$) é:")
    st.latex(r"L = \sqrt{a^2 + b^2}")

    st.markdown("Substituindo $b$, chegamos à nossa função modelada apenas em função da distância $a$:")
    
    st.success("Função do Comprimento da Rede:")
    st.latex(r"L(a) = \sqrt{a^2 + \left(\frac{2a}{a - 1}\right)^2}")
    
    st.markdown("A modelagem está concluída! Na próxima etapa, usaremos esta função para testar valores e encontrar o comprimento mínimo.")
    # TAB 3: EQUAÇÃO SEGMENTÁRIA
    with t_seg:
        st.markdown("Uma representação extremamente elegante quando conhecemos os pontos exatos onde a reta corta os eixos coordenados.")
        st.latex(r"\frac{x}{p} + \frac{y}{q} = 1")
        
        with st.expander("🔍 Ver Dedução Algébrica"):
            st.markdown("Partindo da Equação Geral, transpomos a constante $C$ e dividimos todos os termos por $-C$:")
            st.latex(r"Ax + By = -C \implies \frac{Ax}{-C} + \frac{By}{-C} = 1 \implies \frac{x}{(-C/A)} + \frac{y}{(-C/B)} = 1")
            st.markdown("Substituindo as frações do denominador por $p$ e $q$, chegamos à forma segmentária.")
        
        with st.expander("✍️ Análise Visual de Área Interceptada", expanded=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(r"""
                ### Exemplo Geométrico
                Dada a equação segmentária:
                $$\frac{x}{-2} + \frac{y}{4} = 1$$
                
                Desta forma, identificamos visualmente os eixos sem conta alguma:
                - **Intercepto horizontal ($x$):** Corta em $p = -2 \rightarrow$ Ponto $(-2,0)$
                - **Intercepto vertical ($y$):** Corta em $q = 4 \rightarrow$ Ponto $(0,4)$
                
                **Cálculo Prático de Área:** Esta equação é perfeita para problemas de otimização geométrica porque a área do triângulo formado entre a reta e os eixos é dada de imediato por:
                $$\text{Área} = \frac{|p \cdot q|}{2} = \frac{|-2 \cdot 4|}{2} = 4 \text{ u.a.}$$
                """)
            with col2:
                fig, ax = plt.subplots(figsize=(5, 3.8))
                setup_plot(ax, r"Interceptos Visuais e Área da Equação Segmentária")
                ax.set_xlim(-4, 2)
                ax.set_ylim(-1, 5)
                
                # Reta plotada
                x_vals = np.linspace(-4, 2, 100)
                y_vals = 4 * (1 - x_vals/(-2))
                ax.plot(x_vals, y_vals, color='orange', linewidth=2)
                
                # Destacando interceptos nos eixos de forma muito explícita
                ax.plot(-2, 0, 'ro', markersize=8, zorder=4)
                ax.plot(0, 4, 'ro', markersize=8, zorder=4)
                ax.text(-2.8, -0.6, "p = -2\n(-2,0)", color='red', fontweight='bold', fontsize=9)
                ax.text(0.2, 4.1, "q = 4\n(0,4)", color='red', fontweight='bold', fontsize=9)
                
                # Preenchimento do triângulo da área sob os eixos
                ax.fill_between([-2, 0], [0, 4], color='orange', alpha=0.2, label="Área Interceptada (4 u.a.)")
                ax.legend(fontsize=8)
                
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)

    # TAB 4: EQUAÇÃO PARAMÉTRICA
    with t_param:
        st.markdown("Descreve a posição dos pontos da reta utilizando uma variável auxiliar $t$, chamada de parâmetro.")
        st.latex(r"\begin{cases} x = f_1(t) \\ y = f_2(t) \end{cases}")
        
        with st.markdown("""
        ### 💡 Por que a Equação Paramétrica é Importante? (A Intuição da Cinemática)
        Enquanto as equações anteriores (geral, reduzida) mostram apenas o *lugar estático* da reta no espaço, as equações paramétricas explicam a **dinâmica e a trajetória de um corpo**. Ela responde não só *onde* a reta está, mas *como* e em qual *direção* um objeto se desloca ao longo do tempo $t$.
        
        **Exemplo Físico:** Imagine uma partícula se movendo em linha reta no plano onde sua posição horizontal e vertical mudam a cada segundo conforme o sistema abaixo:
        """):
            st.latex(r"\begin{cases} x(t) = 1 + 2t \\ y(t) = -1 + 3t \end{cases}")
            
            st.markdown("""
            - No instante $t = 0$: a partícula está na coordenada inicial $(1, -1)$.
            - No instante $t = 1$: a partícula deslocou-se para a coordenada $(3, 2)$.
            
            O vetor diretor da velocidade desse movimento é dado pelos coeficientes de $t$, ou seja, $\vec{v} = (2, 3)$.
            """)
        
        with st.expander("✍️ Conversão para a Forma Cartesiana (Eliminação de Parâmetro)"):
            st.markdown("Para sabermos qual a equação geral dessa trajetória no plano, isolamos o tempo $t$ em ambas as equações:")
            st.latex(r"x = 3t + 4 \implies t = \frac{x-4}{3}")
            st.latex(r"y = 2 - 3t \implies t = \frac{2-y}{3}")
            st.markdown("Como o tempo $t$ é único, igualamos as duas expressões para eliminá-lo:")
            st.latex(r"\frac{x-4}{3} = \frac{2-y}{3} \implies x - 4 = 2 - y \implies \boxed{x + y - 6 = 0}")

    st.markdown("---")
    
    # =====================================================
    # FLUXO DO PROBLEMA DA REDE - SELETOR ACADÊMICO
    # =====================================================
    st.markdown("## 🎯 Resolução Cadenciada do Problema da Cantina")
    st.markdown("Utilizando os conceitos revisados acima na lousa digital, faremos a modelagem formal da linha reta ocupada pela rede de proteção.")
    
    # Substituição dos botões antigos por um seletor progressivo muito mais elegante
    fase_aula = st.select_slider(
        "Selecione a fase da modelagem analítica para acompanhar o desenvolvimento:",
        options=[
            "Fase 1: Configuração do Modelo Espacial", 
            "Fase 2: Imposição da Restrição Física", 
            "Fase 3: Dedução Analítica da Função Objetivo"
        ]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if fase_aula == "Fase 1: Configuração do Modelo Espacial":
        st.markdown("### 🏛️ Fase 1: Escolha Estratégica da Equação")
        st.markdown("""
        Como a rede de proteção deve ligar os dois muros perpendiculares da cantina, sabemos que ela cruzará o eixo horizontal $x$ em uma distância $a$ da origem, e o eixo vertical $y$ em uma distância $b$.
        
        Conhecendo explicitamente os interceptos $(a,0)$ e $(0,b)$, a ferramenta matemática ideal e mais elegante para iniciar nossa modelagem é a **Equação Segmentária da Reta**:
        """)
        st.latex(r"\frac{x}{a} + \frac{y}{b} = 1")
        st.info("Aqui, as variáveis independentes do nosso problema de otimização passam a ser os comprimentos dos muros $a$ e $b$.")
            
    elif fase_aula == "Fase 2: Imposição da Restrição Física":
        st.markdown("### 📌 Fase 2: Fixação da Reta no Poste")
        st.markdown("""
        O problema impõe uma restrição física intransponível: a rede precisa obrigatoriamente tangenciar/encostar no poste de sustentação fixado na coordenada exata $P(1,2)$. 
        
        Para que o ponto $P(1,2)$ pertença ao lugar geométrico da reta da rede, suas coordenadas devem satisfazer a equação segmentária escolhida. Substituímos $x=1$ e $y=2$:
        """)
        st.latex(r"\frac{1}{a} + \frac{2}{b} = 1")
        st.markdown("Para conseguirmos equacionar o problema usando apenas uma variável, isolamos a variável $b$ em função de $a$:")
        st.latex(r"\frac{2}{b} = 1 - \frac{1}{a} \implies \frac{2}{b} = \frac{a - 1}{a}")
        st.markdown("Invertendo ambos os membros da igualdade:")
        st.latex(r"\frac{b}{2} = \frac{a}{a - 1} \implies \boxed{b = \frac{2a}{a - 1}}")
        st.warning("Esta relação prova que o ponto de fixação no muro vertical depende estritamente de onde a rede intersectará o chão horizontal.")
            
    elif fase_aula == "Fase 3: Dedução Analítica da Função Objetivo":
        st.markdown("### 📐 Fase 3: Demonstração e Dedução Passo a Passo da Função do Comprimento")
        st.markdown("""
        Queremos encontrar o comprimento linear total $L$ da rede de proteção esticada. Geometricamente, o comprimento da rede é exatamente a **distância euclidiana** entre as duas extremidades de fixação nos muros: o ponto $A(a,0)$ e o ponto $B(0,b)$.
        
        Aplicando a fórmula clássica da distância entre dois pontos no plano cartesiano (decorrente direta do Teorema de Pitágoras no triângulo retângulo da cantina):
        """)
        st.latex(r"L = \sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}")
        st.latex(r"L = \sqrt{(0 - a)^2 + (b - 0)^2} \implies L = \sqrt{a^2 + b^2}")
        
        st.markdown("""
        Como demonstrado na fase anterior, a restrição física do poste nos deu uma equação para $b$ baseada apenas na variável $a$:
        $$b = \frac{2a}{a - 1}$$
        
        Substituindo agora essa expressão de $b$ dentro da raiz do nosso modelo de distância, eliminamos uma incógnita e deduzimos a **Função Objetivo Otimizável** final:
        """)
        st.latex(r"L(a) = \sqrt{a^2 + \left(\frac{2a}{a - 1}\right)^2}")
        st.success("🎉 Chegamos à Função Objetivo matemática que modela o comprimento total da rede em função apenas da distância horizontal 'a'.")
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
