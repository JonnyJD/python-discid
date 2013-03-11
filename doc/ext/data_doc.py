from sphinx.ext import autodoc
from sphinx.util.inspect import safe_repr

def setup(app):
    app.add_autodocumenter(DataDocumenter)

class DataDocumenter(autodoc.DataDocumenter):
    """
    Specialized Documenter subclass for data items.
    These can have a :novalue: option.
    """
    option_spec = {"noindex": autodoc.bool_option,
            "annotation": autodoc.bool_option}

    def add_directive_header(self, sig):
        autodoc.ModuleLevelDocumenter.add_directive_header(self, sig)
        if not "annotation" in self.options:
            try:
                objrepr = safe_repr(self.object)
            except ValueError:
                pass
            else:
                self.add_line(u'   :annotation: = ' + objrepr, '<autodoc>')
