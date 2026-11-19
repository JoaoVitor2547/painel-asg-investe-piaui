"""Gera docs/documentacao_painel_asg.pdf: Parte 1 (como a ferramenta foi feita) e Parte 2 (guia de uso de cada aba).
Numeros, indicadores, testes e capturas de tela sao lidos do proprio index.html, para o documento nunca divergir do painel.
Uso: python3 src/gerar_documentacao.py   (depois de montar.py; requer: pip install reportlab playwright)"""
import os, tempfile
from html import escape as E
from playwright.sync_api import sync_playwright
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether

SITE = 'https://joaovitor2547.github.io/painel-asg-investe-piaui/'
REPO = 'https://github.com/JoaoVitor2547/painel-asg-investe-piaui'
EQUIPE = ['Antonio Guilherme Santos da Silva', 'João Vitor Fernandes de Sousa', 'José Torres de Araujo Neto', 'Julio Pereira de Oliveira Neto',
          'Luiz Matheus Soares Batista Cunha', 'Octavio Alves Freire', 'Ronney Said Bonfim dos Reis']
ABAS = ['geral', 'temas', 'sequencia', 'investe', 'empresas', 'editar', 'dados']

# ---------- 1. le o painel: indicadores, scores, testes e capturas de tela ----------
tmp = tempfile.mkdtemp()
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={'width': 1280, 'height': 860}, device_scale_factor=1.5)
    p.goto('file://' + os.path.abspath('index.html')); p.wait_for_timeout(300)
    IND = p.evaluate("""() => IND.map(i => ({id:i.id, grupo:i.mat || (i.tema==='inv' ? 'Investe' : 'Empresas'), pilar:PIL[i.pilar], nome:i.nome, formula:i.form,
        fonte:i.fonte, origem:i.o, valor:i.v==null ? 'a coletar' : i.f(i.v), meta:i.m==null ? '—' : i.f(i.m), nota:i.sc==null ? '—' : String(Math.round(i.sc))}))""")
    SC = p.evaluate("() => ({...SC})"); W = p.evaluate("() => ({...W})")
    N = p.evaluate("() => ({P:D.P.length,E:D.E.length,X:D.X.length,C:D.C.length,S:D.S.length,K:D.K.length,R:D.R.length,G:D.G.length,N:D.N.length,T:D.T.length,I:D.I.length, comp:COMP.length, tabs:Object.keys(ESQ).length})")
    COMP = p.evaluate("() => COMP.map(c => [c.id, c.t, String(IND.filter(i => i.c===c.id).length)])")
    p.goto('file://' + os.path.abspath('index.html') + '#dados'); p.wait_for_timeout(200)
    TESTES = p.evaluate("() => [...document.querySelectorAll('.tw')[0].querySelectorAll('tbody tr')].map(tr => [...tr.children].map(td => td.textContent.trim()))")
    for a in ABAS:
        p.goto('file://' + os.path.abspath('index.html') + '#' + a); p.wait_for_timeout(250); p.screenshot(path=f'{tmp}/{a}.png')
    b.close()
n1 = lambda v: f'{v:.1f}'.replace('.', ',')
cont = lambda o: sum(1 for i in IND if i['origem'] == o)
assert all(t[4] == 'OK' for t in TESTES), 'ha teste de qualidade em ERRO; corrija a base antes de gerar o documento'

# ---------- 2. estilos ----------
F = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DV', F + 'DejaVuSans.ttf')); pdfmetrics.registerFont(TTFont('DVB', F + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVM', F + 'DejaVuSansMono.ttf')); pdfmetrics.registerFontFamily('DV', normal='DV', bold='DVB', italic='DV', boldItalic='DVB')
AZ, AZC, CZ = colors.HexColor('#1f3a66'), colors.HexColor('#dfe7f4'), colors.HexColor('#566279')
st = lambda n, **k: ParagraphStyle(n, fontName=k.pop('font', 'DV'), **k)
sP = st('p', fontSize=9.5, leading=14, spaceAfter=6)
sH1 = st('h1', font='DVB', fontSize=17, leading=21, textColor=AZ, spaceBefore=4, spaceAfter=10)
sH2 = st('h2', font='DVB', fontSize=12.5, leading=16, textColor=AZ, spaceBefore=12, spaceAfter=6)
sH3 = st('h3', font='DVB', fontSize=10.5, leading=14, spaceBefore=8, spaceAfter=4)
sC = st('c', fontSize=8, leading=10.5); sCB = st('cb', font='DVB', fontSize=8, leading=10.5, textColor=AZ)
sL = st('l', fontSize=9.5, leading=14, leftIndent=14, bulletIndent=4, spaceAfter=3)
sCod = st('cod', font='DVM', fontSize=8, leading=11, backColor=colors.HexColor('#f1f3f7'), borderPadding=6, spaceBefore=4, spaceAfter=10, leftIndent=6, rightIndent=6)
sLeg = st('leg', fontSize=8, leading=11, textColor=CZ, spaceAfter=8)
LARG = 17.4 * cm
P = lambda t, s=sP: Paragraph(t, s)
def lista(itens, num=False): return [Paragraph(t, sL, bulletText=(f'{i}.' if num else '•')) for i, t in enumerate(itens, 1)]
def tabela(cab, linhas, larg):
    d = [[Paragraph(E(str(c)), sCB) for c in cab]] + [[Paragraph(E(str(c)), sC) for c in l] for l in linhas]
    t = Table(d, colWidths=[w * cm for w in larg], repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), AZC), ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#c3cbd9')),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    return [t, Spacer(1, 8)]
