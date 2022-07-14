from django.db import models
from django.db.models import TextChoices, IntegerChoices


class IamportPaymentMethod(TextChoices):
    samsung = 'samsung', '삼성페이'
    card = 'card', '신용카드'
    trans = 'trans', '계좌이체'
    vbank = 'vbank', '가상계좌'
    phone = 'phone', '휴대폰'
    cultureland = 'cultureland', '문화상품권'
    smartculture = 'smartculture', '스마트문상'
    booknlife = 'booknlife', '도서문화상품권'
    happymoney = 'happymoney', '해피머니'
    point = 'point', '포인트'
    ssgpay = 'ssgpay', 'SSGPAY'
    lpay = 'lpay', 'LPAY'
    payco = 'payco', '페이코'
    kakaopay = 'kakaopay', '카카오페이'
    tosspay = 'tosspay', '토스'
    naverpay = 'naverpay', '네이버페이'


class IamportPaymentChannel(TextChoices):
    PC = 'pc', 'PC결제'
    MOBILE = 'mobile', '모바일결제'
    API = 'api', 'API결제'


class IamportPaymentPgProvider(TextChoices):
    INICIS = 'inicis', '이니시스'
    NICE = 'nice', '나이스정보통신'


class IamportPaymentEmbPgProvider(TextChoices):
    CHAI = 'chai', '차이'
    KAKAOPAY = 'kakaopay', '카카오페이'


class IamportPaymentCardCode(TextChoices):
    BC = '361', 'BC카드'
    KJ = '364', '광주카드'
    SAMSUNG = '365', '삼성카드'
    SHINHAN = '366', '신한카드'
    HYUNDAI = '367', '현대카드'
    LOTTE = '368', '롯데카드'
    SH = '369', '수협카드'
    CITY = '370', '씨티카드'
    NH = '371', 'NH카드'
    JB = '372', '전북카드'
    JEJU = '373', '제주카드'
    HANA = '374', '하나SK카드'
    KB = '381', 'KB국민카드'
    WOORI = '041', '우리카드'
    POST = '071', '우체국'


class IamportPaymentCardType(IntegerChoices):
    CREDIT = 0, '신용카드'
    CHECK = 1, '체크카드'


class IamportPaymentCurrency(TextChoices):
    KRW = 'KRW', '원'
    USD = 'USD', '미화달러'
    EUR = 'EUR', '유로'


class IamportPaymentStatus(TextChoices):
    READY = 'ready', '미결제'
    PAID = 'paid', '결제완료'
    CANCELLED = 'cancelled', '결제취소'
    FAILED = 'failed', '결제실패'


class IamportPaymentCustomerUidUsage(TextChoices):
    null = None, '일반결제'
    issue = 'issue', '빌링키 발급'
    payment = 'payment', '결제'
    payment.scheduled = 'payment.scheduled', '예약결제'


HELP_CARD_NUMBER = '7~12번째 자리를 마스킹하는 것이 일반적이지만, PG사의 정책/설정에 따라 다소 차이가 있을 수 있음'
HELP_CARD_TYPE = '해당 정보를 제공하지 않는 일부 PG사의 경우 null로 응답(ex. JTNet, 이니시스-빌링)'
HELP_CUSTOMER_UID = '결제창을 통해 빌링키 발급 성공한 결제건의 경우 요청된 customer_uid 값을 응답'


class IamportPaymentManager(models.Manager):
    pass


