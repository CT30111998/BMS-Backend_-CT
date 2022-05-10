from rest_framework.serializers import ModelSerializer
from .models import AttendanceMaster, FeedbackMaster
from Auth.serializers import AuthUserSerializer


class AttendanceSerializer(ModelSerializer):
    user = AuthUserSerializer(many=False)
    created_by = AuthUserSerializer(many=False)
    updated_by = AuthUserSerializer(many=False)

    class Meta:
        model = AttendanceMaster
        fields = '__all__'


class FeedbackSerializer(ModelSerializer):

    class Meta:
        model = FeedbackMaster
        fields = '__all__'
