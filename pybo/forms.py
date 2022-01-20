from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,PasswordField,EmailField
from wtforms.validators import DataRequired,Length,EqualTo,Email

class QuestionForm(FlaskForm):
    subject=StringField('제목',validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content=TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
    
    
class AnswerForm(FlaskForm):
    content=TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username=StringField('사용자 이름',validators=[DataRequired(),Length(min=3,max=25)])
    password1=PasswordField('비밀번호',validators=[DataRequired(),EqualTo('password2','비밀번호가 일치하지 않습니다.')])
    password2=PasswordField('비밀번호 확인',validators=[DataRequired()])
    email=EmailField('이메일',validators=[DataRequired(),Email()])
    
class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])


'''
질문을 등록할 때 사용할 QuestionForm을 작성하였다. QuestionForm과 같은 플라스크의 폼은 FlaskForm 클래스를 상속하여 만들어야 한다.

QuestionForm의 속성은 "제목"과 "내용"이다. 폼의 속성과 모델의 속성이 비슷함을 알 수 있을 것이다. 글자수의 제한이 있는 "제목"의 경우 StringField를 사용하고 글자수의 제한이 없는 "내용"은 TextAreaField를 사용한다.

플라스크에서 사용할 수 있는 속성에 대한 보다 자세한 내용은 다음 URL을 참고하자.

https://wtforms.readthedocs.io/en/2.3.x/fields/#basic-fields

StringField('제목', validators=[DataRequired()]) 에서 첫번째 입력인수인 "제목"은 폼 라벨(Label)이다. 템플릿에서 이 라벨을 이용하여 "제목"이라는
라벨을 출력할 수 있다. 이 부분은 잠시후에 다시 알아보기로 하자. 두번째 입력인수는 validators이다. 
validators는 검증을 위해 사용되는 도구로 필수 항목인지를 체크하는 DataRequired, 이메일인지를 체크하는 Email, 길이를 체크하는 Length등이 있다.
예를들어 필수값이면서 이메일이어야 하면 validators=[DataRequired(), Email()] 과 같이 사용할 수 있다.
플라스크에서 사용할 수 있는 validators에 대한 보다 자세한 내용은 다음 URL을 참고하자.

https://wtforms.readthedocs.io/en/2.3.x/validators/#built-in-validators
'''