import datetime

from wtforms_alchemy import ModelForm
from wtforms import Form, FieldList
from wtforms import StringField
from wtforms.validators import DataRequired

from .models import Sigh, Tag
from .models import db


class TagForm(Form):
    class Meta:
        model = Tag


class SighForm(ModelForm):
    class Meta:
        model = Sigh

    tags = FieldList(StringField('Tag', validators=[DataRequired(), ]))

    def save(self):
        tag_list = self.data.get('tags')
        tags = filter(lambda x: x, [Tag.query.filter_by(name=tag).first() for tag in tag_list])
        self.data.pop('tags')
        sigh = Sigh(**self.data)
        sigh.tags.extend(tags)
        db.session.add(sigh)
        db.session.commit()
        return sigh
