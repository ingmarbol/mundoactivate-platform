# Sesión 23 - Networking avanzado multicuenta y multisuscripción

## Objetivo
Diseñar conectividad escalable y segmentada con AWS Transit Gateway, Azure Virtual WAN, inspección central, DNS híbrido y private access.

## Alcance
Topología local AWS/Azure/shared services, IPAM sin overlap, aislamiento prod/nonprod, inspection obligatoria, DNS HA y validator dependency-free.

## Prueba
`python3 networking/validate_topology.py --topology networking/topology.json`

Resultado esperado: NETWORK TOPOLOGY VALID.

## Prueba negativa
En una copia temporal cambie azure-prod a 10.10.1.0/24. Debe detectar overlap con aws-prod y terminar con exit code distinto de cero.

## Evidencias
Diagrama, IPAM, association/propagation, flujo ida/retorno por firewall, DNS query path, validación positiva y rechazo.

## Seguridad y costos
No contiene credenciales ni crea recursos. Use IAM/RBAC mínimo, firewall, flow logs e IaC. Modele attachments, data processing, NAT, firewall, endpoints, DNS y egress.

## Limpieza
Eliminar solo copias temporales de prueba; no existen recursos cloud.
