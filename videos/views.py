from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Video


class CourseListView(generic.ListView):
    template_name = "videos/course_list.html"
    queryset = Course.objects.all()


class CourseDetailView(generic.DetailView):
    template_name = "videos/course_detail.html"
    queryset = Course.objects.all()


class VideoDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "videos/video_detail.html"

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        course = self.get_course()
        subscription = self.request.user.subscription
        pricing_tier = subscription.pricing
        subscription_is_active = subscription.status == "active" or subscription.status == "trialing" 
        context.update({
            "has_permission": pricing_tier in course.pricing_tiers.all() and subscription_is_active
        })
        return context

    def get_course(self):
        return get_object_or_404(Course, slug=self.kwargs["slug"])

    def get_object(self):
        video = get_object_or_404(Video, slug=self.kwargs["video_slug"])
        return video

    def get_queryset(self):
        course = self.get_course()
        return course.videos.all()
        