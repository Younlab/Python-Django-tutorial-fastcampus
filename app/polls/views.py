from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Question, Choice


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


# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(id=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404('Question does not exist')
#     question = get_object_or_404(Question, id=question_id, pub_date__isnull=False)
#     context = {
#         'question': question,
#     }
#
#     return render(request, 'polls/detail.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question':question,
    }
    return render(request, 'polls/results.html', context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question':question,
            'error_message':"You didn't select a choice."
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
