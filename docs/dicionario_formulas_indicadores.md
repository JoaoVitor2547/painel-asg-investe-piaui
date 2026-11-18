# Dicionário de fórmulas e indicadores

Gerado por `src/gerar_dicionarios.py` a partir do catálogo do próprio painel. Os valores vêm da base sintética do repositório.

## Score ASG

| Medida | Fórmula | Observação |
| --- | --- | --- |
| Nota do indicador (quanto maior, melhor) | mín(valor ÷ meta; 1) × 100 | Mostra quanto da meta de 2030 já foi alcançado. Limitada a 100. |
| Nota do indicador (quanto menor, melhor) | mín(meta ÷ valor; 1) × 100 | Usada em prazos, consumo, concentração e pendências. |
| Nota do pilar (Ambiental, Social, Governança) | média das notas dos indicadores do pilar que têm meta e valor | Indicadores sem meta ou sem dado não entram. |
| Nota do tema (T1, T14) | média das notas dos indicadores do tema | T1: 5 indicadores. T14: 8 indicadores. |
| SCORE ASG | (Ambiental × 25 + Social × 25 + Governança × 50) ÷ 100 | Média ponderada dos três pilares. O peso maior da Governança reflete os temas do grupo (T1 e T14). Os pesos podem ser alterados na aba Editar dados. |
| Faixas de leitura | 0 a 49: crítico · 50 a 79: em evolução · 80 a 100: próximo da meta | Definem a cor da barra de cada cartão. |

### Resultado com a base atual

| Medida | Nota (0 a 100) |
| --- | --- |
| SCORE ASG | 69,4 |
| Ambiental | 69,9 |
| Social | 71,1 |
| Governança | 68,3 |
| Tema T1 | 71,6 |
| Tema T14 | 75,2 |

## Indicadores (41)

