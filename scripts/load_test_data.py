from app import db
from app.models import Problem, Course


# Truncate the course and problem tables
db.session.query(Problem).delete()
db.session.query(Course).delete()


# Load some courses
calc1 = Course(title="CALCULUS I", subject="MATH", number="2413", description="A first course in calculus, covering limits and continuity, derivatives, linear approximations, applications including graphs and extrema, definition and properties of the integral and the Fundamental Theorem of Calculus, and antidifferentiation. This course presents a threefold approach to calculus: numerical, graphical, and analytical techniques are all emphasized. The fourth credit hour is devoted to active-learning and inquiry based activities to reinforce course material. Prerequisite: MATH 2312 with a grade of C or better. Fall, Spring.", active=True)
calc2 = Course(title="CALCULUS II", subject="MATH", number="2414", description="A continuation of MATH 2413. Topics include applications of the integral, additional techniques of anti-differentiation, improper integrals, introduction to differential equations, Taylor polynomials and Taylor series, and the Mean Value Theorem. Prerequisites: MATH 2413 with a grade of C or better. Fall, Spring", active=True)
calc3 = Course(title="ADVANCED CALCULUS", subject="MATH", number="3316", description="A rigorous treatment of the real-number system; of real sequences; and of limits, continuity and derivatives of functions of one real variable. Prerequisite: MATH 2414 and MATH 3318 with a grade of C or better or consent of instructor. Fall.", active=True)
lin_alg = Course(title="LINEAR ALGEBRA", subject="MATH", number="3305", description="Systems of equations, determinants, algebra and geometry of finite-dimensional linear vector spaces, linear transformations, the algebra of matrices, and the theory of eigenvalues and eigenvectors. Prerequisite: MATH 2413. Spring.", active=True)
stats = Course(title="APPLIED STATISTICS", subject="MATH", number="3320", description="A first course in applied statistics emphasizing statistical thinking using real and computer-generated data. Topics include data description, hypothesis testing using z-test, t-test, chi‑squared, linear regression and ANOVA. MINITAB software is used extensively. Prerequisite: MATH 2413. Fall, Spring, Summer.", active=True)

courses = [calc1, calc2, calc3, lin_alg, stats]
for course in courses:
    db.session.add(course)


# Load some problems
p1 = Problem(body="Compute the derivative of \(f(x)=x^2\)", notes="Introduction to derivatives", solution="\[f'(x)=2x\]", course=1, user_id=1, language="en")
p2 = Problem(body="Compute the integral \(\\displaystyle\\int_0^1\\frac{1}{x}dx\)", notes="A tricky definite integral", solution="DNE (or \(-\infty\)", course=1, user_id=1, language="en")
p3 = Problem(body="Some related rates problem using an image", notes="This one has an image with it, hosted in s3", solution="It's obvious", course=1, user_id=1, language="en", image='s3://problematic-data/courses/1/problems/3/images/1.png')
p4 = Problem(body="Some Calc II problem (with notes and solution as None)", notes=None, solution=None, course=2, user_id=1, language="en")
p5 = Problem(body="Some other Calc II problem (with notes and solution as empty string)", notes="", solution="", course=2, user_id=1, language="en")
p6 = Problem(body="Some Calc III problem (with notes and solution not supplied)", course=3, user_id=1, language="en")
p7 = Problem(body="Some other Calc III problem", notes="", solution="", course=4, user_id=1, language="en")
p8 = Problem(body="Some linear algegbra problem", notes="", solution="", course=4, user_id=1, language="en")
p9 = Problem(body="Some stats problem", notes="This is for stats", solution="Compute the \(z\)-score", course=5, user_id=1, language="en")
p10 = Problem(body="Some other stats problem", notes="Used on a midterm", solution="\[x=0.5\]", course=5, user_id=1, language="en")

problems = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
for problem in problems:
    db.session.add(problem)


# Commit changes
db.session.commit()
