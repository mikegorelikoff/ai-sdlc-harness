---
layout: default
title: Explanation
description: Understand why the harness uses repository evidence, dual artifact layers, adaptive rigor, and explicit authority boundaries.
kicker: Understand the system
permalink: /explanation/
nav_order: 30
---

Explanation pages are understanding-oriented. They describe the design choices behind the workflow so you can adapt it without breaking its safety model.

<div class="doc-grid">
{% assign group = site.data.navigation | where: "url", "/explanation/" | first %}
{% for item in group.children %}<a class="doc-card" href="{{ item.url | relative_url }}"><strong>{{ item.title }}</strong><span>Read the design reasoning →</span></a>{% endfor %}
</div>

For step-by-step outcomes, use [How-to guides]({{ '/how-to/' | relative_url }}). For exact paths, schemas, and commands, use [Reference]({{ '/reference/' | relative_url }}).
