import re

JAVASCRIPT  = 'js'
ALL         = 'all'
MULTILINE   = 'multiline'
INLINE      = 'inline'

DOCUMENTATION_PATTERN = {
    JAVASCRIPT: {
        ALL: "/\*[\s\S]*?\*/|(?:[^\\\:]|^)//.*$",
        MULTILINE: '/\*[\s\S]*?\*/',
        INLINE: '([^\\\:]|^)//.*$'
    }
}

DOCUMENTATION_REGEX = {
    lang: {
        key: re.compile(DOCUMENTATION_PATTERN[lang][key]) for key in DOCUMENTATION_PATTERN[lang].keys()
    } for lang in DOCUMENTATION_PATTERN.keys()
}

ADW_GLOBALS = {
    'quotations': """/((["'])(?:(?:\\\\)|\\\2|(?!\\\2)\\|(?!\2).|[\n\r])*\2)/""",
    'multiline_comment': """/(\/\*(?:(?!\*\/).|[\n\r])*\*\/)/""",
    'single_line_comment': """/(\/\/[^\n\r]*[\n\r]+)/""",
    'regex_literal': """/(?:\/(?:(?:(?!\\*\/).)|\\\\|\\\/|[^\\]\[(?:\\\\|\\\]|[^]])+\])+\/)/""",
    'html_comments': """/(<!--(?:(?!-->).)*-->)/""",
}

EXT_ANY_FILE = ""

