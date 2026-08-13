from flask import Blueprint, current_app, render_template, request
from flask_login import login_required, current_user

from app.extensions import cache
from app.models import Seminar

bp = Blueprint('dashboard', __name__, url_prefix='/')


@bp.route('/dashboard/', methods=['GET'])
@login_required
def index():
    q = (request.args.get('q') or '').strip()
    sort_by = request.args.get('sort_by', 'date')
    direction = request.args.get('direction', 'desc')

    allowed_sort_fields = {'date': Seminar.date, 'topic': Seminar.topic, 'speaker': Seminar.speaker, 'hours': Seminar.hours, 'organizer': Seminar.organizer}
    sort_column = allowed_sort_fields.get(sort_by, Seminar.date)
    if direction == 'asc':
        query = Seminar.query.filter_by(user_id=current_user.id)
        if q:
            query = query.filter(
                (Seminar.topic.ilike(f'%{q}%')) |
                (Seminar.speaker.ilike(f'%{q}%')) |
                (Seminar.organizer.ilike(f'%{q}%')) |
                (Seminar.notes.ilike(f'%{q}%'))
            )
        seminars = query.order_by(sort_column.asc()).all()
    else:
        query = Seminar.query.filter_by(user_id=current_user.id)
        if q:
            query = query.filter(
                (Seminar.topic.ilike(f'%{q}%')) |
                (Seminar.speaker.ilike(f'%{q}%')) |
                (Seminar.organizer.ilike(f'%{q}%')) |
                (Seminar.notes.ilike(f'%{q}%'))
            )
        seminars = query.order_by(sort_column.desc()).all()

    total_seminars = Seminar.query.filter_by(user_id=current_user.id).count()
    total_hours = Seminar.query.filter_by(user_id=current_user.id).with_entities(__import__('sqlalchemy').func.sum(Seminar.hours)).scalar() or 0
    avg_hours = Seminar.query.filter_by(user_id=current_user.id).with_entities(__import__('sqlalchemy').func.avg(Seminar.hours)).scalar() or 0
    unique_organizers = Seminar.query.filter_by(user_id=current_user.id).with_entities(Seminar.organizer).distinct().count()
    return render_template(
        'dashboard.html',
        seminars=seminars,
        total_seminars=total_seminars,
        total_hours=total_hours,
        avg_hours=avg_hours,
        unique_organizers=unique_organizers,
        search=q,
        sort_by=sort_by,
        direction=direction,
    )


@bp.route('/health')
def health():
    return {'status': 'healthy', 'database': 'connected'}
