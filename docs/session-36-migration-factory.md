# Sesión 36 - Cloud Migration Factory y Application Modernization multicloud

Laboratorio del proyecto **Plataforma multicloud segura y observable**. Convierte un inventario de aplicaciones, dependencias y requisitos RTO/RPO en waves con gates de seguridad, costos, cutover, rollback, hypercare y decommission.

## Ejecutar

    python3 migration-factory/validate_migration_factory.py \
      --inventory migration-factory/application-inventory.yaml \
      --waves migration-factory/wave-plan.yaml \
      --policy migration-factory/migration-policy.yaml

Resultado esperado: RESULT: MIGRATION FACTORY PLAN VALID.

## Prueba negativa

En una copia temporal de wave-plan.yaml, cambie business_validation_required a false. El validator debe devolver INVALID.

## Evidencias

- Inventario y dependency map sin credenciales ni datos reales.
- Decisión 7R por workload.
- Wave plan y criterios de entrada/salida.
- Outputs positivo y negativo.
- Test report, cutover/rollback runbook, hypercare y cost baseline.
- Evidencia de cleanup/decommission aprobada.

El laboratorio no crea recursos cloud. No publique archivos env, keys, certificates, cloud credentials, personal data ni estados de Terraform.
