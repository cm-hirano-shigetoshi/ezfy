#!/usr/bin/env perl
use strict;
use warnings;

my $fzf = "${fzf}";

my $input = q${base_task.input};
my $query = q${base_task.query};
my $preview = q${base_task.preview};
my $opts = q${base_task.opts};
my $filter = q${base_task.line_select.filter};

${extra.declaration}

while (1) {
    my $cmd = "";
    $cmd .= "$input";
    $cmd .= " ${extra.before_fzf}";
    $cmd .= " | SHELL=bash $fzf";
    $cmd .= " --print-query";
    $cmd .= " --expect='${expects.definition}'";
    $cmd .= " ${binds}";
    $cmd .= " $opts";
    $cmd .= " --query=\"$query\"";
    $cmd .= " --preview='$preview'";
    my ($q, $k, $ref_outputs) = &split_outputs(`$cmd`."");
    if ($opts =~ /--select-1/ && $k eq "") {
        $k = "select-1";
    }


    if (0) {
${expects.operation}
    } elsif ($k eq "ctrl-m" || $k eq "select-1") {
        print &pre_process($ref_outputs, "\n", "");
    }

    last;
}

sub make_temp {
    return `mktemp -t 'fzfer_line_select_xxxxxxxx`;
}

sub split_outputs {
    if ($_[0] =~ /^\s*$/) {
        exit -1;
    }

    my @lines = split("\n", $_[0]);
    my ($q, $k) = (shift(@lines), shift(@lines));
    return ($q, $k, \@lines);
}

sub nth {
    my ($o, $n, $d) = @_;
    my $joiner = ($d eq '\s+')? " " : $d;
    my @nth = split(",", $n);
    my @return = ();
    foreach (@{$o}) {
        my @tokens = grep { length($_) > 0 } split($d, $_);
        my @one_line = ();
        foreach (@nth) {
            s/(-\d+)/scalar(@tokens) + $1 + 1/ge;
            if ($_ eq "..") {
                for (my $i=1; $i<=$#tokens+1; $i++) {
                    push(@one_line, $tokens[$i-1]);
                }
            } elsif (/^(\d+)\.\.(\d+)$/) {
                for (my $i=$1; $i<=$2; $i++) {
                    push(@one_line, $tokens[$i-1]);
                }
            } elsif (/^(\d+)\.\.$/) {
                for (my $i=$1; $i<=$#tokens+1; $i++) {
                    push(@one_line, $tokens[$i-1]);
                }
            } elsif (/^\.\.(\d+)$/) {
                for (my $i=1; $i<=$1; $i++) {
                    push(@one_line, $tokens[$i-1]);
                }
            } else {
                push(@one_line, $tokens[$_-1]);
            }
        }
        push(@return, join($joiner, @one_line));
    }
    return \@return;
}

sub expand_home {
    my @lines = map {
        s/^~/$ENV{HOME}/; $_;
    } @{$_[0]};
    return \@lines;
}

sub quotation {
    if ($_[1] eq "") {
      my @lines = map {
          if (/'/) {
              '"' . $_ . '"';
          } elsif (/[ \["&()|`;<!]/) {
              "'" . $_ . "'";
          } else {
              $_;
          }
      } @{$_[0]};
      return \@lines;
    } else {
      my @lines = map {
          $_[1] . $_ . $_[1];
      } @{$_[0]};
      return \@lines;
    }
}

sub line_select {
    open(my $file, "cat '$_[0]' | fzf --ansi --filter='^' |");
    my @lines = (<$file>);
    close($file);
    my @selected = ();
    foreach (@{$_[1]}) {
        if (/^\s*(\d+)\s/) {
            $_ = $lines[$1-1];
            s/^\s*(\d+)\s+//;
            s/[\r\n]//g;
            push(@selected, $_);
        }
    }
    return \@selected;
}

