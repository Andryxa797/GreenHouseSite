from django.urls import path, include
from rest_framework.routers import SimpleRouter
from house.views import DataHouseViewSet, HomeView, DataView, DataTableView, user_login, user_logout, \
    user_register, lk_view, followers_view, OwnerViewSet

router = SimpleRouter()
router.register(r'api-owner', OwnerViewSet)
router.register(r'api-data/(?P<owner>[^/.]+)', DataHouseViewSet)

urlpatterns = [
    path('login/', user_login, name='MyLogin'),
    path('logout/', user_logout, name='MyLogout'),
    path('register/', user_register, name='MyRegister'),

    path("", HomeView.as_view(), name='home'),
    path("data/<slug:owner_name>/<int:count_value_chart>/", DataView.as_view(), name='data_detail'),
    path("data/<slug:owner_name>/table/<slug:category>/", DataTableView.as_view(), name='data_detail_table'),
    path("lk/", lk_view, name='lk'),
    path("lk/followers/", followers_view, name='followers'),

]

urlpatterns += router.urls
