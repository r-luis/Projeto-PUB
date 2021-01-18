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


links = 'http://www.periodicos.ufc.br/informacaoempauta/issue/view/986' #3.1.2.1


bs = abrirSite(links)

meta = bs.find_all('meta')


# Coletando os metadados da revista
def metadadosColeta(linkinicial, metad):
    """Essa função coleta os metadados de um artigo (testado no OJS 3.1.2.1)
    linkinicial => o link do artigo, assim a função pode escrever os metadados na forma correta
    metad => a variável que contém todos os metadados
    Ex: variável = bs.find_all('meta')
    metadadosColeta(linkinicial, variável)
    """
    for m in metad:
        if 'content' in m.attrs:
            try:
                print(f"<{linkinicial}> <{m.attrs['name'].replace('DC', 'dc')}> '{m.attrs['content']}'")
            except:
                pass

# metadadosColeta(links, meta)

secoes = bs.find_all('div', {'class': 'section'})

# Coleta dos links dos artigos
link_artigos = []

for secao in secoes:
    subs = secao.find_all('div', {'class', 'title'})
    for s in subs:
        link_artigos.append(s.find('a')['href'])

# Coleta dos metadados do conteúdo da revista
print('@prefix dc: <http://purl.org/dc/elements/1.1/> .')
for link in link_artigos:
    artigo = abrirSite(link)
    meta_artigo = artigo.find_all('meta')
    metadadosColeta(link, meta_artigo)