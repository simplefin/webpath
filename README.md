<!--
Copyright (c) The SimpleFIN Team
See LICENSE for details.
-->

# Installation #

Since `lxml` is a dependency, you'll need `libxml2` and `libxslt` installed.
Then, if you have the repo checked out, do this:

```
python setup.py install
```

Or install with `pip`:

```
pip install 'git+git://github.com/simplefin/webpath.git@master#egg=webpath'
```

# An example #

Run this

```bash
webpath run --output-format=json
```

And paste this set of steps to GET `https://www.google.com` then dump out a list
of all the HTML forms on the page  (After pasting, press `Ctrl-D`):

```yaml
- action: http
  kwargs:
    method: get
    url: https://www.google.com
- action: http.getForms
  html: $_.text
- action: set
  key: forms
  value: $_
- action: dump
  keys: 
    - forms
```

To see something like this output:

```json
{
  "forms": [
    {
      "html": "<form action=\"/search\" name=\"f\"><table cellpadding=\"0\" cellspacing=\"0\"><tr valign=\"top\"><td width=\"25%\">&#160;</td><td align=\"center\" nowrap><input name=\"ie\" value=\"ISO-8859-1\" type=\"hidden\"><input value=\"en\" name=\"hl\" type=\"hidden\"><input name=\"source\" type=\"hidden\" value=\"hp\"><div class=\"ds\" style=\"height:32px;margin:4px 0\"><input style=\"color:#000;margin:0;padding:5px 8px 0 6px;vertical-align:top\" autocomplete=\"off\" class=\"lst\" value=\"\" title=\"Google Search\" maxlength=\"2048\" name=\"q\" size=\"57\"></div><br style=\"line-height:0\"><span class=\"ds\"><span class=\"lsbb\"><input class=\"lsb\" value=\"Google Search\" name=\"btnG\" type=\"submit\"></span></span><span class=\"ds\"><span class=\"lsbb\"><input class=\"lsb\" value=\"I'm Feeling Lucky\" name=\"btnI\" onclick=\"if(this.form.q.value)this.checked=1; else top.location='/doodles/'\" type=\"submit\"></span></span></td><td class=\"fl sblc\" align=\"left\" nowrap width=\"25%\"><a href=\"/advanced_search?hl=en&amp;authuser=0\">Advanced search</a><a href=\"/language_tools?hl=en&amp;authuser=0\">Language tools</a></td></tr></table><input id=\"gbv\" name=\"gbv\" type=\"hidden\" value=\"1\"></form>", 
      "data": {
        "q": "", 
        "btnI": "I'm Feeling Lucky", 
        "btnG": "Google Search", 
        "gbv": "1", 
        "source": "hp", 
        "hl": "en", 
        "ie": "ISO-8859-1"
      }, 
      "form": {
        "action": "/search", 
        "name": "f"
      }
    }
  ]
}
```

# Actions #

These are the available actions.  It's also not terribly difficult to add
your own actions.

## Control actions ##

### `loop` ###

Iterate over a list of things, performing a set of actions on them.  The
`$item` variable will be each item within the context of the loop.

- `iterable`: Thing to iterate over.
- `actions`: List of actions to do per item in `iterable`

For instance:

```yaml
- action: loop
  iterable: ['jim', 'john', 'james']
  actions:
    - action: dosomething
      thing: $item
```


### `set` ###

Set a variable.

- `key`: Name of the variable to set.
- `value`: Value to set the variable to.

```yaml
- action: set
  key: foo
  value: foo value
- action: set
  key: alsofoo
  value: $_
```


### `ask` ###

Ask a user for some data.  The result might be cached by the system running
this if the system wants to.  The result is stored in a variable.

- `key`: Name of variable to set.
- `prompt`: Human-readable prompt.

```yaml
- action: ask
  key: user_id
  prompt: "What is your user id?"
```


### `dump` ###

Dump some variables.  This will set the `$_` to a dict of the dumped
variables.

- `keys`: List of keys to dump.

```yaml
- action: set
  key: soccer
  value: "Is awesome"
- action: dump
  keys:
    - soccer
```


## Web actions ##


### `http` ###

Make a web request using the [Python `requests` library](http://docs.python-requests.org/)
This will set `$_` to a `requests` Response object.  So if you want the content
of the response use `$_.text`.

- `kwargs`: A dictionary that will be passed unchanged to `requests.request`

```yaml
- action: http
  kwargs:
    method: get
    url: https://www.google.com
```


### `http.getForms` ###

Get a list of forms from an HTML document.

- `html`: HTML string from which to get the forms.

```yaml
- action: http.getForms
  html: "<form><input name="something" value="something"></form>"
```
