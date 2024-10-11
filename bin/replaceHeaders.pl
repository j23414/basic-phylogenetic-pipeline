#! /usr/bin/env perl
# Auth: Jennifer Chang
# Date: 2018/03/21

use strict;
use warnings;

# ======================= Check Arguments
my $USAGE = "USAGE: $0 <headers.fa> <fastatoformat.fa> > <newseq.fa>\n";
$USAGE=$USAGE."    First column before the pipe must match\n";

if(@ARGV<2){
    die $USAGE;
    exit;
}

# ======================= Initial Variables
my ($fn1, $fn2)=@ARGV;
my %color=();

print STDERR "Pulling headers for strains from $fn1 to reformat headers in $fn2\n";

# ======================= Read original first file
my $fh;
open($fh, '<:encoding(UTF-8)', $fn1)
    or die "!!Could not open file '$fn1'";

my %headers;
my @field;
my $line;

# Read in the headers
while(<$fh>){
    chomp;
    if(/>(.+)/){
	    $line=$1;
	    @field=split(/\|/,$line);
	    $headers{$field[0]}=$line;
    }
}
close($fh);

# Replace them in the new file
open($fh, '<:encoding(UTF-8)', $fn2)
    or die "!!Could not open file '$fn2'";

while(<$fh>){
    chomp;
    if(/>(.+)/){
	    $line=$1;
	    @field=split(/\|/,$line);
	    print(">$headers{$field[0]}\n");
    } else {
	    print "$_\n";
    }
}

close($fh);
