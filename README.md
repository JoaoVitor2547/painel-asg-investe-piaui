# Painel ASG · Investe Piauí

Painel web de indicadores ambientais, sociais e de governança (ASG) da Investe Piauí, com foco em **governança ética, compliance e integridade**.

**Ferramenta publicada:** https://joaovitor2547.github.io/painel-asg-investe-piaui/

Projeto acadêmico do **Grupo 2** para o Desafio Investe Piauí — BI e Governança ASG (Ciência de Dados, iCEV, 2026.2). Não é um canal oficial da agência.

## O projeto

O Grupo 2 recebeu dois temas da Matriz de Materialidade:

| Tema | O que o painel acompanha |
| --- | --- |
| **T1 — Governança ética e compliance** | Treinamento de integridade, adesão ao código de conduta, declarações de conflito de interesses, cláusulas ASG e avaliação de fornecedores |
| **T14 — Integridade e combate à corrupção (controles internos)** | Due diligence das empresas da carteira, cláusula anticorrupção, canal de denúncias e teste dos controles internos |

O painel segue a sequência trabalhada em sala: Plano de Governo → Compromissos de Governo → Pacote de Indicadores → Plano de Compliance → Plano Estratégico ASG de 4 anos. Os indicadores estão separados em dois olhares: **ASG Investe** (a agência) e **ASG Empresas** (os empreendimentos atraídos).

### Telas

| Tela | Pergunta que responde |
| --- | --- |
| Visão geral | Qual é o Score ASG e como estão os temas do grupo e a carteira? |
| Temas T1 e T14 | Como a agência está em compliance e integridade? |
| Do plano ao painel | De qual compromisso vem cada indicador, qual o controle e qual a meta até 2030? |
| ASG Investe | A agência atrai bem, decide rápido e dá o exemplo? |
| ASG Empresas | O que os empreendimentos entregam ao estado? |
| Editar dados | O que muda nos indicadores se eu incluir, alterar ou excluir um registro? |
| Qualidade dos dados | Dá para confiar nos números? |

A tela **Editar dados** permite incluir, alterar e excluir registros de 8 tabelas e exportar ou importar a base. Também recebe um **arquivo CSV ou JSON** com vários registros: a ferramenta lê o arquivo, confere linha por linha e mostra um laudo com o que pode ser usado e o motivo de cada linha recusada, antes de incluir qualquer coisa. A cada mudança o painel recalcula os 41 indicadores, as notas e os gráficos. As edições ficam salvas só no navegador de quem editou (localStorage); a base publicada não muda.

## Dados utilizados

Todos os registros são **sintéticos**. O cadastro real de empresas e projetos é protegido por sigilo comercial e pela LGPD, e o desafio exige termo de confidencialidade. A carteira simulada foi calibrada para fechar com os totais divulgados pelo Governo do Piauí em dezembro de 2025: 120 empreendimentos, R$ 44,7 bilhões previstos, 10,5 mil empregos gerados e 25,2 mil previstos.

| Arquivo | Conteúdo | Tabelas lidas pelo painel |
| --- | --- | --- |
| `dados/base_asg_grupo2.xlsx` | Carteira da agência, no formato do dicionário de exemplo da Investe Piauí | Projetos, CidadeProjeto, Empresas, Processos_Externos, CONTRATOS, CONSUMO_SEDE, Comunicação, RESULTADOS ASG |
| `dados/base_integridade_grupo2.xlsx` | Temas T1 e T14 | DUE_DILIGENCE, CANAL_DENUNCIAS, COLABORADORES_INTEGRIDADE, CONTROLES_INTERNOS, CONTRATOS_INTEGRIDADE |
| `dados/dados.json` | Extrato enxuto das duas planilhas, embutido no painel | gerado por `src/extrair.py` |

A documentação completa (como a ferramenta foi feita e guia de uso de cada aba) está em [`docs/documentacao_painel_asg.pdf`](docs/documentacao_painel_asg.pdf).

Cada planilha traz o seu dicionário na aba `DICIONARIO DE DADOS`. A versão reunida está em [`docs/dicionario_de_dados.md`](docs/dicionario_de_dados.md).

## Indicadores e fórmulas

