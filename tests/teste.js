// Teste automatizado do painel: abre as 7 telas em computador e celular, procura erros e exercita o editor.
// Uso: npm install playwright && node tests/teste.js   (rodar a partir da raiz do repositorio)
const {chromium}=require('playwright'), path=require('path');
const URL='file://'+path.resolve('index.html'), TELAS=['geral','temas','sequencia','investe','empresas','editar','dados'];
(async()=>{ const b=await chromium.launch(); let falhas=0;
 for(const [w,h,tag,esquema] of [[1280,900,'computador','light'],[400,800,'celular','dark']]){
  const p=await b.newPage({viewport:{width:w,height:h},colorScheme:esquema}), erros=[];
  p.on('pageerror',e=>erros.push(String(e))); p.on('console',m=>{ if(m.type()==='error'&&!/ERR_|Failed to load resource/.test(m.text())) erros.push(m.text()) });
  for(const t of TELAS){ await p.goto(URL+'#'+t); await p.waitForTimeout(250);
   const sobra=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
   if(process.env.FOTOS) await p.screenshot({path:`/tmp/f_${tag}_${t}.png`,fullPage:true});
   const ok=sobra<=0&&!erros.length; if(!ok) falhas++; console.log(ok?'OK  ':'ERRO',tag,t,'estouro:',sobra,erros.join(' | ')); }
  if(tag==='computador'){
   await p.goto(URL+'#dados'); console.log('testes de qualidade:',await p.textContent('.kpi .v'));
   await p.goto(URL+'#editar'); const antes=await p.textContent('.kpi .v');
   await p.click('button[data-tab="T"]');                       // tabela Colaboradores
   await p.fill('#ed-id','COL99'); await p.fill('#ed-area','Teste'); await p.selectOption('#ed-trein','Não');
   await p.click('#f-ed button[type=submit]'); console.log('editor:',(await p.textContent('.msg')).trim(),'| score',antes,'->',await p.textContent('.kpi .v'));
   await p.fill('#ed-id','COL99'); await p.click('#f-ed button[type=submit]'); console.log('duplicado recusado:',(await p.textContent('.msg')).trim());
   await p.reload(); await p.waitForTimeout(200); console.log('persistiu apos recarregar:',await p.evaluate(()=>D.T.some(t=>t.id==='COL99')));
   await p.click('button[data-acao="restaurar"]'); await p.click('button[data-acao="restaurar-sim"]'); console.log('restaurado:',await p.evaluate(()=>D.T.length),(await p.textContent('.msg')).trim());
   await p.goto(URL+'#editar'); const fs=require('fs'), tmp=require('os').tmpdir()+'/projetos_teste.csv';
   fs.writeFileSync(tmp,'Código;Nome do projeto;Código da empresa;Setor;Município;Status;da;dc;ip;ir;ep;eg;ei;miss;estr;coluna extra\n'+
     'PRJ901;Usina Teste;EMP001;Energia;Picos;Implantado;2025-01-10;2025-03-01;50.000.000;50000000;120;120;240;Sim;Não;x\n'+
     'PRJ902;Hotel Teste;EMP002;Turismo;Parnaíba;Em implantação;2025-02-01;2025-04-01;8000000;1000000;40;;80;Não;Não;y\n'+
     'PRJ001;Repetido;EMP001;Energia;Picos;Implantado;2025-01-10;2025-03-01;1000;0;1;1;1;Sim;Não;z\n'+
     'PRJ903;Setor errado;EMP001;Petróleo;Picos;Implantado;2025-01-10;2025-03-01;1000;0;1;1;1;Sim;Não;z\n'+
     'PRJ904;Realizado maior;EMP001;Agro;Uruçuí;Implantado;10/01/2025;2025-03-01;1000;5000;1;1;1;Sim;Não;z\n');
   await p.setInputFiles('#arq',tmp); await p.waitForSelector('button[data-acao="arq-add"]');
   console.log('arquivo:',(await p.textContent('.panel .chip.demo, .panel .chip.calc, .panel .chip.bad')).trim(),'| válidos:',await p.evaluate(()=>UI.rel.ok.length),'| com problema:',await p.evaluate(()=>UI.rel.ruins.map(x=>x.n+':'+x.er[0]).join(' || ')),'| ignoradas:',await p.evaluate(()=>UI.rel.ignoradas.join(',')));
   await p.click('button[data-acao="arq-add"]'); console.log('após adicionar:',await p.evaluate(()=>D.P.length),'projetos; PRJ901 previsto =',await p.evaluate(()=>D.P.find(x=>x.c==='PRJ901').ip),'|',(await p.textContent('.msg')).trim());
   await p.click('button[data-acao="restaurar"]'); await p.click('button[data-acao="restaurar-sim"]'); console.log('restaurado:',await p.evaluate(()=>D.P.length));
   console.log('scores:',JSON.stringify(await p.evaluate(()=>Object.fromEntries(Object.entries(SC).map(([k,v])=>[k,v==null?null:Math.round(v*10)/10])))));
   console.log('indicadores:',await p.evaluate(()=>IND.length), await p.evaluate(()=>IND.filter(i=>i.mat).map(i=>i.id+'='+(i.v==null?'nd':i.f(i.v))).join(' ; ')));
  } await p.close(); }
 await b.close(); console.log(falhas?`${falhas} tela(s) com problema`:'todas as telas sem erro'); process.exit(falhas?1:0); })();
