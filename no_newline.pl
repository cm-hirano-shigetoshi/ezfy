#!/usr/bin/env perl
use strict;
use warnings;

my $new_line = "";
while (<>) {
    s/[\r\n]//g;
    print $new_line;
    $new_line = "\n";
    print;
}

