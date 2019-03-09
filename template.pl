#!/usr/bin/env perl
use strict;
use warnings;

my $fzf = "/Users/hirano.shigetoshi/local/bin/fzf";

# tasks
my $input = '${init_task.input}';
my $query = '${init_task.query}';
my $preview = '${init_task.preview}';
my $opts = '${init_task.opts}';

while (1) {
    my $cmd = "";
    $cmd .= "$input";
    $cmd .= " | $fzf";
    $cmd .= " --print-query";
    $cmd .= " --expect='${expects.definition}'";
    $cmd .= " $opts";
    $cmd .= " --query='$query'";
    $cmd .= " --preview='$preview'";

    #$cmd .= " --exact --multi --no-mouse --print-query";
    #$cmd .= " --ansi";
    #$cmd .= " --reverse";
    #$cmd .= " --query='$query'";
    #$cmd .= " --expect='ctrl-t'";
    #$cmd .= " --preview='echo {}'";
    #$cmd .= " --preview-window='up'";
    #$cmd .= " --with-nth=1..";
    my ($q, $k, $ref_outputs) = &split_outputs(`$cmd`."");


    if ($k eq "ctrl-m") {
        &stdout($ref_outputs);
    ${expects.operation}
    }
    #if ($k eq "ctrl-m") {
    #    &stdout($ref_outputs);
    #} elsif ($k eq "ctrl-t") {
    #    $input = "date";
    #    $query = "1";
    #    next;
    #}


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

sub stdout {
    print join("\n", @{$_[0]});
}

