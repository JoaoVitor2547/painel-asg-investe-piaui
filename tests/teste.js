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
   console.log('scores:',JSON.stringify(await p.evaluate(()=>Object.fromEntries(Object.entries(SC).map(([k,v])=>[k,v==null?null:Math.round(v*10)/10])))));
   console.log('indicadores:',await p.evaluate(()=>IND.length), await p.evaluate(()=>IND.filter(i=>i.mat).map(i=>i.id+'='+(i.v==null?'nd':i.f(i.v))).join(' ; ')));
  } await p.close(); }
 await b.close(); console.log(falhas?`${falhas} tela(s) com problema`:'todas as telas sem erro'); process.exit(falhas?1:0); })();
