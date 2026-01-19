====================================     SAML Lab – Version 1.0   ============================================

A lightweight, containerised SAML 2.0 Service Provider (SP) built with Flask and python3-saml, designed primarily for learning, testing, and experimentation with Microsoft Entra ID (Azure AD).

This project focuses on clarity, observability, and correctness rather than production hardening.

==========================================  Purpose   =======================================================

This lab exists to:

Understand SAML authentication end-to-end

Inspect real SAML claims from Entra ID

Experiment with group → role mapping

Observe session state and lifecycle

Provide a stable baseline for future enhancements

===================================================== Architecture Overview ============================================

Framework: Flask

SAML Library: python3-saml (OneLogin)

IdP: Microsoft Entra ID (Azure AD)

Containerisation: Docker + docker-compose

Auth Flow: SP-initiated SAML login

============================================== Implemented Features (v1.0) ==========================================
1. SAML Authentication (SP-Initiated)

Redirects users to Entra ID for authentication

Processes SAML responses via /acs

Validates assertions and extracts claims
================================================ Environment-Driven Configuration ======================================

Sensitive values are injected via environment variables:

Flask secret key

IdP entity ID

IdP SSO URL

IdP signing certificate

This keeps secrets out of source control and supports containerised deployments.

================================================ Session Management ==============================================

After authentication, the app stores:

NameID

Session Index

Login timestamp (UTC)

Raw SAML attributes

Derived roles

Debug state

Session state is visible and inspectable via the UI.

======================================================== Claims Inspection UI ===================================================
A dedicated Claims page shows:

Identity summary (NameID, Session Index)

Session overview (login time, roles, group count)

Derived roles (from group mapping)

Raw SAML claims (verbatim from Entra ID)

Debug indicators when enabled

This makes the SAML assertion fully transparent.

========================================================  Group → Role Mapping (Foundation) =====================================

Supports mapping Entra group Object IDs to internal roles

Mapping logic is centralized and extensible

Gracefully handles users with no groups or roles

(Currently manual mapping; ready for future automation.)

=================================================== Debug Mode Toggle =================================================== 

Debug state can be toggled at runtime

Enables additional diagnostic visibility without redeploying

Designed for learning and troubleshooting

===================================================  Local Logout =================================================== 

Clears the Flask session cleanly

Always works, regardless of IdP state

===================================================  Federated Logout (Gracefully Handled) =======================================

Supports SAML Single Logout initiation

Defensive fallback ensures logout never breaks the app

If IdP SLO fails, the user is still logged out locally

This avoids fragile failure loops common in SAML SLO implementations.

===================================================  Explicitly Out of Scope (v1.0) ===========================================

These are intentionally not implemented yet:

Production-grade security hardening

HTTPS termination (handled externally if needed)

Metadata endpoint auto-generation

Dynamic certificate rotation

Attribute-based access control (ABAC)

Persistent user storage

Multi-tenant IdP support

=================================================== Intended Usage =================================================== 

This project is ideal for:

Learning SAML deeply (beyond “it works”)

Debugging Entra ID SAML claims

Testing group/role mappings

Prototyping identity-aware applications

Serving as a reference implementation

It is not intended to be dropped into production unchanged.

===================================================  Roadmap / Future Enhancements ============================================

Planned or possible improvements:

IdP certificate rotation awareness

Metadata endpoint (/metadata)

Signed SP requests

Stronger SLO validation

Role-based access enforcement

UI polish and navigation

Test coverage for SAML flows

Optional persistence layer

=================================================== Design Philosophy =================================================== 

Clarity over cleverness

Fail safe, not fragile

Visibility beats abstraction

Working code > perfect code

SAML is complex. This lab embraces that complexity instead of hiding it.

=================================================== Versioning =================================================== 

Current version: v1.0

This version represents:

A stable authentication flow

A known-good baseline

A reference point for future iterations

All future changes will be built on top of this foundation.