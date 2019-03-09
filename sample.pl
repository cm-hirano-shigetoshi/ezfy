#!/usr/bin/env perl
use strict;
use warnings;

my $fzf = "/Users/hirano.shigetoshi/local/bin/fzf";
my $default_settings = "--exact --multi --no-mouse --print-query";

my ($initial_input, $initial_query) = ("", "");
#$initial_input = "tac ~/.zsh/directory_all.txt | awk '!a[\$1]++'";
$initial_input = "git log --graph --decorate --oneline --color=always";
$initial_query = "";
my ($input, $query) = ($initial_input, $initial_query);

while (1) {
    my $cmd = "";
    $cmd .= "$input";
    $cmd .= " | $fzf";
    $cmd .= " $default_settings";
    $cmd .= " --ansi";
    $cmd .= " --reverse";
    $cmd .= " --query='$query'";
    $cmd .= " --expect='ctrl-t'";
    $cmd .= " --preview='echo {}'";
    $cmd .= " --preview-window='up'";
    $cmd .= " --with-nth=1..";
    my ($q, $k, $ref_outputs) = &split_outputs(`$cmd`."");


    if ($k eq "ctrl-t") {
        $input = "date";
        $query = "1";
        next;
    } else {
        &stdout($ref_outputs);
    }


    last;
}

sub split_outputs {
    my @lines = split("\n", $_[0]);
    my ($q, $k) = (shift(@lines), shift(@lines));
    return ($q, $k, \@lines);
}

sub stdout {
    print join("\n", @{$_[0]});
}

