from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, ProblemForm, SearchForm, MessageForm
from app.models import User, Problem, Message, Notification, Course
from app.translate import translate
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    courses = Course.query.order_by(Course.number.asc())
    form = ProblemForm(courses=courses)
    if form.validate_on_submit():
        language = guess_language(form.problem.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        problem = Problem(body=form.problem.data, notes=form.notes.data, solution=form.solution.data,
                          author=current_user, course=form.course.data, language=language)
        db.session.add(problem)
        db.session.commit()
        flash(_('Your problem is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    problems = current_user.followed_problems().paginate(
        page, current_app.config['PROBLEMS_PER_PAGE'], False)
    next_url = url_for('main.index', page=problems.next_num) \
        if problems.has_next else None
    prev_url = url_for('main.index', page=problems.prev_num) \
        if problems.has_prev else None
    return render_template('index.html', title=_('Home'), form=form,
                           problems=problems.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    problems = Problem.query.order_by(Problem.timestamp.desc()).paginate(
        page, current_app.config['PROBLEMS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=problems.next_num) \
        if problems.has_next else None
    prev_url = url_for('main.explore', page=problems.prev_num) \
        if problems.has_prev else None
    return render_template('index.html', title=_('Explore'),
                           problems=problems.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    problems = user.problems.order_by(Problem.timestamp.desc()).paginate(
        page, current_app.config['PROBLEMS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=problems.next_num) if problems.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=problems.prev_num) if problems.has_prev else None
    return render_template('user.html', user=user, problems=problems.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


# todo: Only allow editing if the problem's author is the current_user
# todo: Fix "CSRF is missing" issue
@bp.route('/edit_problem/<problem_id>', methods=['GET', 'POST'])
@login_required
def edit_problem(problem_id):
    courses = Course.query.order_by(Course.number.asc())
    problem = Problem.query.filter_by(id=problem_id).first_or_404()
    form = ProblemForm(original_problem=problem, courses=courses)
    if form.validate_on_submit():
        problem.body = form.problem.data
        problem.notes = form.notes.data
        problem.solution = form.solution.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.problem.data = problem.body
        form.notes.data = problem.notes
        form.solution.data = problem.solution
    return render_template('edit_problem.html', form=form)


# todo: Only allow deleting if the problem's author is the current_user
@bp.route('/delete_problem/<problem_id>', methods=['GET', 'POST'])
@login_required
def delete_problem(problem_id):
    Problem.query.filter_by(id=problem_id).delete()
    db.session.commit()
    flash(_('Your problem has been deleted.'))
    return redirect(url_for('main.index'))


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    problems, total = Problem.search(g.search_form.q.data, page,
                               current_app.config['PROBLEMS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['PROBLEMS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), problems=problems,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['PROBLEMS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
