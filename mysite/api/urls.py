from rest_framework.routers import SimpleRouter

from .views import PostView, ProfileView, AuthorView

router = SimpleRouter()
router.register('posts', PostView)
router.register('profile', ProfileView)
router.register('authors', AuthorView, basename='users')

urlpatterns = router.urls