import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin

s=requests.session()
s.headers["User-Agent"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

def get_forms(url):
    Soup=BeautifulSoup(s.get(url).content,"html.parser")
    return Soup.find_all("form")

def form_details(form):
    detailsOfForm={}
    action=form.attrs.get("action")
    method=form.attrs.get("method","get")
    input=[]
    for input_tag in form.find_all("input"):
        input_type=input_tag.attrs.get("type","text")
        input_name=input_tag.attrs.get("name")
        input_value=input_tag.attrs.get("value","")
        input.append({
            "type":input_type,
            "name":input_name,
            "value":input_value,
        })
    detailsOfForm['action']=action
    detailsOfForm['method']=method
    detailsOfForm['input']=input
    return detailsOfForm

def vulnerable(response):
    errors=("Quoted string not property terminated",
             "unclosed quoted mark after the character string",
             "you have an error in your sql syntax"   )
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

def sql_injection_scan(url):
    forms=get_forms(url)
    print(f"[t] Detected {len(forms)} forms on {url},")

    for form in forms:
        details=form_details(form)

        for i in "\"'":
            data={}
            for input_tag in details["inputs"]:
                if input_tag["type"]=="hidden" or input_tag["value"]:
                    data[input_tag['name']]=input_tag["value"]+i
                elif input_tag["type"]!="submit":
                    data[input_tag["name"]]=f"test{i}"
            print(url)
            form_details(form)
            
            if details["method"]=="post":
                res=s.post(url,data=data)
            elif details["method"]=="get":
                res=s.get(url,params=data)
            if vulnerable(res):
                print("sql injection attack vulnerability in link",url)
            else:
                print("no sql injection attack vulnerability detected")
                break

if __name__=="__main__":
    urlToBeChecked="http://testvulnweb.com"
    sql_injection_scan(urlToBeChecked)


