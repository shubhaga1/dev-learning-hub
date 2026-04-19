# Day 05 — Develop AEM Components and Templates

## Creating a Component

Minimum files needed:

```
/apps/mysite/components/helloworld/
  .content.xml          ← registers the component
  helloworld.html       ← HTL template
```

**.content.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:jcr="http://www.jcp.org/jcr/1.0"
          xmlns:cq="http://www.day.com/jcr/cq/1.0"
    jcr:primaryType="cq:Component"
    jcr:title="Hello World"
    componentGroup="My Site"/>
```

**helloworld.html (HTL):**
```html
<div class="helloworld">
    <h2>${properties.title @ context='html'}</h2>
    <p>${properties.description}</p>
</div>
```

`properties` is auto-available — reads from the component's JCR node.

---

## Dialog — Let Authors Configure the Component

```
/apps/mysite/components/helloworld/
  _cq_dialog/
    .content.xml   ← Coral UI dialog definition
```

```xml
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0"
          xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:primaryType="nt:unstructured"
    jcr:title="Hello World Dialog"
    sling:resourceType="cq/gui/components/authoring/dialog">
  <content sling:resourceType="granite/ui/components/coral/foundation/fixedcolumns">
    <items jcr:primaryType="nt:unstructured">
      <column sling:resourceType="granite/ui/components/coral/foundation/container">
        <items jcr:primaryType="nt:unstructured">
          <title
              jcr:primaryType="nt:unstructured"
              sling:resourceType="granite/ui/components/coral/foundation/form/textfield"
              fieldLabel="Title"
              name="./title"
              required="{Boolean}true"/>
          <description
              jcr:primaryType="nt:unstructured"
              sling:resourceType="granite/ui/components/coral/foundation/form/textarea"
              fieldLabel="Description"
              name="./description"/>
        </items>
      </column>
    </items>
  </content>
</jcr:root>
```

When author fills dialog → AEM saves `title` and `description` properties on the component node → HTL reads them via `properties`.

---

## Editable Templates (Modern Approach)

Stored in `/conf/<site>/settings/wcm/templates/`.

Three layers:
1. **Structure** — fixed zones (header, footer). Locked for authors.
2. **Initial Content** — pre-populated components when page is created.
3. **Layout Container policy** — allowed components per parsys (paragraph system).

```
Template structure:
  /conf/mysite/settings/wcm/templates/page/
    structure/       ← jcr:content with locked components
    initial/         ← jcr:content with default content
    policies/        ← which components allowed where
    thumbnail.png    ← preview in template picker
```

---

## resourceSuperType — Component Inheritance

```xml
<!-- Override just one method, inherit the rest from Core Components -->
<jcr:root
    jcr:primaryType="cq:Component"
    jcr:title="Custom Text"
    sling:resourceSuperType="core/wcm/components/text/v2/text"/>
```

Like Java extends — your component only needs to override what's different.
HTL uses `data-sly-use` to delegate to parent rendering.

---

## Component Groups

```xml
componentGroup="My Site"      <!-- shows in component browser under "My Site" -->
componentGroup=".hidden"      <!-- hides from browser (base components) -->
```
