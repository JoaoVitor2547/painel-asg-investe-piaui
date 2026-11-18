"""Le as duas planilhas da pasta dados/ e gera dados/dados.json, so com as colunas que o painel usa.
Uso: python3 src/extrair.py   (rodar a partir da raiz do repositorio)"""
import json
from openpyxl import load_workbook

def leitor(caminho):
    wb = load_workbook(caminho, data_only=True)
    def rows(aba):
        it = wb[aba].iter_rows(values_only=True)
        cab = [str(x) if x is not None else '' for x in next(it)]
        return [dict(zip(cab, r)) for r in it if r[0] not in (None, '')]
    return rows

d = lambda v: v.strftime('%Y-%m-%d') if hasattr(v, 'strftime') else None
prazo = lambda a, b: (b - a).days if hasattr(a, 'strftime') and hasattr(b, 'strftime') else None
A = leitor('dados/base_asg_grupo2.xlsx')          # base principal (carteira)
B = leitor('dados/base_integridade_grupo2.xlsx')  # base dos temas T1 e T14

cid = {r['Código do Projeto']: r['Cidade'] for r in A('CidadeProjeto')}
P = [dict(c=r['Código do Projeto'], e=r['Código da Empresa'], n=r['Nome do Projeto'], s=r['Setor Investe'],
          miss=r['Captada por Missão'], estr=r['Investimento Estrangeiro'],
          da=d(r['Data de Atração']), dc=d(r['Data de Captação']),
          ip=r['Investimento Previsto'], ir=r['Investimento Realizado (adicional)'] or 0,
          ep=r['Empregos Diretos Previsto'], eg=r['Empregos Gerados (adicional)'], ei=r['Empregos Indiretos'],
          st=r['Status do Projeto'], cid=cid.get(r['Código do Projeto']))
     for r in A('Projetos') if str(r['Código do Projeto']).startswith('PRJ')]
E = [dict(c=r['Código da Empresa'], s=r['Setor Investe'], pais=r['Pais de Origem'])
     for r in A('Empresas') if str(r['Código da Empresa']).startswith('EMP')]
X = [dict(id=r['ID Demanda'], org=r['Orgão (SEMAR/INTERPI/Equatorial)'], nome=r['Nome Demanda'], prj=r['ID Projeto'],
          sla=r['Prazo SLA (dias)'], dias=prazo(r['Data Solicitação'], r['Data Resposta']))
     for r in A('Processos_Externos') if str(r['ID Demanda']).startswith('DEM')]
anti = {r['id_contrato']: r for r in B('CONTRATOS_INTEGRIDADE')}
C = [dict(id=r['id_contrato'], ano=r['ano'], obj=r['objeto_resumido'], asg=r['possui_clausula_asg'],
          anti=anti[r['id_contrato']]['Cláusula anticorrupção'], forn=anti[r['id_contrato']]['Fornecedor avaliado quanto à integridade'])
     for r in A('CONTRATOS') if str(r['id_contrato']).startswith('CT-')]
S = [dict(m=r['mes (AAAA-MM)'], kwh=r['kwh_energia'], agua=r['m3_agua'], res=r['kg_residuos']) for r in A('CONSUMO_SEDE')]
K = [dict(prj=r['Código do Projeto'], tipo=r['Atividade Principal']) for r in A('Comunicação') if str(r['Código do Projeto']).startswith('PRJ')]
R = [dict(id=r['id_indicador'], ano=r['Ano'], val=r['Valor Medido']) for r in A('RESULTADOS ASG') if str(r['Código da Medição']).startswith('MED')]
G = [dict(e=r['Código da Empresa'], dd=r['Due diligence realizada'], risco=r['Nível de risco'], pend=r['Pendência aberta'],
          decl=r['Declaração anticorrupção assinada']) for r in B('DUE_DILIGENCE')]
N = [dict(id=r['ID Relato'], dr=d(r['Data do registro']), cat=r['Categoria'], meta=r['Prazo-meta (dias)'],
          dias=prazo(r['Data do registro'], r['Data de conclusão da apuração']), proc=r['Procedente']) for r in B('CANAL_DENUNCIAS')]
T = [dict(id=r['ID Colaborador'], area=r['Área'], trein=r['Treinamento de integridade 2026'],
          cod=r['Termo do código de conduta assinado'], conf=r['Declaração de conflito de interesses entregue']) for r in B('COLABORADORES_INTEGRIDADE')]
I = [dict(id=r['ID Controle'], nome=r['Controle'], proc=r['Processo'], test=r['Testado em 2026'], res=r['Resultado do teste'],
          plano=r['Plano de ação no prazo']) for r in B('CONTROLES_INTERNOS')]

dados = dict(P=P, E=E, X=X, C=C, S=S, K=K, R=R, G=G, N=N, T=T, I=I)
json.dump(dados, open('dados/dados.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print({k: len(v) for k, v in dados.items()})
