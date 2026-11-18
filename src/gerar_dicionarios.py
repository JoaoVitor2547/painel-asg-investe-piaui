"""Gera os dicionarios da pasta docs/ a partir das fontes, para nunca divergirem do painel:
 - docs/dicionario_formulas_indicadores.(md|xlsx): lido do catalogo de indicadores do proprio index.html
 - docs/dicionario_de_dados.(md|csv): uniao das abas DICIONARIO DE DADOS das duas planilhas
Uso: python3 src/gerar_dicionarios.py   (depois de montar.py; requer: pip install playwright openpyxl)"""
import csv, os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(); p.goto('file://' + os.path.abspath('index.html'))
    IND = p.evaluate("""() => IND.map(i => ({id:i.id, tema:i.mat || (i.tema==='inv' ? 'ASG Investe' : 'ASG Empresas'), pilar:PIL[i.pilar], nome:i.nome,
        formula:i.form, fonte:i.fonte, origem:ORG[i.o][1], valor:i.v==null ? 'a coletar' : i.f(i.v), meta:i.m==null ? '' : i.f(i.m),
        sentido:i.m==null ? '' : (i.dir>0 ? 'quanto maior, melhor' : 'quanto menor, melhor'), nota:i.sc==null ? '' : Math.round(i.sc),
        controle:i.ctrl, compromisso:i.c + ' · ' + COMP.find(c => c.id===i.c).t}))""")
    SC = p.evaluate("() => ({...SC})"); W = p.evaluate("() => ({...W})"); b.close()

cab = ['Código', 'Tema', 'Pilar', 'Indicador', 'Fórmula', 'Fonte (tabela)', 'Origem do valor', 'Valor atual', 'Meta 2030 (proposta)',
       'Sentido', 'Nota (0-100)', 'Controle de compliance', 'Compromisso de governo']
ch = ['id', 'tema', 'pilar', 'nome', 'formula', 'fonte', 'origem', 'valor', 'meta', 'sentido', 'nota', 'controle', 'compromisso']
n1 = lambda v: '—' if v is None else f'{v:.1f}'.replace('.', ',')

score = [
 ('Nota do indicador (quanto maior, melhor)', 'mín(valor ÷ meta; 1) × 100', 'Mostra quanto da meta de 2030 já foi alcançado. Limitada a 100.'),
 ('Nota do indicador (quanto menor, melhor)', 'mín(meta ÷ valor; 1) × 100', 'Usada em prazos, consumo, concentração e pendências.'),
 ('Nota do pilar (Ambiental, Social, Governança)', 'média das notas dos indicadores do pilar que têm meta e valor', 'Indicadores sem meta ou sem dado não entram.'),
 ('Nota do tema (T1, T14)', 'média das notas dos indicadores do tema', 'T1: 5 indicadores. T14: 8 indicadores.'),
 ('SCORE ASG', f"(Ambiental × {W['amb']} + Social × {W['soc']} + Governança × {W['gov']}) ÷ {W['amb']+W['soc']+W['gov']}",
  'Média ponderada dos três pilares. O peso maior da Governança reflete os temas do grupo (T1 e T14). Os pesos podem ser alterados na aba Editar dados.'),
 ('Faixas de leitura', '0 a 49: crítico · 50 a 79: em evolução · 80 a 100: próximo da meta', 'Definem a cor da barra de cada cartão.'),
]
res = [('SCORE ASG', SC['geral']), ('Ambiental', SC['amb']), ('Social', SC['soc']), ('Governança', SC['gov']), ('Tema T1', SC['T1']), ('Tema T14', SC['T14'])]

os.makedirs('docs', exist_ok=True)
with open('docs/dicionario_formulas_indicadores.md', 'w', encoding='utf-8') as f:
    f.write('# Dicionário de fórmulas e indicadores\n\n')
    f.write('Gerado por `src/gerar_dicionarios.py` a partir do catálogo do próprio painel. Os valores vêm da base sintética do repositório.\n\n')
    f.write('## Score ASG\n\n| Medida | Fórmula | Observação |\n| --- | --- | --- |\n')
    for a in score: f.write('| ' + ' | '.join(a) + ' |\n')
    f.write('\n### Resultado com a base atual\n\n| Medida | Nota (0 a 100) |\n| --- | --- |\n')
    for a, v in res: f.write(f'| {a} | {n1(v)} |\n')
    f.write(f'\n## Indicadores ({len(IND)})\n\n| ' + ' | '.join(cab) + ' |\n|' + ' --- |' * len(cab) + '\n')
    for i in IND: f.write('| ' + ' | '.join(str(i[k]).replace('|', '/') for k in ch) + ' |\n')

wb = Workbook(); ws = wb.active; ws.title = 'INDICADORES'
def cabecalho(ws, cols, larg):
    for j, h in enumerate(cols, 1):
        c = ws.cell(row=1, column=j, value=h); c.font = Font(name='Arial', bold=True, size=10); c.fill = PatternFill('solid', fgColor='C9D6EC')
        c.alignment = Alignment(wrap_text=True, vertical='center'); ws.column_dimensions[c.column_letter].width = larg[j-1]
    ws.freeze_panes = 'A2'
def corpo(ws):
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font = Font(name='Arial', size=10); c.alignment = Alignment(wrap_text=True, vertical='top')
cabecalho(ws, cab, [9, 14, 13, 42, 54, 30, 18, 14, 16, 20, 11, 48, 44])
for i in IND: ws.append([i[k] for k in ch])
corpo(ws)
w2 = wb.create_sheet('SCORE ASG'); cabecalho(w2, ['Medida', 'Fórmula', 'Observação'], [44, 60, 80])
for a in score: w2.append(list(a))
w2.append([]); w2.append(['Resultado com a base atual', 'Nota (0 a 100)'])
for a, v in res: w2.append([a, None if v is None else round(v, 1)])
corpo(w2)
wb.save('docs/dicionario_formulas_indicadores.xlsx')

linhas = []
for arq in ['dados/base_asg_grupo2.xlsx', 'dados/base_integridade_grupo2.xlsx']:
    wsd = load_workbook(arq, data_only=True)['DICIONARIO DE DADOS']
    for r in list(wsd.iter_rows(values_only=True))[1:]:
        if r[0]: linhas.append([os.path.basename(arq)] + [str(x or '') for x in r[:4]])
with open('docs/dicionario_de_dados.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';'); w.writerow(['ARQUIVO', 'ABA', 'VARIÁVEL', 'DESCRIÇÃO DA VARIÁVEL', 'COMO PREENCHER']); w.writerows(linhas)
with open('docs/dicionario_de_dados.md', 'w', encoding='utf-8') as f:
    f.write('# Dicionário de dados\n\nUnião das abas `DICIONARIO DE DADOS` das duas planilhas da pasta `dados/`. Formato do dicionário de exemplo da Investe Piauí.\n\n')
    f.write('| Arquivo | Aba | Variável | Descrição | Como preencher |\n| --- | --- | --- | --- | --- |\n')
    for l in linhas: f.write('| ' + ' | '.join(x.replace('|', '/') for x in l) + ' |\n')
print(len(IND), 'indicadores;', len(linhas), 'variáveis no dicionário de dados;', {k: round(v, 1) for k, v in SC.items()})
