# Day 11 — Custom OSGi Configuration

## Why OSGi Config?

Externalize settings (URLs, timeouts, feature flags) without redeploying code.
Different values per environment (dev/stage/prod).

---

## Defining Config in Java

```java
package com.mysite.core.services.impl;

import org.osgi.service.component.annotations.*;
import org.osgi.service.metatype.annotations.*;

@Component(service = ApiService.class)
@Designate(ocd = ApiServiceImpl.Config.class)   // link to config schema
public class ApiServiceImpl implements ApiService {

    @ObjectClassDefinition(name = "My Site - API Service Configuration")
    public @interface Config {
        @AttributeDefinition(name = "API Endpoint", description = "Base URL for the API")
        String apiEndpoint() default "https://api.example.com";

        @AttributeDefinition(name = "Timeout (ms)")
        int timeoutMs() default 5000;

        @AttributeDefinition(name = "Enable Cache")
        boolean enableCache() default true;

        @AttributeDefinition(name = "Allowed Domains")
        String[] allowedDomains() default {"example.com", "mysite.com"};
    }

    private String apiEndpoint;
    private int timeoutMs;
    private boolean enableCache;

    @Activate
    @Modified
    protected void activate(Config config) {
        this.apiEndpoint  = config.apiEndpoint();
        this.timeoutMs    = config.timeoutMs();
        this.enableCache  = config.enableCache();
    }

    @Override
    public String getEndpoint() { return apiEndpoint; }
}
```

---

## Config Files (in code — stored in JCR)

Path: `/apps/mysite/config/com.mysite.core.services.impl.ApiServiceImpl.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0"
          xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:primaryType="sling:OsgiConfig"
    apiEndpoint="https://api.mysite.com"
    timeoutMs="{Long}3000"
    enableCache="{Boolean}true"
    allowedDomains="[mysite.com,cdn.mysite.com]"/>
```

---

## Environment-Specific Configs

```
/apps/mysite/
  config/                     ← applies to all run modes
    ...ApiServiceImpl.xml
  config.author/              ← author instance only
    ...ApiServiceImpl.xml
  config.publish/             ← publish instance only
    ...ApiServiceImpl.xml
  config.dev/                 ← dev run mode only
    ...ApiServiceImpl.xml
  config.prod/                ← prod run mode only
    ...ApiServiceImpl.xml
  config.author.dev/          ← author + dev run mode
    ...ApiServiceImpl.xml
```

Run modes set on AEM startup: `-Dsling.run.modes=publish,prod`

---

## Viewing/Editing Config in OSGi Console

`http://localhost:4502/system/console/configMgr`

- Find your service by name
- Edit values inline (saved to `/apps` or `/conf`)
- Restart not needed — `@Modified` method fires automatically

---

## Config as a Service (Inject Anywhere)

```java
// Make the config accessible to other services
@Component(service = SiteConfiguration.class)
@Designate(ocd = SiteConfiguration.Config.class)
public class SiteConfiguration {

    @ObjectClassDefinition(name = "Site Configuration")
    public @interface Config {
        String brandName() default "My Site";
        String supportEmail() default "support@mysite.com";
    }

    private Config config;

    @Activate @Modified
    protected void activate(Config config) { this.config = config; }

    public String getBrandName()    { return config.brandName(); }
    public String getSupportEmail() { return config.supportEmail(); }
}
```

Inject in any other service with `@Reference private SiteConfiguration siteConfig;`
