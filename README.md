# Delta-lineage-in-Russia
This repository contains scripts used in [link to a paper] 
These scripts were used to produce data for drawing Figure 6 of the paper

**get_imports_all_countries.PlusSizeOfImportSubtree.py** - takes phylogenetic tree with GISAID names(hCoV-19/country/name/year|ID|date) as tip labels. For each country, finds import events, as defined in the paper (note: this definition is very conservative, therefore the results correspond the minimum set of imports into each country). 
Creates intermediate output and final output with the deepest imports.
Columns of final output: import node, country, number of children from this country, date of earliest sample, fraction of the clade formed by this node in a whole tree.

**H0_forPhyloDiversity.pl** - creates a list of pairwise distances for specified number of random tips paires that serves as a null distribution for phylogenetic clustering estimation.

**PhylogeneticDiversity_in_countries.OneBigH0.py** - takes phylogenetic tree with GISAID names(hCoV-19/country/name/year|ID|date) as tip labels, null distribution of distances obtained by H0_forPhyloDiversity.pl and a focal country from the list. If there are more than 50 samples from the focal country in a tree, estimates phylogenetic distances betwen 100 random pairs of samples from this country as well as p-value and standard score for phylogenetic clustering of samples from the focal country on the tree. Output contains columns: country, number of samples in a tree, mean pairwise distance, mean of the null distribution, z-score, p-value.         
