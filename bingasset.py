#!/usr/bin/python3
import sys
import requests
import time
import threading
import argparse
import urllib.parse
from bs4 import BeautifulSoup
from urllib.parse import urljoin

domains = []
urls = []

parser = argparse.ArgumentParser(prog = 'BingAsset', description = 'Asset discovery using bing search', epilog = '')

parser.add_argument('-d', '--domain', required=True, help="the domain to look for")
parser.add_argument('-u', '--grab-urls', action="store_true", help="grab urls instead of domain names")

args = parser.parse_args()

domain = ""

if args.domain:
 domain = args.domain

grab_urls = False
if args.grab_urls:
 grab_urls = True

def get_assets(domain_name, count_search=1):
 global domains, urls
 url_search = "https://www.bing.com/search?q={}&first={}".format(urllib.parse.quote_plus("site:{}".format(domain_name)), count_search)
 r = requests.get(url=url_search, timeout=5, allow_redirects=True)
 if r.status_code != 200: return
 soup = BeautifulSoup(r.text, "html.parser")
 links = soup.find_all("a")
 if not links: return
 res = 0
 for i in links:
  domain_curr = i.get("href")
  if not domain_curr: continue
  if not domain_curr.startswith("https://"): continue 
  if not domain_name in domain_curr: continue
  if not domain_curr in urls:
   res += 1
   urls.append(domain_curr)
   if grab_urls: print(domain_curr)   
  dom_d = domain_curr.split("https://")[1]
  if "/" in dom_d: dom_d = dom_d.split("/")[0]
  if not dom_d in domains:
   domains.append(dom_d)
   if not grab_urls: print(dom_d)
   t=threading.Thread(target=get_assets, args=(dom_d,))
   t.start()
 if res > 0:
  get_assets(domain_name, count_search+10)

def main():
 get_assets(domain)
    
if __name__ == "__main__":
 domains.append(domain)
 main()

