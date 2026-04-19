# Day 19 & 20 — Queries in AEM

## Query Languages in AEM

| Language | Use |
| --- | --- |
| **JCR-SQL2** | Modern, SQL-like, recommended |
| **XPath** | Older, still common in legacy code |
| **QueryBuilder** | AEM-specific API, easy to write, translates to XPath |
| **Sling Models + ResourceResolver** | For simple traversal (no query needed) |

---

## QueryBuilder (Most Common in AEM)

```java
import com.day.cq.search.QueryBuilder;
import com.day.cq.search.Query;
import com.day.cq.search.result.SearchResult;
import javax.jcr.Session;
import java.util.HashMap;
import java.util.Map;

@Component
public class ProductSearchService {

    @Reference
    private QueryBuilder queryBuilder;

    public List<Resource> findProductsByCategory(ResourceResolver resolver, String category) {
        Map<String, String> params = new HashMap<>();

        params.put("path",          "/content/mysite");           // search under this path
        params.put("type",          "cq:Page");                   // node type
        params.put("1_property",    "jcr:content/category");      // property to filter
        params.put("1_property.value", category);                 // filter value
        params.put("p.limit",       "50");                        // max results (-1 = all)
        params.put("orderby",       "@jcr:content/jcr:title");    // sort
        params.put("orderby.sort",  "asc");

        Session session = resolver.adaptTo(Session.class);
        Query query = queryBuilder.createQuery(PredicateGroup.create(params), session);
        SearchResult result = query.getResult();

        List<Resource> pages = new ArrayList<>();
        for (Hit hit : result.getHits()) {
            try {
                pages.add(hit.getResource());
            } catch (RepositoryException e) {
                // log error
            }
        }
        return pages;
    }
}
```

---

## QueryBuilder — Common Predicates

```
path            → /content/mysite
type            → cq:Page, nt:file, dam:Asset
fulltext        → search text in all properties
1_property      → property name filter
1_property.value→ property value
daterange       → date range filter
p.limit         → max results
p.offset        → pagination offset
orderby         → sort field
orderby.sort    → asc / desc
```

**Multi-property filter:**
```
1_property       = jcr:content/status
1_property.value = approved
2_property       = jcr:content/type
2_property.value = article
```

---

## JCR-SQL2

```java
String sql = "SELECT * FROM [cq:Page] AS page " +
             "WHERE ISDESCENDANTNODE(page, '/content/mysite') " +
             "AND page.[jcr:content/category] = 'tech' " +
             "ORDER BY page.[jcr:content/jcr:title]";

Session session = resolver.adaptTo(Session.class);
QueryManager qm = session.getWorkspace().getQueryManager();
javax.jcr.query.Query query = qm.createQuery(sql, javax.jcr.query.Query.JCR_SQL2);
query.setLimit(50);
NodeIterator nodes = query.execute().getNodes();

while (nodes.hasNext()) {
    Node node = nodes.nextNode();
    System.out.println(node.getPath());
}
```

---

## XPath

```java
String xpath = "/jcr:root/content/mysite//element(*, cq:Page)" +
               "[@jcr:content/@category='tech'] " +
               "order by @jcr:content/@jcr:title ascending";

javax.jcr.query.Query query = qm.createQuery(xpath, javax.jcr.query.Query.XPATH);
```

---

## Query Debugger

`http://localhost:4502/libs/cq/search/content/querydebug.html`

Test QueryBuilder params, see generated XPath, view explain plan.

---

## Performance Tips

```
1. Always specify 'path' — never query the entire repository
2. Use indexed properties — check Oak indexes at /oak:index
3. Avoid fulltext for structured data — use property predicates
4. Set p.limit — never use -1 on large datasets
5. Use p.guessTotal=true for pagination (faster count estimate)
6. Prefer JCR-SQL2 over XPath for new code
7. Cache results — don't run same query on every request
```

---

## Create Custom Oak Index (for unindexed properties)

```xml
<!-- /oak:index/categoryIndex -->
<jcr:root
    jcr:primaryType="oak:QueryIndexDefinition"
    type="lucene"
    async="async">
  <indexRules jcr:primaryType="nt:unstructured">
    <cq:Page jcr:primaryType="nt:unstructured">
      <properties jcr:primaryType="nt:unstructured">
        <category
            jcr:primaryType="nt:unstructured"
            name="jcr:content/category"
            propertyIndex="{Boolean}true"/>
      </properties>
    </cq:Page>
  </indexRules>
</jcr:root>
```
