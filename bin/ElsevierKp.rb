#!/usr/bin/env ruby
# -*- ruby -*-
#
# CVS: $Id$
#
# Author:: Min-Yen Kan (mailto:kanmy@comp.nus.edu.sg)
# Copyright:: 2006,2007 by Min-Yen Kan, National University of Singapore
# License::Proprietary
# 
# CVS: $Log$
@@BASE_DIR = "/home/slideseer/"
$:.unshift("#{@@BASE_DIR}/lib/")
require 'optparse'
require 'ostruct'
require 'time'

# defaults
@@VERSION = [1,0]
@@INTERVAL = 100
@@PROG_NAME = File.basename($0)

############################################################
# EXCEPTION HANDLING
int_handler = proc {
  # clean up code goes here
  STDERR.puts "\n# #{@@PROG_NAME} fatal\t\tReceived a 'SIGINT'\n# #{@@PROG_NAME}\t\texiting cleanly"
  exit -1
}
trap "SIGINT", int_handler

############################################################
# PUT CLASS DEFINITION HERE

############################################################

# set up options
@@options = OpenStruct.new
OptionParser.new do |opts|
  opts.banner = "usage: #{@@PROG_NAME} [options] file_name"

  opts.separator ""
  opts.on_tail("-h", "--help", "Show this message") do puts opts; exit end
  opts.on_tail("-v", "--version", "Show version") do puts "#{@@PROG_NAME} " + @@VERSION.join('.'); exit end
end.parse!

# c = Class.new(@@options)
count = 0

# open files
ifs = Array.new                 # ifs = input file s
if (ARGV.size == 0) 
  ifs.push(STDIN)
else
  ifs = ARGV
end

# output header
puts "# <description> file format #{@@VERSION.join(".")} produced by #{@@PROG_NAME}";
puts "# run as \"#{$0}\"";
puts "# on " + Time.new.to_s
puts "# format: <format>";
  
# process each file
ifs.each do
  |fn|
  f = (fn == STDIN or fn == "-") ? STDIN : File.open(fn)

  while !f.eof do
    l = f.gets.chomp
    if /^\#/.match(l) then next end # skip comment lines
    if /^\s*$/.match(l) then next end # skip blank lines
    puts l
    elts = l.split(/\t/)
    count = count+1
    if count % @@INTERVAL == 0 then STDERR.print "[#{count}]" end
  end
end
