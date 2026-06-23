# Cross-cutting services

Email, background jobs, storage, and realtime.

## Email — Amazon SES

- Keep SPF/DKIM/DMARC aligned. Verify the domain, not just individual addresses.

## Background jobs — AWS-native

- EventBridge scheduled rules for cron; SQS for async work triggered by server functions. SST provisions both.
- Reach for Inngest/Trigger.dev only if a project needs durable multi-step workflows that outgrow plain queues.
- **Node 24 gotcha:** the Lambda runtime removed callback-style handlers (`Runtime.CallbackHandlerDeprecated`). Write all custom consumers as `async` handlers with try/catch.

## File storage — S3

- Linked via SST so IAM permissions are generated automatically (see `deploy.md`).

## Realtime

- Out of scope by default. Add only if a project needs it; choose the transport (e.g. API Gateway WebSockets, or a managed service) at that point.
