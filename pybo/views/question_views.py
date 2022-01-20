from flask import Blueprint,render_template,request,url_for,g,flash
from ..models import Question,Answer,User, question_voter
from ..forms import QuestionForm,AnswerForm
from datetime import datetime
from werkzeug.utils import redirect
from .. import db
from pybo.views.auth_views import login_required
from sqlalchemy import func


bp=Blueprint('question',__name__,url_prefix='/question')
#질문 목록 기능에 해당하는 함수명을 list가 아니라 list_로 지정한 이유는 list가 파이썬의 예약어이기 때문이다.
@bp.route('/list/')
def list_():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so',type=str,default='recent')
    
    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query\
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:  # recent
        question_list = Question.query.order_by(Question.create_date.desc())

    # 조회
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username)\
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User)\
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)\
                .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    # 페이징
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw,so=so)

    #order_by는 조회결과를 정렬하는 함수.
    # order_by(Qusestion.create_date.desc()) 작성일시                         
    # 기준으로 역순으로 정렬하라는 의미이다.                                                                                
    #※ 역순이 아닌 작성일시 순으로 조회하기 위해서는 order_by(Question.create_date.asc()) 또는 asc() 를 생략하여 order_by(Question.create_date)와 같이 사용하면된다,
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form=AnswerForm()
    question=Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question=question,form=form)

@bp.route('/create/' ,methods=('GET','POST'))
@login_required
def create():
    form=QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question=Question(subject=form.subject.data,content=form.content.data,create_date=datetime.now(),user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html',form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question=Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question.list_'))

