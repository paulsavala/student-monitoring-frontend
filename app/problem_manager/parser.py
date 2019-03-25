import re

# Things to parse:
# - Change single $ to \(...\)
# - Change itemize/enumerate to ul/ol and li
# - Change bold and italic? Also change \emph and \em

class LatexParser():
    def __init__(self):
        # Counters
        self.inline_counter = 0


    def initialize_counters(self):
        self.inline_counter = 0


    def inline_converter(self, match_object):
        # Lets inline math conversion happen in alternating pairs. So that $...$ is converted to \(...\)
        if self.inline_counter == 0:
            self.inline_counter += 1
            return r'\('
        else:
            self.inline_counter = 0
            return r'\)'


    def bold_converter(self, match_object):
        inside = re.search(r'(?<=\\textbf{)[^}]*(?=})', match_object.group(0))
        if inside is not None:
            return r'<b>{}</b>'.format(inside.group(0))


    def italic_converter(self, match_object):
        print(match_object)
        inside = re.search(r'(?<=\\textit{)[^}]*(?=})', match_object.group(0))
        print(inside)
        if inside is not None:
            return r'<i>{}</i>'.format(inside.group(0))


    def parse(self, raw_latex):
        # Initialize counters
        self.initialize_counters()

        # Change $ to inline \(...\)
        raw_latex = re.sub(r'(?<![\$\\])\$(?![\$\\])', self.inline_converter, raw_latex)

        # Change itemize/enumerate to ul/ol and li to \item
        raw_latex = re.sub(r'\\begin{itemize}', '<ul>', raw_latex)
        raw_latex = re.sub(r'\\end{itemize}', '</ul>', raw_latex)
        raw_latex = re.sub(r'\\begin{enumerate}', '<ol>', raw_latex)
        raw_latex = re.sub(r'\\end{enumerate}', '</ol>', raw_latex)
        raw_latex = re.sub(r'\\item', '<li>', raw_latex)

        # Change bold and italic
        raw_latex = re.sub(r'\\textbf{[^}]*}', self.bold_converter, raw_latex)
        raw_latex = re.sub(r'\\textit{[^}]*}', self.italic_converter, raw_latex)

        return raw_latex