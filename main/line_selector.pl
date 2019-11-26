#!/usr/bin/env perl
use strict;
use warnings;

my %indexes = map{ $_ => 1 } split(",", $ARGV[0]);

my $line_x = 1;
while (<STDIN>) {
    if (defined($indexes{$line_x})) {
        print;
        delete($indexes{$line_x});
        if (scalar(keys(%indexes)) == 0) {
            last;
        }
    }
    $line_x++;
}



