import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from fpdf import FPDF

# Definição das perguntas e traços associados
questions = [
    {"text": "Prefiro ficar sozinho(a) com meus pensamentos a interagir socialmente por longos períodos.", "trait": "Esquizoide"},
    {"text": "Sinto uma necessidade grande de apoio e aprovação dos outros no meu dia a dia.", "trait": "Oral"},
    {"text": "Gosto de ter controle das situações e tenho facilidade em liderar ou persuadir pessoas.", "trait": "Psicopata"},
    {"text": "Costumo evitar confrontos diretos e muitas vezes suporto desconfortos sem reclamar.", "trait": "Masoquista"},
    {"text": "Sou muito competitivo(a) e busco ser excelente em tudo o que me proponho a fazer.", "trait": "Rígido"},
    {"text": "Tenho uma imaginação muito ativa e rica, vivendo bastante no meu mundo interior.", "trait": "Esquizoide"},
    {"text": "Prefiro trabalhar em equipe e estar cercado de pessoas a trabalhar isolado.", "trait": "Oral"},
    {"text": "Consigo perceber facilmente as intenções das pessoas e uso isso ao meu favor.", "trait": "Psicopata"},
    {"text": "Às vezes me sinto sobrecarregado(a) porque assumo mais responsabilidades do que deveria.", "trait": "Masoquista"},
    {"text": "Tenho dificuldade em lidar com mudanças de planos de última hora ou improvisos.", "trait": "Rígido"}
]

# Mapeamento para contagem de perguntas por traço (para cálculo percentual)
trait_names = ["Esquizoide", "Oral", "Psicopata", "Masoquista", "Rígido"]
trait_counts = {trait: 0 for trait in trait_names}
for q in questions:
    trait_counts[q["trait"]] += 1

# Textos de análise de cada traço (pontos fortes e fracos)
analysis_texts = {
    "Esquizoide": (
        "O traço Esquizoide se caracteriza por uma grande capacidade criativa e imaginativa, além de uma rica vida interior. "
        "Indivíduos com esse traço tendem a ser independentes e introspectivos, apreciando a própria companhia e o mundo das ideias. "
        "Como desafio, podem apresentar dificuldade em criar vínculos emocionais profundos ou em se sentir seguros em relacionamentos, podendo parecer distantes ou desligados. "
        "Seu ponto forte está na originalidade e na autonomia, enquanto o ponto fraco pode ser a dificuldade em expressar necessidades ou sentimentos aos outros."
    ),
    "Oral": (
        "O traço Oral é marcado por sociabilidade e afetividade. Pessoas com pontuação alta nesse traço costumam ser comunicativas, empáticas e valorizam a companhia e o apoio mútuo. "
        "Têm facilidade em trabalhar em equipe e demonstram genuíno cuidado com os demais. "
        "Como ponto desafiador, podem ter dependência emocional acentuada – temem rejeição ou solidão e buscam constantemente aprovação. "
        "Sua força está na capacidade de colaboração e na empatia, enquanto a fraqueza pode ser a insegurança e a dificuldade de atuar sozinhas."
    ),
    "Psicopata": (
        "O traço Psicopata (no contexto de caráter, não patológico) está associado a liderança, carisma e estratégia. "
        "Quem apresenta esse traço tende a ser confiante, determinado e sabe influenciar pessoas com facilidade. "
        "Um ponto forte é a habilidade de assumir o comando e tomar decisões sob pressão. "
        "Porém, é preciso cuidado com a tendência ao controle excessivo ou manipulação e com a dificuldade em mostrar vulnerabilidade. "
        "Equilibrar ambição com empatia é o grande desafio desse perfil."
    ),
    "Masoquista": (
        "O traço Masoquista reflete indivíduos muito dedicados, resilientes e capazes de suportar desafios contínuos. "
        "Essas pessoas geralmente são trabalhadoras leais, pacientes e persistentes, conseguindo continuar onde outros desistiriam. "
        "Como desafio, tendem a reprimir suas próprias necessidades e emoções, assumindo mais responsabilidades do que deveriam. "
        "Podem ter dificuldade em impor limites ou dizer 'não', o que leva a sobrecarga. "
        "Sua maior força é a determinação e confiabilidade; já a fraqueza está em não se colocar em primeiro lugar quando necessário."
    ),
    "Rígido": (
        "O traço Rígido caracteriza indivíduos disciplinados, orientados a objetivos e com alto senso de responsabilidade. "
        "Eles buscam excelência em tudo que fazem, sendo organizados e confiáveis. "
        "Um ponto forte desse perfil é a ética de trabalho e a capacidade de cumprir o que promete, além de manter a estabilidade mesmo sob pressão. "
        "Por outro lado, pessoas com traço rígido podem ser inflexíveis e muito autocríticas, tendo dificuldade em lidar com falhas ou mudanças repentinas. "
        "Aprender a ter flexibilidade e lidar melhor com as próprias vulnerabilidades é um passo importante para o desenvolvimento desse perfil."
    )
}

