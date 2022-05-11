from rest_framework.serializers import ModelSerializer
from User.models import UserMaster


class UserSerializer(ModelSerializer):
    class Meta:
        model = UserMaster
        fields = '__all__'


# class UserPermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserPermission
#         fields = '__all__'

    # def to_representation(self, instance):
    #     self.fields['user_id'] = AuthUserSerializer(read_only=True)
    #     return super(UserSerializer, self).to_representation(instance)


