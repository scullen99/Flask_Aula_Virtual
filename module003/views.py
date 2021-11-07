from flask import Blueprint, render_template, send_file
from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, Response
from flask_login import login_required, current_user
from models import get_db, User, Course, Follow, Post, Assignment, Entrega
from sqlalchemy import or_, and_
from module003.forms import *
import datetime
from werkzeug.utils import secure_filename
from werkzeug import FileWrapper
from io import BytesIO

module003 = Blueprint("module003", __name__,static_folder="static",template_folder="templates")
db = get_db()

@module003.route('/')
@login_required
def module003_index():
        if current_user.profile in ('admin','staff','student'):
            follows = Follow.query.filter_by(user_id=current_user.id)
            return render_template("module003_assignment.html",module="module003", rows=follows)
        else:
            flash("Access denied!")
            #abort(404,description="Access denied!")
            return redirect(url_for('index'))


@module003.route('/<course_id>/', methods=['POST', 'GET'])
@login_required
def module003_assignment_course(course_id):
    form = AssigmentForm()
    course = Course.query.filter_by(id=course_id).first()
    follow = Follow.query.filter(and_(Follow.course_id==course_id,
                                              Follow.user_id==current_user.id)).first()
    assignments = Assignment.query.filter_by(course_id=course_id)
    if follow:
        if request.method == 'POST':
            if form.validate_on_submit():
                if form.never_expire.data:
                    assignment = Assignment(
                            course_id = course_id,
                            author_id = current_user.id,
                            name = form.name.data,
                            descripcion= form.descripcion.data)
                else:
                    assignment = Assignment(
                            course_id = course_id,
                            author_id = current_user.id,
                            name = form.name.data,
                            descripcion = form.descripcion.data,
                            date_expire = datetime.datetime.combine(form.date_expire.data, form.time_expire.data))
                try:
                    db.session.add(assignment)
                    db.session.commit()
                    flash("Assignment created")
                except:
                    db.session.rollback()
                    flash("Error creating Assignment!")
            return redirect(url_for('module003.module003_assignment_course', course_id=course.id))
        else:
            if current_user.profile in ('admin','staff','student'):
                follows = Follow.query.filter_by(user_id=current_user.id)
                return render_template("module003_assignment_especifico.html", form=form, module="module003", rows=follows, course=course, assignments=assignments)
            else:
                flash("Access denied!")
                return redirect(url_for('index'))
    else:
        flash("Access denied!")
#       abort(404,description="Access denied!")
        return redirect(url_for('index'))


@module003.route('/<course_id>/<assignment_id>/', methods=['POST', 'GET'])
@login_required
def module003_assignment_send(course_id, assignment_id):

    follow = Follow.query.filter(and_(Follow.course_id==course_id,
                                              Follow.user_id==current_user.id)).first()
    form = GradesForm()
    form2 = DownloadForm()
    course = Course.query.filter_by(id=course_id).first()
    if follow:
        assignment = Assignment.query.filter_by(id=int(assignment_id)).first()
        if course.user_id == current_user.id:
            entrega = Entrega.query.filter_by(assignment_id=int(assignment_id))
            if request.method == 'POST':

                entrega2 = Entrega.query.filter(and_(Entrega.assignment_id==int(assignment_id), Entrega.user == int(request.form['user']))).first()
                if form.validate_on_submit():
                    try:
                        entrega2.nota = float(form.name.data)
                        db.session.commit()
                        flash("Grade updated!")
                    except:
                        db.session.rollback()
                        flash("Error updating grade!")
                    return render_template("module003_correccion_ejercicio.html", module='module003', assignment=assignment, entrega = entrega, form=form, form2=form2)

                if form2.validate_on_submit():
                    file_contents = Entrega.query.filter(and_(Entrega.assignment_id==int(assignment_id), Entrega.user == int(request.form['user']))).first()
                    bytesio = BytesIO(file_contents.file)
                    fileW = FileWrapper(bytesio)
                    return Response(fileW, mimetype="application/zip" , direct_passthrough=True)

            return render_template("module003_correccion_ejercicio.html", module='module003', assignment=assignment, entrega = entrega, form=form, form2=form2)
        else:
            entrega = Entrega.query.filter(and_(Entrega.assignment_id==assignment_id, Entrega.user==current_user.id)).first()
            if request.method == 'POST':
                if entrega:
                    db.session.delete(Entrega.query.filter_by(user=current_user.id, assignment_id=assignment_id).first())
                    db.session.commit()
                    return redirect(url_for('module003.module003_assignment_course',course_id=course_id))

                file_contents = request.files['file']
                newfile = Entrega(name=file_contents.filename, file=file_contents.read(), user=current_user.id, assignment_id=assignment_id)
                try:
                    db.session.add(newfile)
                    db.session.commit()
                    flash("Uploaded file succesfully")
                except:
                    db.session.rollback()
                    flash("Error creating Assignment!")
                return redirect(url_for('module003.module003_assignment_course',course_id=course_id))
            else:
                return render_template("module003_upload_assignment.html", module='module003', assignment=assignment, entrega = entrega, assignment_id=assignment_id)

    else:
        flash("Access denied!")
#       abort(404,description="Access denied!")
        return redirect(url_for('index'))


@module003.route('/test')
def module003_test():
    return 'OK'