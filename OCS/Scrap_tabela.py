from urllib.request import urlopen
from bs4 import BeautifulSoup
#import csv


arq = open('Enancib_2020.ttl', 'w')


#ocs="https://www.revistas.usp.br/incid/issue/view/10127"
#ocs="https://cdmws.isci.com.br/ocs/index.php/cdmws/home/schedConf/presentations"
#ocs="http://enancib.marilia.unesp.br/index.php/xviiienancib/ENANCIB/schedConf/presentations"
#ocs="http://enancib.marilia.unesp.br/index.php/XIXENANCIB/xixenancib/schedConf/presentations"
#ocs="https://seer.ufs.br/index.php/conci/issue/view/735/showToc"
#ocs="http://www.ufpb.br/evento/index.php/enancib2016/enancib2016/schedConf/presentations"

ocs="http://conferencias.ufsc.br/index.php/enancib/2019/schedConf/presentations"
print (ocs)

html = urlopen(ocs)
bsObj = BeautifulSoup(html, "html.parser")
texto = bsObj.find("div",{"id":"content"}).findAll("table")
lista = []
lista.append("@prefix dc: <http://purl.org/dc/elements/1.1/> .\n")
arq.writelines(lista)
b = 0
a = 0
for name in texto:
    while len(lista) > 0 : lista.pop()
    linhas = name.findAll("tr")
    for x in linhas:
        for link in x.findAll("a"):
            if 'href' in link.attrs:
                #print(link.attrs['href'])
                #lista.append("<"+link.attrs['href']+">")
                print(link.attrs['href'])
                html2 = urlopen(link.attrs['href'])
                bs2Obj = BeautifulSoup(html2,"html.parser")
                pagsecundaria = bs2Obj.find_all("meta")
                linha = "<" + link.attrs['href'] + "> <dc:isPartOf> <" + ocs + ">.\n"
                lista.append(linha)
                for metas in pagsecundaria:
                    try:
                        metas["content"]=metas["content"].replace("\"","'")
                        if metas["name"]=="dc:Identifier.URI" :
                            linha = "<" + link.attrs['href'] + "> <" + metas["name"] + "> <" + metas["content"] + ">.\n"
                        else:
                            linha="<"+link.attrs['href']+"> <"+metas["name"]+"> \"" + metas["content"] + "\".\n"
                        linha = linha.replace("DC.", "dc:")
                        lista.append(linha)
                    except:
                        b+=1

            else:
                lista.append(" ")

        a+=1
    #writer.writerow(lista1)
    #print (lista1)
    arq.writelines(lista)



arq.close()
