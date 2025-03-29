# Lab 7: Monitoring using Prometheus and Grafana
Este laboratorio tiene como objetivo proporcionar experiencia práctica en el monitoreo utilizando Prometheus y visualización de métricas a través de Grafana.

## Configuración inicial:
- Clonar el repositorio de GitHub: `https://github.com/XueyingJia/mlip-monitoring-lab`
- Instalar los requerimientos: `pip install -r requirements.txt`

## Configuración de Docker y ejecución del script de monitoreo de Kafka:
- Ejecutar `docker compose up -d`
- Verificar el Prometheus: `http://localhost:9090`
- Visitar la sección Status > Targets:
- Modificar el script de monitoreo de Kafka.
- Ejecutar el script de monitoreo de Kafka: `python kafka-monitoring.py`

## Visualización en Prometheus:
- Verificar que todos los targets estén activos en Prometheus:
  
<img src="prometheus_images/Screenshot from 2025-03-29 05-24-42.png">

## Configuración de Grafana:
- Acceder a Grafana en `http://localhost:3000` (usuario: admin, contraseña: admin).
- Agregar Prometheus como fuente de datos: `http://prometheus:9090`

### Panel 1:
- Add `request_count_total` as metric, filter label http_status and equate to 200.

<img src="prometheus_images/Screenshot from 2025-03-29 05-22-36.png">

### Panel 2:
- Click on add> visualization. In the queries below, add request_count_total as metric.
  
<img src="prometheus_images/Screenshot from 2025-03-29 05-22-24.png">

### Panel 3:
- Track rate of node_cpu_seconds_total.
  
<img src="prometheus_images/Screenshot from 2025-03-29 05-22-12.png">

### Panel 4:
- Use forms of request_latency_seconds. Make use of formula for average= sum/count

<img src="prometheus_images/Screenshot from 2025-03-29 05-22-02.png">
