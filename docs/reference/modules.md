---
layout: default
title: Module catalog
description: Installed capability modules, compatibility ranges, dependencies, and registered skills.
kicker: Reference · Generated catalog
permalink: /reference/modules/
nav_order: 53
---

<div class="catalog">
{% for module in site.data.modules %}
  <article class="catalog-item">
    <header><h3>{{ module.name }}</h3><span class="meta">{{ module.kind }} · v{{ module.version }}</span></header>
    <p>{{ module.description }}</p>
    <p><strong>Harness API:</strong> ≥ {{ module.harness_min }} and &lt; {{ module.harness_max_exclusive }}</p>
    <p><strong>Requires:</strong> {% if module.requires.size > 0 %}{{ module.requires | join: ", " }}{% else %}none{% endif %}</p>
    <p><strong>Skills:</strong> {{ module.skills | join: ", " }}</p>
    <p><a href="https://github.com/{{ site.repository }}/blob/main/{{ module.manifest_path }}">Open manifest →</a></p>
  </article>
{% endfor %}
</div>

Module discovery validates schema, ID uniqueness, dependency presence, API compatibility, skill paths, and protected capability rules before navigation exposes a module.
