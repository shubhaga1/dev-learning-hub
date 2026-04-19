# AWS Lambda — Serverless Functions

## What is Lambda?

Run code without managing servers. You upload a function, AWS runs it on demand.

```
Traditional server:
  EC2 always running → you pay 24/7 even when idle

Lambda:
  Code runs only when triggered → pay per invocation (first 1M free/month)
```

---

## How it works

```
Event Source          Lambda Function        Output
─────────────         ──────────────         ──────
API Gateway     →     handler(event,          → response
S3 upload       →     context) {              → process file
DynamoDB stream →       // your code          → update DB
CloudWatch cron →     }                       → send email
SQS message     →                             → transform data
```

---

## Function anatomy

```javascript
// Node.js handler
exports.handler = async (event, context) => {
  console.log('Event:', JSON.stringify(event));

  // event = what triggered this (HTTP request, S3 event, etc.)
  // context = runtime info (function name, timeout remaining, request ID)

  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Hello from Lambda' })
  };
};
```

```python
# Python handler
def handler(event, context):
    print(f"Received: {event}")
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda'
    }
```

---

## Key Limits

| Setting | Default | Max |
| --- | --- | --- |
| Timeout | 3 seconds | 15 minutes |
| Memory | 128 MB | 10 GB |
| Package size | — | 50 MB zipped / 250 MB unzipped |
| Concurrent executions | 1000 (per account) | request increase |
| /tmp storage | — | 10 GB |

---

## Invocation Types

```
Synchronous:   API Gateway → Lambda → wait for response
               RequestResponse — caller waits

Asynchronous:  S3 event → Lambda → fire and forget
               Event — Lambda queues internally, retries twice on failure

Poll-based:    Lambda polls SQS/Kinesis for messages
               Event source mapping
```

---

## Cold Start vs Warm Start

```
Cold start:
  Lambda not running → AWS provisions container → init runtime → run handler
  Adds 100ms–2s latency (worse for Java/.NET, better for Node/Python)

Warm start:
  Container reused from previous invocation → just run handler
  Much faster

Fix cold starts:
  - Provisioned concurrency (keep N instances warm, costs money)
  - Use smaller runtimes (Node/Python over Java)
  - Keep package size small
  - Move init code outside handler (runs once per container)
```

---

## Lambda + API Gateway Pattern

```
User → HTTPS request → API Gateway → Lambda → DynamoDB
                                         ↓
                                    return JSON → API Gateway → user

API Gateway handles:
  - SSL termination
  - Auth (Cognito, JWT, API keys)
  - Rate limiting / throttling
  - CORS headers
  - Request/response transformation
```

---

## Interview Points

- Lambda is stateless — don't store data in memory between invocations
- Use `/tmp` for temp files within one invocation (wiped after)
- Environment variables for config (not secrets — use Secrets Manager)
- Lambda Layers: shared code/libraries across functions
- Destinations: on success/failure, send event to SNS/SQS/EventBridge
- VPC Lambda: function runs inside your VPC (needs NAT for internet access, adds cold start)
