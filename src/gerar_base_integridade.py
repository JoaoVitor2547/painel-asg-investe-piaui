"""Gera a base sintetica dos temas T1 (governanca etica e compliance) e T14 (integridade e controles internos).
Semente fixa: rodar de novo produz exatamente a mesma planilha."""
import random
from datetime import date, timedelta
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
rng = random.Random(14)
wb = Workbook(); wb.remove(wb.active)
HDR = PatternFill('solid', fgColor='C9D6EC')
def aba(nome, cab, linhas, larg):
    ws = wb.create_sheet(nome)
    for j, h in enumerate(cab, 1):
        c = ws.cell(row=1, column=j, value=h); c.font = Font(name='Arial', bold=True, size=10); c.fill = HDR
        c.alignment = Alignment(wrap_text=True, vertical='center'); ws.column_dimensions[c.column_letter].width = larg[j-1]
    for r in linhas:
        ws.append(r)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.font = Font(name='Arial', size=10)
            if hasattr(c.value, 'strftime'): c.number_format = 'dd/mm/yyyy'
    ws.freeze_panes = 'A2'
sn = lambda p: 'Sim' if rng.random() < p else 'Não'

# empresas e contratos vem da base principal, para as chaves baterem
base = load_workbook('dados/base_asg_grupo2.xlsx', data_only=True)
empresas = [r[0] for r in base['Empresas'].iter_rows(min_row=2, values_only=True) if str(r[0]).startswith('EMP')]
contratos = [r[0] for r in base['CONTRATOS'].iter_rows(min_row=2, values_only=True) if str(r[0]).startswith('CT-')]

dd = []
for e in empresas:
    feita = sn(0.78); risco = rng.choices(['Baixo', 'Médio', 'Alto'], [0.6, 0.28, 0.12])[0] if feita == 'Sim' else None
    dd.append([e, feita, date(2024, 1, 10) + timedelta(days=rng.randint(0, 900)) if feita == 'Sim' else None, risco,
               ('Sim' if rng.random() < (0.5 if risco == 'Alto' else 0.12) else 'Não') if feita == 'Sim' else None, sn(0.85), 'SINTÉTICO'])
aba('DUE_DILIGENCE', ['Código da Empresa', 'Due diligence realizada', 'Data da análise', 'Nível de risco', 'Pendência aberta',
                      'Declaração anticorrupção assinada', 'origem_do_registro'], dd, [18, 20, 16, 14, 16, 26, 18])

cats = ['Conflito de interesses', 'Fraude ou corrupção', 'Descumprimento de norma interna', 'Assédio ou conduta', 'Outros']
den = []
for i in range(1, 27):
    reg = date(2025, 1, 6) + timedelta(days=rng.randint(0, 680)); aberta = reg > date(2026, 10, 5)
    fim = None if aberta else reg + timedelta(days=rng.randint(6, 58))
    den.append([f'DEN{i:03d}', reg, rng.choices(cats, [0.25, 0.15, 0.3, 0.15, 0.15])[0], fim, 30,
                None if aberta else sn(0.4), 'SINTÉTICO'])
den.sort(key=lambda r: r[1])
for r in den[-3:]: r[3] = None; r[5] = None      # os 3 relatos mais recentes ainda estao em apuracao
for i, r in enumerate(den, 1): r[0] = f'DEN{i:03d}'  # numera na ordem de chegada
aba('CANAL_DENUNCIAS', ['ID Relato', 'Data do registro', 'Categoria', 'Data de conclusão da apuração', 'Prazo-meta (dias)',
                        'Procedente', 'origem_do_registro'], den, [12, 16, 30, 26, 16, 12, 18])

