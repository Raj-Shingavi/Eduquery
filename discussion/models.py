from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    can_post = models.CharField(max_length=50, choices=(('all', 'All members'), ('admin', 'Only admin')), default='all')
    can_comment = models.CharField(max_length=50, choices=(('all', 'Everyone'), ('restricted', 'Restricted')), default='all')
    max_members = models.IntegerField(null=True, blank=True)
    tags = models.CharField(max_length=255, help_text="Comma separated keywords")
    icon = models.ImageField(upload_to='group_icons/', null=True, blank=True)
    rules = models.TextField(help_text="Group guidelines and rules")
    discussion_format = models.CharField(max_length=50, choices=(('open', 'Open discussion'), ('poll', 'Poll-based')), default='open')
    
    members = models.ManyToManyField(User, related_name='joined_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_tags_list(self):
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        return []

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_answers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.title}"

class Poll(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='polls')
    question_text = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question_text
        
class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    
    def __str__(self):
        return self.text

class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('poll', 'user') # Users can only vote once per poll
