<!--
Copyright (c) The SimpleFIN Team
See LICENSE for details.
-->

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
  iterable: ['jim', 'john', 'james'],
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

## Other actions ##
