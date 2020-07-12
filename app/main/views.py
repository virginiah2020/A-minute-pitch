from flask import render_template, request, redirect, url_for, abort
from . import main
from ..models import User,Pitch,Comments,PitchCategory,Votes
from .. import db
from . forms import PitchForm, CommentForm, CategoryForm
from flask_login import login_required,current_user

#display categories on the landing page
@main.route('/')
def index():
    """ View root page function that returns index page """

    category = PitchCategory.get_categories()

    title = 'Home- Welcome'
    return render_template('index.html', title = title, categories=category)
@main.route('/category/new-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def new_pitch(id):
    ''' Function to check Pitches form and fetch data from the fields '''
    form = PitchForm()
    category = PitchCategory.query.filter_by(id=id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        content = form.content.data
        new_pitch= Pitch(content=content,category_id= category.id,user_id=current_user.id)
        new_pitch.save_pitch()
        return redirect(url_for('.category', id=category.id))

    return render_template('new_pitch.html', pitch_form=form, category=category)

@main.route('/categories/<int:id>')
def category(id):
    category = PitchCategory.query.get(id)
    if category is None:
        abort(404)

    pitches=Pitch.get_pitches(id)
    return render_template('category.html', pitches=pitches, category=category)

# @main.route('/add/category', methods=['GET','POST'])
# @login_required
# def new_category():
#     '''
#     View new group route function that returns a page with a form to create a category
#     '''
#     form = CategoryForm()

#     if form.validate_on_submit():
#         name = form.name.data
#         new_category = PitchCategory(name=name)
#         new_category.save_category()

#         return redirect(url_for('.index'))

#     title = 'New category'
#     return render_template('new_category.html', category_form = form,title=title)
@main.route('/view-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def view_pitch(id):
    '''
    Function the returns a single pitch for comment to be added
    '''
    print(id)
    pitches = Pitch.query.get(id)
    # pitches = Pitch.query.filter_by(id=id).all()

    if pitches is None:
        abort(404)
    #
    comment = Comments.get_comments(id)
    return render_template('view-pitch.html', pitches=pitches, comment=comment, category_id=id)


#adding a comment
@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    ''' function to post comments '''
    form = CommentForm()
    title = 'post comment'
    pitches = Pitch.query.filter_by(id=id).first()
    
    if pitches is None:
         abort(404)

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comments(opinion=opinion, user_id=current_user.id, pitches_id=pitches.id)
        new_comment.save_comment()
        return redirect(url_for('.view_pitch', id=pitches.id))

    return render_template('post_comment.html', comment_form=form, title=title)

@main.route('/pitch/upvote/<int:id>')
@login_required
def upvote(id):
    '''
    View function that add one to the vote_number column in the votes table
    '''
    pitch_id = Pitch.query.filter_by(id=id).first()

    if pitch_id is None:
         abort(404)

    new_vote = Votes(vote=int(1), user_id=current_user.id, pitches_id=pitch_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_pitch', id=id))

@main.route('/pitch/downvote/<int:id>')
@login_required
def downvote(id):

    '''
    View function that add one to the vote_number column in the votes table
    '''
    pitch_id = Pitch.query.filter_by(id=id).first()

    if pitch_id is None:
         abort(404)

    new_vote = Votes(vote=int(2), user_id=current_user.id, pitches_id=pitch_id.id)
    new_vote.save_vote()
    return redirect(url_for('.view_pitch', id=id))

@main.route('/pitch/downvote/<int:id>')
def vote_count(id):
    '''
    View function to return the total vote count per pitch
    '''
    votes = Votes.query.filter_by(user_id=user_id, line_id=line_id).all()

    total_votes = votes.count()

    return total_votes
