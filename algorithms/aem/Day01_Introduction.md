# Day 01 — Introduction to AEM

## What is AEM?

Adobe Experience Manager — enterprise CMS built on:
- **Apache Sling** (REST-ful web framework, maps URLs to content nodes)
- **Apache Felix** (OSGi container — manages bundles/plugins at runtime)
- **Apache Jackrabbit Oak** (JCR — Java Content Repository, the database)

```
AEM Stack:
  Your Code (Components, Servlets, Services)
       ↓
  Apache Sling  (URL routing, resource resolution)
       ↓
  Apache Felix  (OSGi runtime, dependency injection)
       ↓
  Apache Jackrabbit Oak  (JCR content tree — stores everything as nodes)
```

---

## Why AEM?

- Content stored as **nodes in a tree** (not rows in a table)
- Authors drag-drop components to build pages (no code needed for content)
- Built-in DAM (Digital Asset Management) for images/videos
- Multi-site manager — manage 100s of sites from one place
- Workflows for content approval before publish

---

## AEM Architecture — Author vs Publish

```
Author Instance  →  (Replication)  →  Publish Instance  →  CDN  →  User
  (content team                        (public traffic)
   creates here)
```

- **Author**: where editors create/edit content. Not public-facing.
- **Publish**: what users see. Receives replicated content from Author.
- **Dispatcher**: Apache server in front of Publish — caches pages, security layer.

---

## Content as a Tree (JCR)

Everything in AEM is a node:

```
/content
  /mysite
    /en
      /home           (cq:Page)
        /jcr:content  (cq:PageContent)
          title = "Home"
          sling:resourceType = "mysite/components/page"
```

- **cq:Page** — a page node
- **jcr:content** — holds the actual properties of the page
- **sling:resourceType** — maps node to a component (like a controller)

---

## Key Takeaway

> AEM = Content Tree (JCR) + URL Routing (Sling) + Plugin System (OSGi)

Everything else builds on these three.