def foto(aba, legenda):
    return [Image(f'{tmp}/{aba}.png', width=LARG, height=LARG * 860 / 1280), P(legenda, sLeg)]
def rodape(c, d):
    c.saveState(); c.setFont('DV', 7.5); c.setFillColor(CZ)
    c.drawString(1.8 * cm, 1.1 * cm, 'Painel ASG · Investe Piauí — Grupo 2 — Ciência de Dados, iCEV 2026.2'); c.drawRightString(A4[0] - 1.8 * cm, 1.1 * cm, str(d.page)); c.restoreState()

h = []
# ---------- 3. capa ----------
h += [Spacer(1, 3.2 * cm), Image('assets/logo-investe-piaui.png', width=3.6 * cm, height=3.6 * cm * 260 / 258), Spacer(1, 14),
      P('Painel ASG · Investe Piauí', st('t', font='DVB', fontSize=26, leading=31, textColor=AZ, alignment=1)),
      P('Documentação da ferramenta web', st('t2', fontSize=14, leading=20, alignment=1, textColor=CZ, spaceAfter=22)),
      P('<b>Projeto ASG — Grupo Investe Piauí e iCEV — 2026</b><br/>Disciplina de Ciência de Dados · Engenharia de Software (turma Borg) · 2026.2', st('t3', fontSize=10.5, leading=16, alignment=1, spaceAfter=18)),
      P('<b>Grupo 2</b><br/>Temas da Matriz de Materialidade: T1 — Governança ética e compliance · T14 — Integridade e combate à corrupção (controles internos)', st('t4', fontSize=10.5, leading=16, alignment=1, spaceAfter=18)),
      P('<b>Integrantes</b><br/>' + '<br/>'.join(EQUIPE), st('t5', fontSize=10.5, leading=16, alignment=1, spaceAfter=22)),
      P(f'<b>Ferramenta:</b> <link href="{SITE}" color="#1f3a66">{SITE}</link><br/><b>Repositório:</b> <link href="{REPO}" color="#1f3a66">{REPO}</link>', st('t6', fontSize=9.5, leading=15, alignment=1, spaceAfter=20)),
      P('Teresina, 18 de novembro de 2026', st('t7', fontSize=9.5, alignment=1, textColor=CZ)),
      Spacer(1, 1.2 * cm), P('Projeto acadêmico. Não é um canal oficial da Investe Piauí. Todos os dados usados são sintéticos.', st('t8', fontSize=8.5, alignment=1, textColor=CZ)), PageBreak()]

h += [P('Como este documento está organizado', sH1),
      P('O documento tem duas partes. A <b>Parte 1</b> é técnica: explica como a ferramenta web foi construída, de onde vêm os dados, como cada indicador é calculado e como o código está organizado. A <b>Parte 2</b> é um guia de uso: apresenta cada aba do painel, o que ela mostra e como usar, para quem vai operar a ferramenta sem precisar ler código.'),
      P('Em resumo', sH3)]
h += tabela(['Item', 'Descrição'], [
    ['O que é', 'Página web de um único arquivo que calcula e mostra indicadores ambientais, sociais e de governança (ASG) da Investe Piauí, com foco em governança ética, compliance e integridade'],
    ['Conteúdo', f'7 abas, {len(IND)} indicadores, Score ASG de 0 a 100, {len(TESTES)} testes automáticos de qualidade dos dados e editor de dados'],
    ['Indicadores', f"{cont('calc')} calculados direto das tabelas, {cont('demo')} com medição de demonstração e {cont('nd')} que dependem de dado a coletar das empresas"],
    ['Dados', 'Duas planilhas sintéticas, calibradas com os totais oficiais do Governo do Piauí (120 empreendimentos, R$ 44,7 bilhões)'],
    ['Tecnologias', 'HTML5, CSS3 e JavaScript puro no painel; Python com openpyxl na preparação dos dados; Node.js com Playwright nos testes; GitHub Pages na publicação'],
    ['Resultado atual', f"Score ASG {n1(SC['geral'])}; tema T1 {n1(SC['T1'])}; tema T14 {n1(SC['T14'])}"]], [3.2, 14.2])
