from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# 각 랜딩에 들어갈 스크립트
class Script(models.Model):
	type = models.CharField(max_length=10)
	name = models.CharField(max_length=20)
	content = models.TextField()

	class Meta:
		verbose_name = '스크립트'
		verbose_name_plural = '스크립트'
		indexes = [
			models.Index(fields=['type', 'name'], name='script_search_common'),
		]


# 랜딩 목록
class Landing(models.Model):
	routing_name = models.CharField(max_length=20)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()
	script = models.ManyToManyField(Script)

	class Meta:
		verbose_name = '랜딩'
		verbose_name_plural = '랜딩'
		indexes = [
			models.Index(fields=['routing_name'], name='landing_search_target'),
		]


# 도메인 리스트
class Domain(models.Model):
	name = models.CharField(max_length=40)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

	class Meta:
		verbose_name = '랜딩'
		verbose_name_plural = '랜딩'
		indexes = [
			models.Index(fields=['name'], name='domain_search_target'),
		]


# 핫타임 설정
class HotTime(models.Model):
	start_at = models.DateTimeField()
	finish_at = models.DateTimeField()

	class Meta:
		verbose_name = '핫타임'
		verbose_name_plural = '핫타임'
		indexes = [
			models.Index(fields=['start_at', 'finish_at'], name='hot_time_search_common'),
		]


# 파트너
class Partner(models.Model):
	account_id = models.CharField(max_length=20, unique=True)
	account_pw = models.CharField(max_length=128)
	agent_id = models.OneToOneField('self', on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=30)
	phone_number = models.CharField(max_length=11)
	media = models.CharField(max_length=20)
	is_business = models.BooleanField(default=False)
	ad_type = models.CharField(max_length=10)
	memo = models.TextField()
	status = models.CharField(max_length=10)
	level = models.SmallIntegerField()
	hiding_rate = models.SmallIntegerField()
	commission_pc = models.SmallIntegerField()
	commission_mobile = models.SmallIntegerField
	landing = models.ManyToManyField(Landing)
	domain = models.ManyToManyField(Domain)
	hot_time = models.ManyToManyField(HotTime)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

	class Meta:
		verbose_name = '파트너'
		verbose_name_plural = '파트너'
		indexes = [
			models.Index(fields=['name', 'phone_number'], name='partner_search_target'),
			models.Index(fields=['media', 'is_business', 'ad_type', 'status', 'level', 'created_at'], name='partner_search_common'),
		]


# 클릭 로그
class Click(models.Model):
	landing_id = models.ForeignKey(Landing, on_delete=models.CASCADE)
	ip_address = models.CharField(max_length=15)
	partner_id = models.ForeignKey(Partner, on_delete=models.RESTRICT)
	created_at = models.DateTimeField()

	class Meta:
		verbose_name = '클릭 로그'
		verbose_name_plural = '클릭 로그'
		indexes = [
			models.Index(fields=['ip_address'], name='click_search_target'),
			models.Index(fields=['created_at'], name='click_search_common'),
		]


# 파트너의 수익금
class Commission(models.Model):
	type = models.CharField(max_length=10)
	is_hide = models.BooleanField(default=False)
	price = models.IntegerField()
	is_bad = models.BooleanField(default=False)
	partner_id = models.ForeignKey(Partner, on_delete=models.RESTRICT)
	member_id = models.ForeignKey('members.Member', on_delete=models.CASCADE)
	payment_id = models.ForeignKey('members.Payment', on_delete=models.CASCADE)
	created_at = models.DateTimeField()

	class Meta:
		verbose_name = '수익금'
		verbose_name_plural = '수익금'
		indexes = [
			models.Index(fields=['type', 'is_hide', 'price', 'is_bad', 'created_at'], name='commission_search_common'),
		]


# 아이피 중복 체크
class IpOverlap(models.Model):
	partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE)
	block_minutes = models.SmallIntegerField()

	class Meta:
		verbose_name = '아이피 중복 체크'
		verbose_name_plural = '아이피 중복 체크'


# 수익금 신청
class Profit(models.Model):
	agent_id = models.ForeignKey(Partner, on_delete=models.CASCADE)
	admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	amount = models.IntegerField()
	status = models.CharField(max_length=10)
	profit_bank_info = models.JSONField()
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

	class Meta:
		verbose_name = '수익금 신청'
		verbose_name_plural = '수익금 신청'
		indexes = [
			models.Index(fields=['status'], name='profit_search_common'),
		]


# 로그인 기록
class PartnerLoginLogs(models.Model):
	partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE)
	ip_address = models.CharField(max_length=15)
	created_at = models.DateTimeField()

	class Meta:
		verbose_name = '파트너 로그인 기록'
		verbose_name_plural = '파트너 로그인 기록'
		indexes = [
			models.Index(fields=['ip_address', 'created_at'], name='login_log_search_common'),
		]
