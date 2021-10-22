from django import forms
from members.models import Member


class MembersForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = ['account_id', 'account_pw']
		labels = {
			'account_id': '아이디',
			'account_pw': '패스워드',
		}