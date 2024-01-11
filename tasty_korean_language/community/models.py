from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=40, default = '')
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0) # 양수입력 필드
    # writer은 다른 모델을 참조하겠다.(User) 외래키 추가
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default = '') # on_delete : User가 delete 될 때 게시글을 어떻게 설정한 것인지에 대해 설정 1. 게시글 같이 지우기(CASCADE) 2. 없는 값으로 해서 게시글은 남겨두기

    def get_absolute_url(self):
        return reverse('community:detail', args=[self.id])

class Reply(models.Model):
    """
        reply: Reply -> Board 연결관계
        comment: 댓글내용
        rep_date: 작성일
    """
    reply = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rep_date = models.DateTimeField()

    def __str__(self):
        return self.comment
    
    
    
    
    
    
    
    
# from django.db import models
# from django.db.models import Count
# from django.urls import reverse
# from django.contrib.auth.models import User


# class Category(models.Model):
#     name = models.CharField(max_length=20, unique=True)
#     description = models.CharField(max_length=200, null=True, blank=True)
#     has_answer = models.BooleanField(default=True)  # 답변가능 여부

#     def __str__(self):
#     #     return self.name
#         return self.description

#     def get_absolute_url(self):
#         return reverse('pybo:index', args=[self.name])


# class Question(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
#     subject = models.CharField(max_length=200)
#     content = models.TextField()
#     create_date = models.DateTimeField()
#     modify_date = models.DateTimeField(null=True, blank=True)
#     voter = models.ManyToManyField(User, related_name='voter_question')  # 추천인 추가
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_question')

#     def __str__(self):
#         return self.subject

#     @staticmethod
#     def order_by_so(question_list, so):
#         if so == 'recommend':
#             # aggretation, annotation에는 relationship에 대한 역방향 참조도 가능 (ex. Count('voter'))
#             question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
#         elif so == 'popular':
#             question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
#         else:  # so == 'recent':
#             question_list = question_list.order_by('-create_date')

#         return question_list

#     def get_absolute_url(self):
#         return reverse('pybo:detail', args=[self.id])


# class Answer(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     content = models.TextField()
#     create_date = models.DateTimeField()
#     modify_date = models.DateTimeField(null=True, blank=True)
#     voter = models.ManyToManyField(User, related_name='voter_answer')  # 추천인 추가

#     def __str__(self):
#         return self.content

#     @staticmethod
#     def order_by_so(answer_list, so):
#         # 정렬
#         if so == 'recommend':
#             # todo num_voter 필드 추가
#             answer_list = answer_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
#         else:  # so == 'recent':
#             answer_list = answer_list.order_by('-create_date')

#         return answer_list

#     def get_page(self, so='recommend'):
#         queryset = Answer.order_by_so(self.question.answer_set.all(), so)

#         index = 0
#         for _answer in queryset:
#             index += 1
#             if self == _answer:
#                 break

#         return (index - 1) // 5 + 1

#     def get_absolute_url(self):
#         return reverse('pybo:detail', args=[self.question.id]) + f'?page={self.get_page()}#answer_{self.id}'


# class Comment(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
#     content = models.TextField()
#     create_date = models.DateTimeField()
#     modify_date = models.DateTimeField(null=True, blank=True)
#     question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
#     answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.content

#     def get_absolute_url(self):
#         if self.question:
#             return reverse('pybo:detail', args=[self.question.id]) + '#comment_question_start'
#         else:  # if self.answer:
#             return reverse('pybo:detail', args=[self.answer.question.id]) + \
#                    f'?page={self.answer.get_page()}#comment_{self.id}'