# Day 09 & 10 — Sling Servlets

## What is a Sling Servlet?

REST endpoint in AEM. Handles HTTP requests for specific resource types or paths.

Two types:
1. **Resource-type servlet** — fires when a node with matching `sling:resourceType` is requested
2. **Path servlet** — fires for a specific path

---

## Resource-Type Servlet (Preferred)

```java
package com.mysite.core.servlets;

import org.apache.sling.api.SlingHttpServletRequest;
import org.apache.sling.api.SlingHttpServletResponse;
import org.apache.sling.api.servlets.SlingSafeMethodsServlet;
import org.osgi.service.component.annotations.Component;

import javax.servlet.Servlet;
import java.io.IOException;
import org.apache.sling.servlets.annotations.SlingServletResourceTypes;

@Component(service = Servlet.class)
@SlingServletResourceTypes(
    resourceTypes = "mysite/components/product",   // matches this component
    methods = "GET",
    extensions = "json"                            // only .json requests
)
public class ProductServlet extends SlingSafeMethodsServlet {

    @Override
    protected void doGet(SlingHttpServletRequest request,
                         SlingHttpServletResponse response) throws IOException {

        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");

        String productId = request.getResource().getValueMap()
                              .get("productId", String.class);

        response.getWriter().write("{\"id\":\"" + productId + "\"}");
    }
}
```

**URL**: `/content/mysite/en/home/jcr:content/product.json`

---

## Path Servlet (Use Sparingly)

```java
@Component(service = Servlet.class)
@SlingServletPaths("/bin/mysite/search")    // explicit path
public class SearchServlet extends SlingAllMethodsServlet {

    @Override
    protected void doGet(SlingHttpServletRequest req,
                         SlingHttpServletResponse resp) throws IOException {

        String query = req.getParameter("q");
        // ... search logic
        resp.getWriter().write("{\"results\":[]}");
    }

    @Override
    protected void doPost(SlingHttpServletRequest req,
                          SlingHttpServletResponse resp) throws IOException {
        // handle POST
    }
}
```

**URL**: `http://localhost:4502/bin/mysite/search?q=aem`

---

## SlingSafeMethodsServlet vs SlingAllMethodsServlet

```
SlingSafeMethodsServlet   → GET, HEAD only (read-only operations)
SlingAllMethodsServlet    → GET, HEAD, POST, PUT, DELETE
```

---

## Reading Request Data

```java
// URL param: ?name=Alice
String name = request.getParameter("name");

// Request body (POST JSON)
StringBuilder sb = new StringBuilder();
BufferedReader reader = request.getReader();
String line;
while ((line = reader.readLine()) != null) sb.append(line);
String body = sb.toString();

// Current resource and its properties
Resource resource = request.getResource();
ValueMap props = resource.getValueMap();
String title = props.get("title", "Default Title");

// Session / user
Session session = request.getResourceResolver().adaptTo(Session.class);
String user = request.getResourceResolver().getUserID();
```

---

## Writing JSON Response

```java
import org.apache.sling.commons.json.JSONObject;

JSONObject json = new JSONObject();
json.put("status", "success");
json.put("count", 42);

response.setContentType("application/json");
response.getWriter().write(json.toString());
```

Or use Gson/Jackson:
```java
Gson gson = new Gson();
response.getWriter().write(gson.toJson(myObject));
```

---

## Servlet Registration Pitfalls

```
1. sling:resourceType must match EXACTLY (case-sensitive)
2. Extension matters: .json vs .html are different servlets
3. Path servlets bypass Sling authentication — add your own auth check
4. Always check bundle is Active in OSGi console if servlet isn't firing
```
