from pybo import db

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)  #db.string은 제목처럼 글자 수제한이있음.
    content = db.Column(db.Text(), nullable=False) #db.Text()는 글자 수 제한이 없음.
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date=db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))
    
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date=db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))
    

'''
db.ForeignKey에 지정한 첫 번째 값 'question.id'는 question 테이블의 id 컬럼을 의미한다.
Question 모델을 통해 테이블이 생성되면 테이블명은 question이 된다.
두 번째 ondelete에 지정한 값은 삭제 연동 설정이다. 즉, 답변 모델의 question_id 속성은 질문 모델의 id 속성과 연결되며 
ondelete='CASCADE'에 의해 데이터베이스에서 쿼리를 이용하여 질문을 삭제하면 해당 질문에 달린 답변도 함께 삭제된다.

그 다음 question 속성은 답변 모델에서 질문 모델을 참조하기 위해 추가했다. 예를 들어 답변 모델 객체에서 질문 모델 객체의 제목을 
참조하려면 answer.question.subject처럼 할 수 있다. 이렇게 하려면 속성을 추가할 때 db.Column이 아닌 db.relationship을 사용해야 한다.

db.relationship에 지정한 첫 번째 값은 참조할 모델명이고 두 번째 backref에 지정한 값은 역참조 설정이다. 역참조란 쉽게 말해 질문에서 
답변을 거꾸로 참조하는 것을 의미한다. 한 질문에는 여러 개의 답변이 달릴 수 있는데 역참조는 이 질문에 달린 답변을 참조할 수 있게 한다. 
예를 들어 어떤 질문에 해당하는 객체가 a_question이라면 a_question.answer_set와 같은 코드로 해당 질문에 달린 답변을 참조할 수 있다.

파이썬 코드를 이용하여 질문 데이터 삭제 시 연관된 답변 데이터 모두 삭제하는 방법

본문에서 "쿼리를 이용하여 질문 데이터를 삭제할 경우 답변도 함께 삭제된다"고 했는데 이는 정확히 말하면 데이터베이스 도구에서 쿼리를 이용하여 
삭제하는경우에 해당한다. 만약 파이썬 코드 a_question.delete() 로 질문 데이터를 삭제하면 해당 질문과 연관된 답변 데이터는 삭제되지 않고 답변 
데이터의 question_id 컬럼만 빈값으로 업데이트된다. 만약 파이썬 코드로 질문 데이터를 삭제할 때 연관된 답변 테이터가 모두 삭제되기를 바란다면 
db.backref 설정에 cascade='all, delete-orphan' 옵션을 추가해야 한다.

>>>question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))


db.Column에는 데이터 타입 외에 여러 속성을 지정할 수 있다.

primary_key

고유 번호 id에 지정한 primary_key는 id 속성을 기본 키로 지정한다. 
기본 키로 지정하면 중복된 값을 가질 수 없게 된다. 고유 번호는 모델에서 각 데이터를 구분하는 유효한 값으로 중복되면 안 된다.

데이터베이스에서는 id와 같은 특징을 가진 속성을 기본 키(primary key)라고 한다. 플라스크는 데이터 타입이 db.Integer이고 기본키로 
지정한 속성은 값이 자동으로 증가하는 특징도 있어서 데이터를 저장할 때 해당 속성값을 지정하지 않아도 1씩 자동으로 증가하여 저장된다.
nullable

그리고 nullable은 속성에 빈값을 허용할 것인지를 결정한다. nullable을 지정하지 않으면 해당 속성은 기본으로 빈값을 허용한다. 
따라서 속성에 빈값을 허용하지 않으려면 nullable=False를 지정해야 한다.
'''

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)


class Comment(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    user= db.relationship('User',backref=db.backref('comment_set'))
    content=db.Column(db.Text(),nullable=False)
    create_date=db.Column(db.DateTime(),nullable=False)
    modify_date=db.Column(db.DateTime())
    question_id=db.Column(db.Integer,db.ForeignKey('question.id',ondelete='CASCADE'),nullable=True)
    question=db.relationship('Question',backref=db.backref('comment_set'))
    answer_id=db.Column(db.Integer,db.ForeignKey('answer.id', ondelete='CASCADE'),nullable=True)
    answer=db.relationship('Answer',backref=db.backref('comment_set'))
    
