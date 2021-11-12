import sys
import ete3
from ete3 import Tree
import random
import re
from datetime import datetime
from collections import defaultdict

tree = ete3.Tree("Delta_21thOct.FinalTree.nwk", format=1) #input tree is from treetime and nonbinary
root = tree.get_tree_root()
root.name = "root"


id_country = dict()
#countries = list()
leaf_dates = dict()
def rename_leaves(node):   #list of all nodes
    for ll in node:   
        l = ll.name
        l_1 = l.strip('\'')
        name = ""
        gisid = "not_GISAID"
        date = ""
        
        pnum = l_1.count('|') #counts number of "|" in prename
        if pnum ==1:
            name,date = l_1.split("|")
        if pnum ==2:
            name,gisid,date=l_1.split("|")

        date1 = date

        if ("?" in date) or (not date.startswith("20")):
            date1 = "2300-01-01"
        datecheck = date1.split("-")
        
        if len(datecheck) ==2:
            date1 = date+"-28"#set to max possible date
        if len(datecheck) ==1:
            date1 = date+"-12-31"#set to the latest possible date if data is missing
        if (datecheck[0] == "19" or datecheck[0] == "20" or datecheck[0] == "21"):
            date1 = "20"+date


        country = l_1.split("/",maxsplit=3)[1]
        if country == "cat" or country == "hamster" or country == "mink" or country == "hCoV-19":
            country = "unknown"
        
        if country == "England" or country == "Northern Ireland" or country == "Scotland" or country == "Wales":
            country = "United Kingdom"
            
        if country == "Crimea":
            country = "Russia"


        id_country[l] = country
        date_date = datetime.strptime(date1, "%Y-%m-%d").date()
        leaf_dates[l] = date_date
        

    return node


tree = rename_leaves(tree)


limit = "2020-12-01"
limit_date = datetime.strptime(limit, "%Y-%m-%d").date()
def get_earliest_date(node,count):
    predate = datetime.strptime("2300-01-01", "%Y-%m-%d").date()
    for l in node:
        if leaf_dates[l.name] < predate and leaf_dates[l.name] > limit_date and id_country[l.name] == count:
            predate = leaf_dates[l.name]
    return predate

k = 0
nodes = list()
for node in tree.traverse("levelorder"):
    if not node.is_leaf():
        k = k+1
        node.name = "Internal_"+str(k)
    nodes.append(node)

nodes.reverse()


country_deepmost_imports = defaultdict(list)
node_countries_imports = defaultdict(dict)
node_countries = defaultdict(list)                

for node in nodes:
    if node.is_leaf():
        country = id_country[node.name]  
        node_countries[node].append(country)
    else:
        country_children = defaultdict(list)
        for c in node.children:
            countries = node_countries[c]
            for count in countries:
                if count != "unknown":
                    country_children[count].append(c)
            
        if len(country_children) == 1:
            count = list(country_children.keys())[0]
            node_countries[node].append(count)

        elif len(country_children) > 1:
            for key_country in list(country_children.keys()):
                rus = country_children[key_country]
                if len(rus) == 1:
                    child = rus[0]
                    
                    if child in node_countries_imports and key_country in node_countries_imports[child]:
                        node_countries_imports[child][key_country].clear()
                    else:
                         node_countries_imports[child][key_country] = list()
                    node_countries_imports[child][key_country].append(child.name)
                        
                    if not child.is_leaf():
                        earliest_date = get_earliest_date(child,key_country)
                        outf = open("ML_21thOctTree.DELTA.SimpleImportsNEW.tsv", 'a')
                        children = 0
                        for nd in child:
                            nm = nd.name
                            if nm in id_country:
                                if id_country[nm] == key_country:
                                    children += 1
                        outf.write(str(child.name)+"\t"+key_country+"\t"+str(children)+"\t"+str(earliest_date)+"\n")
                        outf.close()                
                    
                    else:
                        earliest_date = leaf_dates[child.name]
                        outf = open("ML_21thOctTree.DELTA.SimpleImportsNEW.tsv", 'a')
                        outf.write(str(child.name)+"\t"+key_country+"\t1\t"+str(earliest_date)+"\n")
                        outf.close()
                else:
                    node_countries[node].append(key_country)
                    
                
        for child in node.children:
            if child in node_countries_imports:
                countries_imports = node_countries_imports[child]
                for cnt in countries_imports:
                    import_list = countries_imports[cnt]
                    if cnt not in node_countries_imports[node]:
                        node_countries_imports[node][cnt] = list()

                    node_countries_imports[node][cnt].extend(import_list)


    if node.is_root():
        countries_imports = node_countries_imports[node]
        for  cnt in countries_imports:
            import_list = countries_imports[cnt]
            country_deepmost_imports[cnt].extend(import_list)


all_leaves = len(tree)
outf1 = open("ML_21thOctTree.DEEPMOSTSimpleImportsNEW.PlusSubtreeSize.tsv","w")
with open("ML_21thOctTree.DELTA.SimpleImportsNEW.tsv") as inf:
    for line in inf:
        line1 = line.rstrip()
        country = line1.split("\t")[1]
        node = line1.split("\t")[0]

        if country in country_deepmost_imports and node in country_deepmost_imports[country]:
            tree_node = tree&node
            import_leaves = len(tree_node)
            size = import_leaves/all_leaves

            outf1.write(line1+"\t"+str(size)+"\n")

outf1.close()
tree.write(format=1,outfile = "Delta_21thOct.FinalTree.RenamedInternals.nwk")
