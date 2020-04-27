from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Question, Answer, Tag, Profile, Rating

def right_menu_objects():
    tags=Tag.objects.all()
    members=Profile.objects.all()

    return tags, members

def paginate(objects_list, number_of_objects_on_page, request):
    pages_count = request.GET.get('page')
    if pages_count is None:
        pages_count=1

    paginator = Paginator(objects_list, number_of_objects_on_page)

    page = paginator.page(pages_count)
    return page.object_list, page

def get_questions(request):
    questions, page = paginate(Question.objects.all(), 3, request)
    right_menu_tags, right_menu_members = right_menu_objects()

    attr = {
        'questions': questions,
        'page': page,
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }
    return render(request, 'questions.html', attr)

def question(request, qid):
    q = Question.objects.get(id=qid)
    a, page = paginate(Answer.objects.filter(question=q), 3, request)
    right_menu_tags, right_menu_members = right_menu_objects()

    attr = {
        'question': q,
        'answers': a,
        'page': page,
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }
    return render(request, 'question_page.html', attr)

def tag_page(request, tag_name):
    t = Tag.objects.get(name=tag_name)
    questions, page = paginate(Question.objects.filter(tag=t), 3, request)
    right_menu_tags, right_menu_members = right_menu_objects()

    attr = {
        'tag': t.name,
        'questions': questions,
        'page': page,
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }
    return render(request, 'tag_page.html', attr)

def ask(request):
    right_menu_tags, right_menu_members = right_menu_objects()

    attr = {
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }
    return render(request, 'ask.html', attr)

def register(request):
    right_menu_tags, right_menu_members = right_menu_objects()

    attr = {
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }
    return render(request, 'register.html', attr)

def login(request):
    right_menu_tags, right_menu_members = right_menu_objects()

    attr = {
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }
    return render(request, 'login.html', attr)

def settings(request):
    right_menu_tags, right_menu_members = right_menu_objects()

    attr = {
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }
    return render(request, 'settings.html', attr)
