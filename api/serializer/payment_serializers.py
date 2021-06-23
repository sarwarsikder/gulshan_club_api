from rest_framework import serializers
from  ..models import PostPayment
from api.serializer.user_serializers import UserSerializer


class PaymentSerializer(serializers.ModelSerializer):
    payment_by = UserSerializer(read_only=True)
    payment_to = UserSerializer(read_only=True)
    class Meta:
        model = PostPayment
        fields = ('payment_by', 'payment_to', 'payment_id', 'trx_id', 'amount', 'currency', 'merchant_invoice', 'transaction_status', 'payment_type')