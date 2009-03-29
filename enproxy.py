import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    self.response.out.write( \
'''
<!DOCTYPE html [ PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" ]>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <script language="javascript">

        function p_submit() {
            var scheme = '';
            if (document.main.scheme[0].checked)
                scheme = document.main.scheme[0].value;
            else
                scheme = document.main.scheme[1].value;

            document.p.action = scheme + '://' + 'enproxy.appspot.com/' + urlEncode( document.main.q.value );
            document.p.submit();
            return false;
        }
    </script>
</head>
<body>
    <table border="0" align="center" width="480px">
        <tr class="">
            <td align="center" valign="middle">
				<br/>
				<br/>
				<br/>
				<br/>
                <img src="images/logo.gif" />
                <div style="padding-left: 20px; padding-top: 20px; padding-bottom: 20px">
                    <div>
                        <br />
							<form method="get" accept-charset="utf-8" name="main" onsubmit="return p_submit()">
								<input type="text" name="q" size="40" />
								<input type="submit" value=" Go " />
						    </form>
                        <label>
                            <br />
                            <input type="radio" name="scheme" value="http" checked="checked" />
                        </label>
                        HTTP
                        <label>
                            <input type="radio" name="scheme" value="https" />
                        </label>
                        HTTPS</div>
                </div>
            </td>
        </tr>
        <tr>
            <td align="left" valign="top" style="padding-left: 50px;">
                <a href="http://enproxy.appspot.com">enProxy</a> is a free/fast web proxy base on
                Google App Engine.
                <br />
                <br />
                Why use enProxy ?
                <ul>
                    <li><span style="color: #008000">Keeps your IP address (and your identity) hidden.</span></li>
                    <li><span style="color: #008000">To any place you want to go.</span></li>
                    <li><span style="color: #008000">It's free, fast, stable.</span></li>
                    <li><span style="color: #008000"><a href="http://enproxy.appspot.com">Open source</a>.<br />
                    </span></li>
                </ul>
            </td>
        </tr>
    </table>
</body>
</html>
''')

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
