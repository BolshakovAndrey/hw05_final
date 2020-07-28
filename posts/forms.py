from django.forms import ModelForm, Textarea
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["group", "text", "image"]
        required = {
            "group": False,
        }
        labels = {
            "group": "Сообщества",
            "text": "Текст записи",
            "image": "Картинка"
        }
        help_texts = {
            "group": "Сообщество, к которому относится данное сообщение."
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": Textarea
        }
        labels = {
            "text": "Комментарий"
        }
        help_texts = {
            "text": "Ваш комментарий тут"
        }