h += [PageBreak()]

# ---------- 4. PARTE 1 ----------
h += [P('Parte 1 — Como a ferramenta foi feita', sH1),
      P('1.1 Objetivo e ponto de partida', sH2),
      P('O Desafio Investe Piauí pediu um painel de BI para a agenda ASG da agência. Por orientação da professora, o Grupo 2 construiu a solução como ferramenta web programada pelo próprio grupo, em vez de Power BI, por ser mais próxima da área de Engenharia de Software.'),
      P('Três definições guiaram o desenho:')]
h += lista(['<b>Os temas do grupo.</b> Na Matriz de Materialidade, o Grupo 2 ficou com T1 (Governança ética e compliance) e T14 (Integridade e combate à corrupção, controles internos). Eles abrem a página principal e têm aba própria.',
            '<b>A sequência trabalhada em sala.</b> Plano de Governo, Compromissos de Governo, Pacote de Indicadores, Plano de Compliance e Plano Estratégico ASG de 4 anos. Cada indicador do painel responde a um compromisso, tem um controle de compliance e, quando cabe, uma meta até 2030.',
            '<b>Dois olhares.</b> ASG Investe (a agência olhando para si) e ASG Empresas (os empreendimentos atraídos).'])
h += [P(f'O painel trabalha com {N["comp"]} compromissos. A redação foi escrita pelo grupo a partir da missão da agência e deve ser trocada pelo texto oficial quando a Investe Piauí o indicar.')]
h += tabela(['Código', 'Compromisso', 'Indicadores ligados'], COMP, [1.8, 12.6, 3.0])

h += [P('1.2 Arquitetura e tecnologias', sH2),
      P('A solução tem duas partes: uma etapa de preparação, que roda em Python e transforma as planilhas em um arquivo de dados, e o painel, que roda inteiro no navegador de quem abre a página.')]
h += tabela(['Camada', 'O que faz', 'Tecnologia e arquivo'], [
    ['Bases de dados', 'Guardam as tabelas e os dicionários de dados', 'Planilhas dados/base_asg_grupo2.xlsx e dados/base_integridade_grupo2.xlsx'],
    ['Geração da base de integridade', 'Cria os dados sintéticos dos temas T1 e T14, com semente fixa', 'Python (src/gerar_base_integridade.py)'],
    ['Extração', 'Lê as duas planilhas e guarda só as colunas que o painel usa', 'Python + openpyxl (src/extrair.py), gera dados/dados.json'],
    ['Modelo da página', 'Contém o visual e toda a lógica de cálculo', 'HTML + CSS + JavaScript (src/template.html)'],
    ['Montagem', 'Encaixa os dados e o logotipo no modelo e grava o painel', 'Python (src/montar.py), gera index.html'],
    ['Dicionários e documentação', 'Gerados a partir do próprio painel, para não divergirem dele', 'Python (src/gerar_dicionarios.py e src/gerar_documentacao.py)'],
    ['Teste', 'Abre as 7 abas em computador e celular, procura erros e exercita o editor', 'Node.js + Playwright (tests/teste.js)'],
    ['Publicação', 'Hospeda o index.html com link público', 'GitHub Pages, a partir da branch main']], [3.6, 6.9, 6.9])
h += [P('Decisões de projeto', sH3)]
h += tabela(['Decisão', 'Motivo'], [
    ['Um único arquivo HTML, com os dados embutidos', 'Abre com duplo clique ou por link, não depende de servidor nem de banco de dados'],
    ['JavaScript puro, sem framework nem biblioteca de gráficos', 'O grupo consegue ler e explicar o código inteiro; nada quebra por atualização de terceiros'],
    ['Gráficos em SVG e CSS escritos à mão', 'São gráficos simples (barras, colunas, rosca, anel, linha, dispersão); desenhá-los direto evita carregar uma biblioteca'],
    ['Indicadores calculados no navegador', 'O número na tela sempre vem do dado; ninguém digita o resultado de um indicador'],
    ['Testes de qualidade a cada abertura e a cada edição', 'Se a base deixar de fechar com os totais oficiais, o erro aparece na tela'],
    ['Edições salvas no navegador (localStorage)', 'Permite simular cenários sem alterar a base publicada e sem exigir login ou servidor']], [6.4, 11.0])

