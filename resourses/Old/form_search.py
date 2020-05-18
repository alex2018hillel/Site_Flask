import Post as Post
import bp as bp
from flask import request, redirect, url_for, render_template
#
# class SearchForm(FlaskForm):
#     q = StringField(_l('Search'), validators=[DataRequired()])
#
#     def __init__(self, *args, **kwargs):
#         if 'formdata' not in kwargs:
#             kwargs['formdata'] = request.args
#         if 'csrf_enabled' not in kwargs:
#             kwargs['csrf_enabled'] = False
#         super(SearchForm, self).__init__(*args, **kwargs)

from flask import g
# from app.main.forms import SearchForm
#
# @bp.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()
#         g.search_form = SearchForm()
#     g.locale = str(get_locale())

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)