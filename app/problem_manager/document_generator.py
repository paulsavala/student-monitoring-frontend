from flask import current_app
import os


class LatexDocument():
    def __init__(self, template, title, course=None, problem_latex=[]):
        self.template = template
        self.title = title
        self.course = course
        self.problem_latex = problem_latex

    def _load_template(self):
        template_file = open(os.path.join(current_app.config['TEMPLATE_DIR'], self.template), mode='r')
        template = template_file.read()
        template_file.close()
        return template

    def generate_latex(self):
        pass
