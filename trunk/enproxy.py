import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch

class MainPage(webapp.RequestHandler):
  DisallowedHeaders = [ 'Content-Length', 'Host', 'Referer', 'User-Agent',
                        'Vary', 'Via', 'X-Forwarded-For']

  InitHeaders = ['Connection', 'Accept', 'Accept-Charset', 'Accept-Encoding'
                 'Accept-Language']

  AdTop = '''
<script type="text/javascript"><!--
google_ad_client = "pub-7330597899926046";
/* 728x90, enProxy */
google_ad_slot = "4639958458";
google_ad_width = 728;
google_ad_height = 90;
//-->
</script>
<script type="text/javascript"
src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
'''
  
  def error2(self, msg) : 
    self.redirect('/index.py')
    
  def proxy(self, url, initHeader):
    # parse url
    if 0 > url.find('://'):
      url = 'http://' + url

    # fill header
    headers = {}
    if initHeader == True :
      for k, v in self.request.headers.iteritems():
        if k in self.InitHeaders:
          headers[k] = v
    else :
      for k, v in self.request.headers.iteritems():
        if k in self.DisallowedHeaders:
          continue
        headers[k] = v
      
    # fetch url
    resp = urlfetch.fetch( url, None, urlfetch.GET, headers, False, False );

    # filter urls
    # response
    for k, v in resp.headers.iteritems():
        self.response.headers[k] = v
    content = self.AdTop + resp.content
    self.response.out.write(content)

  def get(self):
    url = self.request.get("url")
    self.proxy( url, False )
        
  def post(self):
    url = self.request.get("url")
    self.proxy( url, True )
            
application = webapp.WSGIApplication(
                                     [('/enproxy.py', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
