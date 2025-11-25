# {{ category_name }} Summary

## Articles:
{% for article in articles %}
- [{{ article.title }}]({{ article.path }})
  - Summary: {{ article.summary }}
{% endfor %}