---
name: Plotly multi-chart ordering
description: Loading order bug when embedding several Plotly figures on one page via fig.to_html snippets.
---

When rendering multiple Plotly figures on the same page using
`fig.to_html(full_html=False, include_plotlyjs=..., ...)` snippets stitched
into one template, only one figure should carry `include_plotlyjs="cdn"`
(the others use `False` to avoid loading the library multiple times).

**Why:** Each snippet's `<script>` runs `Plotly.newPlot(...)` immediately in
document order. If the CDN-loading snippet is placed *after* a snippet that
assumes Plotly is already loaded, the earlier chart throws
`ReferenceError: Plotly is not defined` in the browser console even though
the page looks fine at a glance (charts loaded later still render).

**How to apply:** Whichever figure appears first in the rendered HTML must be
the one with `include_plotlyjs="cdn"`, regardless of the order you compute or
build the figures in code. Verify by checking that the CDN `<script src>`
appears before the first `Plotly.newPlot` call in the final HTML output.
