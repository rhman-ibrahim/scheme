from django.urls import path
from .views import (
    templates, membership, space
)


app_name    = "team"
urlpatterns = [

    # Templates
    path('membership/<int:id>/', templates.member, name="member"),
    path('settings/', templates.founder, name="founder"),
    path('', templates.index, name="index"),
    
    # Membership
    path('logout/', membership.log_out, name="logout"),
    path('update/membership/<int:id>/', membership.refresh, name="update_membersihp"),
    path('login/', membership.log_in, name="login"),
    path('leave/', membership.leave, name="leave"),
    
    # Space
    path('create/', space.instance, name="instance"),
    path('terminate/member/<int:id>', space.terminate, name="terminate"),
    path('import/friends/', space.friends, name="friends"),
    path('transfer/', space.transfer, name="transfer"),
    path('delete/', space.delete, name="delete")

]