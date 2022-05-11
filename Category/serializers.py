from rest_framework.serializers import ModelSerializer
from .models import AttendanceMaster, FeedbackMaster


class FeedbackSerializer(ModelSerializer):

    class Meta:
        model = FeedbackMaster
        fields = '__all__'