h += [P('1.3 Bases de dados', sH2),
      P('Todos os registros são <b>sintéticos</b>. O cadastro real de empresas e projetos é protegido por sigilo comercial e pela LGPD, e o desafio exige termo de confidencialidade. A carteira simulada foi calibrada: as somas fecham exatamente com os totais divulgados pelo Governo do Piauí em dezembro de 2025 (120 empreendimentos; R$ 44,7 bilhões previstos; 47 implantados, 44 em implantação e 29 em estruturação; 10.500 empregos gerados e 25.200 previstos).'),
      P('A estrutura da carteira segue o dicionário de dados de exemplo fornecido pela Investe Piauí. Cada planilha traz o seu dicionário na aba DICIONARIO DE DADOS.')]
h += tabela(['Planilha', 'Tabela (aba)', 'Registros', 'O que guarda'], [
    ['base_asg', 'Projetos + CidadeProjeto', N['P'], 'Setor, município, datas, investimento previsto e realizado, empregos, status'],
    ['base_asg', 'Empresas', N['E'], 'Setor e país de origem'],
    ['base_asg', 'Processos_Externos', N['X'], 'Demandas a SEMAR, INTERPI e Equatorial, com prazo (SLA)'],
    ['base_asg', 'CONTRATOS', N['C'], 'Contratos da agência e cláusula ASG'],
    ['base_asg', 'CONSUMO_SEDE', f"{N['S']} meses", 'Energia, água e resíduos da sede'],
    ['base_asg', 'Comunicação', N['K'], 'Ações de comunicação por projeto'],
    ['base_asg', 'RESULTADOS ASG', N['R'], 'Medições de demonstração (potência renovável, e-SIC, RH, Investe Nelas)'],
    ['base_integridade', 'DUE_DILIGENCE', N['G'], 'Análise de integridade de cada empresa: realizada, risco, pendência, declaração anticorrupção'],
    ['base_integridade', 'CANAL_DENUNCIAS', N['N'], 'Relatos, categoria, prazo de apuração e resultado, sem identificar pessoas'],
    ['base_integridade', 'COLABORADORES_INTEGRIDADE', N['T'], 'Treinamento, código de conduta e declaração de conflito de interesses'],
    ['base_integridade', 'CONTROLES_INTERNOS', N['I'], 'Controles mapeados, se foram testados e o resultado'],
    ['base_integridade', 'CONTRATOS_INTEGRIDADE', N['C'], 'Cláusula anticorrupção e avaliação do fornecedor, por contrato']], [2.9, 4.8, 2.2, 7.5])

h += [P('1.4 Passo a passo da construção', sH2)]
h += lista(['<b>Entendimento do negócio.</b> Levantamento da missão da agência, da agenda ASG e das perguntas que o painel deve responder (Atividade 01, método CRISP-DM).',
            '<b>Estruturação da base da carteira.</b> Planilha no formato do dicionário da Investe Piauí, com valores distribuídos entre os 120 projetos de modo que as somas por status fechem com os totais oficiais.',
            '<b>Base dos temas T1 e T14.</b> Um script com semente fixa gera cinco tabelas de integridade. As chaves (código da empresa e do contrato) batem com a base da carteira.',
            '<b>Definição dos indicadores.</b> Para cada compromisso, o grupo listou o que medir e conferiu, tabela por tabela, o que a base permite calcular. Cada indicador ganhou fórmula, fonte, controle de compliance e, quando cabe, meta para 2030.',
            '<b>Extração.</b> O script extrair.py lê as planilhas, converte datas para AAAA-MM-DD, calcula prazos em dias e grava o dados.json.',
            '<b>Programação do painel.</b> O arquivo template.html reúne o estilo, a estrutura e o programa que calcula e desenha tudo.',
            '<b>Montagem.</b> O script montar.py encaixa os dados e o logotipo no modelo e grava o index.html.',
            '<b>Teste e conferência.</b> Um roteiro automatizado abre as 7 abas em computador e celular, verifica erros e exercita o editor. Os indicadores foram comparados com um cálculo independente em Python sobre as mesmas planilhas, e coincidiram.',
            '<b>Publicação.</b> O repositório foi enviado ao GitHub e o index.html foi publicado pelo GitHub Pages.'], num=True)
