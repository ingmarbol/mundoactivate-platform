# Sesión 11 - DevSecOps y escaneos de seguridad

## Objetivo

Añadir controles de seguridad reproducibles al Pull Request de la plataforma ACTIVATE ONLINE. El flujo inspecciona dependencias, secretos y configuraciones antes del merge.

## Alcance

- Trivy filesystem: vulnerabilidades de dependencias, secretos y misconfigurations.
- Gitleaks: detección de secretos con salida redacted.
- Permisos mínimos: `contents: read`.
- Sin deployment, credenciales Cloud ni cambios de infraestructura.

SonarQube se estudia y ejecuta localmente o con SonarQube Cloud porque un GitHub hosted runner no puede acceder a un servidor SonarQube expuesto solo en `localhost`.

## Prueba

1. Abrir un Pull Request hacia `main`.
2. Esperar el job `repository-security`.
3. Revisar el primer step fallido y distinguir un error de herramienta de un finding.
4. Para reproducir localmente:

```bash
trivy fs --scanners vuln,secret --severity HIGH,CRITICAL .
trivy config --severity HIGH,CRITICAL .
gitleaks git --redact --no-banner .
```

## Resultado esperado

El workflow se ejecuta sin secretos reales. Los findings HIGH/CRITICAL bloquean el merge hasta su remediación o una excepción documentada con owner y fecha de caducidad.

## Evidencias

- URL del PR y captura de Checks.
- Versión de las herramientas y fecha del análisis.
- Resumen redacted de findings.
- Decisión de triage: fix, mitigación o excepción temporal.
- Para SonarQube: Quality Gate y métricas de new code, sin publicar el token.

## Seguridad

No se deben versionar archivos `.env`, tokens, claves privadas, certificados, credenciales AWS/Azure ni `*.tfstate`. En producción, las Actions externas deben fijarse por commit SHA completo y actualizarse mediante un proceso revisado.

## Costos

GitHub hosted runners consumen minutos según el plan. `concurrency` cancela ejecuciones obsoletas. SonarQube local requiere CPU, memoria, disco, backups y mantenimiento; SonarQube Cloud depende del plan vigente.

## Limpieza

```bash
docker image rm activate:session-11 || true
docker stop sonarqube || true
docker rm sonarqube || true
```

El volumen `sonarqube_data` conserva información. Eliminarlo solo cuando ya no se necesiten proyectos, configuración ni resultados.
