#!/usr/bin/env perl
use strict;
use warnings;

my $fzf = "${fzf}";

my $input = q${base_task.input};
my $query = q${base_task.query};
my $preview = q${base_task.preview};
my $opts = q${base_task.opts};

while (1) {
    my $cmd = "";
    $cmd .= "$input";
    $cmd .= " | $fzf";
    $cmd .= " --print-query";
    $cmd .= " --expect='${expects.definition}'";
    $cmd .= " ${binds}";
    $cmd .= " $opts";
    $cmd .= " --query='$query'";
    $cmd .= " --preview='$preview'";
    my ($q, $k, $ref_outputs) = &split_outputs(`$cmd`."");


    if (0) {
${expects.operation}
    } elsif ($k eq "ctrl-m") {
        print &pre_process($ref_outputs, "\n", "");
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

sub pre_process {
    my ($o, $delimiter, $quote) = @_;
    my $d = $quote . $delimiter . $quote;
    my $s = $quote . join($d, @{$o}) . $quote;
    return $s . "\n";
}

sub make_files {
    my @files = map {
        s/^~/$ENV{HOME}/; $_;
    } @{$_[0]};
    return "\"" . join("\" \"", @files) . "\"";
}

