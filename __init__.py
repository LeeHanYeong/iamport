class IamportPaymentChannel(TextChoices):
    pc = 'pc', '(인증방식)PC결제'
    mobile = 'mobile', '(인증방식)모바일결제'
    api = 'api', '정기결제 또는 비인증방식결제'
