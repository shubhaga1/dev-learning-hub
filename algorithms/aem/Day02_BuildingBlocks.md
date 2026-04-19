# Day 02 — AEM Building Blocks

## 5 Core Building Blocks

### 1. Components
Reusable UI pieces. A component = a folder under `/apps/mysite/components/`.

```
/apps/mysite/components/text/
  text.html          ← HTL template (renders HTML)
  _cq_editConfig.xml ← author UI config (drag handles, edit bars)
  .content.xml       ← component definition (title, group, resourceSuperType)
```

Every component has:
- `sling:resourceType` property pointing to its folder
- An HTL template that renders it
- Optional dialog for author configuration

### 2. Templates
Define the structure of a page — which components are allowed where.

```
Editable Templates (modern — stored in /conf):
  Structure    → fixed content authors can't change (header, footer)
  Initial      → default content for new pages
  Policy       → which components are allowed in each container

Static Templates (legacy — stored in /apps):
  /apps/mysite/templates/page/
    .content.xml  ← allowed components, page thumbnail
```

### 3. Dialogs
Author-facing form for configuring a component. Built with Granite UI / Coral UI.

```xml
<!-- _cq_dialog/.content.xml — touch UI dialog -->
<jcr:root>
  <content jcr:primaryType="nt:unstructured" sling:resourceType="granite/ui/components/coral/foundation/container">
    <items>
      <text
        jcr:primaryType="nt:unstructured"
        sling:resourceType="granite/ui/components/coral/foundation/form/textfield"
        fieldLabel="Title"
        name="./title"/>
    </items>
  </content>
</jcr:root>
```

### 4. Clientlibs (Client-side Libraries)
AEM's way of managing and serving CSS/JS.

```
/apps/mysite/clientlibs/site/
  .content.xml     ← categories: ["mysite.base"], dependencies: ["jquery"]
  css/
    styles.css
  js/
    app.js
```

In HTL: `<sly data-sly-use.clientlib="/libs/granite/sightly/templates/clientlib.html">`

### 5. OSGi Bundles
Your Java code packaged as OSGi bundles (JARs with metadata).

```
Bundle = JAR + MANIFEST.MF with:
  Bundle-SymbolicName: com.mysite.core
  Bundle-Version: 1.0.0
  Import-Package: org.apache.sling.api (dependencies)
  Export-Package: com.mysite.core.models (what others can use)
```

---

## How They Connect

```
URL request: /content/mysite/en/home.html

1. Sling resolves /content/mysite/en/home to a JCR node
2. Node has sling:resourceType = "mysite/components/page"
3. Sling finds /apps/mysite/components/page/page.html
4. HTL renders it, includes child components
5. Each child component reads its dialog-saved properties from JCR
```
