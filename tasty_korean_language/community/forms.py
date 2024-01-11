from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post # model은 Post 양식으로 쓰겠다.
        fields = ('title', 'contents') # 어떤 필드를 입력 받을 지
        exclude = ('writer', ) # 폼에서 writer 입력받지 않게 함
        
        
        
        
# from django import forms
# from .models import Question, Answer, Comment


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question  # 사용할 모델
#         fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
#         labels = {
#             'subject': '제목',
#             'content': '내용',
#         }


# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = ['content']
#         labels = {
#             'content': '답변내용',
#         }


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['content']
#         labels = {
#             'content': '댓글내용',
#         }