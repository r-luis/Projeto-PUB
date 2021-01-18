from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from bs4 import BeautifulSoup


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


def metadadosColeta(linkinicial, metad):
    """Essa função coleta os metadados de um artigo (testado no OJS 3.1.2.1, 2.4.8.0)
    metad => a variável que contém todos os metadados
    Ex: variável = bs.find_all('meta')
    metadadosColeta(variável)
    """
    for m in metad:
        if 'content' in m.attrs:
            try:
                print(f"<{linkinicial}> <{m.attrs['name'].replace('DC', 'dc')}> '{m.attrs['content']}'")
            except:
                pass


links = 'https://seer.ufrgs.br/EmQuestao/issue/view/4213/showToc'  # 2.4.8.0

bs = abrirSite(links)

tabela = bs.find('div', {'id': 'content'}).find_all('table', {'class': 'tocArticle'})

link_artigos = []

for secao in tabela:
    if secao.get_text() != 'PDF':
        link_artigos.append(secao.find('a')['href'])

for link in link_artigos:
    artigo = abrirSite(link)
    meta_artigo = artigo.find_all('meta')
    metadadosColeta(link, meta_artigo)