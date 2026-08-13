from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app, flash, make_response, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from openpyxl import Workbook

from app.extensions import db
from app.forms import SeminarForm
from app.models import Seminar

bp = Blueprint('seminar', __name__, url_prefix='/seminar')


@bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = SeminarForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            seminar = Seminar(
                date=form.date.data,
                topic=form.topic.data,
                speaker=form.speaker.data,
                hours=float(form.hours.data),
                organizer=form.organizer.data,
                notes=form.notes.data,
                user_id=current_user.id,
            )
            db.session.add(seminar)
            db.session.commit()

            flash('Seminar saved successfully!', 'success')
            if request.headers.get('HX-Request') == 'true':
                response = make_response('', 200)
                response.headers['HX-Redirect'] = '/dashboard/'
                return response
            return redirect('/dashboard/')

        return render_template('partials/seminar_form.html', form=form, action_url=url_for('seminar.create'), submit_label='Save Seminar', modal_title='Add New Seminar'), 400

    return render_template('partials/seminar_modal.html', form=form, action_url=url_for('seminar.create'), submit_label='Save Seminar', modal_title='Add New Seminar')


@bp.route('/<int:seminar_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_seminar(seminar_id):
    seminar = Seminar.query.filter_by(id=seminar_id, user_id=current_user.id).first_or_404()
    form = SeminarForm(obj=seminar)
    if request.method == 'POST':
        form = SeminarForm(formdata=request.form, obj=seminar)
        if form.validate_on_submit():
            seminar.date = form.date.data
            seminar.topic = form.topic.data
            seminar.speaker = form.speaker.data
            seminar.hours = float(form.hours.data)
            seminar.organizer = form.organizer.data
            seminar.notes = form.notes.data
            db.session.commit()

            flash('Seminar updated successfully!', 'success')
            if request.headers.get('HX-Request') == 'true':
                response = make_response('', 200)
                response.headers['HX-Redirect'] = '/dashboard/'
                return response
            return redirect('/dashboard/')

        return render_template('partials/seminar_form.html', form=form, action_url=url_for('seminar.edit_seminar', seminar_id=seminar.id), submit_label='Update Seminar', modal_title='Edit Seminar'), 400

    return render_template('partials/seminar_modal.html', form=form, action_url=url_for('seminar.edit_seminar', seminar_id=seminar.id), submit_label='Update Seminar', modal_title='Edit Seminar')


@bp.route('/<int:seminar_id>/inline_edit/', methods=['GET', 'POST'])
@login_required
def inline_edit_seminar(seminar_id):
    seminar = Seminar.query.filter_by(id=seminar_id, user_id=current_user.id).first_or_404()
    form = SeminarForm(obj=seminar)
    if request.method == 'POST':
        form = SeminarForm(formdata=request.form, obj=seminar)
        if form.validate_on_submit():
            seminar.date = form.date.data
            seminar.topic = form.topic.data
            seminar.speaker = form.speaker.data
            seminar.hours = float(form.hours.data)
            seminar.organizer = form.organizer.data
            seminar.notes = form.notes.data
            db.session.commit()
            return render_template('partials/seminar_inline_view.html', seminar=seminar)

        return render_template('partials/seminar_inline_form.html', seminar=seminar, form=form), 400

    return render_template('partials/seminar_inline_form.html', seminar=seminar, form=form)


@bp.route('/<int:seminar_id>/inline_view/', methods=['GET'])
@login_required
def inline_view_seminar(seminar_id):
    seminar = Seminar.query.filter_by(id=seminar_id, user_id=current_user.id).first_or_404()
    return render_template('partials/seminar_inline_view.html', seminar=seminar)


@bp.route('/<int:seminar_id>/delete/', methods=['POST', 'DELETE'])
@login_required
def delete_seminar(seminar_id):
    seminar = Seminar.query.filter_by(id=seminar_id, user_id=current_user.id).first_or_404()
    db.session.delete(seminar)
    db.session.commit()

    flash('Seminar deleted successfully!', 'success')
    if request.headers.get('HX-Request') == 'true':
        response = make_response('', 200)
        response.headers['HX-Redirect'] = '/dashboard/'
        return response
    return redirect('/dashboard/')


@bp.route('/export')
@login_required
def export():
    seminars = Seminar.query.filter_by(user_id=current_user.id).all()
    wb = Workbook()
    ws = wb.active
    ws.title = 'Seminars'
    headers = ['Date', 'Topic', 'Speaker', 'Hours', 'Organizer', 'Notes']
    ws.append(headers)
    for seminar in seminars:
        ws.append([seminar.date.isoformat(), seminar.topic, seminar.speaker, seminar.hours, seminar.organizer, seminar.notes or ''])

    filename = f"seminars_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    output_dir = Path(current_app.instance_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / filename
    wb.save(output)
    return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
