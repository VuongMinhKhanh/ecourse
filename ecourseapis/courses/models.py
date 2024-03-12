from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    avatar = CloudinaryField(null=True)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Course(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = RichTextField()
    image = CloudinaryField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = "__all__"


class Lesson(BaseModel):
    class Meta:
        unique_together = ("subject", "course")

    subject = models.CharField(max_length=255)
    content = RichTextField()
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name="lessons",
        related_query_name="my_lesson"
    )

    tags = models.ManyToManyField("Tag", blank=True, related_name="lessons")

    def __str__(self):
        return self.subject


class Tag(BaseModel):
    name = models.CharField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name


class Interaction(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Comment(Interaction):
    content = models.CharField(max_length=255)


class Like(Interaction):
    class Meta:
        unique_together = ("lesson", "user")
