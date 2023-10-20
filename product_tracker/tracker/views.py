from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from .models  import *
import json
import subprocess
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
def index(request):
    return render(request,"index.html")

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
        page_number = request.GET.get('page', 1)  # Get the requested page number, default to 1 if not provided
        results_per_page = request.GET.get('results_per_page', 10)  # Set the number of results per page
        search_text = request.GET.get('search_text', '')

        results = ProductResult.objects.filter(search_text=search_text).order_by('-created_at')

        if not results.exists():
            return JsonResponse({'message': "no results found for the specified search_text"}, status=404) 

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

        # Paginate the results
        paginator = Paginator(formatted_results, int(results_per_page))

        try:
            paginated_results = paginator.page(page_number)
        except EmptyPage as err:
            return JsonResponse({'error': f'{err}'}, status=400)

        serialized_results = []
        for result in paginated_results:
            serialized_results.append(result)

        context = {
            "results": serialized_results,
            'meta': {
                'total_pages': paginator.num_pages,
                'total_results': paginator.count,
                'current_page': paginated_results.number,
            }
        }

        return JsonResponse(context, safe=False)

def get_unique_search_texts(request):
    if request.method == "GET":
        page_number = request.GET.get('page', 1)  # Get the requested page number, default to 1 if not provided
        results_per_page = request.GET.get('results_per_page', 5)  # Set the number of results per page

        unique_search_texts = ProductResult.objects.values("search_text").distinct()

        # Paginate the results
        paginator = Paginator(unique_search_texts, int(results_per_page))

        try:
            paginated_results = paginator.page(page_number)
        except EmptyPage as err:
            return JsonResponse({'error': f'{err}'}, status=400)

        serialized_data =[text['search_text'] for text in paginated_results]

        context = {
            "search_texts": serialized_data,
            'meta': {
                'total_pages': paginator.num_pages,
                'total_results': paginator.count,
                'current_page': paginated_results.number,
            }
        }

        return JsonResponse(context, safe=False)
        
def get_results(request):
    page_number = request.GET.get('page', 1)  # Get the requested page number, default to 1 if not provided
    results_per_page = request.GET.get('results_per_page', 10)  # Set the number of results per page

    results = ProductResult.objects.all()

    # Paginate the results
    paginator = Paginator(results, results_per_page)

    try:
        paginated_results = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({'error': 'Invalid page number'}, status=400)

    serialized_results = []

    for result in paginated_results:
        serialized_results.append({
            'name': result.name,
            'url': result.url,
            'price': result.price,
            'img': result.img,
            'date': result.created_at,
            'created_at': result.created_at, 
            'search_text': result.search_text,
            'source': result.source 
        })

    context = {
        "results": serialized_results,
        'meta': {
            'total_pages': paginator.num_pages,
            'total_results': paginator.count,
            'current_page': paginated_results.number,
        }
    }

    return JsonResponse(context, safe=False)

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
    page_number = request.GET.get('page', 1)  # Get the requested page number, default to 1 if not provided
    results_per_page = request.GET.get('results_per_page', 5)  # Set the number of results per page
    
    tracked_products = TrackedProducts.objects.all()
    
    paginator = Paginator(tracked_products, int(results_per_page))

    try:
        paginated_results = paginator.page(page_number)
    except EmptyPage as err:
        return JsonResponse({'error': f'{err}'}, status=400)
    
    serialized_results = []

    for product in paginated_results:
        serialized_results.append({
            "id": product.id,
            "name": product.name,
            "created_at": product.created_at,
            "tracked": product.tracked
        })

    context = {
        "results": serialized_results,
        'meta': {
            'total_pages': paginator.num_pages,
            'total_results': paginator.count,
            'current_page': paginated_results.number,
        }
    }

    return JsonResponse(context, safe=False)

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


def get_product_results(request, name):
    # product_name = name
    results = ProductResult.objects.filter(name=name).order_by('-created_at')

    product_dict = {}

    for result in results: 
        name = result.name
        if name not in product_dict:
            product_dict[name] = {
                'name': result.name,
                'url': result.url,
                'img': result.img,
                'price': result.price,
                'source': result.source,
                'created_at': result.created_at,
                'priceHistory': []
            }

        product_dict[name]['priceHistory'].append({
            'price': result.price,
            'date': result.created_at
        })

    formatted_results = list(product_dict.values())

    if len(formatted_results) < 1:
        return JsonResponse({"message": "no product with that name"}, safe=False)
        
    return JsonResponse (formatted_results[0], safe=False)