areas = ['Atração de investimentos', 'Jurídico e compliance', 'Administrativo-financeiro', 'Comunicação', 'Projetos e inovação', 'Presidência e diretoria']
col = [[f'COL{i:02d}', rng.choice(areas), sn(0.74), sn(0.88), sn(0.69), 'SINTÉTICO'] for i in range(1, 43)]
aba('COLABORADORES_INTEGRIDADE', ['ID Colaborador', 'Área', 'Treinamento de integridade 2026', 'Termo do código de conduta assinado',
                                  'Declaração de conflito de interesses entregue', 'origem_do_registro'], col, [14, 28, 26, 30, 36, 18])

ctrl_nomes = [('Segregação de funções na aprovação de projetos', 'Atração'), ('Dupla aprovação de pagamentos', 'Financeiro'),
    ('Checagem de conflito de interesses antes de contratar', 'Contratações'), ('Due diligence de integridade antes do protocolo de intenções', 'Atração'),
    ('Cláusula anticorrupção obrigatória em contratos', 'Jurídico'), ('Registro de reuniões com investidores', 'Atração'),
    ('Conciliação mensal de despesas', 'Financeiro'), ('Revisão de acessos a sistemas e planilhas', 'TI'),
    ('Validação do cadastro empresa–projeto', 'Dados'), ('Registro de brindes e hospitalidades', 'Compliance'),
    ('Publicação de contratos no Portal da Transparência', 'Transparência'), ('Tratamento de relatos do canal de denúncias no prazo', 'Compliance'),
    ('Aprovação da Presidência para empresas da carteira', 'Atração'), ('Guarda de evidências dos indicadores ASG', 'Dados'),
    ('Monitoramento de prazos de órgãos externos (SLA)', 'Atração'), ('Classificação de sigilo antes de divulgar dados', 'Comunicação')]
ci = []
for i, (n, p) in enumerate(ctrl_nomes, 1):
    t = sn(0.75); res = rng.choices(['Efetivo', 'Com falha'], [0.75, 0.25])[0] if t == 'Sim' else None
    ci.append([f'CI{i:02d}', n, p, t, res, (sn(0.6) if res == 'Com falha' else None), 'SINTÉTICO'])
aba('CONTROLES_INTERNOS', ['ID Controle', 'Controle', 'Processo', 'Testado em 2026', 'Resultado do teste', 'Plano de ação no prazo',
                           'origem_do_registro'], ci, [12, 56, 16, 16, 18, 22, 18])

aba('CONTRATOS_INTEGRIDADE', ['id_contrato', 'Cláusula anticorrupção', 'Fornecedor avaliado quanto à integridade', 'origem_do_registro'],
    [[c, sn(0.72), sn(0.55), 'SINTÉTICO'] for c in contratos], [14, 22, 38, 18])

