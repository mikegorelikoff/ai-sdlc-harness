---
layout: default
title: Skill catalog
description: Every installed AI SDLC skill, its purpose, owning module, and authoritative package path.
kicker: Reference · Generated catalog
permalink: /reference/skills/
nav_order: 52
---

This catalog is generated from each package’s `SKILL.md` frontmatter. The linked source is the authoritative execution contract.

<div class="catalog">
{% for skill in site.data.skills %}
  <article class="catalog-item">
    <header><h3><code>{{ skill.id }}</code></h3><span class="meta">{% if skill.modules.size > 0 %}{{ skill.modules | join: " + " }}{% else %}unregistered{% endif %}</span></header>
    <p>{{ skill.description }}</p>
    <p><a href="https://github.com/{{ site.repository }}/blob/main/{{ skill.path }}">Open package contract →</a></p>
  </article>
{% endfor %}
</div>
