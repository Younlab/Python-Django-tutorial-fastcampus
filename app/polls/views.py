from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Question


def index(request):
    # DB에 있는 Question중, 가장 최근에 발행(pub_date)된 순서대로 최대 5개에 해당하는 QuerySet을
    # latest_question_list 변수에 할당
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # latest_question_list의 각 Question의 qusetion_text들을 ', '로 연결시킨 문자열을
    # output 변수에 할당
    # output = ', '.join([q.question_text for q in latest_question_list])
    context = {
        'latest_question_list':latest_question_list,
    }
    # 만들어진 질문 제목들을 모은 문자열을 HttpResponse 클래스의 생성자로 전달, 인스턴스를 리턴
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')
    question = get_object_or_404(Question, id=question_id, pub_date__isnull=False)
    context = {
        'question': question,
    }

    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    response = "You're looking at the results of question %s"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s" % question_id)
