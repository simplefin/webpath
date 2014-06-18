<!--
Copyright (c) The SimpleFIN Team
See LICENSE for details.
-->

Paths
=====

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
- action:
```

Actions
=======

| Action | Description |
|--------|-------------|
| `http_get` | Make an HTTP GET request |


