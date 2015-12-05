import datetime
import misaka
from flask.ext.babel import gettext as _


def timeago(dt):
    now = datetime.datetime.now()
    delta = now - dt
    print delta
    if delta < datetime.timedelta(minutes=2):
        return _('Just now')
    if delta < datetime.timedelta(hours=1):
        return _('{} minutes ago').format(delta.seconds / 60)
    if delta < datetime.timedelta(hours=2):
        return _('1 hour ago')
    if delta < datetime.timedelta(days=1):
        return _('{} hours ago').format(delta.seconds / 3600)
    if delta < datetime.timedelta(days=2):
        return _('1 day ago')
    return _('{} days ago').format(delta.days)


def plain_markdown(text):
    renderer = misaka.HtmlRenderer(flags=misaka.HTML_ESCAPE)
    md = misaka.Markdown(renderer)
    return md.render(text)

