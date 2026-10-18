# Sesión 22 - Supply Chain Security avanzada

## Objetivo
Verificar integridad y procedencia desde source hasta Kubernetes mediante digests, SBOM, provenance, firma y admission policies.

## Alcance
Artefacto sintético, manifest SHA-256, SBOM CycloneDX simplificado, provenance educativa, verifier dependency-free y prueba de tampering. No sustituye una firma criptográfica real con Cosign o GitHub Artifact Attestations.

## Prueba
`python3 supply-chain/verify_supply_chain.py --artifact supply-chain/artifact/app.txt --manifest supply-chain/manifest.json --sbom supply-chain/sbom.json --provenance supply-chain/provenance.json`

Resultado esperado: SUPPLY CHAIN VERIFIED.

## Prueba negativa
Copiar el artefacto a un directorio temporal, modificar la copia y verificarla. Debe producir artifact digest mismatch y exit code distinto de cero.

## Evidencias
Digest, ejecución válida, rechazo por manipulación, threat model, trusted builder/source policy y plan Audit-to-Enforce para EKS/AKS.

## Seguridad y costos
No contiene credenciales, claves ni datos reales. En CI use OIDC, acciones fijadas por SHA, permisos mínimos e identidad keyless. Considere CI, runners, registry, evidencia, admission HA y egress.

## Limpieza
No crea infraestructura ni costos cloud. Elimine solo la copia temporal modificada.
