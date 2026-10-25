# Sesión 25 - API Management y seguridad de APIs multicloud

Baseline educativo para gobernar una API delante de workloads en EKS o AKS. Incluye contrato OpenAPI, OAuth 2.0/OIDC, controles BOLA, throttling, quota, mTLS, WAF, observabilidad y costos.

## Validar localmente

```bash
python3 api/validate_api_policy.py --contract api/openapi.yaml --policy api/gateway-policy.yaml
```

## Prueba negativa

En una copia temporal, elimine authentication.audience. El validator debe finalizar con código distinto de cero.

## Alcance

Los dominios y certificados son placeholders no resolubles. No se incluyen tokens, API keys, secretos ni credenciales Cloud. El XML es un ejemplo de Azure API Management y debe adaptarse antes de desplegar.

## Limpieza

El laboratorio local no crea recursos. En Cloud, elimine custom domains, certificates, WAF associations, stages/APIs, diagnostics y recursos de red solo después de verificar dependencias y retención de logs.
