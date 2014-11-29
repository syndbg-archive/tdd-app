from django.conf.urls import patterns, url

urlpatterns = patterns('lists.views',
                       url(r'^(\d+)/$', 'view_list', name='view_list'),
                       url(r'^new$', 'new_list', name='new_list'),
                       url(r'^users/(.+)$', 'my_lists', name='my_lists')
                       )
