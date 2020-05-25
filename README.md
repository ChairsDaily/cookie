## cookie
Gone are the days of `optparse` or fiddling with `sys.argv`. This is 
command line argument parsing that just makes sense.

*Drop /cookie/cookie/ into `/usr/lib/python3/dist-packages`*

**installation** `$ python3 install.py` adds the given location of `cookie/` to your system path <br>
**testing** - `$ python3 -m unittest discover` uses standard library test suite

Cookie is design to be super simple and extremely scalable. Just add a gateway
into your Python code and the command line is yours.
```python3
from cookie.cookie import Cookie

app = Cookie(__name__)
"""
all your code
"""

@app.get_args
def main (thing='', other=0):
  """
  do things with the things
  using all your code
  """

app.run(main)
```
Meanwhile on the command line...
```
$ python3 app.py --help

Usage:  python3 app.py (executable, False)

	something that is used for a thing
	[-t | --thing THING] 
	
	other thing for something
	[-o | --other OTHER] 

$ python3 -m cookie.exec app.py
```
The next time around we can just do `app --help` :)
