<!--
Copyright (c) The SimpleFIN Team
See LICENSE for details.
-->

# An example #

Install this (with `python setup.py install` or else `pip install 'git+git://github.com/simplefin/webpath.git@master#egg=webpath'`)

Then run this

```
webpath run
```

And paste it this input (followed by `Ctrl-D`):

```
- action: set
  key: foo
  value:
    - item 1
    - item 2
    - 3
    - some: stuff
      other: stuff
- action: dump
  keys: 
    - foo
```

To see this output:

```
foo:
- item 1
- item 2
- 3
- other: stuff
  some: stuff
```


# Paths #

A path is a list of actions to perform.  As YAML, a path looks like this:

```yaml
- action: http_get
  url: https://www.google.com
- action: user_input
  question: "What do you want to search for?"
  answer: search_term
- action: form_submit
  form_index: 0
  params:
    q: $search_term
```

# Actions #

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
  value: $last_result
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

Dump some variables.  This will set the `$last_result` to a dict of the dumped
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
