from flask import Blueprint
from flask import render_template, jsonify
from flask import url_for, request
from flask import redirect

from ..models import Sigh
from ..forms import SighForm


frontend_views = Blueprint('frontend', __name__, url_prefix='/')


@frontend_views.route('/')
def index():
    sighs = Sigh.query.all()
    return render_template('index.jade', page_title='Programmer sighs!', sighs=sighs)


@frontend_views.route('sigh/<int:sigh_id>/')
def render_sigh(sigh_id):
    sigh = Sigh.query.get_or_404(sigh_id)
    return render_template('sigh.jade', page_title='Programmer sighs!', sigh=sigh)


@frontend_views.route('new/', methods=['POST'])
def post_sigh():
    """TODO: Should be login required later"""

    form = SighForm(request.form)
    if form.validate():
        sigh = form.save()
        return jsonify(dict(
            sigh_id=sigh.id_,
            redirect_url=url_for('frontend.render_sigh', sigh_id=sigh.id_),
        ))
    else:
        return jsonify(form.errors), 405
