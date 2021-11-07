from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user
from models import get_db, User, Course, Follow, Post
from module002.forms import *
from sqlalchemy import or_, and_

module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")
db = get_db()

@module002.route('/')
@login_required
def module002_index():
    if current_user.profile in ('admin','staff','student'):
        return render_template("module002_index.html",module="module002")
    else:
        flash("Access denied!")
        return redirect(url_for('index'))



@module002.route('/post', methods=['GET','POST'])
@login_required
def module002_post():
        if current_user.profile in ('admin','staff','student'):
            follows = Follow.query.filter_by(user_id=current_user.id)
            return render_template("module002_post.html",module="module002", rows=follows)
        else:
            flash("Access denied!")
            #abort(404,description="Access denied!")
            return redirect(url_for('index'))

@module002.route('/post/<course_id>/', methods=['POST', 'GET'])
@login_required
def module002_post_course(course_id):
    form = PostForm()
    form2 = HideForm()
    course = Course.query.filter_by(id=course_id).first()
    follow = Follow.query.filter(and_(Follow.course_id==course_id,
                                              Follow.user_id==current_user.id)).first()
    if follow:
        if request.method == 'POST':
            if form.validate_on_submit():
                try:
                    newpost = Post(body=form.body.data, author_id=current_user.id, course_id=course_id, username=current_user.username )
                    db.session.add(newpost)
                    db.session.commit()
                    flash("Post created")
                    return redirect(url_for('module002.module002_post_course', course_id=course.id))
                except:
                    db.session.rollback()
                    flash("Error creating post!")
                return redirect(url_for('module002.module002_post_course', course_id=course.id))

            if form2.validate_on_submit:
                post = Post.query.filter(and_(Post.course_id==int(course_id), Post.id == int(request.form['id']))).first()
                try:
                    post.hidden = True
                    db.session.commit()
                    flash("Post hidden!")
                except:
                    db.session.rollback()
                    flash("Error hidding post!")
                return redirect(url_for('module002.module002_post_course', course_id=course.id))
        else:
            if current_user.profile in ('admin','staff','student'):
                posts = Post.query.filter_by(course_id=course_id)
                follows = Follow.query.filter_by(user_id=current_user.id)
                 #select user.username, body, timestamp from post left join user on post.author_id = user.id;
                return render_template("module002_post_especifico.html",module="module002", form=form, posts=posts, rows=follows, course=course, form2=form2)
            else:
                flash("Access denied!")
                return redirect(url_for('index'))
    else:
        flash("Access denied!")
#       abort(404,description="Access denied!")
        return redirect(url_for('index'))


@module002.route('/test')
def module002_test():
    return 'OK'
