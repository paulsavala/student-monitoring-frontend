from app import db
from app.models import Problem, Course, Institution
from app.problem_manager.parser import LatexParser


# Truncate the course and problem tables
db.session.query(Problem).delete()
db.session.query(Course).delete()
db.session.query(Institution).delete()


# Load some institutions
st_edwards = Institution(name="Saint Edward's University", city="Austin", state="TX", type="COLLEGE")
colorado_mesa = Institution(name="COLORADO MESA UNIVERSITY", city="Grand Junction", state="co", type="COLLEGE")

institutions = [st_edwards, colorado_mesa]
for college in institutions:
    db.session.add(college)


# Load some courses
    # St Edward's
sted_calc1 = Course(title="CALCULUS I", subject="MATH", number="2413", institution_id=1, description="A first course in calculus, covering limits and continuity, derivatives, linear approximations, applications including graphs and extrema, definition and properties of the integral and the Fundamental Theorem of Calculus, and antidifferentiation. This course presents a threefold approach to calculus: numerical, graphical, and analytical techniques are all emphasized. The fourth credit hour is devoted to active-learning and inquiry based activities to reinforce course material. Prerequisite: MATH 2312 with a grade of C or better. Fall, Spring.", active=True)
sted_calc2 = Course(title="CALCULUS II", subject="MATH", number="2414", institution_id=1, description="A continuation of MATH 2413. Topics include applications of the integral, additional techniques of anti-differentiation, improper integrals, introduction to differential equations, Taylor polynomials and Taylor series, and the Mean Value Theorem. Prerequisites: MATH 2413 with a grade of C or better. Fall, Spring", active=True)
sted_calc3 = Course(title="ADVANCED CALCULUS", subject="MATH", number="3316", institution_id=1, description="A rigorous treatment of the real-number system; of real sequences; and of limits, continuity and derivatives of functions of one real variable. Prerequisite: MATH 2414 and MATH 3318 with a grade of C or better or consent of instructor. Fall.", active=True)
sted_lin_alg = Course(title="LINEAR ALGEBRA", subject="MATH", number="3305", institution_id=1, description="Systems of equations, determinants, algebra and geometry of finite-dimensional linear vector spaces, linear transformations, the algebra of matrices, and the theory of eigenvalues and eigenvectors. Prerequisite: MATH 2413. Spring.", active=True)
sted_stats = Course(title="APPLIED STATISTICS", subject="MATH", number="3320", institution_id=1, description="A first course in applied statistics emphasizing statistical thinking using real and computer-generated data. Topics include data description, hypothesis testing using z-test, t-test, chi‑squared, linear regression and ANOVA. MINITAB software is used extensively. Prerequisite: MATH 2413. Fall, Spring, Summer.", active=True)
    # Colorado Mesa
cm_calc1 = Course(title="CALCULUS I", subject="MATH", number="251", institution_id=2, description="A first course in calculus, covering limits and continuity, derivatives, linear approximations, applications including graphs and extrema, definition and properties of the integral and the Fundamental Theorem of Calculus, and antidifferentiation. This course presents a threefold approach to calculus: numerical, graphical, and analytical techniques are all emphasized. The fourth credit hour is devoted to active-learning and inquiry based activities to reinforce course material. Prerequisite: MATH 2312 with a grade of C or better. Fall, Spring.", active=True)
cm_calc2 = Course(title="CALCULUS II", subject="MATH", number="250", institution_id=2, description="A continuation of MATH 2413. Topics include applications of the integral, additional techniques of anti-differentiation, improper integrals, introduction to differential equations, Taylor polynomials and Taylor series, and the Mean Value Theorem. Prerequisites: MATH 2413 with a grade of C or better. Fall, Spring", active=True)
cm_calc3 = Course(title="CALCULUS III", subject="MATH", number="301", institution_id=2, description="A rigorous treatment of the real-number system; of real sequences; and of limits, continuity and derivatives of functions of one real variable. Prerequisite: MATH 2414 and MATH 3318 with a grade of C or better or consent of instructor. Fall.", active=True)
cm_lin_alg = Course(title="LINEAR ALGEBRA", subject="MATH", number="345", institution_id=2, description="Systems of equations, determinants, algebra and geometry of finite-dimensional linear vector spaces, linear transformations, the algebra of matrices, and the theory of eigenvalues and eigenvectors. Prerequisite: MATH 2413. Spring.", active=True)
cm_stats = Course(title="STATISTICS AND PROBABILITY", subject="MATH", number="312", institution_id=2, description="A first course in applied statistics emphasizing statistical thinking using real and computer-generated data. Topics include data description, hypothesis testing using z-test, t-test, chi‑squared, linear regression and ANOVA. MINITAB software is used extensively. Prerequisite: MATH 2413. Fall, Spring, Summer.", active=True)


