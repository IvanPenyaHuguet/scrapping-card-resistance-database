import json
import requests
from bs4 import BeautifulSoup
import re


def getAllArg():
    URL = "https://card.mcmaster.ca/load/json"
    page = requests.get(URL)
    my_data = page.json()
    with open("allarg.json", 'w') as f:
        json.dump(my_data, f)


def search (allarg_json):    
    gen_list = ["AAC(3)-II", "AAC(3)-Id", "AAC(3)-VIa", "AAC_6___I-_3", "AAC(6')-Ib", "ANT(3'')-IIa", "APH(3')-Ia", "APH(3'')-Ib", "APH(6)-Id", "AcrE", "AcrF", "AcrS", "BIL-1", "CARB-1", "CRP", "Escherichia coli 23S", "Escherichia coli EF Tu", "Escherichia coli GlpT", "Escherichia coli LamB", "Escherichia coli UhpA 1", "Escherichia coli ampC1", "FosA7", "H-NS", "Klebsiella_pneumoniae_KpnH+", "MCR-1", "MdtK", "OXA-3", "PmrF", "QnrB", "QnrB1", "QnrB3", "QnrD", "QnrS", "SAT-2", "TEM-", "TolC", "YojI", "aadA16", "aadA2", "aadA7", "acrA", "acrB", "acrD", "ampC", "ampH", "arr-", "bacA", "baeR", "baeS", "catI", "catII from Escherichia", "cmlA", "cpxA", "cyaA", "dfrA1", "dfrA12", "dfrA14", "dfrA2", "emrA", "emrE", "emrK", "emrR", "emrY", "eptA", "evgA", "evgS", "floR+", "gadW", "gadX", "golS", "gyrA_8", "kdpE", "marA", "marR", "mdfA", "mdsA", "mdsB", "mdsC", "mdtA", "mdtB", "mdtC", "mdtE", "mdtG", "mdtH", "mdtN", "mdtO", "mdtP", "mgrB", "mipA", "mphA", "mphB", "msbA", "porin_OmpC", "rrsB", "sdiA", "sul1", "sul2", "sul3", "tetM", "tet(A)", "tet(B)", "tet(C)", "ugd"]
    visitted_uri = []
    a = allarg_json['data']
    for arg_key in a:
        b = a[arg_key]
        for gen in gen_list:
            my_regex = re.escape(gen)
            if re.match(my_regex, b["name"]):                
                uri = b["uri"]
                if uri not in visitted_uri:
                    getData( uri , b ["name"], gen)
                    visitted_uri.append(uri)
            if re.match(my_regex, b["synonym"]):
                print("syn")
                uri = b["uri"]
                if uri not in visitted_uri:
                    getData( uri , b ["name"] , gen)
                    visitted_uri.append(uri)         



def getData (uri , name , gen):
    URL = "https://card.mcmaster.ca" + uri
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    '''tr = soup.find_all(class_="table table-striped table-condensed table-bordered")'''
    res_mech = soup.select('table[vocab="http://dev.arpcard.mcmaster.ca/browse/data"] tbody tr td')
    drug_class = res_mech[7]    
    print (name + " " + gen)
    print (res_mech [9].text)
    print (drug_class.text)
    line = str(name) + "\t" + str(res_mech [9].text) + "\t" + str(drug_class.text+"\n")
    f = open("ARG.txt", "a")
    f.write(line)
    f.close()

def main ():
    getAllArg()
    f = open("ARG.txt", "a")
    f.write("Name"+"\t"+ "Drug Class" + "\t" + "Resistance Mechanism"+"\n")
    f.close()
    with open('allarg.json') as json_file:
        allarg_json = json.load(json_file)  
        json_file.close()
    search(allarg_json)
    

if __name__ == "__main__":
    main()   