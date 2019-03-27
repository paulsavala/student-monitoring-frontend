from flask import render_template, flash, redirect, url_for, request, current_app, \
                    session, jsonify
from flask_login import current_user, login_required
from flask_babel import _
from app import db
from app.problem_manager.forms import ProblemForm, ProblemExplorerForm
from app.models import Problem, Course
from app.problem_manager import bp
from common.utils import empty_str_to_null
from sqlalchemy import and_
from app.problem_manager.parser import LatexParser


# todo: Is this else statement actually required? Won't those get filled from original_problem?
@bp.route('/edit_problem/<problem_id>', methods=['GET', 'POST'])
@login_required
def edit_problem(problem_id):
    courses = Course.query.order_by(Course.number.asc())
    problem = Problem.query.filter_by(id=problem_id).first_or_404()
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
        problem.course = form.course.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.problem.data = problem.latex
        form.notes.data = problem.notes
        form.solution.data = problem.solution

    # Only populate the form with data after checking for a submit. Otherwise, your submit will have data overwritten.
    form = ProblemForm(original_problem=problem, courses=courses)
    return render_template('problem_manager/edit_problem.html', form=form)


# todo: Test if the int casts are really needed
@bp.route('/delete_problem/<problem_id>', methods=['GET', 'POST'])
@login_required
def delete_problem(problem_id):
    problem = Problem.query.filter_by(id=problem_id).first_or_404()
    if int(problem.user_id) != int(current_user.get_id()):
        flash(_('You may only delete your own problems.'))
        return redirect(url_for('main.index'))
    Problem.query.filter_by(id=problem_id).delete()
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
        print(selected_author_ids)
        if selected_author_ids != [] and (0 not in selected_author_ids):
            filter_group.append(Problem.user_id.in_(selected_author_ids))
        if explorer_form.has_solution.data == True:
            filter_group.append(Problem.solution != None)
        if explorer_form.has_notes.data == True:
            filter_group.append(Problem.notes != None)
        problems = Problem.query.filter(and_(*filter_group)).order_by(Problem.created_ts.desc())
    return render_template('problem_manager/explore.html', title=_('Explore'),
                           explorer_form=explorer_form, problems=problems)


# todo: Remove static link to user's problems with problems user added to document
@bp.route('/documents', methods=['GET', 'POST'])
@login_required
def documents():
    page = request.args.get('page', 1, type=int)
    problems = Problem.query.filter_by(user_id=current_user.id)
    return render_template('problem_manager/documents.html', title=_('Documents'),
                           problems=problems)


# ---- STAR FUNCTIONS -------
@bp.route('/add_to_starred')
@login_required
def toggle_starred():
    problem_id = int(request.args.get('button_id').split('-')[-1])
    problem = Problem.query.filter_by(id=problem_id).first()
    if current_user.is_starred(problem):
        current_user.remove_star(problem)
    else:
        current_user.add_star(problem)
    db.session.commit()
    print(f'starred: {problem_id}')
    return jsonify({'problem_id': problem_id})


@bp.route('/remove_from_stared')
@login_required
def remove_from_starred(problem_id):
    problem_id = int(request.args.get('problem_id').split('-')[-1])
    problem = Problem.query.filter_by(id=problem_id).first()
    current_user.remove_star(problem)
    db.session.commit()
    print(f'removed from starred: {problem_id}')
    return jsonify({'problem_id': problem_id})


# ---- DOCUMENT FUNCTIONS -------
@bp.route('/view_documents', methods=['GET'])
@login_required
def view_documents():
    problems = Problem.query.filter(Problem.id.in_(session.get('document_problems', [])))
    return render_template('problem_manager/documents.html', problems=problems)


@bp.route('/add_to_document')
@login_required
def add_to_document():
    problem_id = int(request.args.get('button_id').split('-')[-1])
    if 'document_problems' not in session:
        session['document_problems'] = [problem_id]
    elif problem_id in session['document_problems']:
        session['document_problems'].remove(problem_id)
    else:
        session['document_problems'].append(problem_id)
    session['document_problem_count'] = len(session['document_problems'])
    return jsonify({'document_count': session['document_problem_count']})


@bp.route('/remove_from_document/<problem_id>', methods=['GET', 'POST'])
@login_required
def remove_from_document(problem_id):
    if problem_id in session.get('document_problems', []):
        session['document_problems'].remove(problem_id)
    session['document_problem_count'] = len(session['document_problems'])
    return redirect(url_for('main.index'))


@bp.route('/clear_document')
@login_required
def clear_document():
    session['document_problems'] = []
    session['document_problem_count'] = 0
    return jsonify({'document_count': session['document_problem_count']})


# ------ TEST DATA LOADING --------
@bp.route('/load_test_data')
@login_required
def load_test_data():
    from scripts import load_test_data
    flash(_('Test data loaded'))
    return redirect(url_for('main.index'))
