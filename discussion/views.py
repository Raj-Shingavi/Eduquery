from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Question, Answer, Group, Poll, PollOption, PollVote
from .forms import QuestionForm, AnswerForm, CustomUserCreationForm, GroupForm, PollCreationForm

def home(request):
    """Home view that lists recent questions."""
    questions = Question.objects.select_related('author', 'group').all().order_by('-created_at')[:20]
    return render(request, 'discussion/home.html', {'questions': questions})

def search(request):
    """Keyword Search view."""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Run database keyword search
        results = Question.objects.select_related('author', 'group').filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')
        
    return render(request, 'discussion/search.html', {'query': query, 'results': results})

@login_required
def post_question(request, group_id=None):
    """Allows users to post a new question cleanly mapped to a group if parsed."""
    group = None
    if group_id:
        group = get_object_or_404(Group, id=group_id)
        
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.group = group
            question.save()
            
            messages.success(request, 'Your question was posted successfully!')
            if group:
                return redirect('group_detail', group_id=group.id)
            return redirect('question_detail', question_id=question.id)
    else:
        form = QuestionForm()
        
    return render(request, 'discussion/post.html', {'form': form, 'group': group})

def question_detail(request, question_id):
    """Shows the details of a query and allows other students to answer."""
    question = get_object_or_404(Question.objects.select_related('author', 'group'), id=question_id)
    answers = question.answers.select_related('author').annotate(like_count=Count('likes')).order_by('-like_count', 'created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
            
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = AnswerForm()
        
    return render(request, 'discussion/detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })

def register(request):
    """Registration for new users."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'discussion/register.html', {'form': form})

@login_required
def toggle_like(request, answer_id):
    """Allows teachers to toggle a like on an answer."""
    if request.user.role != 'teacher':
        messages.error(request, 'Only teachers can endorse answers.')
        return redirect('home')
        
    answer = get_object_or_404(Answer, id=answer_id)
    
    if answer.likes.filter(id=request.user.id).exists():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
        
    return redirect('question_detail', question_id=answer.question.id)

# --- COMMUNITIES / GROUPS / POLLS Logic ---

def group_list(request):
    groups = Group.objects.select_related('creator').annotate(member_count=Count('members')).order_by('-created_at')
    return render(request, 'discussion/group_list.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            group.members.add(request.user)
            messages.success(request, "Community Successfully Founded!")
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'discussion/create_group.html', {'form': form})

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    questions = group.questions.select_related('author').order_by('-created_at')
    polls = group.polls.select_related('author').prefetch_related('options').order_by('-created_at')

    is_member = group.members.filter(id=request.user.id).exists()
    
    return render(request, 'discussion/group_detail.html', {
        'group': group,
        'questions': questions,
        'polls': polls,
        'is_member': is_member
    })

@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if group.max_members and group.members.count() >= group.max_members:
        messages.error(request, "This community has reached its maximum member limit.")
    else:
        group.members.add(request.user)
        messages.success(request, f"You have officially joined {group.name}!")
    return redirect('group_detail', group_id=group.id)

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.remove(request.user)
    messages.info(request, f"You have left {group.name}.")
    return redirect('group_detail', group_id=group.id)

@login_required
def create_poll(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if not request.user in group.members.all():
        messages.error(request, "You must join to create a poll.")
        return redirect('group_detail', group_id=group.id)
        
    if request.method == 'POST':
        form = PollCreationForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.group = group
            poll.author = request.user
            poll.save()
            
            # Map the newline separated options
            options = form.cleaned_data['options']
            for opt_text in options:
                PollOption.objects.create(poll=poll, text=opt_text)
                
            messages.success(request, "Poll deployed successfully!")
            return redirect('group_detail', group_id=group.id)
    else:
        form = PollCreationForm()
    return render(request, 'discussion/create_poll.html', {'form': form, 'group': group})

@login_required
def vote_poll(request, poll_id):
    if request.method == 'POST':
        poll = get_object_or_404(Poll, id=poll_id)
        option_id = request.POST.get('option_id')
        if not option_id:
            messages.error(request, "You must select an option!")
            return redirect('group_detail', group_id=poll.group.id)
            
        option = get_object_or_404(PollOption, id=option_id)
        
        # Guard against zero-duplication voting
        has_voted = PollVote.objects.filter(poll=poll, user=request.user).exists()
        if has_voted:
            # We can allow them to swap votes, so we delete old ones
            PollVote.objects.filter(poll=poll, user=request.user).delete()
            
        PollVote.objects.create(poll=poll, option=option, user=request.user)
        messages.success(request, "Your vote has been cast.")
        return redirect('group_detail', group_id=poll.group.id)
