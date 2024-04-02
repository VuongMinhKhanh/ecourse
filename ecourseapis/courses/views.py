from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from courses.models import Category, Course, Lesson, User, Comment
from courses.serializers import CategorySerializer, CourseSerializer, LessonDetailSerializer, UserSerializer, CommentSerializer
from courses import serializers, pagination, my_permission


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

    def get_permissions(self):
        if self.action in ["add_comment"]:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=["get"], url_path="comments", detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.select_related("user").order_by("-id")
        # self.paginator.paginate_queryset(queryset, self.request, view=self)
        paginator = pagination.CommentPaginator()
        page = paginator.paginate_queryset(comments, request)

        if page:
            serializer = serializers.CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(serializers.CommentSerializer(comments, many=True).data)

    # @action(methods=["post"], url_path="comments", detail=True)
    # def add_comment(self, request, pk):
    #     c = self.get_object().comment_set.create(content=request.data.get("content"), user=request.user)
    #
    #     return Response(serializers.CommentSerializer(c))


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ] # nhận dữ liệu là file

    def get_permissions(self):
        if self.action in ["get_current_user"]:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=["get, patch"], url_path="current-user", detail=False)
    def get_current_user(self, request):
        user = request.user

        if request.method.__eq__("patch"):
            for k, v in request.data.items():
                setattr(user, k, v)
                user.save()

        return Response(serializers.UserSerializer(user).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [my_permission.CommentPermissonUser]