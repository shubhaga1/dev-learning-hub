# Day 06 — HTL and Clientlibs

## HTL (HTML Template Language)

AEM's templating language. Replaces JSP. Prevents XSS by design.

```html
<!-- Basic expression -->
${properties.title}

<!-- With XSS context -->
${properties.description @ context='html'}    <!-- allow HTML tags -->
${properties.url @ context='uri'}             <!-- safe URL encoding -->
${properties.text @ context='text'}           <!-- plain text, default -->

<!-- Conditional -->
<div data-sly-test="${properties.title}">
    <h1>${properties.title}</h1>
</div>

<!-- Loop -->
<ul>
    <li data-sly-list.item="${properties.items}">${item}</li>
</ul>

<!-- Include another component -->
<sly data-sly-include="header.html"/>

<!-- Use a Java model -->
<sly data-sly-use.model="com.mysite.core.models.TextModel">
    <p>${model.formattedText}</p>
</sly>

<!-- Resource inclusion -->
<sly data-sly-resource="${'path/to/resource' @ resourceType='mysite/components/text'}"/>
```

---

## HTL Context Rules (XSS Protection)

| Context | When to use |
| --- | --- |
| `text` | Default — plain text, HTML-encoded |
| `html` | Rich text — trust author HTML |
| `uri` | href, src, action attributes |
| `scriptString` | Inside JS strings |
| `styleToken` | CSS property values |
| `attribute` | HTML attribute values |

**Never skip context** — it's your XSS protection.

---

## data-sly-use — Bind to Java/JS Logic

```html
<!-- Use Sling Model -->
<sly data-sly-use.text="com.mysite.core.models.TextModel">
    <div class="${text.cssClass}">
        ${text.title}
    </div>
</sly>

<!-- Use HTL Use-API (JS) -->
<sly data-sly-use.helper="helper.js">
    ${helper.message}
</sly>
```

---

## Clientlibs

AEM manages CSS/JS through client libraries. Handles:
- Minification
- Dependency ordering
- Category-based inclusion

```
/apps/mysite/clientlibs/site/
  .content.xml
  css/styles.css
  js/app.js
```

**.content.xml:**
```xml
<jcr:root
    jcr:primaryType="cq:ClientLibraryFolder"
    categories="[mysite.site]"
    dependencies="[jquery, granite.utils]"/>
```

**Include in HTL page template:**
```html
<sly data-sly-use.clientlib="/libs/granite/sightly/templates/clientlib.html"
     data-sly-call="${clientlib.all @ categories='mysite.site'}"/>

<!-- Or separately -->
<sly data-sly-call="${clientlib.css @ categories='mysite.site'}"/>  <!-- in <head> -->
<sly data-sly-call="${clientlib.js  @ categories='mysite.site'}"/>  <!-- before </body> -->
```

---

## css.txt and js.txt

Control file load order within a clientlib:

```
# css.txt
#base=css
styles.css
components/button.css
components/nav.css
```

```
# js.txt
#base=js
utils.js
app.js
```

Files listed top-to-bottom = load order.

---

## Clientlib Categories Strategy

```
mysite.base     → reset, variables, typography (loaded on every page)
mysite.site     → main site CSS/JS
mysite.author   → author-only styles (loaded in edit mode only)
mysite.vendor   → third-party libs
```

Use `embed` to inline another clientlib:
```xml
embed="[mysite.vendor, mysite.base]"
```
