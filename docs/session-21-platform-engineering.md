# Sesión 21 - Platform Engineering e Internal Developer Platforms

## Objetivo
Convertir las capacidades de MundoActivate en un producto interno mediante golden paths, catálogo, self-service, guardrails y scorecards.

## Alcance
Catálogo local de dos servicios, policy ponderada, guardrails bloqueantes y evaluator dependency-free. No utiliza cuentas cloud.

## Prueba
Ejecute:
`python3 platform/evaluate_scorecard.py --catalog platform/catalog.yaml --policy platform/scorecard-policy.yaml`

Resultado esperado: learning-api 100/100, notification-worker 87/100 y PLATFORM SCORECARD PASSED.

## Prueba negativa
En una copia temporal deje owner vacío o cambie secret_scan a false. El evaluator debe mostrar el guardrail y terminar con exit code no cero.

## Evidencias
Diagrama del IDP, salidas positiva y negativa, umbral, guardrails block/warn/inform y métricas de adopción y flujo.

## Seguridad y costos
No contiene secretos ni PII. Un IDP real debe usar SSO/MFA, OIDC, least privilege, audit, artefactos firmados y separación por ambiente. Evalúe TCO de portal, plugins, upgrades, runners, observability y soporte.

## Limpieza
No crea infraestructura. Elimine solo las copias temporales de la prueba negativa.
