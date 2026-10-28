# routes/api.py
# Endpoint JSON untuk Chart.js.
from flask import Blueprint, jsonify
from flask_login import login_required
from models import Pengajuan
from routes.auth import role_required

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/dashboard')
@login_required
@role_required('admin')
def dashboard_data():
    per_status = {s: Pengajuan.query.filter_by(status=s).count()
                  for s in ['menunggu', 'disetujui', 'ditolak', 'perbaikan']}
    return jsonify({
        'labels': list(per_status.keys()),
        'values': list(per_status.values()),
    })