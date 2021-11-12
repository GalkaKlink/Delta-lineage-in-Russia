use strict;
use Statistics::Test::WilcoxonRankSum;
use Bio::TreeIO;

my $numb = $ARGV[0];
my $in = Bio::TreeIO -> new(-file => 'Delta_21thOct.FinalTree.nwk',
			    -format => 'newick');

my $tree = $in -> next_tree;

open (TABLE, ">>PhyloDistrH0".$numb.".tsv") or die $!;

my @leafnodes = $tree->get_leaf_nodes;
my @leafs;
foreach my $leafnode(@leafnodes)  {
    my $leaf = $leafnode->id;
    push(@leafs,$leaf);
}
    
my $flag1 = 0;
my @all_dists;
            
until($flag1 == 100){
    $flag1 += 1;
    my $rand1 = int(rand($#leafs+1));
    my $rand2=$rand1;
    until($rand2 != $rand1) {
	$rand2 = int(rand($#leafs+1));
    }
    my $nd1 = $leafs[$rand1];
    my $nd2 = $leafs[$rand2];
    
    my $node1 = $tree -> find_node(-id => $nd1);
    my $node2 = $tree -> find_node(-id => $nd2);
    my $distance = $tree->distance(-nodes=>[$node1,$node2]);
    print TABLE $distance."\n";
}
