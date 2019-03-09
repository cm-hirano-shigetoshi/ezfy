#!/usr/bin/env perl
use strict;
use warnings;

my $fzf = "/Users/hirano.shigetoshi/local/bin/fzf";

my ($initial_input, $initial_query, $initial_preview) = ("", "", "");
#$initial_input = "tac ~/.zsh/directory_all.txt | awk '!a[\$1]++'";
$initial_input = "${init_task.input}";
$initial_query = "";
$initial_preview = "${init_task.preview}";
my ($input, $query) = ($initial_input, $initial_query);

while (1) {
    my $cmd = "";
    $cmd .= "$input";
    $cmd .= " | $fzf";
    $cmd .= " --print-query";
    $cmd .= " --query=$query";
    $cmd .= " ${init_task.opts}";
    $cmd .= " --preview='${init_task.preview}'";
    $cmd .= " --expect='${expects.definition}'";

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

