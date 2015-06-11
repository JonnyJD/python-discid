import sys, os

sys.path.insert(0, os.path.abspath('.'))        # for extensions
sys.path.insert(0, os.path.abspath('..'))       # for the code

# -- Mock libdiscid loading ----------------------------------------------------

class Mock(object):
    def __call__(self, *args): return Mock()
    def __getattr__(cls, name): return Mock()

import ctypes
ctypes.cdll.LoadLibrary = Mock()

# to gather version information
import discid

# -- General configuration -----------------------------------------------------

needs_sphinx = "1.0"

extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.coverage',
    'sphinx.ext.extlinks', 'sphinx.ext.intersphinx'
]
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']

# General information about the project.
project = u'python-discid'
copyright = u'2013, Johannes Dewender'
# The short X.Y version / base version
version = ".".join(discid.__version__.split("-")[0].split(".")[0:2])
# The full version, including alpha/beta/rc tags.
release = discid.__version__
# see below for "current" = base version with "-dev" appended if necessary

download_base = "https://github.com/JonnyJD/python-discid/archive"
if release.endswith("dev"):
    current = "%s-dev" % version
    download_url = "%s/master.%%s" % download_base
else:
    current = version
    download_url = "%s/v%s.%%s" % (download_base, release)

extlinks = {
  'source_download': (download_url, ''),
  'issue': ('https://github.com/JonnyJD/python-discid/issues/%s', '#'),
  'musicbrainz': ('http://musicbrainz.org/doc/%s', ''),
}

# there seems to be no way to prefer latest python documentation
intersphinx_mapping = {
  'python': ('http://python.readthedocs.org/en/latest/', None),
  'python2': ('http://python.readthedocs.org/en/v2.7.2/', None),
  'musicbrainzngs':
    ('http://python-musicbrainzngs.readthedocs.org/en/latest/', None),
}

rst_prolog = """
.. currentmodule:: discid
"""

rst_epilog = """
.. |current| replace:: %s
""" % current

# -- Options for HTML output ---------------------------------------------------

html_theme = 'default'
# force default theme on readthedocs to apply our theme options
html_style = "/default.css"
# MusicBrainz colors
html_theme_options = {
        "footerbgcolor": "#e7e7e7",
        "footertextcolor": "#444444",
        "sidebarbgcolor": "#ffffff",
        "sidebartextcolor": "#000000",
        "sidebarlinkcolor": "002bba",
        "relbarbgcolor": "#5c5789",
        "relbartextcolor": "#000000",
        "bgcolor": "#ffffff",
        "textcolor": "#000000",
        "linkcolor": "#002bba",
        "headbgcolor": "#ffba58",
        "headtextcolor": "#515151",
        "codebgcolor":  "#dddddd",
        "codetextcolor": "#000000"
}

html_title = "%s %s documentation" % (project, current)
html_domain_indices = False

# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'python-discid.tex', u'python-discid Documentation',
   u'Johannes Dewender', 'manual'),
]

latex_domain_indices = False

# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'python-discid', u'python-discid Documentation',
     [u'Johannes Dewender'], 1)
]

# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'python-discid', u'python-discid Documentation',
   u'Johannes Dewender', 'python-discid', 'One line description of project.',
   'Miscellaneous'),
]

texinfo_domain_indices = False