h += [P('Para reconstruir a ferramenta a partir do repositório (na pasta raiz):', sP),
      Paragraph('pip install openpyxl playwright reportlab<br/>python3 src/gerar_base_integridade.py &nbsp;&nbsp;# opcional: recria a base dos temas T1 e T14<br/>python3 src/extrair.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# planilhas para dados/dados.json<br/>python3 src/montar.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# gera o index.html<br/>python3 src/gerar_dicionarios.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# atualiza os dicionários<br/>python3 src/gerar_documentacao.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# atualiza este PDF<br/>node tests/teste.js &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# teste automatizado (npm install playwright)', sCod)]

h += [P('1.5 Organização do código', sH2),
      P('O programa do painel, dentro de src/template.html, está dividido em 8 blocos numerados e comentados, executados nesta ordem quando a página abre.')]
h += tabela(['Bloco', 'Nome no código', 'Função'], [
    ['1. Dados', 'ORIG, D, W, salvar()', 'Lê a base embutida; se houver edições salvas no navegador, usa a base editada'],
    ['2. Utilitários', 'nf, pct, bi, sum, div, med, dias, grupo, conta', 'Formatam números no padrão brasileiro, somam, agrupam e contam'],
    ['3. Cálculo', 'calcular()', 'Faz todas as contas uma vez e devolve os resultados em um objeto (M)'],
    ['4. Catálogo', 'COMP, TEMAS, catalogo(), nota(), recalcular()', f'Lista os compromissos, os temas e os {len(IND)} indicadores; calcula as notas e o Score ASG'],
    ['5. Componentes visuais', 'bars, cols, ring, donut, pilha, linha, dispersao, card', 'Cada função devolve o HTML ou SVG de um gráfico ou de um cartão de indicador'],
    ['6. Telas', 'telas.geral … telas.dados', 'Cada aba é uma função que devolve o HTML da tela'],
    ['7. Editor', 'ESQ, converter(), validar(), analisar(), laudo()', 'Esquema de cada tabela editável, conversão de tipos, validação e leitura de arquivo com laudo'],
    ['8. Navegação e eventos', 'render() e os ouvintes de evento', 'Troca de aba pelo endereço (#geral, #temas…), filtros, formulário e botões']], [3.3, 5.9, 8.2])
h += [P('Incluir um indicador novo é acrescentar uma linha em catalogo(): cartões, tabelas, notas e contagens se atualizam sozinhos. Todas as cores são variáveis CSS, com um conjunto para tema claro e outro para tema escuro, e o layout se adapta ao celular.')]

h += [P('Envio de arquivo com conferência', sH3),
      P('Na aba Editar dados, além do formulário, o usuário pode enviar um arquivo CSV ou JSON com vários registros da tabela escolhida. O arquivo é lido no próprio navegador (API FileReader); nada é enviado a servidor. A função analisar() faz a conferência em quatro passos, sem alterar a base:')]
h += lista(['<b>Leitura.</b> Identifica se é CSV ou JSON; no CSV, descobre o separador (ponto e vírgula ou vírgula) e respeita aspas.',
            '<b>Reconhecimento das colunas.</b> Liga cada coluna do arquivo a um campo da tabela, pela chave ou pelo nome do campo, sem diferenciar maiúsculas e acentos. Informa as colunas que faltam e as que a ferramenta não usa.',
            '<b>Conferência registro a registro.</b> Converte os tipos (número, data, opção de lista) e aplica as mesmas regras do formulário: código obrigatório e não repetido, opção válida, valor não negativo, realizado não maior que o previsto, data no formato AAAA-MM-DD.',
            '<b>Laudo.</b> A função laudo() mostra quantos registros podem ser usados e, para cada linha recusada, o número da linha e o motivo. Só depois de o usuário confirmar os registros válidos entram na base e tudo é recalculado.'], num=True)
h += [P('1.6 Score ASG', sH2),
      P('O Score ASG resume em uma nota de 0 a 100 quanto das metas propostas para 2030 já foi alcançado.')]
h += tabela(['Medida', 'Fórmula'], [
    ['Nota do indicador, quando maior é melhor', 'mín(valor ÷ meta; 1) × 100'],
    ['Nota do indicador, quando menor é melhor', 'mín(meta ÷ valor; 1) × 100'],
    ['Nota do pilar (Ambiental, Social, Governança) e do tema (T1, T14)', 'Média das notas dos indicadores que têm meta e valor'],
    ['Score ASG', f"(Ambiental × {W['amb']} + Social × {W['soc']} + Governança × {W['gov']}) ÷ {W['amb'] + W['soc'] + W['gov']}"],
    ['Faixas de leitura', '0 a 49: crítico (barra vermelha) · 50 a 79: em evolução (barra laranja) · 80 a 100: próximo da meta (barra verde)']], [7.4, 10.0])
