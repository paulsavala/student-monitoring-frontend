from flask import render_template, flash, redirect, url_for, request, current_app, \
                    session, jsonify
from flask_login import current_user, login_required
from flask_babel import _
from app import db
from app.problem_manager.forms import ProblemForm, ProblemExplorerForm, DocumentForm
from app.models import Problem, Document, User, Subject, Course, Class
from app.problem_manager import bp
from common.utils import empty_str_to_null
from sqlalchemy import and_
from app.problem_manager.parser import LatexParser
from app.problem_manager.document_generator import LatexDocument


# todo: Is this else statement actually required? Won't those get filled from original_problem?
@bp.route('/edit_problem/<problem_id>', methods=['GET', 'POST'])
@login_required
def edit_problem(problem_id):
    classes = Class.query.order_by(Class.number.asc())
    problem = Problem.query.filter(Problem.id == problem_id).first_or_404()
    form = ProblemForm()
    if form.validate_on_submit():
        if int(problem.user_id) != int(current_user.get_id()):
            flash(_('You may only edit your own problems.'))
            return redirect(url_for('main.index'))
        parser = LatexParser()
        problem.latex = form.problem.data
        problem.parsed_latex = parser.parse(form.problem.data)
        problem.notes = empty_str_to_null(form.notes.data)
        problem.solution = empty_str_to_null(form.solution.data)
        problem.class_id = form.class_name.data
        class_obj = Class.query.filter(Class.id == problem.class_id)
        problem.course_id = class_obj.course_id
        problem.subject_id = class_obj.subject_id
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.problem.data = problem.latex
        form.notes.data = problem.notes
        form.solution.data = problem.solution

    # Only populate the form with data after checking for a submit. Otherwise, your submit will have data overwritten.
    form = ProblemForm(original_problem=problem, classes=classes)
    return render_template('problem_manager/edit_problem.html', form=form)


# todo: Test if the int casts are really needed
@bp.route('/delete_problem/<problem_id>', methods=['GET', 'POST'])
@login_required
def delete_problem(problem_id):
    problem = Problem.query.filter(Problem.id == problem_id).first_or_404()
    if int(problem.user_id) != int(current_user.get_id()):
        flash(_('You may only delete your own problems.'))
        return redirect(url_for('main.index'))
    Problem.query.filter(Problem.id == problem_id).delete()
    db.session.commit()
    flash(_('Your problem has been deleted.'))
    return redirect(url_for('main.index'))


# todo: Test if the int casts are really needed
@bp.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    explorer_form = ProblemExplorerForm()
    problems = []
    if explorer_form.validate_on_submit():
        selected_course_ids = [int(id) for id in explorer_form.course.data]
        filter_group = [Problem.course_id.in_(selected_course_ids)]
        selected_author_ids = [int(id) for id in explorer_form.author.data]
        if selected_author_ids != [] and (0 not in selected_author_ids):
            filter_group.append(Problem.user_id.in_(selected_author_ids))
        if explorer_form.has_solution.data == True:
            filter_group.append(Problem.solution != None)
        if explorer_form.has_notes.data == True:
            filter_group.append(Problem.notes != None)
        problems = Problem.query.filter(and_(*filter_group)).order_by(Problem.created_ts.desc())
    return render_template('problem_manager/explore.html', title=_('Explore'),
                           explorer_form=explorer_form, problems=problems)


# ---- STAR FUNCTIONS -------
# todo: Improve the "visible" handling here and for documents
@bp.route('/toggle_starred')
@login_required
def toggle_starred():
    problem_id = int(request.args.get('button_id').split('-')[-1])
    problem = Problem.query.filter_by(id=problem_id).first()
    visible = True
    if current_user.is_starred(problem):
        current_user.remove_star(problem)
        if request.referrer.split('/')[-1] == str(current_user.id):
            visible = False
    else:
        current_user.add_star(problem)
        problem.starred_count += 1
    db.session.commit()
    return jsonify(problem_id=problem_id, visible=visible)


# ---- DOCUMENT FUNCTIONS -------
@bp.route('/documents', methods=['GET', 'POST'])
@login_required
def documents():
    page = request.args.get('page', 1, type=int)
    user_documents = current_user.documents
    if user_documents.count() > 0:
        document = user_documents.first()
    else:
        document = Document(name='New Document', user_id=current_user.id)
        db.session.add(document)
    problems = document.problems
    form = DocumentForm()
    if form.validate_on_submit():
        title = form.title.data
        class_name = form.class_name.data
        problems_latex = [repr(p.latex).replace("'", '') for p in problems.all()]
        document = LatexDocument(template='simple_exam.tex', blocks={'title': title, 'class': class_name},
                                 problems_latex=problems_latex)
        latex = document.generate_latex()
        return render_template('problem_manager/render_document.html', title=_('Document'), latex=latex)
    return render_template('problem_manager/documents.html', title=_('Documents'),
                           problems=problems, form=form)


@bp.route('/toggle_to_document')
@login_required
def toggle_to_document():
    problem_id = int(request.args.get('button_id').split('-')[-1])
    problem = Problem.query.filter(Problem.id == problem_id).first()
    user_documents = current_user.documents
    visible = True
    if user_documents.count() > 0:
        document = user_documents.first()
    else:
        document = Document(name='New Document', user_id=current_user.id)
        db.session.add(document)
    if document.has_problem(problem):
        document.remove_problem(problem)
        if request.referrer.split('/')[-1] == 'documents':
            visible=False
    else:
        document.add_problem(problem)
        problem.starred_count += 1
    db.session.commit()
    return jsonify(problem_id=problem_id, visible=visible)


@bp.route('/clear_document', methods=['GET', 'POST'])
@login_required
def clear_document():
    document = Document.query.filter(Document.user_id == current_user.id).first_or_404()
    document.clear_document()
    db.session.commit()
    return redirect(url_for('problem_manager.documents'))


# ------ TEST DATA LOADING --------
@bp.route('/load_test_data')
@login_required
def load_test_data():
    from scripts import load_test_data
    flash(_('Test data loaded'))
    return redirect(url_for('main.index'))
