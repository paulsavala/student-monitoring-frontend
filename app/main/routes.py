from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, session
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import EditProfileForm, SearchForm, MessageForm
from app.problem_manager.forms import ProblemForm
from app.models import User, Problem, Message, Notification, Class
from app.translate import translate
from app.main import bp
from app.problem_manager.parser import LatexParser
from app.utils import utils


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        # g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    classes = Class.query.order_by(Class.number.asc())
    form = ProblemForm(classes=classes)
    if form.validate_on_submit():
        parser = LatexParser()
        class_obj = Class.query.filter(Class.id == form.class_name.data).first_or_404()
        problem = Problem(latex=form.problem.data,
                          parsed_latex=parser.parse(form.problem.data),
                          notes=parser.parse(form.notes.data),
                          solution=parser.parse(form.solution.data),
                          user_id=current_user.id,
                          course_id=class_obj.course_id,
                          class_id=form.class_name.data,
                          )
        db.session.add(problem)
        db.session.commit()
        flash(_('Your problem is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    problems = current_user.problems.order_by(Problem.created_ts.desc()).paginate(
        page, current_app.config['PROBLEMS_PER_PAGE'], False)
    next_url = url_for('main.index', page=problems.next_num) \
        if problems.has_next else None
    prev_url = url_for('main.index', page=problems.prev_num) \
        if problems.has_prev else None
    return render_template('index.html', title=_('Home'), form=form,
                           problems=problems, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<user_id>')
@login_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    page = request.args.get('page', 1, type=int)

    user_problems = user.problems.filter_by(user_id=user_id).order_by(Problem.created_ts.desc()).paginate(
        page, current_app.config['PROBLEMS_PER_PAGE'], False)
    next_url = url_for('main.user', user_id=user_id,
                       page=user_problems.next_num) if user_problems.has_next else None
    prev_url = url_for('main.user', user_id=user_id,
                       page=user_problems.prev_num) if user_problems.has_prev else None

    # Starred problems
    starred_problems = current_user.starred_problems().order_by(Problem.created_ts.desc()).paginate(
        page, current_app.config['PROBLEMS_PER_PAGE'], False)
    # next_url = url_for('main.user', user_id=user_id,
    #                    page=starred_problems.next_num) if starred_problems.has_next else None
    # prev_url = url_for('main.user', user_id=user_id,
    #                    page=starred_problems.prev_num) if starred_problems.has_prev else None
    return render_template('user.html', user=user, user_problems=user_problems,
                           starred_problems=starred_problems,
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
        current_user.title = form.title.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.title.data = current_user.title
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', user_id=user.id))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', user_id=user.id))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', user_id=user.id))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('main.user', user_id=user.id))


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
