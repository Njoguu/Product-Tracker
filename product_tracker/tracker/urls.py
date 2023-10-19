from django.urls import path
from .views import *

urlpatterns = [
    path("", view=index, name="index"),
    path("results/", view=results, name="results"),
    path("unique-search-texts/", view=get_unique_search_texts, name="get_unique_search_texts"),
    path("product/<str:name>/", view=get_product_results, name="get_product_results"),
    path("all-results/", view=get_results, name="get_results"),
    path("start-scraper/", view=start_scraper, name="start_scraper"),
    path("add-tracked-product/", view=add_tracked_product, name="add_tracked_product"),
    path("tracked-product/<int:product_id>/", view=toggle_tracked_product, name="toggle_tracked_product"),
    path("tracked-products/", view=get_tracked_products, name="get_tracked_products"),
    path("update-tracked-products/", view=update_tracked_products, name="update_tracked_products")
]