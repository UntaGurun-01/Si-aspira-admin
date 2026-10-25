from flask import Blueprint, render_template
from flask_login import login_required

about_bp = Blueprint('about', __name__, url_prefix='/about')


@about_bp.route('/')
@about_bp.route('')
@login_required
def index():
    developers = [
        {
            'name': 'Agam Al Hakim Hasibuan',
            'role': 'Frontend Developer',
            'badge': 'badge-frontend',
            'icon': 'bi-code-slash',
            'photo': 'img/developers/frontend.png',
            'desc': 'Merancang antarmuka pengguna responsif, styling tema dark modern, animasi interaktif, dan kenyamanan navigasi pengguna.'
        },
        {
            'name': 'Habil Maulana',
            'role': 'Backend Developer',
            'badge': 'badge-backend',
            'icon': 'bi-server',
            'photo': 'img/developers/backend.png',
            'desc': 'Mengembangkan logika server Python/Flask, manajemen database relasional, autentikasi sesi, dan pemrosesan alur tiket.'
        },
        {
            'name': 'M.Totti Airindo',
            'role': 'Full-Stack Developer',
            'badge': 'badge-fullstack',
            'icon': 'bi-layers-fill',
            'photo': 'img/developers/fullstack.png',
            'desc': 'Menjembatani integrasi frontend dan backend, optimasi performa sistem, validasi keamanan, dan pengujian fitur end-to-end.'
        },
        {
            'name': 'M.Dzuryadi',
            'role': 'UI/UX Designer',
            'badge': 'badge-uiux',
            'icon': 'bi-palette-fill',
            'photo': 'img/developers/uiux.png',
            'desc': 'Menyusun wireframe, rancangan prototipe antarmuka, pemilihan palet warna dark navy, tata letak visual, dan pengalaman pengguna.'
        }
    ]
    return render_template('about/index.html', developers=developers)
