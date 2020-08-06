from rest_framework.routers import DefaultRouter
from project.apps.posts.views import PostsViewSet

router = DefaultRouter()
router.register(r'', PostsViewSet, basename='posts')
urlpatterns = router.urls