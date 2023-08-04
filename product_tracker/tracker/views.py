from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from .models  import *
import json
import subprocess
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the index page")

@csrf_exempt
def results(request):
    if request.method == "POST":
        data = json.loads(request.body)
        results = data.get('data')
        search_text = data.get('search_text')
        source = data.get('source')

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
        search_text = request.GET.get('search_text', '')
        results = ProductResult.objects.filter(search_text=search_text).order_by('-created_at')

        if not results.exists():
            return JsonResponse({'messagae': "No results found for the specified search_text"}, status=404) 

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
        unique_search_texts =[text['search_text'] for text in unique_search_texts]

        return JsonResponse({'search_text': unique_search_texts}, safe=False)
        
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

@csrf_exempt
def start_scraper(request):
    if request.method == "POST":
        data = json.loads(request.body)
        url = data.get('url')
        search_text = data.get('search_text')

        # TODO: Add run scraper separately
        command = f"python ../web-scraper/__init__.py {url} \"{search_text}\" /results"
        subprocess.Popen(command, shell=True)

        response = {"mesage": "scraper started successfully"}
        return JsonResponse(response, status=200)
    
@csrf_exempt    
def add_tracked_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        
        try:
            tracked_product = TrackedProducts(name=name)
            tracked_product.save()
            response = {"message": "Tracked product added successfully", "id": tracked_product.id}
            return JsonResponse(response, status=201)
        
        except IntegrityError:
            response = {"error": "Product with this name already exists"}
            return JsonResponse(response, status=400)

@csrf_exempt    
def toggle_tracked_product(request, product_id):
    if request.method == "PUT":
        tracked_product = TrackedProducts.objects.get(id=product_id)
        if tracked_product is None:
            response = {"message", "Tracked product not found"}
            return JsonResponse(response, status=404)
    
        tracked_product.tracked = not tracked_product.tracked
        tracked_product.save()

        response = {"message": "Tracked product toggled successfully"}
        return JsonResponse(response, status=204)
    
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

@csrf_exempt
def update_tracked_products(request):
    if request.method == "POST":
        tracked_products = TrackedProducts.objects.all()
        url = "https://www.jumia.co.ke/" 

        product_names = []
        for tracked_product in tracked_products:
            name = tracked_product.name
            if not tracked_product.tracked: 
                continue

            # TODO: Add run scraper separately
            command = f"python ../web-scraper/__init__.py {url} \"{name}\" /results"
            subprocess.Popen(command, shell=True)

            product_names.append(name)
        
        response = {"message":"Scrapers started successfully", "products":product_names}

        return JsonResponse(response, status=200)
    