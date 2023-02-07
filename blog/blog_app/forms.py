from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ("author", "comment")
		widgets = {
			"comment": forms.Textarea(attrs={"rows": 5, "cols": 40})
		} # size of textarea field

