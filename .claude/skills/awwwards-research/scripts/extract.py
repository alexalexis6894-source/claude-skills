"""Извлечение карточек и всех собственных Elements из сохранённого HTML."""
import gzip, json, re, sys
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
BASE='https://www.awwwards.com'
def text(n): return n.get_text(' ',strip=True) if n else ''
def parse_site(html,url):
    s=BeautifulSoup(html,'html.parser')
    h=s.h1
    if not h or text(h)=='Page not found': raise ValueError('Нет карточки проекта')
    # Ссылки собственных элементов присутствуют в обоих вариантах карточки.
    elements={}
    for a in s.select('.gallery-site a[href^="/inspiration/"], #elements a[href^="/inspiration/"]'):
        u=urljoin(BASE,a['href']); title=text(a)
        if u not in elements or title: elements[u]={'url':u,'title':title}
    headings=[text(h) for h in s.select('h2')]
    award=next((x for x in headings if re.match(r'(Site of the|Honorable Mention|Nominee)',x)),None)
    official=[]
    for x in headings:
        m=re.search(r'(SOTD / SCORE|DEV AWARD).*?([0-9]+\.[0-9]+)\s*/\s*10',x)
        if m: official.append({'type':m[1],'value':float(m[2])})
    desc=s.select_one('meta[property="og:description"]')
    description=desc.get('content','') if desc else ''
    dh=next((x for x in s.select('h2') if text(x)=='Description'),None)
    if dh:
        block=dh.find_parent(class_='c-heading')
        full=block.select_one('h3') if block else None
        if full: description=text(full)
    votes=[]
    for scope in s.select('#jury_votes, #user_votes'):
        vals=[float(text(n)) for n in scope.select('.grid-score__item--total') if re.fullmatch(r'\d+(\.\d+)?',text(n))]
        if vals:votes.append({'group':scope.get('id'),'loaded_scores':vals,'loaded_mean':round(sum(vals)/len(vals),3),'scope':'loaded rows only'})
    if not votes:
        vals=[float(text(n)) for n in s.select('.list-users-votes .grid-score__item--total') if re.fullmatch(r'\d+(\.\d+)?',text(n))]
        if vals:votes.append({'group':'community','loaded_scores':vals,'loaded_mean':round(sum(vals)/len(vals),3),'scope':'loaded rows only'})
    return {'url':url,'title':text(h),'award':award,'official_scores':official,'votes_label':[x for x in headings if x.startswith('Votes')],'votes':votes,'description':description,'elements':list(elements.values()),'page_text_chars':len(s.get_text(' ',strip=True)),'html_bytes':len(html.encode())}
def parse_element(html,url):
    s=BeautifulSoup(html,'html.parser'); root=s.select_one('.gallery-element')
    if not root or not root.h1: raise ValueError('Нет карточки элемента')
    h=root.h1; parent=h.select_one('a[href^="/sites/"]')
    title=' '.join(str(x).strip() for x in h.find_all(string=True,recursive=False)).strip()
    # Описание берём только из собственного блока, не из рекомендаций More inspiration.
    desc=[text(x) for x in s.select('.gallery-element__description, .description-element') if text(x)]
    media=[]
    for n in root.select('source[src],img[src]'):
        media.append(n.get('src'))
    for n in root.select('video[poster]'): media.append(n['poster'])
    return {'url':url,'title':title,'parent_url':urljoin(BASE,parent['href']) if parent else None,'description':' '.join(desc) or None,'tags':[text(x) for x in s.select('.list-tags .button--tag')],'media':list(dict.fromkeys(media)),'page_text_chars':len(s.get_text(' ',strip=True)),'html_bytes':len(html.encode())}
if __name__=='__main__':
    folder=Path(sys.argv[1]); output=Path(sys.argv[2]); sites=[]; elements=[]; errors=[]
    # Поддерживает и обычный HTML, и сжатые страницы (pages/*.html.gz) из сторонних сборщиков.
    for p in sorted([*folder.glob('*.html'),*folder.glob('pages/*.html.gz')]):
        stem=p.name.removesuffix('.gz').removesuffix('.html')
        if not stem.startswith(('sites--','inspiration--')): continue
        url=BASE+'/'+stem.replace('--','/',1)
        html=gzip.decompress(p.read_bytes()).decode() if p.suffix=='.gz' else p.read_text()
        try:
            data=(parse_site if stem.startswith('sites--') else parse_element)(html,url)
            (sites if stem.startswith('sites--') else elements).append(data)
        except Exception as e: errors.append({'url':url,'error':str(e)})
    output.write_text(json.dumps({'sites':sites,'elements':elements,'errors':errors},ensure_ascii=False,indent=2))
    print(json.dumps({'sites':len(sites),'elements':len(elements),'errors':errors}))
