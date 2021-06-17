from django.shortcuts import render
from . import models
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup

base_url = "https://losangeles.craigslist.org/search/bbb?query={}"
base_img_url = "https://images.craigslist.org/{}_300x300.jpg"

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):   
    # Note req.POST returns a dictionary so use get() method to access its attr
    search = request.POST.get('search')
    models.Search.objects.create(search= search)
    final_url = base_url.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data,features='html.parser')
    
    post_list = soup.find_all('li', {'class': 'result-row'})
    
    final_posting =[]

    for post in post_list:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_posted = post.find(class_='result-date').text
        if post.find(class_='result-price'):
            post_price =post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        
        
        if post.find(class_='result-image').get('data-ids'):
            post_img_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_img_url = base_img_url.format(post_img_id)
        else:
            post_img_url = "https://images.craigslist.org/images/peace.jpg"

        final_posting.append((post_title, post_url,post_posted,post_price,post_img_url))    
    
    # print(final_posting)
    search_text = {
        'search': search,
        'final_posting': final_posting,
    }
    return render(request, 'my_app/new_search.html', search_text)