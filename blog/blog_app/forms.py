from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		# fields = ["author", "comment"] # choose author when commenting
		fields = ["comment"]
		widgets = { # size of textarea field
			"comment": forms.Textarea(attrs={"rows": 4, "cols": 40})
		}
