from pybo import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text(), nullable = False)
    create_date = db.Column(db.DateTime(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref = db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)



class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    # 만약 a_question.delete() 처럼 파이썬 코드로 질문 데이터를 삭제하면 해당 질문과 연결된 답변 데이터는 삭제되지 않고
    # 답변 데이터의 question_id 컬럼만 빈값으로 업데이트된다. 만약 파이썬 코드로 질문 데이터를 삭제할 때 연결된 답변 모두를
    # 삭제하기 바란다면 다음처럼 db.backref 설정에 cascade='all, delete-orphan'를 추가해야 한다.
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200),  nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