dic = [
 ('DUE_DILIGENCE', 'Código da Empresa', 'Identificador da empresa (chave para a aba Empresas da base principal)', 'Código existente na aba Empresas'),
 ('DUE_DILIGENCE', 'Due diligence realizada', 'Indica se a empresa passou por análise de integridade', 'Sim ou Não'),
 ('DUE_DILIGENCE', 'Data da análise', 'Data em que a análise foi concluída', 'Data; vazio se não realizada'),
 ('DUE_DILIGENCE', 'Nível de risco', 'Classificação de risco de integridade resultante da análise', 'Baixo, Médio ou Alto; vazio se não realizada'),
 ('DUE_DILIGENCE', 'Pendência aberta', 'Indica se há apontamento da análise ainda sem tratamento', 'Sim ou Não; vazio se não realizada'),
 ('DUE_DILIGENCE', 'Declaração anticorrupção assinada', 'Indica se a empresa assinou a declaração anticorrupção', 'Sim ou Não'),
 ('CANAL_DENUNCIAS', 'ID Relato', 'Identificador único do relato', 'Código único (DEN001…)'),
 ('CANAL_DENUNCIAS', 'Data do registro', 'Data de entrada do relato no canal', 'Data'),
 ('CANAL_DENUNCIAS', 'Categoria', 'Assunto do relato', 'Lista fechada de categorias; nunca identificar pessoas (LGPD)'),
 ('CANAL_DENUNCIAS', 'Data de conclusão da apuração', 'Data em que a apuração terminou', 'Data; vazio enquanto em apuração'),
 ('CANAL_DENUNCIAS', 'Prazo-meta (dias)', 'Prazo interno para concluir a apuração', 'Inteiro de dias'),
 ('CANAL_DENUNCIAS', 'Procedente', 'Resultado da apuração', 'Sim ou Não; vazio enquanto em apuração'),
 ('COLABORADORES_INTEGRIDADE', 'ID Colaborador', 'Identificador sem nome, para não expor dado pessoal', 'Código (COL01…)'),
 ('COLABORADORES_INTEGRIDADE', 'Área', 'Área de lotação', 'Lista padronizada de áreas'),
 ('COLABORADORES_INTEGRIDADE', 'Treinamento de integridade 2026', 'Indica se concluiu o treinamento anual', 'Sim ou Não'),
 ('COLABORADORES_INTEGRIDADE', 'Termo do código de conduta assinado', 'Indica adesão formal ao código de conduta', 'Sim ou Não'),
 ('COLABORADORES_INTEGRIDADE', 'Declaração de conflito de interesses entregue', 'Indica entrega da declaração anual', 'Sim ou Não'),
 ('CONTROLES_INTERNOS', 'ID Controle', 'Identificador do controle', 'Código (CI01…)'),
 ('CONTROLES_INTERNOS', 'Controle', 'Descrição do controle interno', 'Texto objetivo'),
 ('CONTROLES_INTERNOS', 'Processo', 'Processo a que o controle pertence', 'Lista padronizada'),
 ('CONTROLES_INTERNOS', 'Testado em 2026', 'Indica se o controle foi testado no ano', 'Sim ou Não'),
 ('CONTROLES_INTERNOS', 'Resultado do teste', 'Resultado do teste do controle', 'Efetivo ou Com falha; vazio se não testado'),
 ('CONTROLES_INTERNOS', 'Plano de ação no prazo', 'Para controles com falha, indica se o plano de ação está em dia', 'Sim ou Não; vazio se não se aplica'),
 ('CONTRATOS_INTEGRIDADE', 'id_contrato', 'Identificador do contrato (chave para a aba CONTRATOS da base principal)', 'Código existente na aba CONTRATOS'),
 ('CONTRATOS_INTEGRIDADE', 'Cláusula anticorrupção', 'Indica se o contrato traz cláusula anticorrupção', 'Sim ou Não'),
 ('CONTRATOS_INTEGRIDADE', 'Fornecedor avaliado quanto à integridade', 'Indica se o fornecedor passou por avaliação antes da assinatura', 'Sim ou Não'),
]
aba('DICIONARIO DE DADOS', ['ABA', 'VARIÁVEL', 'DESCRIÇÃO DA VARIÁVEL', 'COMO PREENCHER'], [list(d) for d in dic], [28, 40, 60, 50])
ws = wb.create_sheet('LEIA-ME', 0); ws.column_dimensions['A'].width = 120
for t in ['BASE DE GOVERNANÇA E INTEGRIDADE — GRUPO 2 — TEMAS T1 E T14 DA MATRIZ DE MATERIALIDADE',
          'T1: Governança ética e compliance · T14: Integridade e combate à corrupção (controles internos).',
          'Todos os registros são SINTÉTICOS, gerados com semente fixa por src/gerar_base_integridade.py. Nenhum representa pessoa, empresa ou relato real.',
          'As chaves Código da Empresa e id_contrato batem com a base principal (base_asg_grupo2.xlsx).',
          'O dicionário de dados desta base está na aba DICIONARIO DE DADOS, no mesmo formato do dicionário de exemplo da Investe Piauí.']:
    ws.append([t])
ws['A1'].font = Font(name='Arial', bold=True, size=11)
wb.save('dados/base_integridade_grupo2.xlsx'); print('ok', len(dd), len(den), len(col), len(ci), len(contratos))
