# Day 16 — Schedulers in AEM

## What are Schedulers?

Run Java code on a schedule (like cron jobs). Built on Apache Sling Scheduler.

Use cases: cleanup tasks, sync with external APIs, cache warming, report generation.

---

## Runnable Scheduler (Simplest)

```java
package com.mysite.core.schedulers;

import org.apache.sling.commons.scheduler.ScheduleOptions;
import org.apache.sling.commons.scheduler.Scheduler;
import org.osgi.service.component.annotations.*;

@Component(immediate = true, service = CleanupScheduler.class)
public class CleanupScheduler implements Runnable {

    @Reference
    private Scheduler scheduler;

    private int schedulerId;

    @Activate
    protected void activate() {
        schedulerId = hashCode();

        ScheduleOptions options = scheduler
            .EXPR("0 0 2 * * ?")  // cron: every day at 2 AM
            .name("cleanup-job-" + schedulerId)
            .canRunConcurrently(false);   // only one instance at a time

        scheduler.schedule(this, options);
    }

    @Deactivate
    protected void deactivate() {
        scheduler.unschedule("cleanup-job-" + schedulerId);
    }

    @Override
    public void run() {
        System.out.println("Running cleanup...");
        // do your work here
    }
}
```

---

## Scheduler with OSGi Config

```java
@Component(immediate = true, service = SyncScheduler.class)
@Designate(ocd = SyncScheduler.Config.class)
public class SyncScheduler implements Runnable {

    @ObjectClassDefinition(name = "Sync Scheduler")
    public @interface Config {
        @AttributeDefinition(name = "Cron Expression")
        String cronExpression() default "0 0/30 * * * ?";  // every 30 min

        @AttributeDefinition(name = "Enabled")
        boolean enabled() default true;
    }

    @Reference
    private Scheduler scheduler;

    private static final String JOB_NAME = "sync-scheduler";

    @Activate @Modified
    protected void activate(Config config) {
        removeScheduler();
        if (config.enabled()) {
            addScheduler(config.cronExpression());
        }
    }

    @Deactivate
    protected void deactivate() {
        removeScheduler();
    }

    private void addScheduler(String cronExpr) {
        ScheduleOptions options = scheduler.EXPR(cronExpr)
            .name(JOB_NAME)
            .canRunConcurrently(false);
        scheduler.schedule(this, options);
    }

    private void removeScheduler() {
        scheduler.unschedule(JOB_NAME);
    }

    @Override
    public void run() {
        // sync logic
        System.out.println("Syncing data at: " + java.time.LocalDateTime.now());
    }
}
```

---

## Cron Expression Format

```
 ┌──── second (0-59)
 │  ┌─── minute (0-59)
 │  │  ┌── hour (0-23)
 │  │  │  ┌─ day of month (1-31)
 │  │  │  │  ┌ month (1-12)
 │  │  │  │  │  ┌ day of week (0-7, 0/7=Sun)
 │  │  │  │  │  │
 0  0  2  *  *  ?    → every day at 2:00 AM
 0  0/30 *  *  *  ?  → every 30 minutes
 0  0  8  ?  *  MON-FRI  → weekdays at 8 AM
 0  0  12  1  *  ?   → 1st of every month at noon
```

---

## Sling Jobs vs Schedulers

| | Scheduler | Sling Job |
| --- | --- | --- |
| Triggered by | Time (cron) | Event / on demand |
| Persistence | No — lost on restart | Yes — survives restart |
| Retry on fail | No | Yes (configurable) |
| Clustering | Runs on each node | Runs on one node |
| Use for | Periodic tasks | Reliable async processing |

See Day 18 for Sling Jobs.
