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
    st.markdown("Bem-vindos ao laboratório matemático! Antes de resolvermos o problema da rede da cantina, precisamos construir as nossas ferramentas de trabalho.")

    import matplotlib.pyplot as plt
    import numpy as np

    def setup_plot(ax, title=""):
        """Configura o visual padrão dos gráficos para manter o design limpo."""
        ax.axhline(0, color='black', linewidth=1.2)
        ax.axvline(0, color='black', linewidth=1.2)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_title(title, fontsize=11, fontweight='bold')
        return ax

    # Função Mágica para desenhar a Regra de Sarrus
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

    # =====================================================
    # PARTE 1: INVESTIGAÇÃO TEÓRICA PROGRESSIVA
    # =====================================================
    st.markdown("### 🔬 Parte 1: Investigação das Equações da Reta")
    st.markdown("Na geometria analítica, uma mesma reta pode 'vestir' diferentes equações dependendo do que queremos descobrir. Clique nos botões abaixo para investigar cada uma delas:")

    # Menu de navegação interno estilo "Pills" / Radio Horizontal
    forma_escolhida = st.radio(
        "Selecione o modelo matemático para explorar:",
        ["1. Equação Geral", "2. Equação Reduzida", "3. Equação Segmentária", "4. Equação Paramétrica"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("---")

    if forma_escolhida == "1. Equação Geral":
        st.markdown("#### A Equação Geral: $Ax + By + C = 0$")
        st.markdown("É a representação mais abrangente. Todo ponto $P(x,y)$ que satisfaz a igualdade pertence à reta.")
        
        st.info("💡 **Como descobrir?** Se conhecemos dois pontos da reta, usamos a condição de alinhamento com um terceiro ponto genérico $P(x,y)$ através do **Determinante**.")
        
        with st.expander("🔍 Investigar a Dedução Algébrica (Regra de Sarrus)", expanded=False):
            st.markdown("Ao duplicarmos as duas primeiras colunas da matriz de coordenadas, calculamos o determinante multiplicando as diagonais:")
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

        with st.expander("✍️ Aplicar em um Caso Real: Pontos A(0,2) e B(3,0)", expanded=False):
            st.markdown("Substituindo os números na matriz, o padrão se repete de forma simplificada:")
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
            st.success("Equação Geral deduzida: **2x + 3y - 6 = 0**")

    elif forma_escolhida == "2. Equação Reduzida":
        st.markdown("#### A Equação Reduzida: $y = mx + q$")
        st.markdown("Expressa a reta como função explícita de $x$. Fundamental para o Cálculo Diferencial pois escancara a **inclinação** da reta.")
        
        st.markdown("### O Comportamento da Inclinação ($m$)")
        st.markdown("O coeficiente angular $m$ dita como a reta se comporta visualmente no plano:")
        
        fig, axs = plt.subplots(1, 4, figsize=(12, 3.5))
        
        setup_plot(axs[0], "1. Crescente (m > 0)")
        axs[0].set_xlim(-2, 2); axs[0].set_ylim(-2, 2)
        axs[0].plot([-2, 2], [-2, 2], color='blue', linewidth=2.5)
        
        setup_plot(axs[1], "2. Decrescente (m < 0)")
        axs[1].set_xlim(-2, 2); axs[1].set_ylim(-2, 2)
        axs[1].plot([-2, 2], [2, -2], color='red', linewidth=2.5)
        
        setup_plot(axs[2], "3. Constante (m = 0)")
        axs[2].set_xlim(-2, 2); axs[2].set_ylim(-2, 2)
        axs[2].plot([-2, 2], [1, 1], color='green', linewidth=2.5)
        
        setup_plot(axs[3], "4. Vertical (m Indef.)")
        axs[3].set_xlim(-2, 2); axs[3].set_ylim(-2, 2) 
        axs[3].axvline(1, color='orange', linewidth=2.5)
        
        # Mantendo a grade visível, mas ocultando apenas os textos dos eixos para ficar limpo
        for ax in axs: 
            ax.set_xticklabels([])
            ax.set_yticklabels([])
        st.pyplot(fig, use_container_width=True)
        st.caption("*Nota: Na reta vertical, não existe função $y = f(x)$, a equação é apenas $x = k$.*")

    elif forma_escolhida == "3. Equação Segmentária":
        st.markdown("#### A Equação Segmentária: $\\frac{x}{p} + \\frac{y}{q} = 1$")
        st.markdown("Uma representação visualmente elegante: se você sabe onde a reta corta as paredes (eixos), você já tem a equação pronta!")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.info("""
            **Por que ela é útil?**
            - O número debaixo do $x$ ($p$) é onde a reta corta o eixo horizontal.
            - O número debaixo do $y$ ($q$) é onde corta o eixo vertical.
            - Permite calcular a área do triângulo rapidamente: $Area = \frac{|p \cdot q|}{2}$
            """)
            st.markdown("Dada a reta: **$\\frac{x}{-2} + \\frac{y}{4} = 1$**")
            st.markdown("Corta em $x = -2$ e $y = 4$. A área do triângulo formado é $\\frac{|-2 \cdot 4|}{2} = 4$.")
            
        with col2:
            fig, ax = plt.subplots(figsize=(5, 3.8))
            setup_plot(ax, r"Interceptos e Área")
            ax.set_xlim(-4, 2)
            ax.set_ylim(-1, 5)
            
            x_vals = np.linspace(-4, 2, 100)
            y_vals = 4 * (1 - x_vals/(-2))
            ax.plot(x_vals, y_vals, color='orange', linewidth=2.5)
            
            # Destacando interceptos
            ax.plot(-2, 0, 'ro', markersize=8, zorder=4)
            ax.plot(0, 4, 'ro', markersize=8, zorder=4)
            ax.text(-3.3, -0.6, "p = -2", color='red', fontweight='bold')
            ax.text(0.2, 4.1, "q = 4", color='red', fontweight='bold')
            
            # Área colorida
            ax.fill_between([-2, 0], [0, 4], color='orange', alpha=0.2, label="Área = 4 u.a.")
            ax.legend(loc="lower right")
            st.pyplot(fig, use_container_width=True)

    elif forma_escolhida == "4. Equação Paramétrica":
        st.markdown("#### As Equações Paramétricas")
        st.latex(r"\begin{cases} x = f_1(t) \\ y = f_2(t) \end{cases}")
        st.markdown("As formas anteriores mostram a reta como um objeto estático. A equação paramétrica traz a reta à vida: ela descreve a **trajetória** e a **velocidade** de um objeto de acordo com o tempo ($t$).")
        
        with st.expander("Cinemática Visual: O movimento no tempo", expanded=True):
            st.markdown("Imagine uma partícula cuja posição obedece ao sistema: **$x = 3t + 4$** e **$y = 2 - 3t$**")
            
            fig, ax = plt.subplots(figsize=(8, 3))
            setup_plot(ax, "A partícula avança ao longo da reta conforme o tempo (t) passa")
            ax.set_xlim(0, 11); ax.set_ylim(-5, 6)
            
            x_vals = np.linspace(0, 11, 100)
            y_vals = (6 - x_vals)
            ax.plot(x_vals, y_vals, color='gray', linestyle='--', alpha=0.5)
            
            tempos = [-1, 0, 1, 2]
            cores = ['#D8BFD8', '#DA70D6', '#BA55D3', '#800080']
            for i, t in enumerate(tempos):
                x_t = 3*t + 4
                y_t = 2 - 3*t
                ax.plot(x_t, y_t, marker='o', color=cores[i], markersize=10)
                ax.annotate(f' t={t}s\n ({x_t},{y_t})', (x_t+0.3, y_t), fontsize=10, fontweight='bold')
                
            st.pyplot(fig, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # =====================================================
    # PARTE 2: A MODELAGEM MATEMÁTICA DO PROBLEMA
    # =====================================================
    st.markdown("### 🎯 Parte 2: O Desafio da Cantina")
    st.markdown("Agora que dominamos o arsenal da geometria analítica, vamos traduzir o espaço físico da escola (muros e poste) para uma linguagem matemática rigorosa. Deslize o controle abaixo para avançar na dedução lógica da função:")
    
    # Seletor Deslizante para a Investigação Progressiva
    fase_aula = st.select_slider(
        "Arraste para avançar na resolução:",
        options=[
            "1. Espaço Físico", 
            "2. O Poste (Restrição)", 
            "3. O Comprimento (Distância)",
            "4. A Função Final"
        ]
    )
    
    st.markdown("---")
    
    if fase_aula == "1. Espaço Físico":
        st.markdown("#### Passo 1: Escolhendo o Modelo Ideal")
        st.markdown("""
        A rede de proteção será amarrada ligando os dois muros perpendiculares da escola. 
        Se adotarmos o canto do muro como a origem $(0,0)$, a rede cruzará o eixo horizontal $X$ numa distância **$a$** e o eixo vertical $Y$ numa distância **$b$**.
        
        Como conhecemos exatamente os locais de corte (os interceptos $(a,0)$ e $(0,b)$), a ferramenta matemática mais natural para descrever a rede é a **Equação Segmentária**:
        """)
        st.latex(r"\frac{x}{a} + \frac{y}{b} = 1")
        st.info("💡 **Conclusão da Fase:** O nosso problema agora se resume a descobrir os valores perfeitos para as variáveis de posicionamento $a$ e $b$. Arraste o controle para a próxima fase.")

    elif fase_aula == "2. O Poste (Restrição)":
        st.markdown("#### Passo 2: A Matemática da Restrição")
        st.markdown("""
        A rede não pode ficar solta: ela precisa **obrigatoriamente tangenciar o poste** de sustentação que fica na coordenada exata **$P(1,2)$**.
        
        Na geometria analítica, se um ponto pertence a uma reta, ele deve satisfazer sua equação. Substituindo $x=1$ e $y=2$ na equação da nossa rede:
        """)
        st.latex(r"\frac{1}{a} + \frac{2}{b} = 1")
        st.markdown("Isolando a variável $b$, obtemos a relação de dependência entre as duas paredes:")
        st.latex(r"\frac{2}{b} = 1 - \frac{1}{a} \implies \frac{2}{b} = \frac{a - 1}{a} \implies \boxed{b = \frac{2a}{a - 1}}")
        st.warning("⚠️ **Conclusão da Fase:** Provamos matematicamente que o local onde amarramos a rede no muro vertical ($b$) está totalmente preso/amarrado ao local onde escolhemos amarrar no muro horizontal ($a$). Arraste para a próxima fase.")
            
    elif fase_aula in ["3. O Comprimento (Distância)", "4. A Função Final"]:
        st.markdown("#### Passo 3: Minimizando o Custo (Distância)")
        st.markdown("""
        O grêmio estudantil quer economizar. Precisamos calcular o **comprimento total $L$ da rede esticada**. 
        Como a rede forma um triângulo retângulo com os muros da escola, aplicamos o **Teorema de Pitágoras** (que é a base da fórmula de Distância entre dois Pontos):
        """)
        st.latex(r"L = \sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}")
        st.latex(r"L = \sqrt{(0 - a)^2 + (b - 0)^2} \implies L = \sqrt{a^2 + b^2}")
        
        if fase_aula == "4. A Função Final":
            st.markdown("Para criarmos uma função otimizável que dependa de uma única decisão, substituímos o valor de $b$ que isolamos na Fase 2 dentro da nossa equação de Pitágoras:")
            
            st.success("🎉 **Modelagem Concluída! Chegamos à Função Objetivo:**")
            st.latex(r"L(a) = \sqrt{a^2 + \left(\frac{2a}{a - 1}\right)^2}")
            st.markdown("Nós acabamos de converter um problema de engenharia física do pátio da escola em uma pura função matemática $L(a)$. **Avançe para a Etapa 3 (Laboratório de Testes) na barra lateral** para começarmos a procurar o menor comprimento possível!")# ETAPA 3: TESTES

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