São **41 indicadores**: 32 calculados direto das tabelas, 4 com medição de demonstração e 5 que dependem de um questionário a aplicar às empresas (aparecem como "a coletar"). O catálogo completo, com fórmula, fonte, meta e controle de cada um, está em [`docs/dicionario_formulas_indicadores.md`](docs/dicionario_formulas_indicadores.md) e na planilha de mesmo nome.

### Score ASG

| Medida | Fórmula |
| --- | --- |
| Nota do indicador, quanto maior melhor | `mín(valor ÷ meta; 1) × 100` |
| Nota do indicador, quanto menor melhor | `mín(meta ÷ valor; 1) × 100` |
| Nota do pilar e do tema | média das notas dos indicadores que têm meta e valor |
| **Score ASG** | `(Ambiental × 25 + Social × 25 + Governança × 50) ÷ 100` |

A nota mostra quanto da meta proposta para 2030 já foi alcançado. O peso maior da Governança reflete os temas do grupo e pode ser alterado na tela Editar dados. Com a base atual: Score ASG 69,4; T1 71,6; T14 75,2.

## Tecnologias

| Camada | Tecnologia |
| --- | --- |
| Painel | HTML5, CSS3 e JavaScript puro, em um único arquivo (`index.html`), sem framework nem biblioteca de gráficos |
| Gráficos | SVG e CSS escritos à mão |
| Preparação dos dados | Python 3 com openpyxl |
| Teste automatizado | Node.js com Playwright |
| Publicação | GitHub Pages |

## Como executar

Abrir a ferramenta: acessar o link publicado, ou baixar o repositório e dar duplo clique em `index.html`. Não precisa de servidor.

Reconstruir depois de alterar as planilhas ou o código (rodar na raiz do repositório):

```bash
pip install openpyxl playwright reportlab
python3 -m playwright install chromium   # navegador usado para ler o painel e gerar dicionários e PDF
python3 src/gerar_base_integridade.py   # opcional: recria a base sintética dos temas T1 e T14
python3 src/extrair.py                  # planilhas -> dados/dados.json
python3 src/montar.py                   # src/template.html + dados -> index.html
python3 src/gerar_dicionarios.py        # atualiza os dicionários da pasta docs/
python3 src/gerar_documentacao.py       # atualiza o PDF de documentação
```

Teste automatizado das 7 telas, em computador e celular, e do editor:

```bash
npm install playwright
npx playwright install chromium
node tests/teste.js
```

## Estrutura do repositório

```
index.html                      painel publicado (gerado; não editar à mão)
src/template.html               visual e lógica do painel (é aqui que se edita)
src/extrair.py                  planilhas -> dados.json
src/montar.py                   gera o index.html
src/gerar_base_integridade.py   gera a base sintética dos temas T1 e T14
src/gerar_dicionarios.py        gera os dicionários da pasta docs/
src/gerar_documentacao.py       gera o PDF de documentação
dados/                          bases de dados e dados.json
docs/                           documentação em PDF, dicionário de dados e dicionário de fórmulas e indicadores
tests/teste.js                  teste automatizado
assets/                         logotipo usado no cabeçalho
```

## Limitações

- A base é sintética: os valores mostram o que a ferramenta faz, não a situação real da agência.
- A redação dos compromissos de governo foi escrita pelo grupo e deve ser trocada pelo texto oficial.
- As metas de 2030 são proposta do grupo, a pactuar com a Investe Piauí.
- As edições feitas na tela Editar dados não são compartilhadas entre usuários.

## Equipe

Grupo 2 — Engenharia de Software (turma Borg), disciplina de Ciência de Dados, iCEV, 2026.2.

- Antonio Guilherme Santos da Silva
- João Vitor Fernandes de Sousa
- José Torres de Araujo Neto
- Julio Pereira de Oliveira Neto
- Luiz Matheus Soares Batista Cunha
- Octavio Alves Freire
- Ronney Said Bonfim dos Reis

## Créditos

A marca da Investe Piauí aparece apenas para identificar a agência parceira do desafio. Fonte dos totais oficiais: Governo do Piauí, "Piauí atrai 120 empreendimentos entre 2023 e 2025 e projeta R$ 44,7 bilhões em investimentos", dez. 2025.
