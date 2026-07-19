---
layout: default
title: Reference
description: Look up exact workflow, capability, artifact, flag, schema, validation, layout, and compatibility contracts.
kicker: Technical reference
permalink: /reference/
nav_order: 50
---

Reference pages are information-oriented. They favor stable names, paths, tables, and command contracts over narrative guidance.

<div class="doc-grid">
{% assign group = site.data.navigation | where: "url", "/reference/" | first %}
{% for item in group.children %}<a class="doc-card" href="{{ item.url | relative_url }}"><strong>{{ item.title }}</strong><span>Open the contract →</span></a>{% endfor %}
</div>

For rationale, use [Explanation]({{ '/explanation/' | relative_url }}). For a bounded procedure, use [How-to guides]({{ '/how-to/' | relative_url }}).
