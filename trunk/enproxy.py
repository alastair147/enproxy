import os, re
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch

class MainPage(webapp.RequestHandler):
  DisallowedHeaders = [ 'Content-Length', 'Host', 'Referer', 'User-Agent', 'Vary', 'Via', 'X-Forwarded-For' ]
  InitHeaders = [ 'Connection', 'Accept', 'Accept-Charset', 'Accept-Encoding', 'Accept-Language' ]
  HtmlContentTypes = [ 'text/html', 'application/xml+xhtml', 'application/xhtml+xml' ]
  CssContentTypes = [ 'text/css' ]
  
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

  def proxify_css(self, content) :
    return content
##     $css = proxify_inline_css($css);
##
##    preg_match_all("#@import\s*(?:\"([^\">]*)\"?|'([^'>]*)'?)([^;]*)(;|$)#i", $css, $matches, PREG_SET_ORDER);
##
##    for ($i = 0, $count = count($matches); $i < $count; ++$i)
##    {
##        $delim = '"';
##        $url   = $matches[$i][2];
##
##        if (isset($matches[$i][3]))
##        {
##            $delim = "'";
##            $url = $matches[$i][3];
##        }
##
##        $css = str_replace($matches[$i][0], '@import ' . $delim . proxify_css_url($matches[$i][1]) . $delim . (isset($matches[$i][4]) ? $matches[$i][4] : ''), $css);
##    }
##
##    return $css; 
  def proxify_html(self, content) :
    return content
