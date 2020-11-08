from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests


def baixararquivo(url, nomearquivo):
    '''Funciona apenas no Enancib 2018/2019'''
    nomearquivo = nomearquivo.replace("/", "-")
    links_with_text2 = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    for page1 in soup.find_all('a'):
        if 'Versão de Impressão' in page1.text:
            links_with_text2.append(page1['href'])
        else:
            print('erro no download do pdf')

    soup = {}
    print(nomearquivo, '-', url)
    # docnum = 111  # Teste somente
    for link in links_with_text2:
        r = requests.get(link, stream=True)
        with open("Arquivos/" + nomearquivo + ".pdf", "wb") as pdf:
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    pdf.write(chunk)
    return True


def baixadireto(url, nomearquivo):
    '''Funciona em todos os anos já que o link é substituído pelo link direto de download.
    Dessa maneira o scrapping não precisa puxar os links diretos, além de resolver o problema
    dos anos de 2015 a 2017, onde o 'viewRST' não funciona.'''
    nomearquivo = nomearquivo.replace("/", "-")
    r = requests.get(url)
    print(nomearquivo, '-', url)
    with open('Arquivos/' + nomearquivo + '.pdf', 'wb') as pdf:
        for chunk in r.iter_content(chunk_size=2048):
            if chunk:
                pdf.write(chunk)


nome = "Enancib_2015"
# nome = "Enancib_2016"
# nome = "Enancib_2017"
# nome = "Enancib_2018"
# nome = "Enancib_2019"

arq = open(nome + '.ttl', 'w', encoding='utf-8')

ocs = "http://www.ufpb.br/evento/index.php/enancib2015/enancib2015/schedConf/presentations"
# ocs = "http://www.ufpb.br/evento/index.php/enancib2016/enancib2016/schedConf/presentations"
# ocs = "http://enancib.marilia.unesp.br/index.php/XVIII_ENANCIB/ENANCIB/schedConf/presentations"
# ocs = "http://enancib.marilia.unesp.br/index.php/XIX_ENANCIB/xixenancib/schedConf/presentations"
# ocs = "http://conferencias.ufsc.br/index.php/enancib/2019/schedConf/presentations"

# Programa Principal
html = urlopen(ocs)
bsObj = BeautifulSoup(html, 'html.parser')
texto = bsObj.find('div', {'id': 'content'}).find_all('table')
ver = bsObj.find('meta', {'name': 'generator'})['content'][-7:]
lista = list()
lista.append("@prefix dc: <http://purl.org/dc/elements/1.1/> .\n")
print(f'Versão: {ver}')
arq.writelines(lista)

a = 0
b = 0

for name in texto:
    while len(lista) > 0:
        lista.pop()
    linhas = name.find_all('tr')
    vez = 1
    for x in linhas:
        for link in x.find_all('a'):
            if 'href' in link.attrs:
                print(link.attrs['href'])
                if vez % 2 == 0:
                    try:
                        baixadireto(link.attrs['href'].replace('/view/', '/download/'), nome + '_' + link.attrs['href'].split('/view/')[1])
                        # baixararquivo(link.attrs['href'].replace('/view/', '/viewRST/'),
                                      # nome + '_' + link.attrs['href'].split('/view/')[1])
                    except:
                        print('erro de download no pdf')
                vez += 1
                html2 = urlopen(link.attrs['href'].replace('/view/', '/viewPaper/'))
                bsObj2 = BeautifulSoup(html2, 'html.parser')
                metadados = bsObj2.find_all('meta')
                linha = '<' + link.attrs['href'] + '> <dc:isPartOf> <' + ocs + '>. \n'
                lista.append(linha)
                for metas in metadados:
                    try:
                        metas['content'] = metas['content'].replace('\"', "'")
                        if metas['name'] == 'DC:Identifier.URI':
                            linha = '<' + link.attrs['href'] + '> <' + metas['name'] + '> <' + metas['content'] + '>.\n'
                        else:
                            linha = '<' + link.attrs['href'] + '> <' + metas['name'] + '> \'' + metas[
                                'content'] + '\' \n'

                        linha = linha.replace('DC.', 'dc:')
                        lista.append(linha)
                    except:
                        b += 1
            else:
                lista.append('')
        a += 1
    arq.writelines(lista)

# print(b, a)
arq.close()
# print(texto)