courses = [sted_calc1, sted_calc2, sted_calc3, sted_lin_alg, sted_stats,
           cm_calc1, cm_calc2, cm_calc3, cm_lin_alg, cm_stats]
for course in courses:
    db.session.add(course)


# Load some problems
parser = LatexParser()

p1 = Problem(latex=r"Compute the derivative of \(f(x)=x^2\)",
            parsed_latex=parser.parse(r"Compute the derivative of \(f(x)=x^2\)"),
            notes="Introduction to derivatives",
            solution=r"\[f'(x)=2x\]",
            course_id=1,
            user_id=1)
p2 = Problem(latex=r"Compute the integral $\displaystyle\int_0^1\frac{1}{x}dx$ (using dollar signs for math mode)",
            parsed_latex=parser.parse(r"Compute the integral $\displaystyle\int_0^1\frac{1}{x}dx$ (using dollar signs for math mode)"),
            notes="A tricky definite integral",
            solution=r"DNE (or \(-\infty\))",
            course_id=6,
            user_id=1)
p3 = Problem(latex="Some related rates problem using an image (not yet)",
            parsed_latex=parser.parse("Some related rates problem using an image (not yet)"),
            notes="This one has an image with it, hosted in s3",
            solution="It's obvious",
            course_id=1,
            user_id=1,
            image='s3://problematic-data/courses/1/problems/3/images/1.png')
p4 = Problem(latex="Some Calc II problem (with notes and solution as None)",
            parsed_latex=parser.parse("Some Calc II problem (with notes and solution as None)"),
            notes=None,
            solution=None,
            course_id=2,
            user_id=1)
p5 = Problem(latex="Some other Calc II problem (with notes and solution as empty string)",
            parsed_latex=parser.parse("Some other Calc II problem (with notes and solution as empty string)"),
            notes="",
            solution="",
            course_id=7,
            user_id=1)
p6 = Problem(latex=r"""Some Calc III problem (with notes and solution not supplied) and some lists:
                    \begin{itemize}
                        \item Item 1
                        \item Item 2
                    \end{itemize}
                    How about an enumerate?
                    \begin{enumerate}
                        \item Item 1
                        \item Item 2
                    \end{enumerate}""",
            parsed_latex=parser.parse(r"""Some Calc III problem (with notes and solution not supplied) and some lists:
                                \begin{itemize}
                                    \item Item 1
                                    \item Item 2
                                \end{itemize}
                                How about an enumerate?
                                \begin{enumerate}
                                    \item Item 1
                                    \item Item 2
                                \end{enumerate}"""),
            course_id=3,
            user_id=1)
p7 = Problem(latex=r"\begin{align} f(x)&=x^2 \\ \Rightarrow f'(x)&=2x \end{align}",
            parsed_latex=parser.parse(r"\begin{align} f(x)&=x^2 \\ \Rightarrow f'(x)&=2x \end{align}"),
            solution="Just pretend like it's one-dimensional and do what you would normally do",
            course_id=4,
            user_id=1)
p8 = Problem(latex=r"""$$ \begin{pmatrix}
                    a & b \\
                    c & d
                    \end{pmatrix} $$""",
            parsed_latex=parser.parse(r"""$$ \begin{pmatrix}
                                a & b \\
                                c & d
                                \end{pmatrix} $$"""),
            notes="Please don't let it be row reduction...",
            course_id=9,
            user_id=1)
p9 = Problem(latex=r"\textbf{This is bold}, {\bf as is this}",
            parsed_latex=parser.parse(r"\textbf{This is bold}, {\bf as is this}"),
            notes="This is for stats",
            solution="Compute the \(z\)-score",
            course_id=5,
            user_id=1)
p10 = Problem(latex=r"\textit{This is italic} and this is not. This $ is a normal money sign, and this \$ one is escaped.",
            parsed_latex=parser.parse(r"\textit{This is italic} and this is not. This $ is a normal money sign, and this \$ one is escaped."),
            notes="Used on a midterm",
            solution="\[x=0.5\]",
            course_id=5,
            user_id=1)

problems = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
for problem in problems:
    db.session.add(problem)



# Commit changes
db.session.commit()
