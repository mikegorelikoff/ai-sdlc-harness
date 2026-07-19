---
layout: default
title: How-to guides
description: Complete a specific AI SDLC task with bounded steps and an explicit result.
kicker: Solve a task
permalink: /how-to/
nav_order: 10
---

How-to guides are task-oriented. Choose the result you need now; each guide assumes you already understand basic Git and software delivery concepts.

<div class="doc-grid">
{% assign group = site.data.navigation | where: "url", "/how-to/" | first %}
{% for item in group.children %}<a class="doc-card" href="{{ item.url | relative_url }}"><strong>{{ item.title }}</strong><span>Open the focused procedure →</span></a>{% endfor %}
</div>

For a guided learning journey, begin with [Ship a first feature]({{ '/tutorials/first-feature/' | relative_url }}). For exact schemas and command contracts, use [Reference]({{ '/reference/' | relative_url }}).
