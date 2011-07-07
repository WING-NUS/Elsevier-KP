#!/usr/bin/env perl
# -*- cperl -*-
=head1 NAME

elsevier.cgi

=head1 SYNOPSIS

Put Synopsis here.

=head1 DESCRIPTION

=head1 HISTORY

 ORIGIN: created from templateApp.pl version 3.4 by Min-Yen Kan <kanmy@comp.nus.edu.sg>

=cut
require 5.0;
use Getopt::Std;
use CGI;

### USER customizable section
my $tmpfile .= $0; $tmpfile =~ s/[\.\/]//g;
$tmpfile .= $$ . time;
if ($tmpfile =~ /^([-\@\w.]+)$/) { $tmpfile = $1; }                 # untaint tmpfile variable
$tmpfile = "/tmp/" . $tmpfile;
$0 =~ /([^\/]+)$/; my $progname = $1;
my $outputVersion = "1.0";
my $baseDir = "/home/min/public_html/elsevier";
my $binDir = "$baseDir/";
my $libDir = "$baseDir/";
my $logFile = "$libDir/cgiLog.txt";
my $seed = $$;
my $debug = 0;

my $loadThreshold = 0.5;
my $loadKey = "wing";
### END user customizable section

$| = 1;								    # flush output

### Ctrl-C handler
sub quitHandler {
  print STDERR "\n# $progname fatal\t\tReceived a 'SIGINT'\n# $progname - exiting cleanly\n";
  exit;
}

### HELP Sub-procedure
sub Help {
  print STDERR "usage: $progname -h\t\t\t\t[invokes help]\n";
  print STDERR "       $progname -v\t\t\t\t[invokes version]\n";
  print STDERR "       $progname [-q] filename(s)...\n";
  print STDERR "Options:\n";
  print STDERR "\t-q\tQuiet Mode (don't echo license)\n";
  print STDERR "\n";
  print STDERR "Will accept input on STDIN as a single file.\n";
  print STDERR "\n";
}

### VERSION Sub-procedure
sub Version {
  if (system ("perldoc $0")) {
    die "Need \"perldoc\" in PATH to print version information";
  }
  exit;
}

sub License {
  print STDERR "# Copyright 2004 \251 by Min-Yen Kan\n";
}

my $q = new CGI;
print "Content-Type: text/html\n\n";
print <<END;
<HTML><HEAD><TITLE>Echo</TITLE>
END
print "</HEAD><BODY>";

###
### MAIN program
###

my $query = $q->param('query');

if ($query eq "") {		# test input has input
  print "You must input some data.  <A HREF=\"index.html\">Start over.</A>\n";
  exit;
}

# need to untaint query
#$query =~ /([\s\w]+)/;
#$query = $1;			# untainted!
@words = split(/\s+/,$query);
print "$words[0] " . ($#words+1) . " ";
$hostname = `hostname`;
print "$hostname";
print "</BODY></HTML>\n";

open (LOGFILE, ">>$logFile") || die "# $progname fatal\t\tCouldn't open logfile file \"$logFile\"";
print LOGFILE "# Executed for REMOTE_ADDR " . $q->remote_addr() . " at " . localtime(time) . "\n";
print LOGFILE "$query\n";
close (LOGFILE);

###
### END of main program
###

