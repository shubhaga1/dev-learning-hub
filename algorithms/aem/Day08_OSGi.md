# Day 08 — OSGi Components and Services

## What is OSGi?

Plugin system for Java. Lets you install/uninstall/update modules (bundles) at runtime without restart.

AEM uses **Apache Felix** as the OSGi container.

```
OSGi Container (Felix)
  ├── Bundle: com.mysite.core (your code)
  ├── Bundle: org.apache.sling.api
  ├── Bundle: com.adobe.cq.wcm.core.components
  └── Bundle: org.apache.jackrabbit.oak
```

---

## Bundle vs Component vs Service

```
Bundle   = JAR file with OSGi metadata. Unit of deployment.
Component = Java class managed by OSGi (annotated with @Component)
Service   = Interface registered in OSGi service registry. Others can look it up.
```

---

## Defining a Service

```java
// Interface
package com.mysite.core.services;

public interface EmailService {
    void sendEmail(String to, String subject, String body);
}
```

```java
// Implementation
package com.mysite.core.services.impl;

import org.osgi.service.component.annotations.Component;
import com.mysite.core.services.EmailService;

@Component(service = EmailService.class)   // registers as OSGi service
public class EmailServiceImpl implements EmailService {

    @Override
    public void sendEmail(String to, String subject, String body) {
        // send email logic
        System.out.println("Sending to: " + to);
    }
}
```

---

## Consuming a Service

```java
@Component(service = NotificationComponent.class)
public class NotificationComponent {

    @Reference                         // OSGi injects the service
    private EmailService emailService;

    public void notifyUser(String email) {
        emailService.sendEmail(email, "Welcome", "Hello from AEM");
    }
}
```

---

## OSGi Component Lifecycle

```
@Activate   → called when component is started (bundle started, config available)
@Deactivate → called when component is stopped
@Modified   → called when OSGi config changes (without restart)
```

```java
@Component(service = CacheService.class, immediate = true)
public class CacheServiceImpl implements CacheService {

    private Map<String, Object> cache;

    @Activate
    protected void activate(ComponentContext context) {
        cache = new HashMap<>();
        System.out.println("Cache activated");
    }

    @Deactivate
    protected void deactivate() {
        cache.clear();
        System.out.println("Cache cleared");
    }
}
```

---

## Multiple Implementations — Service Ranking

```java
@Component(service = PaymentService.class, property = {
    "service.ranking:Integer=100"     // higher = preferred
})
public class StripePaymentService implements PaymentService { ... }

@Component(service = PaymentService.class, property = {
    "service.ranking:Integer=10"
})
public class PayPalPaymentService implements PaymentService { ... }
```

When code injects `@Reference PaymentService`, it gets the highest-ranked one.

---

## OSGi Console

`http://localhost:4502/system/console/bundles` — see all bundles, their state

Bundle states:
- **Active** — running normally
- **Resolved** — installed but not started (missing dependency?)
- **Installed** — JAR uploaded but dependencies not met
- **Fragment** — extends another bundle

**Most common issue**: bundle stuck in "Installed" = missing Import-Package dependency.
Check: `/system/console/depfinder`
