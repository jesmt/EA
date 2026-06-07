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

    # Biblioteca para os gráficos dinâmicos
    import matplotlib.pyplot as plt
    import numpy as np

    def setup_plot(ax, title=""):
        """Configura o visual padrão dos gráficos para manter o design limpo e acadêmico."""
        ax.axhline(0, color='black', linewidth=1.2)
        ax.axvline(0, color='black', linewidth=1.2)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlabel('Eixo X', fontsize=8)
        ax.set_ylabel('Eixo Y', fontsize=8)
        return ax

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
        st.title("Equação Geral da Reta")

        st.markdown("""
        A **Equação Geral** é a representação mais abrangente da reta no plano cartesiano.
        Todo ponto $P(x,y)$ que satisfaz a igualdade pertence ao lugar geométrico descrito pela reta.
        """)

        st.info("Fórmula da Equação Geral")
        st.latex(r"Ax + By + C = 0")

        st.markdown("""
        Onde $A$, $B$ e $C$ são constantes reais, sendo $A$ e $B$ não simultaneamente nulos.
        """)

        # =====================================================
        # DEDUÇÃO ANALÍTICA
        # =====================================================
        with st.expander("🔍 Dedução Analítica (Condição de Alinhamento)", expanded=False):
            st.markdown("""
            Para que os pontos conhecidos $A(x_A,y_A)$, $B(x_B,y_B)$ e um ponto genérico
            $P(x,y)$ pertençam à mesma reta, eles devem ser colineares.
            A figura abaixo ilustra a construção geométrica utilizando triângulos semelhantes.
            """)

            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.set_xlim(0, 6)
            ax.set_ylim(0, 5)

            ax.plot([0.2, 6], [0.75 * 0.2 + 0.25, 0.75 * 6 + 0.25], color="black", linewidth=2)

            A = (1, 1)
            B = (3, 2.5)
            P = (5, 4)

            ax.scatter(*A, color="black")
            ax.scatter(*B, color="black")
            ax.scatter(*P, color="black")

            ax.text(0.8, 1.1, "A")
            ax.text(2.8, 2.6, "B")
            ax.text(5.1, 4.1, "P(x,y)")

            ax.plot([1, 3], [1, 1], 'b')
            ax.plot([3, 3], [1, 2.5], 'b')

            ax.plot([3, 5], [2.5, 2.5], 'teal')
            ax.plot([5, 5], [2.5, 4], 'teal')

            ax.grid(True)
            fig.tight_layout()

            _, col_grafico1, _ = st.columns([1, 2, 1])
            with col_grafico1:
                st.pyplot(fig, use_container_width=True)

            st.markdown("Da semelhança dos triângulos:")
            st.latex(r"\frac{x_B-x_A}{x-x_B} = \frac{y_B-y_A}{y-y_B}")

            st.markdown("Multiplicando em cruz e expandindo os termos, reorganizamos a expressão até obter a forma geral:")
            st.latex(r"x(y_A-y_B) + y(x_B-x_A) + (x_Ay_B-x_By_A) = 0")
            st.success("Obtivemos a forma estrutural Ax + By + C = 0")

        # =====================================================
        # DETERMINANTE (SARRUS VISUAL)
        # =====================================================
        with st.expander("📐 Dedução por Determinante (Disposição de Sarrus)", expanded=False):
            st.markdown("""
            Três pontos estão alinhados quando o determinante da matriz de suas coordenadas é nulo. 
            Para visualizar a **Regra de Sarrus**, repetimos as duas primeiras colunas à direita da matriz:
            """)

            st.latex(r"""
            \begin{matrix}
            x & y & 1 & \mathbf{|} & x & y \\
            x_A & y_A & 1 & \mathbf{|} & x_A & y_A \\
            x_B & y_B & 1 & \mathbf{|} & x_B & y_B
            \end{matrix} = 0
            """)

            st.markdown("**1. Diagonais Principais (Multiplicadas da esquerda para a direita, mantendo o sinal $+$):**")
            st.latex(r"\color{blue}{(x \cdot y_A \cdot 1)} + \color{blue}{(y \cdot 1 \cdot x_B)} + \color{blue}{(1 \cdot x_A \cdot y_B)} \implies x y_A + y x_B + x_A y_B")

            st.markdown("**2. Diagonais Secundárias (Multiplicadas da direita para a esquerda, invertendo o sinal $-$):**")
            st.latex(r"\color{red}{(1 \cdot y_A \cdot x_B)} + \color{red}{(x \cdot 1 \cdot y_B)} + \color{red}{(y \cdot x_A \cdot 1)} \implies y_A x_B + x y_B + y x_A")

            st.markdown("**3. Agrupamento Final (Principais $-$ Secundárias):**")
            st.latex(r"(x y_A + y x_B + x_A y_B) - (y_A x_B + x y_B + y x_A) = 0")
            st.latex(r"x(y_A - y_B) + y(x_B - x_A) + (x_A y_B - x_B y_A) = 0")
            st.success("Resultando perfeitamente na mesma Equação Geral.")

        # =====================================================
        # EXEMPLO PRÁTICO (SARRUS VISUAL)
        # =====================================================
        with st.expander("✍️ Exemplo Prático com Regra de Sarrus", expanded=True):
            st.markdown("""
            Encontre a equação geral da reta que passa pelos pontos dados:
            - $A(0,2)$
            - $B(3,0)$
            
            Montando a matriz expandida com a técnica de repetição de colunas:
            """)

            st.latex(r"""
            \begin{matrix}
            x & y & 1 & \mathbf{|} & x & y \\
            0 & 2 & 1 & \mathbf{|} & 0 & 2 \\
            3 & 0 & 1 & \mathbf{|} & 3 & 0
            \end{matrix} = 0
            """)

            st.markdown("Desenvolvendo os produtos das linhas diagonais:")
            st.latex(r"\text{Diagonais Principais (+): } (x \cdot 2 \cdot 1) + (y \cdot 1 \cdot 3) + (1 \cdot 0 \cdot 0) = 2x + 3y + 0")
            st.latex(r"\text{Diagonais Secundárias (-): } (1 \cdot 2 \cdot 3) + (x \cdot 1 \cdot 0) + (y \cdot 0 \cdot 1) = 6 + 0 + 0")
            
            st.markdown("Subtraindo os dois blocos de resultados:")
            st.latex(r"(2x + 3y) - (6) = 0 \implies \boxed{2x + 3y - 6 = 0}")

            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("""
                ### Verificação de Pertencimento
                Substituindo pontos conhecidos para validação:
                - **Para A(0,2):** $2(0) + 3(2) - 6 = 0 \Rightarrow 0 = 0$ (Ok!)
                - **Para B(3,0):** $2(3) + 3(0) - 6 = 0 \Rightarrow 0 = 0$ (Ok!)
                - **Para um ponto externo C(-3,4):** $2(-3) + 3(4) - 6 = -6 + 12 - 6 = 0$ (Ok!)
                """)
            with col2:
                fig, ax = plt.subplots(figsize=(4.5, 3.5))
                x = np.linspace(-4, 6, 200)
                y = (6 - 2 * x) / 3

                ax.plot(x, y, linewidth=2, color="purple", label="2x + 3y - 6 = 0")
                ax.scatter([0, 3, -3], [2, 0, 4], color="red", zorder=3)
                ax.text(0.2, 2.2, "A(0,2)")
                ax.text(3.2, 0.2, "B(3,0)")
                ax.text(-2.8, 4.2, "C(-3,4)")

                setup_plot(ax, "Validação Geométrica do Exemplo")
                ax.legend(fontsize=8)
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)

    # TAB 2: EQUAÇÃO REDUZIDA
    with t_reduzida:
        st.markdown("Expressa a reta como função explícita de $x$. É a base do estudo de funções afins e do Cálculo Diferencial.")
        st.latex(r"y = mx + q")
        st.markdown("Onde **$m$** é o coeficiente angular (inclinação) e **$q$** é o coeficiente linear (intercepto no eixo $y$).")
        
        with st.expander("🔍 Ver Dedução e Comportamento dos 4 Casos do Plano"):
            st.markdown(r"Isolando $y$ na equação geral $Ax + By + C = 0$ (considerando $B \neq 0$):")
            st.latex(r"By = -Ax - C \implies y = \left(-\frac{A}{B}\right)x + \left(-\frac{C}{B}\right)")
            st.markdown(r"Identificamos que: $m = -\frac{A}{B}$ e $q = -\frac{C}{B}$. O valor de $m$ dita a inclinação da reta:")
            
            # Gráficos dinâmicos dos 4 casos de m - Corrigido o plano Cartesiano do Caso Vertical
            fig, axs = plt.subplots(1, 4, figsize=(11, 3))
            
            for ax in axs:
                setup_plot(ax)
                ax.set_xlim(-3, 3)
                ax.set_ylim(-3, 3)
            
            axs[0].set_title("1. Crescente (m > 0)", fontsize=9, color="blue")
            axs[0].plot([-3, 3], [-3, 3], color='blue', linewidth=2, label="y = x")
            
            axs[1].set_title("2. Decrescente (m < 0)", fontsize=9, color="red")
            axs[1].plot([-3, 3], [3, -3], color='red', linewidth=2, label="y = -x")
            
            axs[2].set_title("3. Constante (m = 0)", fontsize=9, color="green")
            axs[2].plot([-3, 3], [1, 1], color='green', linewidth=2, label="y = 1")
            
            # Caso 4 corrigido: agora exibe perfeitamente o plano cartesiano e a reta vertical
            axs[3].set_title("4. Vertical (m Indef.)", fontsize=9, color="orange")
            axs[3].axvline(1.5, color='orange', linewidth=2, label="x = 1.5")
            
            for ax in axs: 
                ax.legend(fontsize=7, loc="upper right")
                
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)

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
