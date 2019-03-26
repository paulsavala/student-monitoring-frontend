import re

# Things to parse:
# - Change single $ to \(...\)
# - Change itemize/enumerate to ul/ol and li

class LatexParser():
    def __init__(self):
        # Counters
        self.inline_counter = 0


    def initialize_counters(self):
        self.inline_counter = 0


    def inline_converter(self, match_object):
        # Lets inline math conversion happen in alternating pairs. So that $...$ is converted to \(...\)
        if self.inline_counter == 0:
            self.inline_counter = 1
            return r'\('
        else:
            self.inline_counter = 0
            return r'\)'


    def bold_converter(self, match_object):
        inside = re.search(r'(?<=\\textbf{)[^}]*(?=})', match_object.group(0))
        if inside is not None:
            return r'<b>{}</b>'.format(inside.group(0))
        inside = re.search(r'{\\bf[^}]*}', match_object.group(0))
        if inside is not None:
            return r'<b>{}</b>'.format(inside.group(0))
        return ''


    def italic_converter(self, match_object):
        inside = re.search(r'(?<=\\textit{)[^}]*(?=})', match_object.group(0))
        if inside is not None:
            return r'<i>{}</i>'.format(inside.group(0))
        inside = re.search(r'{\\it[^}]*}', match_object.group(0))
        if inside is not None:
            return r'<i>{}</i>'.format(inside.group(0))
        return ''


    def parse(self, raw_latex):
        # Initialize counters
        self.initialize_counters()

        # Change $ to inline \(...\)
        parsed_latex = re.sub(r'(?<![\$\\])\$(?![\$])', self.inline_converter, raw_latex)

        # Change itemize/enumerate to ul/ol and li to \item
        parsed_latex = re.sub(r'\\begin{itemize}', '<ul>', parsed_latex)
        parsed_latex = re.sub(r'\\end{itemize}', '</ul>', parsed_latex)
        parsed_latex = re.sub(r'\\begin{enumerate}', '<ol>', parsed_latex)
        parsed_latex = re.sub(r'\\end{enumerate}', '</ol>', parsed_latex)
        parsed_latex = re.sub(r'\\item', '<li>', parsed_latex)

        # Change bold and italic
        parsed_latex = re.sub(r'\\textbf{[^}]*}', self.bold_converter, parsed_latex)
        parsed_latex = re.sub(r'{\\bf[^}]*}', self.bold_converter, parsed_latex)
        parsed_latex = re.sub(r'\\textit{[^}]*}', self.italic_converter, parsed_latex)
        parsed_latex = re.sub(r'{\\it[^}]*}', self.italic_converter, parsed_latex)

        return parsed_latex
