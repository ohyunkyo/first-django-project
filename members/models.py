from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# 제품 정의
class Product(models.Model):
	name = models.CharField(max_length=40, unique=True)
	period = models.SmallIntegerField()
	amount = models.IntegerField()
	discount_amount = models.IntegerField()
	description = models.TextField()
	status = models.CharField(max_length=10, default='inactive')
	is_hide = models.BooleanField(default=False)

	class Meta:
		verbose_name = '제품'
		verbose_name_plural = '제품'
		indexes = [
			models.Index(fields=['amount', 'discount_amount', 'status', 'is_hide'], name='product_search_common')
		]


# 무통장 입금 은행 정보
class BankInfo(models.Model):
	title = models.CharField(max_length=10, unique=True)
	bank_name = models.CharField(max_length=10)
	account_number = models.CharField(max_length=50)
	owner = models.CharField(max_length=10)

	class Meta:
		verbose_name = '은행 정보'
		verbose_name_plural = '은행 정보'
		indexes = [
			models.Index(fields=['bank_name', 'account_number', 'owner'], name='bank_info_search_common')
		]


# 회원
class Member(models.Model):
	account_id = models.CharField(max_length=13, unique=True)
	account_pw = models.CharField(max_length=128)
	name = models.CharField(max_length=30)
	status = models.CharField(max_length=20, default='active')
	expire_at = models.DateTimeField(null=True)
	sms_receive_time = models.SmallIntegerField(default=11)
	sms_receive_day = models.SmallIntegerField(default=1)
	is_sms_info = models.BooleanField(default=True)
	is_sms_combination = models.BooleanField(default=True)
	is_sms_result = models.BooleanField(default=True)
	join_at = models.DateTimeField()
	join_ip = models.CharField(max_length=15)
	join_domain = models.URLField(null=True)
	join_referer = models.URLField(null=True)
	join_intro_url = models.URLField(null=True)
	join_device = models.CharField(max_length=10, default='pc')
	charge_admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
	consulting_status_fst = models.CharField(max_length=10, default='waiting')
	consulting_status_snd = models.CharField(max_length=10, default='waiting')
	is_auth = models.BooleanField(default=False)
	product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, default=None, null=True)

	class Meta:
		verbose_name = '회원'
		verbose_name_plural = '회원'
		indexes = [
			models.Index(fields=['name'], name='member_search_target'),
			models.Index(fields=['status', 'expire_at', 'join_at', 'join_device', 'consulting_status_fst', 'consulting_status_snd'], name='member_search_common'),
			models.Index(fields=['sms_receive_time', 'sms_receive_day', 'is_sms_info', 'is_sms_combination', 'is_sms_result'], name='member_sms_send')
		]

	def __str__(self):
		return self.account_id


# 회원 메모
class Memo(models.Model):
	type = models.CharField(max_length=10)
	member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
	admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	memo = models.TextField()
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField(null=True)
	reserved_at = models.DateTimeField(null=True)

	class Meta:
		verbose_name = '메모'
		verbose_name_plural = '메모'
		indexes = [
			models.Index(fields=['type', 'created_at', 'reserved_at'], name='memo_search_common'),
		]


# 회원 상담 내역
class Counseling(models.Model):
	type = models.CharField(max_length=10)
	member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
	admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	consulting_status_fst = models.CharField(max_length=10)
	consulting_status_snd = models.CharField(max_length=10)
	consulting_memo = models.TextField()
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField(null=True)

	class Meta:
		verbose_name = '상담내용'
		verbose_name_plural = '상담내용'
		indexes = [
			models.Index(fields=['type', 'consulting_status_fst', 'consulting_status_snd', 'created_at'], name='counseling_search_common'),
		]


# 회원 1:1 문의
class QnA(models.Model):
	title = models.CharField(max_length=10)
	contents = models.TextField()
	answer = models.TextField()
	member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
	admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField()
	answer_at = models.DateTimeField()

	class Meta:
		verbose_name = '일대일 문의'
		verbose_name_plural = '일대일 문의'
		indexes = [
			models.Index(fields=['title'], name='qna_search_target'),
			models.Index(fields=['created_at', 'answer_at'], name='qna_search_common'),
		]


# 정기결제 정보
class Subscription(models.Model):
	member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
	product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, default=None, null=True)
	status = models.CharField(max_length=10)
	start_at = models.DateTimeField()
	payment_info = models.JSONField()
	payment_fail_code = models.CharField(max_length=10)
	payment_fail_msg = models.TextField()

	class Meta:
		verbose_name = '정기결제'
		verbose_name_plural = '정기결제'
		indexes = [
			models.Index(fields=['status', 'start_at', 'payment_fail_code'], name='common_search'),
		]


# 결제 정보
class Payment(models.Model):
	member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
	pg_company = models.CharField(max_length=20)
	pg_code = models.CharField(max_length=64, unique=True)
	method = models.CharField(max_length=10)
	product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, default=None, null=True)
	subscription_id = models.ForeignKey(Subscription, on_delete=models.SET_NULL, default=None, null=True)
	type = models.CharField(max_length=10)
	status = models.CharField(max_length=10)
	amount = models.IntegerField()
	admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, related_name='payment_admin', null=True)
	charge_admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, related_name='payment_charge_admin', null=True)
	phone_number = models.CharField(max_length=11)
	device = models.CharField(max_length=10)
	ip_address = models.CharField(max_length=15)
	bank_info_id = models.ForeignKey(BankInfo, on_delete=models.SET_NULL, default=None, null=True)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()

	class Meta:
		verbose_name = '결제'
		verbose_name_plural = '결제'
		indexes = [
			models.Index(fields=['phone_number'], name='payment_search_target'),
			models.Index(fields=['pg_company', 'method', 'status', 'device', 'created_at'], name='payment_search_common'),
		]


# 회원 정지 로그
class MemberPauseLog(models.Model):
	member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
	admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	reason = models.CharField(max_length=10)
	remaining = models.SmallIntegerField()
	created_at = models.DateTimeField()

	class Meta:
		verbose_name = '정지 로그'
		verbose_name_plural = '정지 로그'
		indexes = [
			models.Index(fields=['reason', 'remaining', 'created_at'], name='member_pause_search_common'),
		]


# 회원정보 변경 로그
class MemberModifyLog(models.Model):
	member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
	admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	changed_data = models.JSONField()
	updated_at = models.DateTimeField()

	class Meta:
		verbose_name = '회원정보 변경 로그'
		verbose_name_plural = '회원정보 변경 로그'
		indexes = [
			models.Index(fields=['updated_at'], name='member_modify_search_common'),
		]


# 배정로그
class AssignmentLog(models.Model):
	member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
	admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignment_charge_admin')
	assignment_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignment_admin')
	that_status = models.JSONField()
	created_at = models.DateTimeField()

	class Meta:
		verbose_name = '회원정보 변경 로그'
		verbose_name_plural = '회원정보 변경 로그'
		indexes = [
			models.Index(fields=['created_at'], name='assignment_search_common'),
		]


# 공지사항
class Notice(models.Model):
	title = models.CharField(max_length=30)
	contents = models.TextField()
	file_name = models.ImageField(upload_to='notice/')
	type = models.CharField(max_length=10)
	status = models.CharField(max_length=10)
	admin_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField()

	class Meta:
		verbose_name = '일대일 문의'
		verbose_name_plural = '일대일 문의'
		indexes = [
			models.Index(fields=['type', 'status', 'created_at'], name='notice_search_common'),
		]
