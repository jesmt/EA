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
    st.markdown("Revisão detalhada baseada nos fundamentos da Geometria Analítica para equações da reta[cite: 1, 4].")

    # Inicializa o passo da aula para o problema específico
    if 'passo_aula' not in st.session_state:
        st.session_state.passo_aula = 0

    # Biblioteca para os gráficos dinâmicos
    import matplotlib.pyplot as plt
    import numpy as np

    def setup_plot(ax, title=""):
        """Configura o visual padrão dos gráficos para manter o design limpo."""
        ax.axhline(0, color='black',linewidth=1)
        ax.axvline(0, color='black',linewidth=1)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_title(title, fontsize=10)
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
Onde:

- $A$, $B$ e $C$ são constantes reais;
- $A$ e $B$ não podem ser simultaneamente nulos.
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

        fig, ax = plt.subplots(figsize=(8,5))

        ax.set_xlim(0,6)
        ax.set_ylim(0,5)

        ax.plot([0.2,6],[0.75*0.2+0.25,0.75*6+0.25],
                color="black", linewidth=2)

        A=(1,1)
        B=(3,2.5)
        P=(5,4)

        ax.scatter(*A,color="black")
        ax.scatter(*B,color="black")
        ax.scatter(*P,color="black")

        ax.text(0.8,1.1,"A")
        ax.text(2.8,2.6,"B")
        ax.text(5.1,4.1,"P(x,y)")

        ax.plot([1,3],[1,1],'b')
        ax.plot([3,3],[1,2.5],'b')

        ax.plot([3,5],[2.5,2.5],'teal')
        ax.plot([5,5],[2.5,4],'teal')

        ax.grid(True)

        st.pyplot(fig,use_container_width=True)

        st.markdown("""
Da semelhança dos triângulos:

""")

        st.latex(
            r"\frac{x_B-x_A}{x-x_B}"
            r"="
            r"\frac{y_B-y_A}{y-y_B}"
        )

        st.markdown("Multiplicando em cruz:")

        st.latex(
            r"(x_B-x_A)(y-y_B)"
            r"="
            r"(x-x_B)(y_B-y_A)"
        )

        st.markdown("Expandindo:")

        st.latex(
            r"x_By-x_By_B-x_Ay+x_Ay_B"
            r"="
            r"xy_B-xy_A-x_By_B+x_By_A"
        )

        st.markdown("Reorganizando os termos:")

        st.latex(
            r"x(y_A-y_B)"
            r"+"
            r"y(x_B-x_A)"
            r"+"
            r"(x_Ay_B-x_By_A)"
            r"=0"
        )

        st.success("Obtivemos a forma geral Ax + By + C = 0")

    # =====================================================
    # DETERMINANTE
    # =====================================================

    with st.expander("📐 Dedução por Determinante e Regra de Sarrus"):

        st.markdown("""
A Álgebra Linear mostra que três pontos estão alinhados quando o determinante da matriz formada por suas coordenadas é nulo.
""")

        st.latex(
            r"\begin{vmatrix}"
            r"x & y & 1 \\"
            r"x_A & y_A & 1 \\"
            r"x_B & y_B & 1"
            r"\end{vmatrix}=0"
        )

        st.markdown("""
Aplicando a Regra de Sarrus:
""")

        st.latex(
            r"xy_A+x_By+x_Ay_B"
            r"-"
            r"x_By_A-xy_B-x_Ay=0"
        )

        st.markdown("Agrupando:")

        st.latex(
            r"x(y_A-y_B)"
            r"+"
            r"y(x_B-x_A)"
            r"+"
            r"(x_Ay_B-x_By_A)"
            r"=0"
        )

        st.success(
            "A mesma equação obtida pela semelhança de triângulos."
        )

    # =====================================================
    # EXEMPLO PRÁTICO
    # =====================================================

    with st.expander("✍️ Exemplo Prático", expanded=True):

        st.markdown("""
Considere a reta que passa pelos pontos:

- $A(0,2)$
- $B(3,0)$
""")

        st.markdown("""
Substituindo os pontos no determinante:
""")

        st.latex(
            r"\begin{vmatrix}"
            r"x & y & 1\\"
            r"0 & 2 & 1\\"
            r"3 & 0 & 1"
            r"\end{vmatrix}=0"
        )

        st.markdown("Aplicando a Regra de Sarrus:")

        st.latex(
            r"2x + 3y - 6 = 0"
        )

        st.success("Equação Geral da reta")

        st.latex(
            r"\boxed{2x+3y-6=0}"
        )

        col1, col2 = st.columns([1,1])

        with col1:

            st.markdown("""
### Verificação Algébrica

**Ponto C(-3,4)**

$$
2(-3)+3(4)-6=0
$$

**Ponto A(0,2)**

$$
2(0)+3(2)-6=0
$$

**Ponto B(3,0)**

$$
2(3)+3(0)-6=0
$$

Todos pertencem à reta.
""")

        with col2:

            fig, ax = plt.subplots(figsize=(6,4))

            x = np.linspace(-4,6,200)
            y = (6 - 2*x)/3

            ax.plot(
                x,
                y,
                linewidth=2,
                label="2x + 3y - 6 = 0"
            )

            ax.scatter(
                [0,3,-3],
                [2,0,4],
                color="red"
            )

            ax.text(0.1,2.2,"A(0,2)")
            ax.text(3.1,0.2,"B(3,0)")
            ax.text(-2.8,4.2,"C(-3,4)")

            ax.axhline(0,color='black')
            ax.axvline(0,color='black')

            ax.grid(True)

            ax.legend()

            st.pyplot(fig,use_container_width=True)

        # TAB 2: EQUAÇÃO REDUZIDA
        with t_reduzida:
            st.markdown("Expressa a reta como função explícita de $x$. É a mais usada no Cálculo Diferencial[cite: 91, 93].")
            st.latex(r"y = mx + q")
            st.markdown("Onde **$m$** é o coeficiente angular (inclinação) e **$q$** é o coeficiente linear (corte na origem)[cite: 96].")
            
            with st.expander("🔍 Ver Dedução e Comportamento"):
                st.markdown("Isolando $y$ em $Ax + By + C = 0$ (onde $B \neq 0$)[cite: 97, 98]:")
                st.latex(r"y = \left(-\frac{A}{B}\right)x + \left(-\frac{C}{B}\right) \implies m = -\frac{A}{B}, \, q = -\frac{C}{B}")
                st.markdown("O coeficiente **$m = \tan \theta = \frac{\Delta y}{\Delta x}$** dita o comportamento[cite: 104]:")
                
                # Gráficos dinâmicos dos 4 casos de m
                fig, axs = plt.subplots(1, 4, figsize=(10, 2.5))
                setup_plot(axs[0], "1. Crescente (m > 0)")
                axs[0].plot([-2, 2], [-2, 2], color='blue') # [cite: 111]
                
                setup_plot(axs[1], "2. Decrescente (m < 0)")
                axs[1].plot([-2, 2], [2, -2], color='red') # [cite: 112]
                
                setup_plot(axs[2], "3. Constante (m = 0)")
                axs[2].plot([-2, 2], [1, 1], color='green') # [cite: 114]
                
                setup_plot(axs[3], "4. Vertical (m Indef.)")
                axs[3].axvline(1, color='orange') # [cite: 116, 120]
                
                for ax in axs: ax.set_xticks([]); ax.set_yticks([])
                st.pyplot(fig, use_container_width=True)

        # TAB 3: EQUAÇÃO SEGMENTÁRIA
        with t_seg:
            st.markdown("Representação otimizada para identificação imediata das interseções nos eixos, útil para calcular áreas[cite: 124, 125].")
            st.latex(r"\frac{x}{p} + \frac{y}{q} = 1")
            
            with st.expander("🔍 Ver Dedução"):
                st.markdown("Na Equação Geral, transpomos a constante e dividimos tudo por $-C$[cite: 129, 131]:")
                st.latex(r"\frac{x}{(-C/A)} + \frac{y}{(-C/B)} = 1 \implies p = -\frac{C}{A}, \, q = -\frac{C}{B}")
            
            with st.expander("✍️ Exemplo e Análise Visual"):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("Equação do Exemplo Prático: $\frac{x}{-2} + \frac{y}{4} = 1$[cite: 161].")
                    st.markdown("- Intercepto em $x$: $p = -2$\n- Intercepto em $y$: $q = 4$ [cite: 162]")
                    st.markdown("Sinais diferentes de $p$ e $q$ implicam $m > 0$ (reta crescente)[cite: 163, 164, 166].")
                with col2:
                    fig, ax = plt.subplots(figsize=(4, 3))
                    setup_plot(ax)
                    ax.plot([-3, 2], [-2, 8], color='orange')
                    ax.plot([-2, 0], [0, 4], 'ro')
                    ax.text(-2.5, -0.5, "(-2,0)", color='red')
                    ax.text(0.2, 4, "(0,4)", color='red')
                    st.pyplot(fig, use_container_width=True)

        # TAB 4: EQUAÇÃO PARAMÉTRICA
        with t_param:
            st.markdown("Descreve a 'história' do ponto sobre a reta usando uma variável escalar (tempo $t$), muito útil na cinemática[cite: 176, 177].")
            st.latex(r"\begin{cases} x = f_1(t) \\ y = f_2(t) \end{cases}")
            
            with st.expander("✍️ Conversão para Cartesiana"):
                st.markdown("Dado $x = 3t + 4$ e $y = 2 - 3t$[cite: 182]. Isolando $t$ em ambas:")
                st.latex(r"t = \frac{x-4}{3} \quad \text{e} \quad t = \frac{2-y}{3}")
                st.markdown("Igualando as expressões para eliminar o parâmetro $t$[cite: 181, 184]:")
                st.latex(r"\frac{x-4}{3} = \frac{2-y}{3} \implies x - 4 = 2 - y \implies x + y - 6 = 0")

    st.markdown("---")
    
    # --- FLUXO DO PROBLEMA DA REDE ---
    st.markdown("### 🎯 Voltando ao Problema da Cantina")
    st.markdown("Dada a revisão acima, como modelamos a linha reta de rede de proteção?")
    
    col_botoes, col_conteudo = st.columns([1, 2])
    
    with col_botoes:
        if st.button("Revelar Passo 1 ➡️"): st.session_state.passo_aula = max(st.session_state.passo_aula, 1)
        if st.button("Revelar Passo 2 ➡️"): st.session_state.passo_aula = max(st.session_state.passo_aula, 2)
        if st.button("Revelar Passo 3 ➡️"): st.session_state.passo_aula = max(st.session_state.passo_aula, 3)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reiniciar Lousa"):
            st.session_state.passo_aula = 0
            st.rerun()

    with col_conteudo:
        if st.session_state.passo_aula >= 1:
            st.info("**Passo 1: Escolha da Equação**\n\nComo conhecemos os interceptos nos muros (eixos $x$ e $y$), a **Forma Segmentária** é a mais direta[cite: 124]:")
            st.latex(r"\frac{x}{a} + \frac{y}{b} = 1")
            
        if st.session_state.passo_aula >= 2:
            st.warning("**Passo 2: Amarração no Poste**\n\nA rede precisa encostar no poste em $P(1,2)$. Substituindo na equação:")
            st.latex(r"\frac{1}{a} + \frac{2}{b} = 1 \implies b = \frac{2a}{a - 1}")
            
        if st.session_state.passo_aula >= 3:
            st.success("**Passo 3: A Função Objetivo**\n\nUsamos Pitágoras para expressar o comprimento $L$ em função apenas de $a$:")
            st.latex(r"L(a) = \sqrt{a^2 + \left(\frac{2a}{a - 1}\right)^2}")
        
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
