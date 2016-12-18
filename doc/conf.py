
import sys
import os
import shlex

sys.path.insert( 0, os.path.abspath( '../NIST/' ) )

################################################################################

project = u'NIST'
copyright = u'2016, Marco De Donno'
author = u'Marco De Donno'

version = u'0.20.0'
release = u'0.20.0'

################################################################################

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
]

templates_path = [ '_templates' ]

source_suffix = '.rst'

master_doc = 'index'

language = None

exclude_patterns = ['_build']

show_authors = True

pygments_style = 'sphinx'

todo_include_todos = False

################################################################################
#    Options for HTML output
################################################################################

html_theme = 'classic'

html_theme_options = {}

html_static_path = [ '_static' ]

html_last_updated_fmt = '%b %d, %Y'

html_show_sourcelink = True

html_show_sphinx = False

htmlhelp_basename = 'NISTdoc'

################################################################################
#    Options for LaTeX output
################################################################################

latex_elements = {
    'papersize': 'a4paper'
}

latex_documents = [
   ( 
        master_doc,
        'NIST.tex',
        u'NIST Documentation',
        u'Marco De Donno',
        'howto'
    ),
]

latex_show_pagerefs = True

latex_show_urls = True

################################################################################
#    Options for manual page output
################################################################################

man_pages = [
    ( 
        master_doc,
        'nist',
        u'NIST Documentation',
        [author],
        1
    )
]

man_show_urls = True
