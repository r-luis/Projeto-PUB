from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests


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


def baixadireto(url, nomearquivo):
    """
    Faz o download direto do arquivo PDF
    e coloca direto no diretório que é mostrado.
    """
    nomearquivo = nomearquivo.replace("/", "-")
    r = requests.get(url)
    print(nomearquivo, '-', url)
    with open('Arquivos/' + nomearquivo + '.pdf', 'wb') as pdf:
        for chunk in r.iter_content(chunk_size=2048):
            if chunk:
                pdf.write(chunk)


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


nome = 'info_em_pauta'
links = 'http://www.periodicos.ufc.br/informacaoempauta/issue/view/986'  # 3.1.2.1
bs = abrirSite(links)
meta = bs.find_all('meta')
secoes = bs.find_all('div', {'class': 'section'})
pdfs = bs.find_all('a', {'class': 'obj_galley_link pdf'})

# Coleta dos links dos artigos
link_artigos = []

for secao in secoes:
    subs = secao.find_all('div', {'class', 'title'})
    for s in subs:
        link_artigos.append(s.find('a')['href'])

# Coletando os metadados da revista
print('@prefix dc: <http://purl.org/dc/elements/1.1/> .')
for link in link_artigos:
    artigo = abrirSite(link)
    meta_artigo = artigo.find_all('meta')
    metadadosColeta(link, meta_artigo)
    # Coletando as referências
    ref = artigo.find('div', {'class': 'item references'}).find('div').get_text().split('\n')
    for f in ref:
        if len(f.strip()) == 0:
            pass
        else:
            print(f"<{link}> <dc.bibliographicCitation> '{f.strip()}'")

# Coleta dos PDF's
for pdf in pdfs:
    link_download = pdf['href'].replace('view', 'download')
    nome_arq = link_download.split('/download/')[1].replace('/', '-')
    baixadireto(link_download, nome + '_' + nome_arq)
