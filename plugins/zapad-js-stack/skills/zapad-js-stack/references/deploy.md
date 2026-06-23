# Deploy & compute

AWS Lambda via SST, the colocated model, and the cold-start posture.

## One Lambda, colocated (invariant #4)

The whole SSR app plus all server functions compile into a single Lambda behind CloudFront, with static assets on S3. There is no second service. Build a separate API tier *only* when a second consumer appears (mobile app, public API, high-volume webhooks). Until then, colocated server functions in one repo is the happy path — simpler, fewer hops, faster to ship. Extracting later (into e.g. Hono) is a refactor, not a rewrite, because server functions are just functions.

## Nitro preset & build output (invariant #5)

- Set the Nitro **`aws-lambda` preset explicitly**. The default `node-server` preset outputs an HTTP server, not a Lambda handler, and fails with `Runtime.HandlerNotFound`.
- Build output is `.output/server/` (the Lambda handler) and `.output/public/` (static → S3).
- **Streaming SSR** (`awsLambda: { streaming: true }`) requires a **Lambda Function URL** as the origin, not classic API Gateway REST, which buffers responses. If streaming matters, put a Function URL behind CloudFront.

## Compute posture

- Run the Lambda on **arm64/Graviton** — faster Node cold starts, ~20% cheaper.
- Ship a **ZIP** package, not a container image (containers cold-start slower and can't use snapshot restore).
- Lambda **SnapStart does not support Node.js**, so the cold-start posture is arm64 + a small bundle (`compilerBuild = "small"`, see `data.md`).
- Reach for **provisioned concurrency** only on an app where first-paint latency is critical — it reintroduces an always-on cost.

## SST

- SST's `TanStackStart` component wires up Lambda + CloudFront + S3 and applies the preset.
- Use resource **linking** so attaching an S3 bucket, secret, or RDS Proxy auto-generates the IAM permissions — don't hand-write IAM policies.
- Region is `sa-east-1`; confirm the DB sits behind RDS Proxy before the first deploy.
