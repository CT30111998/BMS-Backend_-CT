from rest_framework.serializers import ModelSerializer
from Auth.serializers import AuthUserSerializer
from .models import ShiftMaster


# class UserDepartmentSerializer(ModelSerializer):
#     # department = AuthUserSerializer(many=False)
#     user = AuthUserSerializer(many=False)
#     # created_by = AuthUserSerializer(many=False)
#     # updated_by = AuthUserSerializer(many=False)
#
#     class Meta:
#         model = UserDepartment
#         fields = ('user',)


class ShiftSerializer(ModelSerializer):
    created_by = AuthUserSerializer(many=False)
    updated_by = AuthUserSerializer(many=False)

    class Meta:
        model = ShiftMaster
        fields = '__all__'
