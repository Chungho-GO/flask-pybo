from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired("제목은 필수 항목입니다.")])
    content = TextAreaField('내용', validators=[DataRequired("내용은 필수 항목입니다.")])

'''
StringField('제목', validators=[DataRequired()]) 에서 첫번째 입력인수인 "제목"은 폼 라벨(Label)이다.
템플릿에서 이 라벨을 이용하여 "제목"이라는 라벨을 출력할 수 있다. 이 부분은 잠시후에 다시 알아보기로 하자. 
두번째 입력인수는 validators이다. validators는 검증을 위해 사용되는 도구로 필수 항목인지를 체크하는 DataRequired,
이메일인지를 체크하는 Email, 길이를 체크하는 Length등이 있다. 예를들어 필수값이면서 이메일이어야 하면 
validators=[DataRequired(), Email()] 과 같이 사용할 수 있다. 
플라스크에서 사용할 수 있는 validators에 대한 보다 자세한 내용은 다음 URL을 참고하자.
'''

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired("내용은 필수 항목입니다.")])


class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])