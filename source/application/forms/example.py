# -*- coding:utf-8 -*-

from wtforms.ext.appengine.ndb import model_form

from flask.ext import wtf
from flask.ext.wtf import validators

from application.models import ExampleModel


class ExampleForm(wtf.Form):
    example_name = wtf.TextField('Name', validators=[validators.Required()])
    example_description = wtf.TextAreaField('Description', validators=[validators.Required()])

# App Engine ndb model form example
ExampleForm = model_form(ExampleModel, wtf.Form, field_args={
    'example_name': dict(validators=[validators.Required()]),
    'example_description': dict(validators=[validators.Required()]),
})
