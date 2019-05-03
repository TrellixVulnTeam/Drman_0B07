from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from Drman import settings

class ElrteWidget(forms.Textarea):
    """
    A widget that draws the Elrte WYSIWYG editor for large text fields.
    """
    def __init__(self, attrs=None, lang='en', styleWithCSS=False, height=400, width=0, toolbar='maxi'):
        self.lang, self.styleWithCSS, self.height = lang, styleWithCSS, height
        self.width,  self.toolbar = width,  toolbar
        super(ElrteWidget, self).__init__(attrs)

    def _media(self):
        l_js = [settings.JQUERY_URL, settings.ELRTE_JS_ELRTE_URL, settings.JQUERY_UI_URL]
        if self.lang != 'en':
            l_js.append('%selrte.%s.js' % (settings.ELRTE_LANG_URL, self.lang))

        l_css = [settings.ELRTE_CSS_ELRTE_URL, settings.JQUERY_UI_CSS_URL]

        return forms.Media(css={'screen': l_css}, js=l_js)

    media = property(_media)

    def render(self, name, value, attrs=None):
        width = ('    width: %i,' % self.width) if self.width > 0 else ''

        html = super(ElrteWidget, self).render(name, value, attrs)
        html += ('<script type="text/javascript">'
                 '(function($) { '
                 '$(document).ready(function() {'
                 '  var opts = {'
                 '    doctype : \'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN">\','
                 '    lang : \'%(lang)s\','
                 '    styleWithCss: %(style)s,'
                 '    height: %(height)i,'
                 '%(width)s'
                 '    fmAllow: false,'
                 '    toolbar: \'%(toolbar)s\','
                 '     };'
                 '  $("#%(id)s").elrte(opts);'
                 '});'
                 '})(jQuery);'
                 '</script>' % {'lang': self.lang,
                                'id': attrs['id'],
                                'style': str(self.styleWithCSS).lower(),
                                'width': width,
                                'height': self.height,
                                'toolbar': self.toolbar,
                                })
        return mark_safe(html)