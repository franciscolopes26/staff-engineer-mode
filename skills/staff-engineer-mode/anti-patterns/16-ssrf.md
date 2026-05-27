# RF-28: SSRF (Server-Side Request Forgery)

> Cross-reference: SKILL.md → Red Flag Detection Catalog → RF-28

## Detection

Grep for `requests.get(url)`, `httpx.get(url)`, `fetch(url)`, `urllib.request.urlopen(url)` where `url` traces back to a request body, query parameter, or webhook payload. Code review red flag: any endpoint named like `/fetch`, `/proxy`, `/preview`, `/og-tags`, `/import-from-url`, or "webhook validator" that does not pass the URL through an allow-list and a private-IP filter before issuing the outbound call.

## Smell

```python
# POST /api/fetch-image  { "url": "https://..." }
# "Users want to import their avatar from any URL."

@app.post("/api/fetch-image")
def fetch_image(payload: dict):
    url = payload["url"]
    resp = requests.get(url, timeout=5)
    return Response(
        content=resp.content,
        media_type=resp.headers.get("content-type", "application/octet-stream"),
    )

# Attacker sends:
#   POST /api/fetch-image
#   { "url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/ec2-role" }
#
# The pod runs on EC2. The metadata service answers from the link-local
# address with the role's temporary AWS credentials, and our endpoint
# faithfully proxies them back in the response body. The attacker now
# has AccessKeyId + SecretAccessKey + SessionToken for the role,
# typically with S3, DynamoDB, and Secrets Manager permissions.
```

## Why this fails in production

SSRF turns any "fetch a URL on the user's behalf" feature into a portal to your VPC — the attacker pivots from the public internet to your cloud metadata service, internal admin panels on `10.x` and `172.16.x`, Redis on `127.0.0.1:6379`, the Kubernetes API on `10.96.0.1`, or staging databases that only allow internal traffic. The 2019 Capital One breach exfiltrated 100M customer records this exact way: an SSRF on a WAF reached the EC2 metadata endpoint, lifted IAM credentials, and walked into S3. A blocklist on the host string is not enough — DNS rebinding and IPv6-mapped addresses (`::ffff:169.254.169.254`) bypass naive checks.

## Fix

```python
import ipaddress
import socket
from urllib.parse import urlparse

ALLOWED_HOSTS = {"cdn.example.com", "uploads.example.com"}
BLOCKED_NETS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


def validate_outbound_url(raw: str) -> str:
    parsed = urlparse(raw)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("only http(s) is allowed")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"host not in allow-list: {parsed.hostname}")

    # Resolve AFTER allow-list check to defeat DNS rebinding: even if the
    # name is allowed, the A/AAAA record must not point at a private range.
    for family, _type, _proto, _canon, sockaddr in socket.getaddrinfo(
        parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80)
    ):
        ip = ipaddress.ip_address(sockaddr[0])
        if any(ip in net for net in BLOCKED_NETS):
            raise ValueError(f"host resolves to private range: {ip}")
    return raw


@app.post("/api/fetch-image")
def fetch_image(payload: dict):
    url = validate_outbound_url(payload["url"])
    # allow_redirects=False — a 302 to 169.254.169.254 would re-open the hole.
    resp = requests.get(url, timeout=5, allow_redirects=False)
    return Response(content=resp.content, media_type=resp.headers.get("content-type"))
```

## Reasoning

Every outbound call from a server is an attack surface; the network identity of the caller (your VPC, your IAM role, your service mesh) is exactly what an external attacker is trying to borrow. Validation belongs at the egress boundary just as input validation belongs at the ingress boundary — and the validation must survive DNS resolution, redirects, and IPv6 alternate encodings.

## Citation

- OWASP Top 10 (2021), A10 Server-Side Request Forgery; PortSwigger Web Security Academy — "SSRF attacks".
- *Release It!*, Michael Nygard (2nd ed., 2018), ch. 4 "Stability Anti-Patterns" — Integration Points (every outbound integration is also an attack surface).

## See also

- @scripts/threat-model.md
- @SECURITY.md
- @references/release-it.md
