# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup

# Arquivos e Links
# arq = open('Enancib_2015.ttl', 'w', encoding='utf-8')
arq = open('Enancib_2016.ttl', 'w', encoding='utf-8')
# arq = open('Enancib_2017.ttl', 'w', encoding='utf-8')
# arq = open('Enancib_2018.ttl', 'w', encoding='utf-8')
# arq = open('Enancib_2019.ttl', 'w', encoding='utf-8')

# ocs: str = "http://www.ufpb.br/evento/index.php/enancib2015/enancib2015/schedConf/presentations"
ocs: str = "http://www.ufpb.br/evento/index.php/enancib2016/enancib2016/schedConf/presentations"
# ocs: str = "http://enancib.marilia.unesp.br/index.php/XVIII_ENANCIB/ENANCIB/schedConf/presentations"
# ocs: str = "http://enancib.marilia.unesp.br/index.php/XIX_ENANCIB/xixenancib/schedConf/presentations"
# ocs: str = "https://conferencias.ufsc.br/index.php/enancib/2019/schedConf/presentations"


# Programa Principal
html = urlopen(ocs)
# html = requests.get(ocs).text.encode('utf8').decode('ascii', 'ignore')
bsObj = BeautifulSoup(html, 'html.parser')
# bsObj.encode("utf-8")
texto = bsObj.find('div', {'id': 'content'}).find_all('table')
lista = list()
lista.append("@prefix dc: <http://purl.org/dc/elements/1.1/> .\n")
arq.writelines(lista)

a = 0
b = 0

for name in texto:
    while len(lista) > 0:
        lista.pop()
    linhas = name.find_all('tr')
    for x in linhas:
        for link in x.find_all('a'):
            if 'href' in link.attrs:
                print(link.attrs['href'])
                html2 = urlopen(link.attrs['href'])
                bsObj2 = BeautifulSoup(html2, 'html.parser')
                metadados = bsObj2.find_all('meta')
                linha = '<' + link.attrs['href'] + '> <dc:isPartOf> <' + ocs + '>'
                lista.append(linha)
                for metas in metadados:
                    try:
                        metas['content'] = metas['content'].replace('\"', "'")
                        if metas['name'] == 'dc:Identifier.URI':
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
    #try:
    arq.writelines(lista)
    #except UnicodeEncodeError:
        #print('Erro Unicode')

# print(b, a)
arq.close()
# print(texto)
