from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
#import csv


def baixararquivo(url,nomearquivo):
    nomearquivo=nomearquivo.replace("/","-")
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


nome="Enancib_2017"
arq = open(nome+'.ttl', 'w')


#ocs="https://www.revistas.usp.br/incid/issue/view/10127"
#ocs="https://cdmws.isci.com.br/ocs/index.php/cdmws/home/schedConf/presentations"

ocs="http://enancib.marilia.unesp.br/index.php/xviiienancib/ENANCIB/schedConf/presentations"

#ocs="http://enancib.marilia.unesp.br/index.php/XIXENANCIB/xixenancib/schedConf/presentations"
#ocs="https://seer.ufs.br/index.php/conci/issue/view/735/showToc"
#ocs="http://www.ufpb.br/evento/index.php/enancib2016/enancib2016/schedConf/presentations"
#ocs="http://conferencias.ufsc.br/index.php/enancib/2019/schedConf/presentations"

html = urlopen(ocs)
bsObj = BeautifulSoup(html, "html.parser")
texto=bsObj.find("div",{"id":"content"}).find("table")
lista=[]
lista.append("@prefix dc: <http://purl.org/dc/elements/1.1/> .\n")
arq.writelines(lista)
b=0
a=0
for name in texto:
    while len(lista) > 0: lista.pop()
    linhas=name.findNext("tr")
    vez=0
    for x in linhas:
            link = x.findNext("a")
            if 'href' in link.attrs:

                #print(link.attrs['href'])
                #lista.append("<"+link.attrs['href']+">")
                print (link.attrs['href'])
                linksegundapagina=link.attrs['href'].replace('/view/','/viewPaper/')
                #if (vez==2):
                    #try:
                        #baixararquivo(link.attrs['href'].replace('/view/','/viewRST/'), nome+'_'+link.attrs['href'].split('/view/')[1])
                    #except:
                        #print('erro de download no pdf')
                vez+=1
                html2=urlopen(linksegundapagina)
                bs2Obj = BeautifulSoup(html2,"html.parser")
                pagsecundaria=bs2Obj.find_all("meta")
                linha = "<" + link.attrs['href'] + "> <dc:isPartOf> <" + ocs + ">.\n"
                lista.append(linha)
                for metas in pagsecundaria:
                    try:
                        metas["content"]=metas["content"].replace("\"","'")
                        if metas["name"]=="dc:Identifier.URI" :
                            linha = "<" + link.attrs['href'] + "> <" + metas["name"] + "> <" + metas[
                                "content"] + ">.\n"
                        else :
                            linha="<"+link.attrs['href']+"> <"+metas["name"]+"> \""+metas["content"]+"\".\n"
                        linha = linha.replace("DC.", "dc:")
                        lista.append(linha)
                    except:
                        b+=1


            a+=1
    #writer.writerow(lista1)
    #print (lista1)
    arq.writelines(lista)

arq.close()
print("finalizado")