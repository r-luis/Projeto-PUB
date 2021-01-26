from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests

site = 'https://repositorio.ufba.br'
nome = 'UFBA'
arq = open(nome + '.ttl', 'w', encoding='utf-8')

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


def metadadosColeta(linkinicial, metad, arquivo):
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
                arquivo.write(f"<{linkinicial}> <{m.attrs['name'].replace('DC', 'dc')}> '{m.attrs['content']}'\n")
            except:
                pass


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
'''next = bs3.find_all('a')
for n in next:
    if 'next' in n.get_text():
        print(site + n['href'])'''

links = []  # coletando os links para abrir as páginas

for t in tabela:
    links.append(site + t.find('a')['href'])
    #print(t.find('a').get_text())

# coletando os metadados
for link in links:
    bs3 = abrirSite(link)

    meta = bs3.find_all('meta')
    metadadosColeta(link, meta, arq)

arq.close()
