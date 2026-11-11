# Sesión 32 - Threat Modeling y Secure Architecture Review

El laboratorio modela la plataforma multicloud desde la perspectiva de un atacante, identifica amenazas STRIDE y valida que los riesgos críticos tengan owner, respuesta, controles y criterios verificables.

## Ejecutar

```bash
python3 -m pip install pyyaml
python3 threat-model/validate_threat_model.py \
  --architecture threat-model/architecture.yaml \
  --threats threat-model/threats.yaml
```

Resultado esperado: `RESULT: THREAT MODEL VALID`.

## Prueba negativa

Sobre una copia temporal, cambie `TM-001` de `status: mitigated` a `status: open`. Su riesgo es 4 x 5 = 20, por lo que el validador debe rechazar el modelo.

## Evidencias

- Diagrama con componentes, flujos y trust boundaries.
- Registro STRIDE con attack paths y assets.
- Cálculo de riesgo y respuesta por amenaza.
- Controles mapeados a AWS, Azure y Kubernetes.
- Acceptance criteria que puedan automatizarse.
- Salida positiva y prueba negativa.

## Seguridad, costos y limpieza

No incluya nombres reales de usuarios, IP privadas sensibles, tokens, credenciales, Secret objects, archivos `.env`, claves privadas ni `*.tfstate`. El laboratorio es local. Elimine solo las copias temporales; conserve el modelo versionado como living document.

