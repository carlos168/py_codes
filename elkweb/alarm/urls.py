from django.conf.urls import url, include


from alarm.views import miner

urlpatterns = [
    url(r'miner/add$', miner.Add, ),
    url(r'miner/list$', miner.List, ),

    # url(r'login/register$', login.create_user, ),
    # url(r'login/delete$', login.del_user, ),
    # url(r'login/login$', login.login, ),
    # url(r'login/logout$', login.logout, ),
    # url(r'login/get_verify$', login.get_verify, ),

]
