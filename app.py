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
    st.title("📐 Colocando no Papel")
    st.markdown("Para descobrir o valor exato, precisamos traduzir o desenho da rede e dos muros para a linguagem da Matemática.")
    
    # --- NOVA SEÇÃO: A REVISÃO (O "Flashback") ---
    with st.expander("📚 Flashback: O 'Kit de Sobrevivência' das Retas"):
        st.markdown("A geometria analítica é como um armário: dependendo do problema, escolhemos a 'roupa' (equação) certa para a reta.")
        
        tab1, tab2, tab3 = st.tabs(["Segmentária (A nossa!)", "Geral (A universal)", "Reduzida (A clássica)"])

        with tab1:
            st.markdown("### 1. Forma Segmentária (A mais prática!)")
            st.latex(r"\frac{x}{a} + \frac{y}{b} = 1")
            st.markdown("""
            * **Por que usar:** Como a rede corta os eixos (muros) em pontos específicos $a$ e $b$, essa equação já nos dá a resposta pronta.
            * **Visual:** O $a$ e o $b$ são exatamente os lugares onde a rede toca os muros!
            """)

        with tab2:
            st.markdown("### 2. Forma Geral")
            st.latex(r"ax + by + c = 0")
            st.markdown("É a forma mais bruta e universal. Toda reta pode ser escrita assim, mas não nos diz de cara onde ela corta os eixos.")

        with tab3:
            st.markdown("### 3. Forma Reduzida")
            st.latex(r"y = mx + q")
            st.markdown("""
            * **$m$:** Inclinação (taxa de variação).
            * **$q$:** Onde corta o eixo Y.
            """)

        st.markdown("---")
        st.subheader("🛠️ Laboratório: Brincando com as Retas")
        st.markdown("Mova os pontos no GeoGebra abaixo para ver a equação mudar. Note como a **Segmentária** se ajusta quando tocamos os eixos.")
        
        # Link do GeoGebra (Substitua pelo seu link correto)
        geogebra_url = "https://www.geogebra.org/material/iframe/id/fpy3pppp/width/800/height/500/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/true/rc/false/ld/false/sdz/true/ctl/false"
        components.iframe(geogebra_url, width=800, height=450)

    # --- LÓGICA DO PROBLEMA (Continuação) ---
    if 'passo_aula' not in st.session_state:
        st.session_state.passo_aula = 0

    st.markdown("---")
    st.info("Agora que relembramos as ferramentas, vamos ao nosso problema!")

    if st.button("Revelar Passo 1: A Equação da Reta"):
        st.session_state.passo_aula = 1

    if st.session_state.passo_aula >= 1:
        st.markdown("### Passo 1: A Forma Segmentária na Prática")
        st.markdown("Já que sabemos que a rede encosta nos muros nos pontos **A(a,0)** e **B(0,b)**, usamos a equação:")
        st.latex(r"\frac{x}{a} + \frac{y}{b} = 1")
        
        st.warning("🗣️ **Discussão:** A rede tem um obstáculo obrigatório. Qual é o ponto que ela NÃO pode ignorar?")

        if st.button("Revelar Passo 2: O Poste Central"):
            st.session_state.passo_aula = 2

    if st.session_state.passo_aula >= 2:
        st.markdown("### Passo 2: Passando pelo poste P(1,2)")
        st.markdown("Se $P(1,2)$ pertence à reta, substituímos $x=1$ e $y=2$:")
        st.latex(r"\frac{1}{a} + \frac{2}{b} = 1")
        st.markdown("Isolando o $b$, descobrimos a relação entre a posição dos dois muros:")
        st.latex(r"b = \frac{2a}{a - 1}")

        if st.button("Revelar Passo 3: O Comprimento da Rede"):
            st.session_state.passo_aula = 3

    if st.session_state.passo_aula >= 3:
        st.markdown("### Passo 3: Pitágoras")
        st.markdown("O comprimento da rede é a hipotenusa:")
        st.latex(r"AB(a) = \sqrt{a^2 + \left(\frac{2a}{a - 1}\right)^2}")
        
        st.success("Modelagem pronta!")
        
        if st.button("🔄 Reiniciar Lousa"):
            st.session_state.passo_aula = 0
            st.rerun()

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
