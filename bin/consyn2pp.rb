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
train = false
OptionParser.new do |opts|
  opts.banner = "usage: #{@@PROG_NAME} [options] file_name"

  opts.separator ""
  opts.on_tail("-h", "--help", "Show this message") do puts opts; exit end
  opts.on_tail("-t", "--train", "Train mode") do |t| train = true; end
  opts.on_tail("-q", "--quiet", "Quiet Mode") do |q| quiet = true; end
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
if (!quiet)
  puts "# <description> file format #{@@VERSION.join(".")} produced by #{@@PROG_NAME}"
  puts "# run as \"#{$0}\""
  puts "# on " + Time.new.to_s
  puts "# format: <format>"
end

# process each file
ifs.each do
  |fn|
  f = (fn == STDIN or fn == "-") ? STDIN : File.open(fn)

  seen_title = false
  para_counter = section_counter = 0
  doc = REXML::Document.new(f)
  REXML::XPath.each(doc, "//*") { |elt| 
    case elt.name
    when "title"
      if (!seen_title) 
      	seen_title = true
        puts "TITLE", ConSyn2Pp.zap_xml(elt)
      end
    when "keyword"
      if (train) then puts "KEYWORD", ConSyn2Pp.zap_xml(elt) end
    when "para"
      if false then puts "PARA #{para_counter}\n" end
      puts ConSyn2Pp.zap_xml(elt), "\n"
      para_counter += 1
    when "section-title"
      if false then puts "SECTION-TITLE #{section_counter}" end
      puts ConSyn2Pp.zap_xml(elt), "\n"
      section_counter += 1
    end
  }
end
