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

#Programa Principal
site = 'https://repositorio.unesp.br'
nome = 'UNESP'
arq = open(nome + '.ttl', 'w', encoding='utf-8')

abre_site = abrirSite(site)

# Abre a primeira página dos Artigos (Provavelmente funciona para outras abas)
abrir_artigos = abre_site.find_all('a', {'class': 'list-group-item ds-option'})

for link in abrir_artigos:
    if 'Artigo' in link.get_text():
        tabela_artigos = abrirSite(site + link['href']) # Página onde se encontra os artigos
        #print((site + link['href']))

# Coleta os metadados, Baixa os PDF's e troca de página
#while True:
for p in range(0, 10):
    todos_links = tabela_artigos.find_all('div', 'row ds-artifact-item')
    for link in todos_links:
        link_artigo = site + link.find('a')['href'] # Link para abrir o artigo (Para escrever no arquivo .ttl)
        artigo = abrirSite(link_artigo)
        meta = artigo.find_all('meta')
        metadadosColeta(link_artigo, meta, arq)

        pdfs = artigo.find_all('a', {'target': '_blank'})
        for pdf in pdfs:
            if not 'http' in pdf['href']:
                link_download = site + pdf['href']
                nome_arq = link_artigo.split('/handle/')[1].replace('/', '-')
                baixadireto(link_download, nome + '_' + nome_arq)
    # Encontra a próxima página de artigos para coleta (Para coletar tudo, trocar o laço for pelo laço while True)
    try:
        next_page = site + '/' + tabela_artigos.find('a', {'class': 'next-page-link'})['href']
        tabela_artigos = abrirSite(next_page)
        #print(next_page)
    except:
        break

# Coletando os links dos artigos e abrindo para coletar seus metadados