h += [P(f"O peso maior da Governança reflete os temas do grupo e pode ser alterado na aba Editar dados. As metas são proposta do grupo, a pactuar com a agência. Com a base atual: <b>Score ASG {n1(SC['geral'])}</b>; Ambiental {n1(SC['amb'])}; Social {n1(SC['soc'])}; Governança {n1(SC['gov'])}; tema T1 {n1(SC['T1'])}; tema T14 {n1(SC['T14'])}.")]

h += [P(f'1.7 Catálogo dos {len(IND)} indicadores', sH2),
      P('Valores calculados sobre a base sintética. A coluna Grupo indica o tema material (T1, T14) ou o olhar (Investe, Empresas). A fórmula, a fonte e o controle de cada indicador estão no dicionário de fórmulas e indicadores, que acompanha a entrega.')]
h += tabela(['Código', 'Grupo', 'Pilar', 'Indicador', 'Valor', 'Meta 2030', 'Nota'],
            [[i['id'], i['grupo'], i['pilar'], i['nome'], i['valor'], i['meta'], i['nota']] for i in IND], [1.6, 2.0, 2.4, 6.6, 1.9, 1.7, 1.2])
h += [P(f"Origem dos valores: {cont('calc')} indicadores são calculados da base a cada abertura; {cont('demo')} usam medição de demonstração, porque a fonte real ainda não foi carregada (ANEEL/SIGA, e-SIC, RH e programa Investe Nelas); {cont('nd')} aparecem como “a coletar”, porque dependem de um questionário ASG a ser respondido pelas empresas.")]

h += [P('1.8 Qualidade dos dados', sH2),
      P(f'O painel executa {len(TESTES)} testes toda vez que abre ou que um dado é editado. Os testes T01 a T11 comparam a carteira com os totais oficiais; os demais conferem a estrutura das tabelas. Com a base publicada, os {len(TESTES)} passam.')]
h += tabela(['Teste', 'O que confere', 'Esperado', 'Obtido', 'Resultado'], TESTES, [1.5, 9.0, 2.2, 2.2, 2.5])

h += [P('1.9 Limitações', sH2)]
h += lista(['A base é sintética: os valores mostram o que a ferramenta faz, não a situação real da agência.',
            'A redação dos compromissos de governo é do grupo e deve ser trocada pelo texto oficial.',
            'As metas de 2030 são proposta do grupo, ainda não pactuadas com a Investe Piauí.',
            f"{cont('demo')} indicadores usam valor de demonstração e {cont('nd')} dependem de questionário às empresas.",
            'As edições feitas na aba Editar dados ficam só no navegador de quem editou; não são compartilhadas entre usuários.',
            'Não há controle de acesso: quem tem o link vê todas as abas. Com dados reais, a versão pública precisaria omitir o detalhe por empresa.'])
h += [PageBreak()]

# ---------- 5. PARTE 2 ----------
h += [P('Parte 2 — Guia de uso: o que cada aba oferece', sH1),
      P(f'Para abrir a ferramenta, acesse <link href="{SITE}" color="#1f3a66">{SITE}</link> em qualquer navegador, no computador ou no celular. Não precisa instalar nada nem fazer login. O menu no topo tem 7 abas; cada uma responde a uma pergunta.')]
h += tabela(['Aba', 'Pergunta que responde'], [
    ['Visão geral', 'Qual é o Score ASG e como estão os temas do grupo e a carteira da agência?'],
    ['Temas T1 e T14', 'Como a agência está em compliance e em integridade?'],
    ['Do plano ao painel', 'De qual compromisso vem cada indicador, qual é o controle e qual é a meta até 2030?'],
    ['ASG Investe', 'A agência atrai bem, decide rápido e dá o exemplo?'],
    ['ASG Empresas', 'O que os empreendimentos atraídos entregam ao estado?'],
    ['Editar dados', 'O que muda nos indicadores se eu incluir, alterar ou excluir um registro?'],
    ['Qualidade dos dados', 'Dá para confiar nos números?']], [4.2, 13.2])
h += [P('Como ler um cartão de indicador', sH2), P('Todo indicador aparece no mesmo formato, em qualquer aba:')]
h += lista(['<b>Código e etiqueta de origem.</b> A etiqueta diz se o número foi calculado da base (verde), se é demonstração (laranja) ou se ainda não há dado (cinza).',
            '<b>Nome e valor</b> em destaque.',
            '<b>Barra e nota.</b> Mostram quanto da meta de 2030 já foi alcançado: verde (80 ou mais), laranja (50 a 79) ou vermelha (abaixo de 50). Só aparecem em indicadores com meta.',
            '<b>Linha de contexto,</b> quando existe, como “36 de 42 colaboradores”.',
            '<b>Como é calculado.</b> Ao clicar, abre a fórmula, a fonte, o controle de compliance e o compromisso de governo ligado.'])
