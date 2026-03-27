====================================
SAML Lab – Version 1.0
====================================

A lightweight, containerised SAML 2.0 Service Provider (SP) built with Flask and python3-saml, designed for hands-on learning, testing, and experimentation with Microsoft Entra ID.

This project leans into clarity, visibility, and real-world behaviour over production polish, it’s a lab you can actually *understand*, not just run.

------------------------------------

## Purpose

This lab exists to:

* Understand SAML authentication end-to-end
* Inspect real SAML claims from Entra ID
* Experiment with group → role mapping
* Observe session state and lifecycle
* Provide a stable foundation for future identity experiments

------------------------------------

## Architecture Overview

* **Framework:** Flask
* **SAML Library:** python3-saml (OneLogin)
* **Identity Platform:** Microsoft Entra ID (Azure AD / External ID)
* **Containerisation:** Docker + docker-compose
* **Auth Flow:** SP-initiated SAML login

------------------------------------

## What’s New (v1.0+)

Beyond standard Entra ID authentication, this lab now supports **social identity federation** via Entra External ID.

Users can now sign in using:

* Google
* Facebook

This means anyone can test the application using their own personal accounts — no need for a corporate Entra tenant user.

👉 Apple ID support is planned and will be added in a future iteration.

Under the hood, all social authentication is still routed through Entra ID, keeping the architecture consistent with enterprise SSO patterns.

-------------------------------------

## Implemented Features (v1.0)

### SAML Authentication (SP-Initiated)

* Redirects users to Entra ID for authentication
* Processes SAML responses via `/acs`
* Validates assertions and extracts claims

-------------------------------------

## Environment-Driven Configuration

All sensitive values are injected via environment variables:

* Flask secret key
* IdP entity ID
* IdP SSO URL
* IdP signing certificate

No secrets are hardcoded. This keeps the project portable and container-friendly.

-------------------------------------

## Session Management

After authentication, the app stores:

* NameID
* Session Index
* Login timestamp (UTC)
* Raw SAML attributes
* Derived roles
* Debug state

Session data is fully visible via the UI for inspection.

------------------------------------

## Claims Inspection UI

A dedicated Claims page provides:

* Identity summary (NameID, Session Index)
* Session overview (login time, roles, group count)
* Derived roles (from group mapping)
* Raw SAML claims (exactly as issued by Entra ID)
* Debug indicators when enabled

Nothing is hidden — what Entra sends is exactly what you see.

-------------------------------------

## Group → Role Mapping (Foundation)

* Maps Entra group Object IDs to internal roles
* Centralised and easy to extend
* Handles users with no groups safely

(Currently manual mapping — ready for automation later.)

--------------------------------------

## Debug Mode Toggle

* Can be switched on/off at runtime
* Adds extra diagnostic visibility
* No redeploy required

------------------------------------

## Logout Behaviour

### Local Logout

* Clears Flask session reliably
* Always works regardless of IdP state

### Federated Logout (SLO)

* Attempts full SAML logout via Entra ID
* Fails gracefully if IdP logout fails
* Never breaks the user session flow

------------------------------------

## Explicitly Out of Scope (v1.0)

This is intentionally a lab, not a production system:

* No production-grade hardening
* No HTTPS termination (handled externally)
* No metadata auto-generation
* No dynamic certificate rotation
* No ABAC / advanced authorization
* No persistence layer
* No multi-tenant IdP routing

------------------------------------

## Intended Usage

This project is ideal for:

* Learning SAML beyond surface-level setups
* Debugging Entra ID SAML claims
* Testing federation scenarios (including social login)
* Prototyping identity-aware applications
* Serving as a clean reference implementation

------------------------------------

## Roadmap / Future Enhancements

* Apple ID integration
* Metadata endpoint (`/metadata`)
* Certificate rotation awareness
* Signed SAML requests
* Role-based access enforcement
* UI improvements
* Optional persistence layer
* Expanded identity provider support

------------------------------------

## Open Source & Contribution

This project is open source and available for anyone to use, learn from, and improve.

Contributions are welcome — whether it’s fixing bugs, improving the UI, or extending identity integrations.

If you’ve ever wrestled with SAML in the wild, you already know: shared knowledge makes this space better.

A permissive open-source license is included to encourage collaboration and reuse.

------------------------------------

## Versioning

**Current version:** v1.0

This version represents:

* A stable SAML authentication flow
* Social login via Entra External ID (Google & Facebook)
* A reliable baseline for future enhancements

------------------------------------

## v1.01

* Introduced mandatory enforcement for `givenName` and `surname` attributes
* Ensures identity completeness for downstream processing


