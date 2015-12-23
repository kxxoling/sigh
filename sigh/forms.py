import datetime

from wtforms_alchemy import ModelForm
from wtforms import Form, FieldList
from wtforms import StringField
from wtforms.validators import DataRequired

from .models import Sigh, Tag, Comment


class TagForm(Form):
    class Meta:
        model = Tag


class SighForm(ModelForm):
    class Meta:
        model = Sigh

    tags = FieldList(StringField('Tag', validators=[DataRequired(), ]))

    def save(self, **kwargs):
        tag_list = self.data.get('tags')
        tags = filter(lambda x: x, [Tag.query.filter_by(name=tag).first() for tag in tag_list])
        self.data.pop('tags')
        kwargs.update(self.data)
        sigh = Sigh(**kwargs)
        sigh.tags.extend(tags)
        sigh.save()
        return sigh


class CommentForm(ModelForm):
    class Meta:
        model = Comment

    def save(self, **kwargs):
        # A strange error occurred here: two dict type variable kwargs and self.data seams are read-only?
        dct = {}
        for k in kwargs:
            dct[k] = kwargs[k]
        for k in self.data:
            dct[k] = self.data[k]
        comment = Comment(**dct)
        comment.save()
        return comment