h += [P('As cores dos pilares são fixas: verde para Ambiental, laranja para Social e azul para Governança.')]

GUIA = [
 ('geral', '2.1 Visão geral', 'É a página de entrada. Em uma tela, mostra a nota geral, os temas do grupo e o retrato da carteira.',
  ['<b>Score ASG</b> no topo, em um anel de 0 a 100.', '<b>Temas do grupo:</b> T1 e T14, cada um com sua nota e o número de indicadores. Clicar leva à aba dos temas.',
   '<b>Score por pilar</b> (Ambiental, Social, Governança) e <b>leitura automática dos dados:</b> frases geradas pelo painel com o setor líder, os pontos de atenção, os indicadores mais longe da meta e os destaques.',
   '<b>A carteira da agência:</b> número de projetos, investimento previsto, percentual executado e empregos; gráficos de projetos por status, investimento atraído por ano e por setor.',
   '<b>Frentes da Investe Piauí:</b> os setores estratégicos, com projetos e valor de cada um, e os programas da agência.',
   '<b>Dois olhares:</b> atalhos para ASG Investe e ASG Empresas.'],
  'Comece por aqui. A leitura automática já aponta onde olhar primeiro; os cartões dos temas e os atalhos levam ao detalhe.'),
 ('temas', '2.2 Temas T1 e T14', 'Reúne os 13 indicadores dos dois temas que a Matriz de Materialidade atribuiu ao Grupo 2.',
  ['<b>T1 — Governança ética e compliance:</b> 5 indicadores sobre treinamento de integridade, código de conduta, conflito de interesses, cláusula ASG e avaliação de fornecedores. Gráficos de treinamento por área e de cláusulas dos contratos.',
   '<b>T14 — Integridade e combate à corrupção:</b> 8 indicadores sobre due diligence das empresas, declaração e cláusula anticorrupção, canal de denúncias e controles internos. Gráficos de risco das empresas, situação dos controles e relatos por categoria.',
   '<b>Controles que pedem ação:</b> lista dos controles internos não testados ou com falha.'],
  'Use para acompanhar o programa de integridade. As áreas com menor percentual de treinamento aparecem primeiro; a tabela final mostra por onde começar nos controles.'),
 ('sequencia', '2.3 Do plano ao painel', 'Mostra a sequência trabalhada em sala e prova que nenhum indicador está solto.',
  ['<b>As 5 etapas:</b> Plano de Governo, Compromissos de Governo, Pacote de Indicadores, Plano de Compliance e Plano Estratégico ASG de 4 anos.',
   '<b>Compromissos, indicadores e controles:</b> tabela com todos os indicadores, o compromisso a que respondem, o valor atual e o controle de compliance.',
   '<b>Caminho até 2030:</b> para cada indicador com meta, o valor de hoje, a trajetória ano a ano de 2027 a 2030 e a nota.'],
  'Clique nos botões C1 a C6 para ver só os indicadores de um compromisso. A tabela de metas serve de base para pactuar os valores com a agência.'),
 ('investe', '2.4 ASG Investe', 'O olhar para dentro da agência: desempenho da atração de investimentos, prazos e conduta.',
  ['<b>Quatro números de resumo:</b> conversão da carteira, tempo da atração à captação, demandas externas no prazo e nota do pilar Governança.',
   '<b>Carteira por estágio,</b> em investimento previsto.', '<b>Indicadores por pilar</b> (Governança, Social e Ambiental). Os de integridade ficam na aba Temas T1 e T14.',
   '<b>Demandas no prazo por órgão</b> (SEMAR, INTERPI, Equatorial) e <b>consumo de energia da sede</b> mês a mês.'],
  'Use para avaliar a operação da agência. O gráfico por órgão mostra onde os projetos travam fora dela.'),
 ('empresas', '2.5 ASG Empresas', 'O olhar para fora: o que os empreendimentos atraídos entregam em energia limpa, emprego e território.',
  ['<b>Indicadores dos empreendimentos.</b> Os que dependem de questionário às empresas aparecem como “a coletar”, em vez de um número inventado.',
   '<b>Investimento × empregos por projeto</b> (cada ponto é um projeto, colorido por setor; passar o mouse mostra o nome) e <b>empresas por país de origem.</b>',
   '<b>Resultado por setor,</b> municípios que mais recebem investimento e empregos gerados por setor.', '<b>Tabela dos projetos da carteira,</b> com filtro.'],
  'Escolha um setor e um status nos filtros acima da tabela. O total de projetos, de investimento e de empregos do recorte aparece ao lado.'),
 ('editar', '2.6 Editar dados', f'Torna a ferramenta viva: permite incluir, alterar e excluir registros de {N["tabs"]} tabelas e ver o efeito na hora.',
  ['<b>Notas no topo:</b> Score ASG e notas dos temas, com o valor de antes e de depois de cada edição.',
   '<b>1. Escolha a tabela:</b> Projetos, Due diligence, Canal de denúncias, Colaboradores, Controles internos, Contratos, Demandas externas ou Consumo da sede.',
   '<b>2. Formulário:</b> preencha os campos e clique em Adicionar registro. O painel recusa código repetido, número negativo, realizado maior que previsto e data fora do formato, e explica o motivo.',
   '<b>3. Registros:</b> cada linha tem os botões Editar e Excluir.',
   '<b>Envio de arquivo:</b> logo abaixo do formulário, o botão Escolher arquivo recebe um CSV ou JSON com vários registros da tabela escolhida. A ferramenta lê o arquivo inteiro, confere linha por linha e mostra um laudo: aprovado, aprovado em parte ou recusado, com o motivo de cada linha que não pode ser usada. Nada entra na base até você clicar em Adicionar os registros válidos. O botão Baixar modelo CSV entrega um arquivo com as colunas certas e uma linha de exemplo.',
   '<b>Importar e exportar:</b> exporta a base inteira em JSON ou substitui a base por um arquivo JSON exportado antes.',
   '<b>Pesos do Score ASG:</b> altere o peso de cada pilar.', '<b>Restaurar base original:</b> apaga as edições e volta ao ponto de partida.'],
  'Exemplo: escolha Colaboradores, cadastre um colaborador sem treinamento e veja o indicador T1.1 e a nota do tema caírem. Para incluir muitos projetos de uma vez, escolha Projetos, baixe o modelo CSV, preencha no Excel, salve como CSV e envie; o laudo diz o que está pronto para uso. As edições ficam salvas só no seu navegador; a base publicada não muda e outras pessoas não veem as suas alterações.'),
 ('dados', '2.7 Qualidade dos dados', 'Mostra se os números merecem confiança e de onde vem cada dado.',
  [f'<b>{len(TESTES)} testes automáticos,</b> com o valor esperado, o obtido e o resultado (OK ou ERRO).',
   '<b>Contagem dos indicadores</b> por origem: calculados, de demonstração e sem dado.', '<b>De onde vem cada dado:</b> origem de cada tabela hoje e o que falta para virar dado real.'],
  'Confira esta aba depois de editar ou importar dados. Se um teste de T01 a T11 ficar em ERRO após uma edição, é porque os totais da carteira deixaram de fechar com o número oficial.'),
]
for aba, tit, serve, itens, uso in GUIA:
    h += [KeepTogether([P(tit, sH2), P('<b>Para que serve.</b> ' + serve)] + foto(aba, f'Aba {tit[4:]}, como aparece ao abrir.'))]
    h += [P('O que você encontra', sH3)] + lista(itens) + [P('<b>Como usar.</b> ' + uso)]
