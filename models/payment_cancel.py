from django.db import models


class PaymentCancelAnnotation(models.Model):
    pg_tid = models.CharField('PG사 승인취소번호', max_length=500)
    amount = models.IntegerField('취소 금액')
    cancelled_at = models.IntegerField('결제취소된 시각', help_text='UNIX timestamp')
    reason = models.CharField('결제취소 사유', max_length=500)
    receipt_url = models.CharField('취소에 대한 매출전표 확인 URL', help_text='PG사에 따라 제공되지 않는 경우도 있음', max_length=500)
