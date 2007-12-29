#!/usr/bin/perl
use lib '../../site/lib';
use lib '../../../lib/lib/perl5/site_perl/5.8.6/darwin-thread-multi-2level';
use strict;
use warnings;
use CGI;
use CGI::Carp 'fatalsToBrowser';
use util;

my $fac = util::siteFactory->new;

# variables to be interpolated in template
my $vars = $fac->create_template_vars();

my $cgi = CGI->new;
print $cgi->header;
print '</div>';
my $template = $fac->create_plain_template;
$template->process( 'footer.tmpl', $vars ) || die $template->error();
