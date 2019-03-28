from flask import current_app
import re
import os


class LatexDocument:
    def __init__(self, template, blocks={}, problems_latex=[]):
        self.template = template
        self.blocks = blocks
        self.problems_latex = problems_latex

    def _load_template(self):
        with open(os.path.join(current_app.config['TEMPLATE_DIR'], self.template), 'r') as f:
            template = f.read()
        return template

    def parse_blocks(self, document):
        for block in self.blocks:
            document = re.sub(r'<<\s*{}\s*>>'.format(block), self.blocks[block], document)

        wrapped_problems = [r'{{\\bf Problem {0}:}} {1}'.format(i, problem_latex)
                            for i, problem_latex in enumerate(self.problems_latex)]

        problem_block_latex = r'\n\\vspace{1cm}\\newline\n\n'.join(wrapped_problems)
        document = re.sub(r'<<\s*problem_block\s*>>', problem_block_latex, document)
        return document

    def generate_latex(self):
        template_str = self._load_template()
        document = self.parse_blocks(template_str)
        return document