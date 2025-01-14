#!/usr/bin/perl
use strict;
use warnings;

sub load_alignments {
    my ($file_path) = @_;
    my %alignment;
    my $header;
    my $sequence = "";

    open(my $fh, '<', $file_path) or die "Could not open file '$file_path': $!";
    while (my $line = <$fh>) {
        chomp $line;
        if ($line =~ /^>(.*)/) {
            if ($header) {
                $alignment{$header} = $sequence;
            }
            $header = $1;
            $sequence = "";
        } else {
            $sequence .= $line;
        }
    }
    # Last sequence
    if ($header) {
        $alignment{$header} = $sequence;
    }
    close($fh);

    return \%alignment;
}

sub write_combined_alignment {
    my ($alignment1, $alignment2, $output_file) = @_;

    open(my $out, '>', $output_file) or die "Could not open file '$output_file': $!";
    foreach my $header (keys %$alignment1) {
        if (exists $alignment2->{$header}) {
            print $out ">$header\_LHS\n$alignment1->{$header}\n";
            print $out ">$header\_RHS\n$alignment2->{$header}\n";
        }
    }
    close($out);
}

# Main program
if (@ARGV != 3) {
    die "Usage: $0 alignment1.fasta alignment2.fasta output.fasta\n";
}

my ($alignment1_file, $alignment2_file, $output_file) = @ARGV;

my $alignment1 = load_alignments($alignment1_file);
my $alignment2 = load_alignments($alignment2_file);

write_combined_alignment($alignment1, $alignment2, $output_file);

print "Combined alignment written to $output_file\n";
