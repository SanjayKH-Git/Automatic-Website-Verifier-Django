from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import requests
import os
import mimetypes
from django.views.static import serve
# Create your views here.
def index(request):
    # return HttpResponse("AutoWeb")
    return render(request, 'index.html')

#filename=""

def VerifyWeb(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file-upload']
        print(uploaded_file)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        print(uploaded_file.name)

        ex_file = pd.read_excel(name)
        Active_series = pd.Series([])
        content_series = pd.Series([])
        for sl, webLink in enumerate(ex_file['WebsiteLink'].values):
            try:
                status_code = requests.head(webLink).status_code
                if status_code == 200:
                    Active_series[sl] = "yes"
                    page = requests.get(webLink)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    for title in soup.find_all('title'):
                        content_series[sl] = title.get_text()
                else:
                    Active_series[sl] = "No"

            except Exception:
                Active_series[sl] = "No"

        ex_file = pd.DataFrame(ex_file)
        ex_file['Active'] = Active_series
        ex_file['Content'] = content_series
        ex_file.to_excel(name, index=False)
        VerifyWeb.fileurl = fs.url(name)
        print(VerifyWeb.fileurl)
        print("done")
        return render(request, 'Verified.html')
#fl_path=""
def download(request):
    print("dow")
    filepath= VerifyWeb.fileurl
    print(filepath)
    #print(os.path.basename(filepath))
    #print(os.path.dirname(filepath))
    return serve(request, os.path.basename(filepath), os.getcwd())

#ff=VerifyWeb.fileurl