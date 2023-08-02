from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models  import *
import json
import subprocess

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the index page")

def results(request):
    if request.method == "POST":
        results = request.json.get('data')
        search_text = request.json.get('search_text')
        source = request.json.get('source')

        for result in results:
            ProductResult.objects.create(
                name = result['name'],
                url = result['url'],
                img = result['img'],
                price = result['price'],
                search_text = search_text,
                source = source
        )
            
        response = {"message": "Received Data Successfully"}
        return JsonResponse(response, status=200)
    
    elif request.method == "GET":
        search_text = request.GET.get('search_text')
        results = ProductResult.objects.all().filter(search_text=search_text).order_by('-created_at')

        product_dict = {}
        for result in results:
            url = result.url
            if url not in product_dict:
                product_dict[url] = {
                    'name': result.name,
                    'url': result.url,
                    'img': result.img,
                    'source': result.source,
                    'created_at': result.created_at,
                    'priceHistory': []
                }

                product_dict[url]['priceHistory'].append({
                    'price': result.price,
                    'date': result.created_at
                })

        formatted_results = list(product_dict.values())
        

        return JsonResponse (formatted_results, safe=False)
    
        # response = {"message": "Invalid Request"}
        # return JsonResponse(response, status=400)

def get_unique_search_texts(request):
    if request.method == "GET":
        unique_search_texts = ProductResult.objects.values("search_text").distinct()
        unique_search_texts =[text[0] for text in unique_search_texts]

        return JsonResponse(unique_search_texts, safe=False)
        
def get_results(request):
    results = ProductResult.objects.all()
    product_results = []
    for result in results:
        product_results.append({
            'name': result.name,
            'url': result.url,
            'price': result.price,
            'img': result.img,
            'date': result.created_at,
            'created_at': result.created_at, 
            'search_text': result.search_text,
            'source': result.source 
        })

    return JsonResponse(product_results, safe=False)

def start_scraper(request):
    if request.method == "POST":
        url = request.json.get('url')
        search_text = request.json.get('search_text')

        # TODO: Add run scraper separately
        command = f"python ../scraper/__init__py {url} \"{search_text}\" /results"
        subprocess.Popen(command, shell=True)

        response = {"mesage": "scraper started successfully"}
        return json.dumps(response), 200
    
def add_tracked_product(request):
    if request.method == "POST":
        name = request.json.get("name")
        tracked_product = TrackedProducts(name=name)
        TrackedProducts.objects.create(tracked_product)

        response = {"message": "TRacked product added successfully", "id": tracked_product.id}

        return json.dumps(response)
    
def toggle_tracked_product(request, product_id):
    if request.method == "PUT":
        tracked_product = TrackedProducts.objects.query(product_id)
        if tracked_product is None:
            response = {"message", "Tracked product not found"}
            return json.dumps(response), 404
    
        tracked_product.tracked = not tracked_product.tracked

        response = {"message": "Tracked product toggled successfully"}
        return json.dumps(response), 200
    
def get_tracked_products(request):
    tracked_products = TrackedProducts.objects.all()

    results = []
    for product in tracked_products:
        results.append({
            "id": product.id,
            "name": product.name,
            "created_at": product.created_at,
            "tracked": product.tracked
        })

    return JsonResponse(results, safe=False)

def update_tracked_products(request):
    if request.method == "POST":
        tracked_products = TrackedProducts.objects.all()
        url = "https://amazon.ca" #TODO: change url

        product_names = []
        for tracked_product in tracked_products:
            name = tracked_product.name
            if not tracked_product.tracked:
                continue

            # TODO: Add run scraper separately
            command = f"python ../scraper/__init__py {url} \"{name}\" /results"
            subprocess.Popen(command, shell=True)

            product_names.append(name)
        
        response = {"message":"Scrapers started successfully", "products":product_names}

        return json.dumps(response), 200
    