class IamportPayment(models.Model):
    imp_uid = models.CharField("아임포트 결제 고유 UID", max_length=500)
    merchant_uid = models.CharField("가맹점에서 전달한 거래 고유 UID", max_length=500)
    pay_method = models.CharField('결제방법', choices=IamportPaymentMethod.choices, blank=True, max_length=500)
    channel = models.CharField("결제가 발생된 경로", choices=IamportPaymentChannel.choices, blank=True, max_length=500)
    pg_provider = models.CharField("PG사 명칭", IamportPaymentPgProvider.choices, blank=True, max_length=500)
    emb_pg_provider = models.CharField("허브형결제 PG사 명칭", blank=True, max_length=500)
    pg_tid = models.CharField("PG사 승인정보", blank=True, null=True, max_length=500)
    pg_id = models.CharField("거래가 처리된 PG사 상점아이디", blank=True, null=True, max_length=500)
    escrow = models.BooleanField("에스크로결제 여부", blank=True, null=True)
    apply_num = models.CharField("카드사 승인정보", help_text='계좌이체/가상계좌는 값 없음', blank=True, max_length=500)
    bank_code = models.CharField("은행 표준코드", help_text='금융결제원기준', blank=True, max_length=500)
    bank_name = models.CharField("은행 명칭", help_text='실시간계좌이체 결제 건의 경우', blank=True, max_length=500)
    card_code = models.CharField("카드사 코드번호", help_text='금융결제원 표준코드번호', blank=True, max_length=500)
    card_name = models.CharField("카드사 명칭", help_text='신용카드 결제 건의 경우', blank=True, max_length=500)
    card_quota = models.IntegerField("할부개월 수", help_text='0이면 일시불', blank=True, null=True)
    card_number = models.CharField("결제에 사용된 마스킹된 카드번호", help_text=HELP_CARD_NUMBER, blank=True, max_length=500)
    card_type = models.IntegerField("카드유형", choices=IamportPaymentCardType.choices, help_text=HELP_CARD_TYPE, blank=True, null=True)
    vbank_code = models.CharField("가상계좌 은행 표준코드", help_text='금융결제원기준', blank=True, max_length=500)
    vbank_name = models.CharField("입금받을 가상계좌 은행명", blank=True, max_length=500)
    vbank_num = models.CharField("입금받을 가상계좌 계좌번호", blank=True, max_length=500)
    vbank_holder = models.CharField("입금받을 가상계좌 예금주", blank=True, max_length=500)
    vbank_date = models.IntegerField("입금받을 가상계좌 마감기한", help_text='UNIX timestamp', blank=True, null=True)
    vbank_issued_at = models.IntegerField("가상계좌 생성 시각", help_text='UNIX timestamp', blank=True, null=True)
    name = models.CharField("주문명칭", blank=True, max_length=500)
    amount = models.IntegerField("주문(결제)금액", blank=True, null=True)
    cancel_amount = models.IntegerField("결제취소금액", blank=True, null=True)
    currency = models.CharField("결제승인 화폐단위", choices=IamportPaymentCurrency.choices, blank=True, max_length=500)
    buyer_name = models.CharField("주문자명", blank=True, max_length=500)
    buyer_email = models.CharField("주문자 Email주소", blank=True, max_length=500)
    buyer_tel = models.CharField("주문자 전화번호", blank=True, max_length=500)
    buyer_addr = models.CharField("주문자 주소", blank=True, max_length=500)
    buyer_postcode = models.CharField("주문자 우편번호", blank=True, max_length=500)
    custom_data = models.CharField("가맹점에서 전달한 custom data", help_text='JSON string 전달', blank=True, max_length=500)
    user_agent = models.CharField("구매자가 결제를 시작한 단말기의 UserAgent 문자열", blank=True, max_length=500)
    status = models.CharField("결제상태", choices=IamportPaymentStatus.choices, blank=True, max_length=500)
    started_at = models.IntegerField("결제시작시점", help_text='UNIX timestamp, IMP.request_pay() 를 통해 결제창을 최초 오픈한 시각', blank=True, null=True)
    paid_at = models.IntegerField("결제완료시점", help_text='UNIX timestamp, 결제완료가 아닐 경우 0', blank=True, null=True)
    failed_at = models.IntegerField("결제실패시점", help_text='UNIX timestamp, 결제실패가 아닐 경우 0', blank=True, null=True)
    cancelled_at = models.IntegerField("결제취소시점", help_text='UNIX timestamp, 결제취소가 아닐 경우 0', blank=True, null=True)
    fail_reason = models.CharField("결제실패 사유", blank=True, max_length=500)
    cancel_reason = models.CharField("결제취소 사유", blank=True, max_length=500)
    receipt_url = models.CharField("신용카드 매출전표 확인 URL", blank=True, max_length=500)
    cash_receipt_issued = models.BooleanField("현금영수증 자동발급 여부", blank=True, null=True)
    customer_uid = models.CharField(help_text=HELP_CUSTOMER_UID, blank=True, max_length=500)
    customer_uid_usage = models.CharField("customer_uid가 결제처리에 사용된 상세 용도", choices=IamportPaymentCustomerUidUsage.choices, blank=True, max_length=500)

    '''
    cancel_history (Array[PaymentCancelAnnotation], optional): 취소/부분취소 내역 ,
    cancel_receipt_urls (Array[string], optional): (Deprecated : cancel_history 사용 권장) 취소/부분취소 시 생성되는 취소 매출전표 확인 URL. 부분취소 횟수만큼 매출전표가 별도로 생성됨 ,
    '''
