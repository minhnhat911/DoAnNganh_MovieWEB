from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    submit = SubmitField('Gửi bình luận')