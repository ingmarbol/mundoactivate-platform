# Sesión 10: CI/CD con GitHub Actions y Jenkins

## Objetivo

Validar cada cambio de `mundoactivate-platform` mediante Pipeline-as-Code antes del merge a `main`.

## Alcance

- Validación del modelo Docker Compose.
- Construcción de la imagen Docker asociada al commit.
- Workflow de GitHub Actions para Pull Requests y `main`.
- `Jenkinsfile` equivalente para comparación práctica.
- Sin publicación de imágenes ni deployment.

## Prueba local

```bash
cp .env.example .env
docker compose config --quiet
docker build --pull --tag activate:session-10 .
docker image inspect activate:session-10 --format '{{.Id}}'
```

## Resultado esperado

Los comandos terminan con código 0 y el último imprime el identificador `sha256` de la imagen.

## Evidencias

- Check `validate-and-build` en verde.
- Logs de validación y build.
- ID de la imagen creada.
- Diff revisado y sin datos sensibles.

## Seguridad

- `GITHUB_TOKEN` limitado a `contents: read`.
- CI de Pull Request sin secretos ni credenciales Cloud.
- `.env` generado únicamente desde `.env.example`.
- Para producción, fijar las Actions por commit SHA completo y usar OIDC en jobs de deployment separados.

## Costos

La concurrencia cancela ejecuciones obsoletas. Este laboratorio no crea recursos AWS/Azure ni publica imágenes en un registry.

## Limpieza

```bash
docker image rm activate:session-10 || true
rm -f .env
```
