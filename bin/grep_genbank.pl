#!/usr/bin/perl
use strict;
use warnings;
use Getopt::Long;

my $genbank_id;
GetOptions("genbank=s" => \$genbank_id) or die "Usage: $0 --genbank <id>\n";

die "Please provide a GenBank ID using --genbank <id>\n" unless $genbank_id;

my $in_desired_entry = 0;
my $current_entry = "";
my $entry_found = 0;

while (my $line = <>) {
    if ($in_desired_entry) {
        $current_entry .= $line;
        if ($line =~ /^\/\/$/) {
            print $current_entry;
            $entry_found = 1;
            last;
        }
    } elsif ($line =~ /^LOCUS\s+(\S+)/) {
        my $locus = $1;
        if ($locus eq $genbank_id) {
            $in_desired_entry = 1;
            $current_entry = $line;
        }
    }
}

if (!$entry_found) {
    print "GenBank entry with ID '$genbank_id' not found.\n";
}