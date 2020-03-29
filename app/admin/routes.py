from app.models import License, User
from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required

from app.admin import bp
from app.admin.forms import LoginForm
from app.models import License, User


@bp.route('/list')
@login_required
def list_active_bots():
    _licenses = License.query.order_by(License.last_seen.asc()).all()
    if _licenses is not None:
        active = []
        inactive = []
        for _license in _licenses:
            if _license.last_seen + timedelta(minutes=5) >= datetime.utcnow():
                active.append({'license_key': _license.license_key, 'email': _license.email, 'country': _license.country,
                            'order_number': _license.order_number, 'last_seen': _license.last_seen,
                            'current_ip': _license.current_ip, 'all_ips': _license.all_ips, 'age': 'active'})
            else:
                inactive.append({'license_key': _license.license_key, 'email': _license.email, 'country': _license.country,
                            'order_number': _license.order_number,
                            'last_seen': _license.last_seen + timedelta(minutes=5), 'current_ip': _license.current_ip,
                            'all_ips': _license.all_ips, 'age': 'inactive'})

    return render_template('list.html', active=active, inactive=inactive)