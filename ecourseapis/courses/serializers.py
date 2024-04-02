from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from courses.models import Category, Course, Lesson, Tag, Comment, User


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemSerializer(ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req["image"] = instance.image.url

        return req


class CourseSerializer(ItemSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "image", "active"]


class LessonSerializer(ItemSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "subject", "image", "created_date"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class LessonDetailSerializer(LessonSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ["content", "tags"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}} # trường password chỉ để đăng ký, đừng đọc, trả về

    def create(self, validated_data): # validate data, hash mật khẩu
        data = validated_data.copy()

        user = User(**data) # tương đương username=User["username"] (giống nhau username nên tự hiểu)
        user.set_password(user.password) # băm password
        user.save()

        return user


class CommentSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ["id", "content", "created_date", "user"]