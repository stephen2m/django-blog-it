import re
import htmlentitydefs
from bs4 import BeautifulSoup
from django import template
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter

register = template.Library()
code_regex = re.compile(r'<pre>(.*?)</pre>', re.DOTALL)


def unescape(text):
    """
    Removes HTML or XML character references and entities from a text string.

    :param text The HTML (or XML) source text.
    :return The plain text, as a Unicode string, if necessary.
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


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

        return to_return
    except Exception:
        return value
