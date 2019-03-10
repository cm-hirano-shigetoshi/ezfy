#!/usr/bin/env perl
use strict;
use warnings;

my $fzf = "${fzf}";

my $input = '${base_task.input}';
my $query = '${base_task.query}';
my $preview = '${base_task.preview}';
my $opts = '${base_task.opts}';

while (1) {
    my $cmd = "";
    $cmd .= "$input";
    $cmd .= " | $fzf";
    $cmd .= " --print-query";
    $cmd .= " --bind='${binds}'";
    $cmd .= " --expect='${expects.definition}'";
    $cmd .= " $opts";
    $cmd .= " --query='$query'";
    $cmd .= " --preview='$preview'";
    $cmd .= " --preview='$preview'";
    my ($q, $k, $ref_outputs) = &split_outputs(`$cmd`."");


    if (0) {
${expects.operation}
    } elsif ($k eq "ctrl-m") {
        open(my $stdout, "| cat");
        print $stdout join("\n", @{$ref_outputs});
        close($stdout);
    }

    last;
}

sub split_outputs {
    if ($_[0] =~ /^\s*$/) {
        exit -1;
    }

    my @lines = split("\n", $_[0]);
    my ($q, $k) = (shift(@lines), shift(@lines));
    return ($q, $k, \@lines);
}

