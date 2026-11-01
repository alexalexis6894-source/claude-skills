import fs from 'node:fs';
import path from 'node:path';
// Скачивает только перечисленные публичные карточки Awwwards, без внешних сайтов.
const [manifest, output] = process.argv.slice(2);
if (!manifest || !output) throw new Error('Нужны manifest.json и папка результата');
fs.mkdirSync(output, {recursive:true});
const rows = JSON.parse(fs.readFileSync(manifest, 'utf8'));
const log=[];
for (const row of rows) {
  const url=new URL(row.url);
  if(url.origin!=='https://www.awwwards.com' || !/^\/(sites|inspiration)\/[^/]+$/.test(url.pathname)) throw new Error('Недопустимый адрес');
  const key=url.pathname.slice(1).replaceAll('/','--');
  const file=path.join(output,key+'.html');
  const start=Date.now();
  if(fs.existsSync(file)) {log.push({url:row.url,file,cached:true});continue;}
  try {
    const r=await fetch(url,{signal:AbortSignal.timeout(20000)});
    if(r.status===429){log.push({url:row.url,status:429,error:'rate_limit'});break;}
    const html=await r.text();
    if(r.ok)fs.writeFileSync(file,html);
    log.push({url:row.url,file,status:r.status,bytes:Buffer.byteLength(html),ms:Date.now()-start});
  }catch(e){log.push({url:row.url,error:e.message,ms:Date.now()-start});}
  await new Promise(r=>setTimeout(r,250));
}
fs.writeFileSync(path.join(output,'fetch-log.json'),JSON.stringify(log,null,2));
console.log(JSON.stringify({requested:rows.length,processed:log.length,errors:log.filter(x=>x.error||x.status>=400).length,elapsed_ms:log.reduce((s,x)=>s+(x.ms||0),0)}));
