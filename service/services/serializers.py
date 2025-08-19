from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from services.models import Subscription, Plan


class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(ModelSerializer):
    plan = PlanSerializer()
    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    price = SerializerMethodField()

    def get_price(self, instance):
        return (instance.service.full_price -
                instance.service.full_price * (instance.plan.discount_percent / 100))

    class Meta:
        model = Subscription
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')
