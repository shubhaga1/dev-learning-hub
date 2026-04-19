# Day 07 — Sling Models

## What are Sling Models?

Java classes that map JCR node properties to POJOs. Used from HTL.

Think of it as: **JCR node → Java object → HTL template**

---

## Basic Sling Model

```java
package com.mysite.core.models;

import org.apache.sling.api.resource.Resource;
import org.apache.sling.models.annotations.Model;
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;
import javax.annotation.PostConstruct;

@Model(adaptables = Resource.class)   // adapt from a Resource node
public class TextModel {

    @ValueMapValue                    // reads "title" property from JCR node
    private String title;

    @ValueMapValue(name = "jcr:description")  // different JCR property name
    private String description;

    private String formattedTitle;

    @PostConstruct
    protected void init() {
        // runs after all injections complete
        formattedTitle = title != null ? title.toUpperCase() : "";
    }

    public String getTitle()          { return title; }
    public String getDescription()    { return description; }
    public String getFormattedTitle() { return formattedTitle; }
}
```

**In HTL:**
```html
<sly data-sly-use.model="com.mysite.core.models.TextModel">
    <h1>${model.formattedTitle}</h1>
    <p>${model.description}</p>
</sly>
```

---

## Adaptables

| Adaptable | Use when |
| --- | --- |
| `Resource.class` | Reading component properties from JCR |
| `SlingHttpServletRequest.class` | Need request params, session, user |

```java
@Model(adaptables = SlingHttpServletRequest.class)
public class SearchModel {

    @SlingObject
    private SlingHttpServletRequest request;

    @RequestAttribute
    private String query;             // from request attribute

    public String getQuery() { return request.getParameter("q"); }
}
```

---

## Common Injectors

```java
@ValueMapValue              // JCR property value
@ChildResource              // child node as Resource
@OSGiService                // inject an OSGi service
@SlingObject                // Resource, ResourceResolver, SlingHttpServletRequest
@ScriptVariable             // HTL script variables (currentPage, currentNode)
@Self                       // the model itself (for delegation)
@Via("resource")            // change injection source
```

---

## Injecting OSGi Service into Model

```java
@Model(adaptables = Resource.class)
public class ProductModel {

    @OSGiService
    private ProductService productService;   // injected from OSGi container

    @ValueMapValue
    private String productId;

    public Product getProduct() {
        return productService.findById(productId);
    }
}
```

---

## Model Exporter — JSON API

```java
@Model(
    adaptables = Resource.class,
    resourceType = "mysite/components/product",
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL
)
@Exporter(name = "jackson", extensions = "json")   // expose as JSON
public class ProductModel implements ComponentExporter {

    @ValueMapValue
    private String title;

    @ValueMapValue
    private Double price;

    public String getTitle() { return title; }
    public Double getPrice() { return price; }

    @Override
    public String getExportedType() {
        return "mysite/components/product";
    }
}
```

Access at: `/content/mysite/en/home/jcr:content/product.model.json`

---

## @PostConstruct vs Constructor

```
Constructor    → fields NOT yet injected, don't use them here
@PostConstruct → all @ValueMapValue etc. are injected, safe to use
```