# Sugestões de carreira para cada traço dominante
suggestion_texts = {
    "Esquizoide": (
        "prefere ambientes de trabalho independentes ou criativos, que permitam autonomia e reflexão. "
        "Carreiras em pesquisa, desenvolvimento tecnológico, artes ou escrita podem ser adequadas, pois aproveitam sua criatividade e não exigem interação social constante."
    ),
    "Oral": (
        "tende a se destacar em funções que envolvam contato humano e trabalho em equipe. "
        "Áreas como recursos humanos, ensino, atendimento ao cliente ou saúde são interessantes, pois valorizam sua capacidade de comunicação e cooperação."
    ),
    "Psicopata": (
        "geralmente se sai bem em cargos de liderança ou empreendimentos autônomos. "
        "Pode prosperar em gestão de equipes, negócios próprios, vendas ou advocacia, onde sua assertividade e carisma sejam ativos importantes no dia a dia profissional."
    ),
    "Masoquista": (
        "pode prosperar em funções de suporte e operações, onde sua dedicação e resiliência sejam valorizadas. "
        "Carreiras em controle de qualidade, administração, engenharia ou serviços de apoio são adequadas, lembrando de buscar ambientes que não sobrecarreguem sua disposição de ajudar."
    ),
    "Rígido": (
        "costuma se adequar a carreiras estruturadas e com perspectiva de crescimento. "
        "Áreas como finanças, engenharia, gerenciamento de projetos ou cargos administrativos combinam com sua organização e foco em resultados, embora deva praticar a flexibilidade nessas funções."
    )
}

# Inicialização do estado da aplicação
if "question_idx" not in st.session_state:
    st.session_state.question_idx = 0
    # Inicia pontuação de cada traço com 0
    st.session_state.scores = {trait: 0 for trait in trait_names}

# Interface do usuário - apresentação
st.title("Teste de Traços de Caráter (Bioenergética)")
st.write("Responda as perguntas abaixo de acordo com o quanto você se identifica com cada afirmação. Use a escala de 1 a 5, em que 1 significa 'discordo totalmente' e 5 significa 'concordo totalmente'. Após cada resposta, clique em **Próxima** para continuar.")