##    //
##    // PROXIFY HTML RESOURCE
##    //
##    
##    $tags = array
##    (
##        'a'          => array('href'),
##        'img'        => array('src', 'longdesc'),
##        'image'      => array('src', 'longdesc'),
##        'body'       => array('background'),
##        'base'       => array('href'),
##        'frame'      => array('src', 'longdesc'),
##        'iframe'     => array('src', 'longdesc'),
##        'head'       => array('profile'),
##        'layer'      => array('src'),
##        'input'      => array('src', 'usemap'),
##        'form'       => array('action'),
##        'area'       => array('href'),
##        'link'       => array('href', 'src', 'urn'),
##        'meta'       => array('content'),
##        'param'      => array('value'),
##        'applet'     => array('codebase', 'code', 'object', 'archive'),
##        'object'     => array('usermap', 'codebase', 'classid', 'archive', 'data'),
##        'script'     => array('src'),
##        'select'     => array('src'),
##        'hr'         => array('src'),
##        'table'      => array('background'),
##        'tr'         => array('background'),
##        'th'         => array('background'),
##        'td'         => array('background'),
##        'bgsound'    => array('src'),
##        'blockquote' => array('cite'),
##        'del'        => array('cite'),
##        'embed'      => array('src'),
##        'fig'        => array('src', 'imagemap'),
##        'ilayer'     => array('src'),
##        'ins'        => array('cite'),
##        'note'       => array('src'),
##        'overlay'    => array('src', 'imagemap'),
##        'q'          => array('cite'),
##        'ul'         => array('src')
##    );
##
##    preg_match_all('#(<\s*style[^>]*>)(.*?)(<\s*/\s*style[^>]*>)#is', $_response_body, $matches, PREG_SET_ORDER);
##
##    for ($i = 0, $count_i = count($matches); $i < $count_i; ++$i)
##    {
##        $_response_body = str_replace($matches[$i][0], $matches[$i][1]. proxify_css($matches[$i][2]) .$matches[$i][3], $_response_body);
##    }
##
##    preg_match_all("#<\s*([a-zA-Z\?-]+)([^>]+)>#S", $_response_body, $matches);
##
##    for ($i = 0, $count_i = count($matches[0]); $i < $count_i; ++$i)
##    {
##        if (!preg_match_all("#([a-zA-Z\-\/]+)\s*(?:=\s*(?:\"([^\">]*)\"?|'([^'>]*)'?|([^'\"\s]*)))?#S", $matches[2][$i], $m, PREG_SET_ORDER))
##        {
##            continue;
##        }
##        
##        $rebuild    = false;
##        $extra_html = $temp = '';
##        $attrs      = array();
##
##        for ($j = 0, $count_j = count($m); $j < $count_j; $attrs[strtolower($m[$j][1])] = (isset($m[$j][4]) ? $m[$j][4] : (isset($m[$j][3]) ? $m[$j][3] : (isset($m[$j][2]) ? $m[$j][2] : false))), ++$j);
##        
##        if (isset($attrs['style']))
##        {
##            $rebuild = true;
##            $attrs['style'] = proxify_inline_css($attrs['style']);
##        }
##        
##        $tag = strtolower($matches[1][$i]);
##
##        if (isset($tags[$tag]))
##        {
##            switch ($tag)
##            {
##                case 'a':
##                    if (isset($attrs['href']))
##                    {
##                        $rebuild = true;
##                        $attrs['href'] = complete_url($attrs['href']);
##                    }
##                    break;
##                case 'img':
##                    if (isset($attrs['src']))
##                    {
##                        $rebuild = true;
##                        $attrs['src'] = complete_url($attrs['src']);
##                    }
##                    if (isset($attrs['longdesc']))
##                    {
##                        $rebuild = true;
##                        $attrs['longdesc'] = complete_url($attrs['longdesc']);
##                    }
##                    break;
##                case 'form':
##                    if (isset($attrs['action']))
##                    {
##                        $rebuild = true;
##                        
##                        if (trim($attrs['action']) === '')
##                        {
##                            $attrs['action'] = $_url_parts['path'];
##                        }
##                        if (!isset($attrs['method']) || strtolower(trim($attrs['method'])) === 'get')
##                        {
##                            $extra_html = '<input type="hidden" name="' . $_config['get_form_name'] . '" value="' . encode_url(complete_url($attrs['action'], false)) . '" />';
##                            $attrs['action'] = '';
##                            break;
##                        }
##                        
##                        $attrs['action'] = complete_url($attrs['action']);
##                    }
##                    break;
##                case 'base':
##                    if (isset($attrs['href']))
##                    {
##                        $rebuild = true;  
##                        url_parse($attrs['href'], $_base);
##                        $attrs['href'] = complete_url($attrs['href']);
##                    }
##                    break;
##                case 'meta':
##                    if ($_flags['strip_meta'] && isset($attrs['name']))
##                    {
##                        $_response_body = str_replace($matches[0][$i], '', $_response_body);
##                    }
##                    if (isset($attrs['http-equiv'], $attrs['content']) && preg_match('#\s*refresh\s*#i', $attrs['http-equiv']))
##                    {
##                        if (preg_match('#^(\s*[0-9]*\s*;\s*url=)(.*)#i', $attrs['content'], $content))
##                        {                 
##                            $rebuild = true;
##                            $attrs['content'] =  $content[1] . complete_url(trim($content[2], '"\''));
##                        }
##                    }
##                    break;
##                case 'head':
##                    if (isset($attrs['profile']))
##                    {
##                        $rebuild = true;
##                        $attrs['profile'] = implode(' ', array_map('complete_url', explode(' ', $attrs['profile'])));
##                    }
##                    break;
##                case 'applet':
##                    if (isset($attrs['codebase']))
##                    {
##                        $rebuild = true;
##                        $temp = $_base;
##                        url_parse(complete_url(rtrim($attrs['codebase'], '/') . '/', false), $_base);
##                        unset($attrs['codebase']);
##                    }
##                    if (isset($attrs['code']) && strpos($attrs['code'], '/') !== false)
##                    {
##                        $rebuild = true;
##                        $attrs['code'] = complete_url($attrs['code']);
##                    }
##                    if (isset($attrs['object']))
##                    {
##                        $rebuild = true;
##                        $attrs['object'] = complete_url($attrs['object']);
##                    }
##                    if (isset($attrs['archive']))
##                    {
##                        $rebuild = true;
##                        $attrs['archive'] = implode(',', array_map('complete_url', preg_split('#\s*,\s*#', $attrs['archive'])));
##                    }
##                    if (!empty($temp))
##                    {
##                        $_base = $temp;
##                    }
##                    break;
##                case 'object':
##                    if (isset($attrs['usemap']))
##                    {
##                        $rebuild = true;
##                        $attrs['usemap'] = complete_url($attrs['usemap']);
##                    }
##                    if (isset($attrs['codebase']))
##                    {
##                        $rebuild = true;
##                        $temp = $_base;
##                        url_parse(complete_url(rtrim($attrs['codebase'], '/') . '/', false), $_base);
##                        unset($attrs['codebase']);
##                    }
##                    if (isset($attrs['data']))
##                    {
##                        $rebuild = true;
##                        $attrs['data'] = complete_url($attrs['data']);
##                    }
##                    if (isset($attrs['classid']) && !preg_match('#^clsid:#i', $attrs['classid']))
##                    {
##                        $rebuild = true;
##                        $attrs['classid'] = complete_url($attrs['classid']);
##                    }
##                    if (isset($attrs['archive']))
##                    {
##                        $rebuild = true;
##                        $attrs['archive'] = implode(' ', array_map('complete_url', explode(' ', $attrs['archive'])));
##                    }
##                    if (!empty($temp))
##                    {
##                        $_base = $temp;
##                    }
##                    break;
##                case 'param':
##                    if (isset($attrs['valuetype'], $attrs['value']) && strtolower($attrs['valuetype']) == 'ref' && preg_match('#^[\w.+-]+://#', $attrs['value']))
##                    {
##                        $rebuild = true;
##                        $attrs['value'] = complete_url($attrs['value']);
##                    }
##                    break;
##                case 'frame':
##                case 'iframe':
##                    if (isset($attrs['src']))
##                    {
##                        $rebuild = true;
##                        $attrs['src'] = complete_url($attrs['src']) . '&nf=1';
##                    }
##                    if (isset($attrs['longdesc']))
##                    {
##                        $rebuild = true;
##                        $attrs['longdesc'] = complete_url($attrs['longdesc']);
##                    }
##                    break;
##                default:
##                    foreach ($tags[$tag] as $attr)
##                    {
##                        if (isset($attrs[$attr]))
##                        {
##                            $rebuild = true;
##                            $attrs[$attr] = complete_url($attrs[$attr]);
##                        }
##                    }
##                    break;
##            }
##        }
##    
##        if ($rebuild)
##        {
##            $new_tag = "<$tag";
##            foreach ($attrs as $name => $value)
##            {
##                $delim = strpos($value, '"') && !strpos($value, "'") ? "'" : '"';
##                $new_tag .= ' ' . $name . ($value !== false ? '=' . $delim . $value . $delim : '');
##            }
##
##            $_response_body = str_replace($matches[0][$i], $new_tag . '>' . $extra_html, $_response_body);
##        }
    
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
    ##logging.debug('[request.headers]' + self.request.headers.items())
    ##logging.debug('[resp.headers]' + headers.items())
    resp = urlfetch.fetch( url, None, urlfetch.GET, headers, False, False );
    ##logging.debug('[resp.headers]' + resp.headers.items())
    ##logging.debug('[Content]' + resp.content)
    
    # filter urls
    if headers['Content-Type'] in HtmlContentTypes :
      content = proxify_html( resp.content )
    elif headers['Content-Type'] in CssContentTypes :
      content = proxify_css( resp.content )
    #else : Content-Length > xxx
      
    # response
    for k, v in resp.headers.iteritems():
        self.response.headers[k] = v
    content = self.AdTop + content
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
