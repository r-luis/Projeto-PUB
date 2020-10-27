from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
#import csv


def baixararquivo(url,nomearquivo):
    nomearquivo=nomearquivo.replace("/", "-")
    links_with_text2 = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    for page1 in soup.find_all('a'):
        if 'Versão de Impressão' in page1.text:
            links_with_text2.append(page1['href'])

    soup = {}
    print(nomearquivo)
    print(url)
    #docnum = 111  # Teste somente
    for link in links_with_text2:
        r = requests.get(link, stream=True)
        with open("Arquivos/"+nomearquivo+".pdf", "wb") as pdf:
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    pdf.write(chunk)
    return True


nome ="Enancib_2019"
#arq = open(nome+'.ttl', 'w', encoding='utf-8')

# ocs = "http://www.ufpb.br/evento/index.php/enancib2015/enancib2015/schedConf/presentations"
# ocs = "http://www.ufpb.br/evento/index.php/enancib2016/enancib2016/schedConf/presentations"
# ocs = "http://enancib.marilia.unesp.br/index.php/XVIII_ENANCIB/ENANCIB/schedConf/presentations"
# ocs = "http://enancib.marilia.unesp.br/index.php/XIX_ENANCIB/xixenancib/schedConf/presentations"
ocs = "https://conferencias.ufsc.br/index.php/enancib/2019/schedConf/presentations"

html = urlopen(ocs)
bsObj = BeautifulSoup(html, 'html.parser')
texto = bsObj.find('div', {'id': 'content'}).find_all('table')
lista = list()
lista.append("@prefix dc: <http://purl.org/dc/elements/1.1/> .\n")
#arq.writelines(lista)

a = 0
b = 0

#pdf
for name in texto:
    while len(lista) > 0: lista.pop()
    linhas = name.find_next("tr")
    vez = 0
    for x in linhas:
        link = x.find_next("a")
        if 'href' in link.attrs:
            #print(link.attrs['href'])
            lista.append("<"+link.attrs['href']+">")
            linksegundapagina=link.attrs['href'].replace('/view/','/viewPaper/')
            if vez == 2:
                try:
                    baixararquivo(link.attrs['href'].replace('/view/','/viewRST/'), nome+'_'+link.attrs['href'].split('/view/')[1])
                except:
                    print('erro de download no pdf')
            vez += 1
