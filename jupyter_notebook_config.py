import os
from IPython.lib import passwd

c = c  # noqa: Global 'c' is created by the IPython runtime
c.NotebookApp.ip = '*'
c.NotebookApp.port = int(os.getenv('PORT', 8888))
c.NotebookApp.open_browser = False
c.MultiKernelManager.default_kernel_name = 'python2'

# sets a password if PASSWORD is set in the environment
if 'PASSWORD' in os.environ:
  c.NotebookApp.password = passwd(os.environ['PASSWORD'])
  del os.environ['PASSWORD']
else:
  c.NotebookApp.password = passwd('advisor')

# Support iframe
#c.NotebookApp.tornado_settings = {'headers': {'X-Frame-Options': 'ALLOW-FROM http://127.0.0.1:8000'}}
c.NotebookApp.tornado_settings = {
    "headers": {
        "Content-Security-Policy":
        "frame-ancestors self http://localhost:8000; report-uri /api/security/csp-report"
    }
}
