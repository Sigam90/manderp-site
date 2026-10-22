# Génère site/reglement.html depuis server/docs/reglement.md (même texte que sur Discord).
import re, html, pathlib
racine = pathlib.Path(__file__).resolve().parent
md = (racine.parent / 'server/docs/reglement.md').read_text(encoding='utf-8')

def inline(t):
    t = html.escape(t, quote=False)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)

corps, sommaire, liste = [], [], None
for ligne in md.splitlines():
    if ligne.strip() in ('', '---'):
        if liste: corps.append(f'</{liste}>'); liste = None
        continue
    if ligne.startswith('# '):
        continue
    m = re.match(r'## (\d+)\. (.*)', ligne)
    if m:
        if liste: corps.append(f'</{liste}>'); liste = None
        ancre = f'section-{m.group(1)}'
        titre = m.group(2).capitalize()
        sommaire.append(f'<li><a href="#{ancre}">{html.escape(titre)}</a></li>')
        corps.append(f'<h2 id="{ancre}">{m.group(1)}. {html.escape(titre)}</h2>')
        continue
    for prefixe, balise in (('- ', 'ul'), (r'\d+\. ', 'ol')):
        if re.match(prefixe, ligne):
            if liste != balise:
                if liste: corps.append(f'</{liste}>')
                corps.append(f'<{balise}>'); liste = balise
            corps.append('<li>' + inline(re.sub('^' + prefixe, '', ligne)) + '</li>')
            break
    else:
        if liste: corps.append(f'</{liste}>'); liste = None
        corps.append('<p>' + inline(ligne) + '</p>')
if liste: corps.append(f'</{liste}>')

modele = (racine / 'index.html').read_text(encoding='utf-8')
entete = modele.split('<section class="accroche')[0].replace('<title>Mandé RP · Serveur GTA RP francophone Free Access · Duguba City</title>', '<title>Règlement · Mandé RP</title>')
pied = '<div class="frise"></div>\n<footer>' + modele.split('<footer>')[1]
entete = entete.replace('href="#', 'href="index.html#')
pied = pied.replace('href="#', 'href="index.html#')
page = entete + f'''<main class="page motif">
  <div class="conteneur">
    <span class="etiquette">Duguba City</span>
    <h1>Règlement de <em>Mandé RP</em></h1>
    <nav class="sommaire"><strong>Sommaire</strong><ol>{''.join(sommaire)}</ol></nav>
    <div class="regles">
{chr(10).join(corps)}
    </div>
  </div>
</main>
''' + pied
(racine / 'reglement.html').write_text(page, encoding='utf-8')
print('reglement.html :', len(sommaire), 'sections')
