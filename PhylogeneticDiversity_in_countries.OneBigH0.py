import re
from ete3 import Tree
import optparse
from statistics import stdev
import random
from scipy import stats


parser=optparse.OptionParser()
parser.add_option('-c', '--country', help='', type='str')
parser.add_option('-i', '--infile', help='', type='str')
options, args=parser.parse_args()

focal_country = options.country

t = Tree(options.infile, format = 1)

all_dists = 0
zn_all_dists = 0
dists_array = list()

with open("H0forPhylo.tsv") as null:
    for line in null:
        line = line.rstrip()
        number = float(line)
        all_dists += number
        zn_all_dists += 1 
        dists_array.append(number)

mean_all_dist = all_dists/zn_all_dists
std_all_dist = stdev(dists_array)


leafs = list()
for ll in t:
    l = ll.name
    l_1 = l.strip('\'')
    country = l_1.split("/",maxsplit=3)[1]
    if country=="Crimea":
        country = "Russia"
    if country=="England" or country=="Northern Ireland" or country=="Scotland" or country=="Wales":
        country="United Kingdom"
    if country==focal_country:
        leafs.append(l)

if len(leafs) > 50:
    outf = open("Python.OneBigH0_PhyloTest."+focal_country, "w")
    outf.write("country\tsamples\tmean_count_dist\tmean_DiffCount_dist\tz_score\tp_value\n")
 
    flag = 0
    aa_dists = 0
    zn_dists = 100
    aa_dists_array = list()

    while (flag < 100):
        flag += 1
        rand1 = random.randint(0,len(leafs)-1)   
        rand2=rand1
        while(rand2 == rand1):
            rand2 =  random.randint(0,len(leafs)-1) 
	
        nd1 = leafs[rand1]
        nd2 = leafs[rand2]
	
        dist = t.get_distance(nd1,nd2)
        aa_dists += dist
        aa_dists_array.append(dist)
    
    mean_aa_dist = aa_dists/zn_dists
     
    z_score = (mean_aa_dist-mean_all_dist)/std_all_dist  


    wilcox_test = stats.mannwhitneyu(aa_dists_array, dists_array)
    prob = wilcox_test.pvalue
    prob = round(prob,3)

    samples_number = len(leafs)
    outf.write (focal_country+"\t"+str(samples_number)+"\t"+str(mean_aa_dist)+"\t"+str(mean_all_dist)+"\t"+str(z_score)+"\t"+str(prob)+"\n")


