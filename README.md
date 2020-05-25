## cookie
Gone are the days of `optparse` or fiddling with `sys.argv`. This is 
command line argument parsing that just makes sense.

**installation** `$ python3 install.py` adds the given location of `cookie/` to your system path <br>
**testing** - `$ python3 -m unittest discover` uses standard library test suite

Cookie is design to be super simple and extremely scalable. Just add a gateway
into your Python code and the command line is yours.
```python3
from cookie.cookie import Cookie

app = Cookie(__name__, notes=('my awesome app'))
"""
all your code
"""

@app.get_args
def main (thing1='', thing2=0):
  """
  do things with the things
  using all your code
  """

app.run(main)
```test.py
Meanwhile on the command line...
```
$ 
```
