#  Deployment Strategy: Project Guardian

## Overview
To prevent PII leakage across Flixkart’s infrastructure, the PII Detector & Redactor should be deployed as a **real-time data sanitization layer**. The goal is to intercept sensitive data before it reaches internal logs, APIs, or user-facing applications—without introducing significant latency.


##Recommended Deployment Layer: API Gateway Plugin

### Why the API Gateway?
- **Centralized control** over all incoming and outgoing traffic
- **Low latency** redaction before data hits backend services
- **Scalable** across microservices and external integrations
- **Minimal code changes** required for existing applications

### Integration Strategy
- Embed the Python-based PII detection logic as a plugin in an API Gateway like **Kong**, **NGINX**, or **Envoy**
- Use a lightweight microservice to handle JSON payloads and return redacted responses
- Apply redaction before logging, caching, or forwarding requests


## Alternative Option: Sidecar Container

### Use Case
- Attach to services that handle sensitive customer data (e.g., order processing, user profiles)
- Redacts PII before logs are written or data is forwarded to analytics pipelines

### Benefits
- **Service-specific control**
- **Easy rollback**
- **Compatible with Kubernetes and containerized environments**


##  Deployment Flow

1. **Ingress Layer** receives API request
2. **Gateway Plugin** invokes PII Redactor
3. **Redacted Payload** forwarded to backend services
4. **Sanitized Logs** stored securely
5. **Alerts** triggered if unredacted PII is detected

## Future Enhancements

- Integrate with **SIEM tools** for real-time alerting
- Add **NER-based detection** for unstructured logs
- Extend to **Browser Extensions** for internal admin tools
- Deploy as a **DaemonSet** for system-wide log sanitization

## Summary

| Criteria         | API Gateway Plugin | Sidecar Container |
|------------------|--------------------|-------------------|
| Latency Impact   | Low                | Moderate          |
| Scalability      | High               | Medium            |
| Integration Ease | High               | Medium            |
| Cost Efficiency  | High               | Medium            |

The API Gateway plugin offers the best balance of performance, coverage, and simplicity for Flixkart’s infrastructure.
