import sys, os

sys.path.insert(0, os.path.abspath('.'))        # for extensions
sys.path.insert(0, os.path.abspath('..'))       # for the code

# to gather version information
import discid
# -- General configuration -----------------------------------------------------

needs_sphinx = "1.0"

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.extlinks', 'ext.data_doc']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']

# General information about the project.
project = u'python-discid'
copyright = u'2013, Johannes Dewender'
# The short X.Y version.
version = ".".join(discid._version.split(".")[0:2])
# The full version, including alpha/beta/rc tags.
release = discid._version

libdiscid = '0.3.0'

download_base = "https://github.com/JonnyJD/python-discid/archive"
if release.endswith("dev"):
    download_url = "%s/master.%%s" % download_base
else:
    download_url = "%s/v%s.%%s" % (download_base, release)

extlinks = {
  'source_download': (download_url, ''),
  'issue': ('https://github.com/JonnyJD/python-discid/issues/%s', 'issue '),
  'libdiscid_download':
    ('https://github.com/metabrainz/libdiscid/archive/v%s.%%s' % libdiscid, ''),
}

# -- Options for HTML output ---------------------------------------------------

html_theme = 'default'
html_title = "%s %s documentation" % (project, version)
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

# -- Mock libdiscid loading ----------------------------------------------------

class Mock(object):
    def __call__(self, *args): return Mock()
    def __getattr__(cls, name): return Mock()

import ctypes
ctypes.cdll.LoadLibrary = Mock()
