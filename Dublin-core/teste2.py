from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from bs4 import BeautifulSoup

site = 'https://repositorio.ufba.br'


def abrirSite(s):
    '''Função para abrir sites e já colocar dentro do BS
    automaticamente, sem precisar repetir o mesmo código
    s = url do link a ser definido na função'''
    try:
        html = urlopen(s)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)

    return BeautifulSoup(html, 'html.parser')


# navegando do menu até os artigos pt1
bs = abrirSite(site)
menu = bs.find_all('tr', {'class': 'navigationBarItem'})

for l in menu:
    link = l.find('td', {'class': 'navigationBarItem'}).find_all('a')
    for abre_opc in link:
        if abre_opc.get_text() == 'Document Type':  # Aqui você pode colocar a opção do menu para abrir
            prox = site + abre_opc['href']

# pt 2 - tabela dos artigos
bs2 = abrirSite(prox)
link2 = site + bs2.find('td', {'class': 'evenRowOddCol'}).find('a')['href']

bs3 = abrirSite(link2)

# Abrindo o bs dos artigos
tabela = bs3.find('table', {'class': 'miscTable'}).find_all('td', {'headers': 't2'})

# pegando o link para rodar as páginas (não está funcionando o site)
next = bs3.find_all('a')
for n in next:
    if 'next' in n.get_text():
        print(site + n['href'])

links = [] # coletando os links para abrir as páginas

for t in tabela:
    links.append(site + t.find('a')['href'])
    print(t.find('a').get_text())


# coletando os metadados
for link in links:
    bs3 = abrirSite(link)

    meta = bs3.find('table', {'class': 'itemDisplayTable'}).find_all('tr')

    for metadados in meta:
        print(f'<{link}>', end=' ')
        for cont in metadados.find_all('td'):
            if 'metadataFieldLabel' in cont.attrs['class']:
                print(f'<{cont.get_text()[:-2].lower()}>', end=' ')
            if 'metadataFieldValue' in cont.attrs['class']:
                print(f"'{cont.get_text()}'")
