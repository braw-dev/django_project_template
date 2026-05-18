# Billing and merchant-of-record posture for EU customers

This template defaults to a provider-backed billing model using Polar.

## Default posture

If you keep the default billing flow:

- **Polar is the merchant of record** for checkout transactions
- **Polar issues invoices, receipts, refunds, and tax documents**
- **your Django app stores local billing state** only for product access, support workflows, and webhook-backed synchronization

That means the local `Customer`, `Product`, `Subscription`, `Entitlement`, and `WebhookEvent` tables in Django are **not** the legal or accounting source of truth for customer billing documents.

## What to tell EU customers

For procurement or security review questionnaires, generated projects should answer these points explicitly and honestly:

- **Who is the contracting party for checkout and card processing?** Polar, as merchant of record, unless you replace the default billing provider setup
- **Who issues invoices and tax documents?** Polar
- **Where is billing-related customer data stored?** In the providers and infrastructure you actually configure for the project; document the real locations in your trust pages and subprocessors list
- **What happens if Polar coverage or suitability changes?** Replace the provider-backed billing integration for future billing flows rather than treating the local Django billing models as the merchant of record

## Project-specific follow-up required

Before launch, replace this generic explanation with project-specific details:

- your legal entity or operator name
- the providers you actually use
- where customer and billing data is stored or processed
- what fallback plan exists if billing-provider requirements change for your market

If you later move away from Polar, update this document, the pricing copy, the billing README, and your trust pages together.
