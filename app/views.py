from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required, login_required
from app.models import Question, Answer, Tag, Profile, Rating
from app import forms


def right_menu_objects():
    tags = Tag.objects.all()
    members = Profile.objects.all()

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

    context = {
        'questions': questions,
        'page': page,
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        context['profile'] = profile

    return render(request, 'questions.html', context)


def question(request, qid):
    q = Question.objects.get(id=qid)
    a, page = paginate(Answer.objects.filter(question=q), 3, request)
    right_menu_tags, right_menu_members = right_menu_objects()

    context = {
        'question': q,
        'answers': a,
        'page': page,
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        context['profile'] = profile
    else:
        profile = None

    if request.method == 'POST':
        form = forms.AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.profile = profile
            answer.question = q
            answer.save()
            return redirect(reverse('question', kwargs={'qid': qid}))
    else:
        form = forms.AnswerForm()

    context['form'] = form

    return render(request, 'question_page.html', context)


def tag_page(request, tag_name):
    t = Tag.objects.get(name=tag_name)
    questions, page = paginate(Question.objects.filter(tag=t), 3, request)
    right_menu_tags, right_menu_members = right_menu_objects()

    context = {
        'tag': t.name,
        'questions': questions,
        'page': page,
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        context['profile'] = profile

    return render(request, 'tag_page.html', context)


@login_required
def ask(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = forms.AskForm(data=request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.profile = profile
            q.save()
            for tag in form['tags'].data.split():
                new_tag = Tag.objects.get_or_create(name=tag)
                q.tag.add(new_tag[0])
            q.save()
            return redirect(reverse('question', kwargs={'qid': q.pk}))
    else:
        form = forms.AskForm()

    right_menu_tags, right_menu_members = right_menu_objects()
    context = {
        'form': form,
        'profile': profile,
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }
    return render(request, 'ask.html', context)


def register(request):
    if request.method == 'POST':
        form_user = forms.SignupFormUser(data=request.POST)
        form_profile = forms.SignupFormProfile(data=request.POST)

        if request.POST['password'] == request.POST['password_confirmation']:
            user = form_user.save()
            user.set_password(user.password)
            user.save()
            profile = Profile.objects.get_or_create(user=user,
                                                    nickname=request.POST['nickname'],
                                                    avatar=request.POST['avatar'])
            login(request, user)
            return redirect('questions')

    else:
        form_user = forms.SignupFormUser()
        form_profile = forms.SignupFormProfile()

    right_menu_tags, right_menu_members = right_menu_objects()

    context = {
        'form_u': form_user,
        'form_p': form_profile,
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }

    return render(request, 'register.html', context)


def show_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                print('not none')
                if user.is_active:
                    print('active')
                    login(request, user)
                    return redirect('/settings/')
            else:
                return redirect('/questions/')
    else:
        form = forms.LoginForm()

    right_menu_tags, right_menu_members = right_menu_objects()

    context = {
        'form': form,
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }

    return render(request, 'login.html', context)


@login_required()
def settings(request):
    profile = Profile.objects.get(user=request.user)
    right_menu_tags, right_menu_members = right_menu_objects()

    if request.method == 'POST':
        form_user = forms.SettingsFormUser(data=request.POST, instance=request.user)
        form_profile = forms.SettingsFormProfile(data=request.POST, instance=profile)
        if form_user.is_valid() and form_profile.is_valid():
            user = form_user.save(commit=False)
            user.save()
            profile = form_profile.save(commit=False)
            profile.save()
    else:
        form_user = forms.SettingsFormUser(instance=request.user)
        form_profile = forms.SettingsFormProfile(instance=profile)

    context = {
        'form_u': form_user,
        'form_p': form_profile,
        'profile': profile,
        'right_menu_tags': right_menu_tags,
        'right_menu_members': right_menu_members,
    }
    return render(request, 'settings.html', context)
