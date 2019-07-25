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
        inside = re.search(r'(?<={\\bf\s)[^}]*(?=})', match_object.group(0))
        if inside is not None:
            return r'<b>{}</b>'.format(inside.group(0))
        return ''


    def italic_converter(self, match_object):
        inside = re.search(r'(?<=\\textit{)[^}]*(?=})', match_object.group(0))
        if inside is not None:
            return r'<em>{}</em>'.format(inside.group(0))
        inside = re.search(r'(?<={\\it\s)[^}]*(?=})', match_object.group(0))
        if inside is not None:
            return r'<em>{}</em>'.format(inside.group(0))
        return ''


    def space_converter(self, match_object):
        inside = re.search(r'\\vspace{\s*(\d+)\s*cm\s*}', match_object.group(0))
        if inside is not None:
            return r'<div style="margin-bottom: {}cm"></div>'.format(inside.group(1))
        inside = re.search(r'\\hspace{\s*(\d+)\s*cm\s*}', match_object.group(0))
        if inside is not None:
            return r'<div style="margin-right: {}cm"></div>'.format(inside.group(1))


    # todo: Handle escaped money signs \$ such as \$3.20
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

        # Strip \hspace and \vspace (they're still there in raw_latex)
        parsed_latex = re.sub(r'\\vspace{\s*\d+\s*cm\s*}', r'<br>', parsed_latex)
        parsed_latex = re.sub(r'\\hspace{\s*\d+\s*cm\s*}', r'<br>', parsed_latex)

        # Strip \newpage
        parsed_latex = re.sub(r'\\newpage', '', parsed_latex)

        # Change carriage return, double backslash, and empty lines to <br>, <br> and <br><br>, respectively
        parsed_latex = re.sub(r'\r', r'<br>', parsed_latex)
        parsed_latex = re.sub(r'\\\\(?=[\\\s+])', r'<br>', parsed_latex)
        parsed_latex = re.sub(r'^\s*$', r'<br><br>', parsed_latex)


        return parsed_latex
