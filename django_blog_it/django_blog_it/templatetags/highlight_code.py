import re
from django import template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter

register = template.Library()
code_regex = re.compile(r'<pre>(.*?)</pre>', re.DOTALL)


@register.filter
def pygmentify(value):
    try:
        last_end = 0
        to_return = ''
        for match_obj in code_regex.finditer(value):
            code_string = match_obj.group(1)

            try:
                lexer = guess_lexer(code_string)
            except ValueError:
                lexer = PythonLexer()
            pygmented_string = highlight(
                code_string, lexer, HtmlFormatter()
            )
            to_return += value[last_end:match_obj.start(1)] + \
                pygmented_string
            last_end = match_obj.end(1)

        to_return += value[last_end:]

        return mark_safe(force_unicode(to_return))
    except Exception:
        return mark_safe(force_unicode(value))