| Código | Tema | Pilar | Indicador | Fórmula | Fonte (tabela) | Origem do valor | Valor atual | Meta 2030 (proposta) | Sentido | Nota (0-100) | Controle de compliance | Compromisso de governo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1.1 | T1 | Governança | Colaboradores treinados em integridade | Colaboradores com treinamento de integridade no ano ÷ total de colaboradores | COLABORADORES_INTEGRIDADE | Calculado da base | 85,7% | 100,0% | quanto maior, melhor | 86 | Lista de presença ou certificado do treinamento | C5 · Gestão íntegra, transparente e ágil |
| T1.2 | T1 | Governança | Adesão ao código de conduta | Colaboradores com termo do código de conduta assinado ÷ total | COLABORADORES_INTEGRIDADE | Calculado da base | 95,2% | 100,0% | quanto maior, melhor | 95 | Termo assinado arquivado pelo RH | C5 · Gestão íntegra, transparente e ágil |
| T1.3 | T1 | Governança | Declarações de conflito de interesses entregues | Colaboradores com declaração anual entregue ÷ total | COLABORADORES_INTEGRIDADE | Calculado da base | 66,7% | 100,0% | quanto maior, melhor | 67 | Declaração anual obrigatória, renovada todo ano | C5 · Gestão íntegra, transparente e ágil |
| T1.4 | T1 | Governança | Contratos da agência com cláusula ASG | Contratos com cláusula ASG ÷ total de contratos | CONTRATOS | Calculado da base | 63,9% | 100,0% | quanto maior, melhor | 64 | Conferência do jurídico/compliance na assinatura | C5 · Gestão íntegra, transparente e ágil |
| T1.5 | T1 | Governança | Fornecedores avaliados antes de contratar | Contratos com fornecedor avaliado quanto à integridade ÷ total de contratos | CONTRATOS_INTEGRIDADE | Calculado da base | 41,7% | 90,0% | quanto maior, melhor | 46 | Ficha de avaliação anexada ao processo de contratação | C5 · Gestão íntegra, transparente e ágil |
| T14.1 | T14 | Governança | Empresas da carteira com due diligence de integridade | Empresas com due diligence realizada ÷ total de empresas da carteira | DUE_DILIGENCE | Calculado da base | 77,9% | 100,0% | quanto maior, melhor | 78 | Análise concluída antes do protocolo de intenções | C5 · Gestão íntegra, transparente e ágil |
| T14.2 | T14 | Governança | Empresas de risco alto com pendência aberta | Empresas de risco alto com pendência aberta ÷ empresas de risco alto | DUE_DILIGENCE | Calculado da base | 14,3% | 5,0% | quanto menor, melhor | 35 | Pendência de risco alto tratada antes de qualquer benefício | C5 · Gestão íntegra, transparente e ágil |
| T14.3 | T14 | Governança | Empresas com declaração anticorrupção assinada | Empresas com declaração anticorrupção assinada ÷ total de empresas | DUE_DILIGENCE | Calculado da base | 83,8% | 100,0% | quanto maior, melhor | 84 | Declaração assinada pelo representante legal | C5 · Gestão íntegra, transparente e ágil |
| T14.4 | T14 | Governança | Contratos com cláusula anticorrupção | Contratos com cláusula anticorrupção ÷ total de contratos | CONTRATOS_INTEGRIDADE | Calculado da base | 66,7% | 100,0% | quanto maior, melhor | 67 | Cláusula padrão obrigatória na minuta (Lei 12.846/2013) | C5 · Gestão íntegra, transparente e ágil |
| T14.5 | T14 | Governança | Relatos do canal de denúncias apurados no prazo | Relatos concluídos dentro do prazo-meta ÷ relatos concluídos | CANAL_DENUNCIAS | Calculado da base | 69,6% | 90,0% | quanto maior, melhor | 77 | Prazo calculado pelas datas; sem identificação de pessoas (LGPD) | C5 · Gestão íntegra, transparente e ágil |
| T14.6 | T14 | Governança | Prazo médio de apuração dos relatos | Média de (data de conclusão − data do registro) | CANAL_DENUNCIAS | Calculado da base | 23 dias | 20 dias | quanto menor, melhor | 86 | Calculado automaticamente | C5 · Gestão íntegra, transparente e ágil |
| T14.7 | T14 | Governança | Controles internos testados no ano | Controles testados no ano ÷ total de controles mapeados | CONTROLES_INTERNOS | Calculado da base | 75,0% | 100,0% | quanto maior, melhor | 75 | Plano anual de testes aprovado pela diretoria | C5 · Gestão íntegra, transparente e ágil |
| T14.8 | T14 | Governança | Controles internos efetivos | Controles com resultado Efetivo ÷ controles testados | CONTROLES_INTERNOS | Calculado da base | 91,7% | 90,0% | quanto maior, melhor | 100 | Controle com falha gera plano de ação com prazo | C5 · Gestão íntegra, transparente e ágil |
| IG1 | ASG Investe | Governança | Taxa de conversão da carteira | Projetos implantados ÷ total de projetos | Projetos | Calculado da base | 39,2% | 55,0% | quanto maior, melhor | 71 | Status só da lista institucional | C1 · Atrair investimento estratégico e diversificar a economia |
| IG2 | ASG Investe | Governança | Execução financeira da carteira | Investimento realizado ÷ investimento previsto | Projetos | Calculado da base | 45,4% | 70,0% | quanto maior, melhor | 65 | Valor realizado com comprovação da empresa | C1 · Atrair investimento estratégico e diversificar a economia |
| IG3 | ASG Investe | Governança | Tempo médio entre atração e captação | Média de (Data de Captação − Data de Atração) | Projetos | Calculado da base | 131 dias | 100 dias | quanto menor, melhor | 76 | Datas obrigatórias no cadastro do projeto | C5 · Gestão íntegra, transparente e ágil |
| IG4 | ASG Investe | Governança | Demandas externas respondidas dentro do SLA | Demandas dentro do SLA ÷ demandas respondidas (SEMAR, INTERPI, Equatorial) | Processos_Externos | Calculado da base | 33,3% | 85,0% | quanto maior, melhor | 39 | Status calculado pelas datas, nunca digitado | C5 · Gestão íntegra, transparente e ágil |
| IG5 | ASG Investe | Governança | Prazo médio de resposta dos órgãos | Média de (Data Resposta − Data Solicitação) | Processos_Externos | Calculado da base | 48 dias | 30 dias | quanto menor, melhor | 63 | Calculado automaticamente | C5 · Gestão íntegra, transparente e ágil |
| IG7 | ASG Investe | Governança | Projetos com ação de comunicação registrada | Projetos distintos na aba Comunicação ÷ total de projetos | Comunicação | Calculado da base | 11,7% | 50,0% | quanto maior, melhor | 23 | Divulgação só do que não é sigiloso (LGPD e sigilo comercial) | C5 · Gestão íntegra, transparente e ágil |
| IG8 | ASG Investe | Governança | Prazo médio de resposta do e-SIC | Média de (data da resposta − data do pedido) | Portal da Transparência / e-SIC | Demonstração | 11,6 dias |  |  |  | Lei de Acesso à Informação (Lei 12.527/2011) | C5 · Gestão íntegra, transparente e ágil |
| IG9 | ASG Investe | Governança | Projetos captados em missão institucional | Projetos com 'Captada por Missão' = Sim ÷ total | Projetos | Calculado da base | 29,2% |  |  |  | Campo Sim/Não obrigatório | C1 · Atrair investimento estratégico e diversificar a economia |
| IG10 | ASG Investe | Governança | Projetos com investimento estrangeiro | Projetos com 'Investimento Estrangeiro' = Sim ÷ total | Projetos + Empresas | Calculado da base | 25,0% |  |  |  | País de origem padronizado na aba Empresas | C1 · Atrair investimento estratégico e diversificar a economia |
| IS1 | ASG Investe | Social | Empregos gerados × previstos | Empregos gerados (implantados) ÷ empregos diretos previstos (implantados + em implantação) | Projetos | Calculado da base | 29,4% | 60,0% | quanto maior, melhor | 49 | Conferência anual com o Novo CAGED por município | C2 · Gerar emprego e renda |
| IS2 | ASG Investe | Social | Cobertura territorial da carteira | Municípios com pelo menos um projeto ÷ 224 municípios do Piauí | CidadeProjeto | Calculado da base | 13,8% | 22,0% | quanto maior, melhor | 63 | Nome do município conforme aba CodigoCidade | C4 · Levar desenvolvimento a todos os territórios |
| IS3 | ASG Investe | Social | Concentração do investimento nos 5 maiores municípios | Investimento previsto dos 5 municípios com maior valor ÷ total | Projetos + CidadeProjeto | Calculado da base | 44,3% | 40,0% | quanto menor, melhor | 90 | Recalcular a cada novo projeto captado | C4 · Levar desenvolvimento a todos os territórios |
| IS4 | ASG Investe | Social | Mulheres em cargos de liderança na agência | Mulheres em liderança ÷ total de cargos de liderança | RH da agência | Demonstração | 41,0% | 50,0% | quanto maior, melhor | 82 | Quadro de pessoal do RH, sem dado pessoal identificável (LGPD) | C6 · Inclusão e equidade |
| IS5 | ASG Investe | Social | Empreendedoras atendidas por mês (Investe Nelas) | Contagem de atendimentos no mês | Registros do programa Investe Nelas | Demonstração | 81 |  |  |  | Lista de presença/atendimento do programa | C6 · Inclusão e equidade |
| IA1 | ASG Investe | Ambiental | Energia renovável no investimento da carteira | Investimento previsto do setor Energia ÷ investimento previsto total | Projetos | Calculado da base | 67,5% | 70,0% | quanto maior, melhor | 96 | Classificação de setor conforme lista oficial 'Setor Investe' | C3 · Liderar a transição energética |
| IA2 | ASG Investe | Ambiental | Consumo médio mensal de energia da sede | Média de kwh_energia dos meses de 2026 | CONSUMO_SEDE | Calculado da base | 6.119 kWh | 5.500 kWh | quanto menor, melhor | 90 | Conta de energia arquivada como evidência do mês | C5 · Gestão íntegra, transparente e ágil |
| IA3 | ASG Investe | Ambiental | Consumo médio mensal de água da sede | Média de m3_agua dos meses de 2026 | CONSUMO_SEDE | Calculado da base | 45,1 m³ |  |  |  | Conta de água arquivada como evidência do mês | C5 · Gestão íntegra, transparente e ágil |
| IA4 | ASG Investe | Ambiental | Resíduos gerados pela sede por mês | Média de kg_residuos dos meses de 2026 | CONSUMO_SEDE | Calculado da base | 141 kg |  |  |  | Registro de pesagem/coleta | C5 · Gestão íntegra, transparente e ágil |
| IA5 | ASG Investe | Ambiental | Demandas ambientais (SEMAR) respondidas no prazo | Demandas à SEMAR dentro do SLA ÷ demandas à SEMAR respondidas | Processos_Externos | Calculado da base | 20,0% | 85,0% | quanto maior, melhor | 24 | Datas de solicitação e resposta obrigatórias | C5 · Gestão íntegra, transparente e ágil |
| EA1 | ASG Empresas | Ambiental | Potência renovável outorgada no Piauí | Soma da potência outorgada das usinas do PI | ANEEL — SIGA | Demonstração | 3.590 MW |  |  |  | CSV oficial filtrado por UF = PI | C3 · Liderar a transição energética |
| EA2 | ASG Empresas | Ambiental | Projetos com licença ambiental vigente | Projetos com licença válida ÷ projetos que exigem licença | Questionário ASG às empresas + SEMAR | Sem dado ainda | a coletar |  |  |  | Cópia da licença anexada | C3 · Liderar a transição energética |
| EA3 | ASG Empresas | Ambiental | Emissões evitadas pelos projetos de energia | tCO₂e evitadas por ano, declaradas pela empresa | Questionário ASG às empresas | Sem dado ainda | a coletar |  |  |  | Metodologia de cálculo informada pela empresa | C3 · Liderar a transição energética |
| ES1 | ASG Empresas | Social | Empregos diretos gerados pelos projetos implantados | Soma de Empregos Gerados dos projetos implantados | Projetos | Calculado da base | 10.500 |  |  |  | Reconcilia com o total oficial (teste T10) | C2 · Gerar emprego e renda |
| ES2 | ASG Empresas | Social | Empregos indiretos previstos | Soma de Empregos Indiretos | Projetos | Calculado da base | 71.400 |  |  |  | Inteiro não negativo | C2 · Gerar emprego e renda |
| ES3 | ASG Empresas | Social | Mão de obra local nos projetos | Trabalhadores residentes no município ÷ total de trabalhadores | Questionário ASG às empresas | Sem dado ainda | a coletar |  |  |  | Declaração da empresa, conferida por amostragem | C2 · Gerar emprego e renda |
| ES4 | ASG Empresas | Social | Mulheres no quadro das empresas | Mulheres ÷ total de trabalhadores do projeto | Questionário ASG às empresas | Sem dado ainda | a coletar |  |  |  | Dado agregado, sem identificação pessoal (LGPD) | C6 · Inclusão e equidade |
| EG1 | ASG Empresas | Governança | Empresas de origem estrangeira na carteira | Empresas com país de origem ≠ Brasil ÷ total de empresas | Empresas | Calculado da base | 27,9% |  |  |  | País padronizado | C1 · Atrair investimento estratégico e diversificar a economia |
| EG2 | ASG Empresas | Governança | Empresas com código de conduta e canal de denúncia | Empresas que comprovam os dois itens ÷ total | Questionário ASG às empresas | Sem dado ainda | a coletar |  |  |  | Documento anexado | C5 · Gestão íntegra, transparente e ágil |