h += [P('Dúvidas frequentes', sH2)]
h += lista(['<b>Os números são reais?</b> Não. A base é sintética e calibrada com os totais oficiais; nenhum registro representa empresa ou pessoa real.',
            '<b>Editei um dado e quero desfazer.</b> Use Restaurar base original, na aba Editar dados.',
            '<b>Outra pessoa vê as minhas edições?</b> Não. Elas ficam no seu navegador. Para compartilhar, exporte a base em JSON e envie o arquivo; a outra pessoa importa na mesma aba.',
            '<b>Funciona no celular?</b> Sim. O menu rola para os lados e as tabelas largas rolam dentro da própria moldura.',
            '<b>Onde está o código?</b> No repositório do GitHub indicado na capa; o README explica a estrutura e como executar.'])

os.makedirs('docs', exist_ok=True)
SimpleDocTemplate('docs/documentacao_painel_asg.pdf', pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.7 * cm, bottomMargin=1.8 * cm,
                  title='Painel ASG · Investe Piauí — Documentação', author='Grupo 2 — Ciência de Dados, iCEV 2026.2').build(h, onLaterPages=rodape, onFirstPage=lambda c, d: None)
print('docs/documentacao_painel_asg.pdf gerado;', len(IND), 'indicadores;', len(TESTES), 'testes')
