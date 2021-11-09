from django import forms
from members.models import Member
from members.models import Product


class ProductsForm(forms.ModelForm):
	class Meta:
		mode = Product
		fields = ['name']
		labels = {
			'name': '상품명',
		}


class MembersForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = ['account_id', 'account_pw', 'name', 'status', 'expire_at', 'sms_receive_time', 'sms_receive_day', 'is_sms_info', 'is_sms_combination', 'is_sms_result', 'join_at', 'join_ip', 'join_domain', 'join_referer', 'join_intro_url', 'join_device', 'consulting_status_fst', 'consulting_status_snd', 'is_auth', 'product']
		labels = {
			'account_id': '아이디',
			'account_pw': '패스워드',
			'name': '이름',
			'status': '상태',
			'expire_at': '만료일',
			'sms_receive_time': '문자 수신시간',
			'sms_receive_day': '문자 수신일',
			'is_sms_info': '안내 문자 수신',
			'is_sms_combination': '조합 문자 수신',
			'is_sms_result': '결과 문자 수신',
			'join_at': '가입일',
			'join_ip': '가입 IP',
			'join_domain': '가입 도메인',
			'join_referer': '가입 레퍼러',
			'join_intro_url': '가입 URL',
			'join_device': '가입 기기',
			'consulting_status_fst': '1차 상담상태',
			'consulting_status_snd': '2차 상담상태',
			'is_auth': '인증여부',
			'product': '이용상품',
		}
