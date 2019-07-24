from flask import current_app
from app import db
from app.models import Subject, Course, Class, Institution, User

import os

with current_app.app_context():
    current_app.logger.info('Bootstrapping database...')

    # Truncate the course and problem tables
    db.session.query(Course).delete()
    db.session.query(Class).delete()
    db.session.query(Subject).delete()
    db.session.query(Institution).delete()

    # Load some institutions
    st_edwards = Institution(name="Saint Edward's University", city="Austin", state="TX", type="COLLEGE")
    colorado_mesa = Institution(name="Colorado Mesa University", city="Grand Junction", state="CO", type="COLLEGE")

    institutions = [st_edwards, colorado_mesa]
    for college in institutions:
        db.session.add(college)
        current_app.logger.info(f'Created {college.name}')

    # Create the initial admin user if necessary
    admin_user = User.query.filter_by(admin=True).first()

    if admin_user is None and os.environ.get('WERKZEUG_RUN_MAIN', 'false') == 'false':
        current_app.logger.info('Creating initial admin user')

        admin_user = User(
            username = os.environ['ADMIN_USERNAME'],
            email = os.environ['ADMIN_EMAIL'],
            first_name = os.environ['ADMIN_FIRST_NAME'],
            last_name = os.environ['ADMIN_LAST_NAME'],
            full_name = os.environ['ADMIN_FULL_NAME'],
            institution_id = os.environ['ADMIN_INSTITUTION_ID'],
            admin = True
        )
        admin_user.set_password(os.environ['ADMIN_PASSWORD'])

        db.session.add(st_edwards)
        db.session.add(admin_user)

        current_app.logger.info('Admin user created')
    else:
        current_app.logger.info('Admin user already exists')

    # Load some subjects
    math = Subject(title='Mathematics', short_title='MATH')
    stats = Subject(title='Statistics', short_title='STATS')
    csci = Subject(title='Computer Science', short_title='CS')

    subjects = [math, stats, csci]
    for subject in subjects:
        db.session.add(subject)
        current_app.logger.info(f'Created {subject.title}')


    # Load some courses
    calc1 = Course(title='Calculus I', subject_id=1)  # 1
    calc2 = Course(title='Calculus II', subject_id=1)  # 2
    calc3 = Course(title='Calculus III', subject_id=1)  # 3
    linalg = Course(title='Linear Algebra', subject_id=1)  # 4
    lower_stats_math = Course(title='Lower-division Statistics', subject_id=1)  # 5
    upper_stats_math = Course(title='Upper-division Statistics', subject_id=1)  # 6
    lower_stats_stats = Course(title='Lower-division Statistics', subject_id=2)  # 7
    upper_stats_stats = Course(title='Upper-division Statistics', subject_id=2)  # 8
    analysis1 = Course(title='Real Analysis I', subject_id=1)  # 9
    analysis2 = Course(title='Real Analysis II', subject_id=1)  # 10
    absalg1 = Course(title='Abstract Algebra I', subject_id=1)  # 11
    absalg2 = Course(title='Abstract Algebra II', subject_id=1)  # 12
    complexan1 = Course(title='Complex Analysis I', subject_id=1)  # 13
    complexan2 = Course(title='Complex Analysis II', subject_id=1)  # 14
    geometry1 = Course(title='Geometry I', subject_id=1)  # 15
    geometry2 = Course(title='Geometry II', subject_id=1)  # 16
    history = Course(title='History of Math', subject_id=1)  # 17
    topology = Course(title='Topology', subject_id=1)  # 18
    basicalg = Course(title='Basic Algebra', subject_id=1)  # 19
    precalc = Course(title='Precalculus', subject_id=1)  # 20
    introprog = Course(title='Introduction to Programming', subject_id=3)  # 21

    courses = [calc1, calc2, calc3, linalg, lower_stats_math, upper_stats_math, lower_stats_stats, upper_stats_stats,
              analysis1, analysis2, absalg1, absalg2, complexan1, complexan2, geometry1, geometry2, history, topology,
              basicalg, precalc, introprog]
    for course in courses:
        db.session.add(course)
        current_app.logger.info(f'Created {course.title}')


    # Load some classes
        # St Edward's
    sted_calc1 = Class(title="CALCULUS I", subject_id=1, course_id=1, number="2413", institution_id=1, description="A first course in calculus, covering limits and continuity, derivatives, linear approximations, applications including graphs and extrema, definition and properties of the integral and the Fundamental Theorem of Calculus, and antidifferentiation. This course presents a threefold approach to calculus: numerical, graphical, and analytical techniques are all emphasized. The fourth credit hour is devoted to active-learning and inquiry based activities to reinforce course material. Prerequisite: MATH 2312 with a grade of C or better. Fall, Spring.", active=True)
    sted_calc2 = Class(title="CALCULUS II", subject_id=1, course_id=2, number="2414", institution_id=1, description="A continuation of MATH 2413. Topics include applications of the integral, additional techniques of anti-differentiation, improper integrals, introduction to differential equations, Taylor polynomials and Taylor series, and the Mean Value Theorem. Prerequisites: MATH 2413 with a grade of C or better. Fall, Spring", active=True)
    sted_calc3 = Class(title="ADVANCED CALCULUS", subject_id=1, course_id=3, number="3316", institution_id=1, description="A rigorous treatment of the real-number system; of real sequences; and of limits, continuity and derivatives of functions of one real variable. Prerequisite: MATH 2414 and MATH 3318 with a grade of C or better or consent of instructor. Fall.", active=True)
    sted_lin_alg = Class(title="LINEAR ALGEBRA", subject_id=1, course_id=4, number="3305", institution_id=1, description="Systems of equations, determinants, algebra and geometry of finite-dimensional linear vector spaces, linear transformations, the algebra of matrices, and the theory of eigenvalues and eigenvectors. Prerequisite: MATH 2413. Spring.", active=True)
    sted_stats = Class(title="APPLIED STATISTICS", subject_id=1, course_id=5, number="3320", institution_id=1, description="A first course in applied statistics emphasizing statistical thinking using real and computer-generated data. Topics include data description, hypothesis testing using z-test, t-test, chi‑squared, linear regression and ANOVA. MINITAB software is used extensively. Prerequisite: MATH 2413. Fall, Spring, Summer.", active=True)
        # Colorado Mesa
    cm_calc1 = Class(title="CALCULUS I", subject_id=1, course_id=1, number="250", institution_id=2, description="A first course in calculus, covering limits and continuity, derivatives, linear approximations, applications including graphs and extrema, definition and properties of the integral and the Fundamental Theorem of Calculus, and antidifferentiation. This course presents a threefold approach to calculus: numerical, graphical, and analytical techniques are all emphasized. The fourth credit hour is devoted to active-learning and inquiry based activities to reinforce course material. Prerequisite: MATH 2312 with a grade of C or better. Fall, Spring.", active=True)
    cm_calc2 = Class(title="CALCULUS II", subject_id=1, course_id=2, number="251", institution_id=2, description="A continuation of MATH 2413. Topics include applications of the integral, additional techniques of anti-differentiation, improper integrals, introduction to differential equations, Taylor polynomials and Taylor series, and the Mean Value Theorem. Prerequisites: MATH 2413 with a grade of C or better. Fall, Spring", active=True)
    cm_calc3 = Class(title="CALCULUS III", subject_id=1, course_id=3, number="301", institution_id=2, description="A rigorous treatment of the real-number system; of real sequences; and of limits, continuity and derivatives of functions of one real variable. Prerequisite: MATH 2414 and MATH 3318 with a grade of C or better or consent of instructor. Fall.", active=True)
    cm_lin_alg = Class(title="LINEAR ALGEBRA", subject_id=1, course_id=4, number="345", institution_id=2, description="Systems of equations, determinants, algebra and geometry of finite-dimensional linear vector spaces, linear transformations, the algebra of matrices, and the theory of eigenvalues and eigenvectors. Prerequisite: MATH 2413. Spring.", active=True)
    cm_stats = Class(title="STATISTICS AND PROBABILITY", subject_id=1, course_id=5, number="312", institution_id=2, description="A first course in applied statistics emphasizing statistical thinking using real and computer-generated data. Classs include data description, hypothesis testing using z-test, t-test, chi‑squared, linear regression and ANOVA. MINITAB software is used extensively. Prerequisite: MATH 2413. Fall, Spring, Summer.", active=True)


    classes = [sted_calc1, sted_calc2, sted_calc3, sted_lin_alg, sted_stats,
               cm_calc1, cm_calc2, cm_calc3, cm_lin_alg, cm_stats]
    for class_name in classes:
        db.session.add(class_name)
        current_app.logger.info(f'Created {class_name.title} (Institution {class_name.institution_id})')


    # Commit changes
    db.session.commit()
    current_app.logger.info('Bootstrapping database complete')
