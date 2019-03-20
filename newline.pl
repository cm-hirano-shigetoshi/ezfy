#!/usr/bin/env perl
use strict;
use warnings;

my $mode = $ARGV[0];
$_ = join("", (<STDIN>));
if ($mode eq "no") {
    s/\s+$//;
    print;
} elsif ($mode eq "auto") {
    if (/\n\s*\S/) {
        print;
    } else {
        s/\s+$//;
        print;
    }
}

