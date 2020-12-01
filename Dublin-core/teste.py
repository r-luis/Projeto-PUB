from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from bs4 import BeautifulSoup

site = 'https://repositorio.unesp.br/'
# site = 'https://repositorio.ufba.br/ri/'


try:
    html = urlopen(site)
except HTTPError as e:
    print(e)
except URLError as e:
    print(e)

bs = BeautifulSoup(html, 'html.parser')

#abrindo a seção de artigos
for link in bs.find('div', {'id': 'aspect_discovery_Navigation_list_discovery'}).find_all('a'):
    if 'href' in link.attrs:
        txt = link.get_text()
        if 'Artigo' in txt:
            artigos = site + link.attrs['href']

html2 = urlopen(artigos)
bs2 = BeautifulSoup(html2, 'html.parser')

lista_links = []
lista_metadados = []

#coletando os links dos artigos
lnk = artigos
for c in range(0, 10):
    print(lnk)
    ab = urlopen(lnk)
    sopa = BeautifulSoup(ab, 'html.parser')
    lnk = site + sopa.find('a', {'class': 'next-page-link'})['href']

    for link in sopa.find('div', {'id': 'aspect_discovery_SimpleSearch_div_search-results'}).find_all('a'):
        if 'href' in link.attrs:
            if not 'class' in link.attrs:
                lista_links.append(site + link.attrs['href'])

    #abre o link para os metadados
    for c in lista_links:
        coleta = urlopen(c)
        bscol = BeautifulSoup(coleta, 'html.parser')
        for link in bscol.find('div', {'class': 'simple-item-view-show-full item-page-field-wrapper table'}).find_all('a'):
            if 'href' in link.attrs:
                lista_metadados.append(site + link.attrs['href'])


    cont = 0

    for meta in lista_metadados:
        coleta_meta = urlopen(meta)
        bsmeta = BeautifulSoup(coleta_meta, 'html.parser')
        for data in bsmeta.find('table').find_all('td'):
            if 'class' in data.attrs:
                if cont % 2 == 0:
                    print(f'<{meta}> <{data.get_text()}>', end=' ')
                else:
                    print(f'<{data.get_text()}>')
                cont+=1
        print('')