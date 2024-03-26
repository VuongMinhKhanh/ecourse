from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from courses.models import Category, Course, Lesson, User
from courses.serializers import CategorySerializer, CourseSerializer, LessonDetailSerializer, UserSerializer
from courses import serializers, pagination


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    pagination_class = pagination.CoursePaginator

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queryset = queryset.filter(name__icontains=q)

        cate_id = self.request.query_params.get("category_id")
        if cate_id:
            queryset = queryset.filter(category_id=cate_id)

        return queryset

    @action(methods=["get"], url_path="lessons", detail=True)
    def get_lesson(self, request, pk):
        lessons = self.get_object().lessons.filter(active=True)
        return Response(serializers.LessonSerializer(lessons, many=True).data,
                        status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related("tags").filter(active=True)
    serializer_class = LessonDetailSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ] # nhận dữ liệu là file