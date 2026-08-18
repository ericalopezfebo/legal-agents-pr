# Security model

Inputs, model outputs and tool responses are untrusted. Provider credentials are environment configuration and must never appear in agent files, logs or exceptions. Tool adapters should use least privilege, strict schemas, allowlisted endpoints and minimum-necessary disclosure. This repository does not itself anonymize legal documents; use an appropriate local privacy process before external model transmission.

