from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flask_babel import _
from app import db
from app.problem_manager.forms import ProblemForm
from app.models import Problem, Course
from app.problem_manager import bp


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
        problem.body = form.problem.data
        problem.notes = form.notes.data
        problem.solution = form.solution.data
        problem.course = form.course.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.problem.data = problem.body
        form.notes.data = problem.notes
        form.solution.data = problem.solution

    # Only populate the form with data after checking for a submit. Otherwise, your submit will have data overwritten.
    form = ProblemForm(original_problem=problem, courses=courses)
    return render_template('problem_manager/edit_problem.html', form=form)


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