# Verifica se ainda há perguntas a responder
if st.session_state.question_idx < len(questions):
    idx = st.session_state.question_idx
    total = len(questions)
    # Exibe progresso atual
    st.markdown(f"**Pergunta {idx+1} de {total}**")
    st.progress((idx) * 100 // total)
    # Mostra a pergunta atual
    st.write(f"*{questions[idx]['text']}*")
    # Controle deslizante para resposta (1 a 5)
    answer = st.slider("Sua resposta:", min_value=1, max_value=5, value=3)
    # Botão para próxima pergunta
    if st.button("Próxima"):
        # Soma a resposta à pontuação do traço correspondente
        trait = questions[idx]["trait"]
        st.session_state.scores[trait] += answer
        # Avança para a próxima pergunta
        st.session_state.question_idx += 1
        # Re-renderização automática após clique (Streamlit faz automaticamente)
else:
    # Todas as perguntas foram respondidas - calcular resultados
    scores = st.session_state.scores
    # Calcula porcentagem de cada traço (normalizada de 0 a 100%)
    results_percent = {}
    for trait, score in scores.items():
        # Pontuação mínima e máxima possíveis para este traço
        min_score = trait_counts[trait] * 1  # menor valor (respondendo 1 em todas)
        max_score = trait_counts[trait] * 5  # maior valor (respondendo 5 em todas)
        percent = (score - min_score) / (max_score - min_score) * 100
        # Garante que percentuais mínimos não fiquem negativos
        if percent < 0:
            percent = 0
        results_percent[trait] = int(round(percent))
    # Exibição dos resultados no app
    st.header("Resultados do Teste")
    st.subheader("Percentual em cada traço de caráter:")
    for trait, pct in results_percent.items():
        st.write(f"**{trait}:** {pct}%")
    # Gera gráfico radar (polígono) com as porcentagens
    sns.set_theme(style="whitegrid")
    labels = list(results_percent.keys())
    stats = list(results_percent.values())
    stats += stats[:1]  # repete o primeiro valor no final para fechar o gráfico
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1)
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)  # inicia o eixo polar no topo (90 graus)
    ax.set_theta_direction(-1)      # inverte direção para sentido horário
    # Desenha uma linha poligonal conectando os pontos de cada traço
    ax.plot(angles, stats, color="#007ACC", linewidth=2)  # cor azul padrão
    ax.fill(angles, stats, color="#007ACC", alpha=0.3)    # preenche área com transparência
    ax.set_thetagrids(angles[:-1] * 180/np.pi, labels)
    ax.set_ylim(0, 100)
    ax.set_rlabel_position(180/len(labels))  # posiciona rótulos do eixo radial
    ax.tick_params(colors="#333333")
    ax.grid(color="gray", linestyle="--", linewidth=0.5)
    st.pyplot(fig)  # exibe o gráfico no aplicativo
    # Monta o relatório em PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "Relatório de Traços de Caráter", ln=True, align="C")
    pdf.ln(5)
    # Salva o gráfico radar como imagem e insere no PDF
    chart_path = "grafico_radar.png"
    fig.savefig(chart_path, dpi=150)
    pdf.image(chart_path, x=40, w=130)  # insere a imagem centralizada (largura ~130 mm)
    pdf.ln(10)
    # Escreve a análise de cada traço no PDF
    pdf.set_font("Helvetica", '', 12)
    for trait, pct in results_percent.items():
        # Título do traço com porcentagem
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, f"{trait}: {pct}%", ln=True)
        pdf.set_font("Helvetica", '', 12)
        # Texto de análise do traço
        pdf.multi_cell(0, 8, analysis_texts[trait], ln=True)
        pdf.ln(3)
    # Identifica traços dominantes (maiores porcentagens)
    sorted_traits = sorted(results_percent.keys(), key=lambda t: results_percent[t], reverse=True)
    top1 = sorted_traits[0]
    top2 = sorted_traits[1] if len(sorted_traits) > 1 else None
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "Sugestões de Posicionamento Profissional:", ln=True)
    pdf.set_font("Helvetica", '', 12)
    if top2 and results_percent[top2] >= (results_percent[top1] * 0.8):
        # Se houver dois traços fortes, inclui ambos nas sugestões
        pdf.multi_cell(0, 8, f"Com base nos traços dominantes **{top1}** e **{top2}**, recomenda-se o seguinte:", ln=True)
        pdf.multi_cell(0, 8, f"- {top1}: {suggestion_texts[top1]}", ln=True)
        pdf.multi_cell(0, 8, f"- {top2}: {suggestion_texts[top2]}", ln=True)
    else:
        # Caso contrário, foca no traço mais dominante
        pdf.multi_cell(0, 8, f"Seu traço predominante é **{top1}**. Com base nisso, {suggestion_texts[top1]}", ln=True)
    # Gera bytes do PDF e disponibiliza para download
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button("Baixar resultado em PDF", data=pdf_bytes, file_name="Relatorio_Traços_Caráter.pdf", mime="application/pdf")
