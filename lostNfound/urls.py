from django.urls import path

from . import views

app_name = "lostNfound"
urlpatterns = [
    path("",views.index,name="index"),
    path("login/",views.login,name="login"),
    path("file_report/<int:criminal_id>/",views.file_report,name="file_report"),
    path("report/",views.report,name="report"),
    path("Register/",views.Register,name="Register"),
    path("Registration/",views.Registration,name="Registertion"),
    path("person/<int:person_id>/",views.see_Person,name="see_Person"),
    path("claim/<int:claim_id>/",views.see_Claim,name="see_Claim"),
    path("<int:item_id>/initiate_dissolve/",views.initiate_dissolve,name="initiate_dissolve"),
    path("dissolve_Request/",views.dissolve_Request,name="dissolve_Request"),
    path("dissolve_claim/",views.dissolve_claim,name="dissolve_claim"),
    path("search/",views.search,name="search"),
    path("search_result/",views.search_result,name="search_result"),
    path("<int:item_id>/",views.item,name="item"),
    path("<int:item_id>/<int:claim_id>/",views.see_claim,name="see_claim"),
    path("<int:item_id>/claim/",views.claim,name="claim"),
    path("<int:item_id>/make_claim/",views.make_claim,name="make_claim"),
    path("make_Request/",views.make_Request,name="make_Request"),
    path("Request/",views.Request,name="Request"),
]