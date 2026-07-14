# Crypto tools for Testing

A few simple Python scripts to help test Russian PKI stuff, through usage of GOST R 34.11-2012 algorithms.

## server.py

HTTP API that uses OpenSSL with the GOST engine. It acts as a local CA (Certificate Authority) for  tests.

It makes certificates from CSRs, runs an OCSP responder, and works as a TSA (Time Stamping Authority) server.

It automatically adds AIA (OCSP/caIssuers) and CRLDP (CRL Distribution Points) to all new certificates.

It uses an index.txt file to check and show the status of certificates for the OCSP responder.

Swagger UI: `http://localhost:8080/docs/`

See also: [server.md](LocalCA/README.md)

## Windows CSR Generator (generate_csr.py) with CryptoPro CSP and GOST

A python script that creates Certificate Signing Requests (CSR) on Windows.
It uses CryptoPro CSP to support GOST.
Allows to build custom Subject DN with standard Russian OIDs (like INN, OGRN, SNILS).
It saves the CSR as a Base64 or PEM string. You can copy-paste it to CA.

## TSP and OCSP Clients

Two cli tools to send TSP (RFC 3161) and OCSP requests with GOST hash algorithms.

Install deps: `pip install -r requirements.txt`

### Check Certificate Status (OCSP Client)

This tool calculates `issuerNameHash` and `issuerKeyHash` using GOST R 34.11-2012 (both 256-bit and 512-bit).

`python cli.py ocsp http://ocsp.example.com/ocsp.srf user.pem ca.pem`

### Get a Timestamp (TSP Client)

This tool puts a GOST R 34.11-2012 data hash into the TimeStampReq message.

Example

```python
from TSPOCSPCLIENT import TSPClient

# Connect to the TSA server
client = TSPClient("http://tsa.example.com/tsp/tsp.srf")
result = client.timestamp(b"payload", digest_size=256)

print(result.status)  # Example: 'granted' or 'rejection'

if result.tst_info:
    print(result.tst_info["gen_time"].native)
    # Check if the response is correct
    assert client.verify_imprint(b"payload", result, 256)
```

CLI:

`python cli.py tsp http://tsa.example.com/tsp/tsp.srf document.pdf`

This command saves the response files into the ./output folder.

This tool does not validate GOST signatures on OCSP responses or TimeStampTokens (CMS).

Public servers for example:

`http://pki.tax.gov.ru/tsp/tsp.srf`

 `http://tax4.tensor.ru/tsp/tsp.srf`