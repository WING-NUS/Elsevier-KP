#!/usr/bin/env ruby
# -*- ruby -*-
#
# Author:: Min-Yen Kan (mailto:kanmy@comp.nus.edu.sg)
# Copyright:: 2006--2011 Min-Yen Kan, National University of Singapore
# License::Proprietary
# 
# @@BASE_DIR = "/home/slideseer/"
# $:.unshift("#{@@BASE_DIR}/lib/")
require 'optparse'
require 'ostruct'
require 'time'
require 'rexml/document'
#require 'rexml/xpath'

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
class ConSyn2Pp

  def self.zap_xml(node)
    str = node.to_s
    str.gsub!(/<\/?[^>]+>/,"")
    str.gsub!(/\s+/m," ")
    str
  end
end

############################################################

# set up options
quiet = false
OptionParser.new do |opts|
  opts.banner = "usage: #{@@PROG_NAME} [options] file_name"

  opts.separator ""
  opts.on_tail("-h", "--help", "Show this message") do puts opts; exit end
  opts.on_tail("-q", "--quiet", "Quiet Mode") do |v| quiet = true; end
  opts.on_tail("-v", "--version", "Show version") do puts "#{@@PROG_NAME} " + @@VERSION.join('.'); exit end
end.parse!

c = ConSyn2Pp.new()
count = 0

# open files
ifs = Array.new                 # ifs = input file s
if (ARGV.size == 0) 
  ifs.push(STDIN)
else
  ifs = ARGV
end

# output header
if (quiet)
  puts "# <description> file format #{@@VERSION.join(".")} produced by #{@@PROG_NAME}"
  puts "# run as \"#{$0}\""
  puts "# on " + Time.new.to_s
  puts "# format: <format>"
end

# process each file
ifs.each do
  |fn|
  f = (fn == STDIN or fn == "-") ? STDIN : File.open(fn)

  para_counter = section_counter = 0
  doc = REXML::Document.new(f)
  REXML::XPath.each(doc, "//*") { |elt| 
    case elt.name
    when "title"
      puts "TITLE", ConSyn2Pp.zap_xml(elt)
    when "keyword"
      puts "KEYWORD", ConSyn2Pp.zap_xml(elt)
    when "para"
      puts "PARA #{para_counter}", ConSyn2Pp.zap_xml(elt)
      para_counter += 1
    when "section-title"
      puts "SECTION-TITLE #{section_counter}", ConSyn2Pp.zap_xml(elt)
      section_counter += 1
    end
  }
end
