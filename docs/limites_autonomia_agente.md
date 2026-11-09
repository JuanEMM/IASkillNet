# Límites de autonomía: Asistente de soporte de envíos y reembolsos

## Herramientas y nivel de riesgo

- consultar_estado_envio_con_historial: bajo (solo lee
  información, no modifica nada)

- calcular_costo_envio: bajo (solo calcula, no ejecuta
  ninguna acción externa)

- generar_reembolso: alto (mueve dinero de forma
  irreversible; requiere aprobación humana)

## Herramientas que requieren aprobación humana

- generar_reembolso: mueve dinero de forma irreversible.
  Antes de ejecutarse, esperar_aprobacion muestra el
  pedido y el monto y espera un "s" del supervisor
  (máximo 300 segundos). Se rechaza por defecto si
  hay timeout, si stdin no está disponible o si la
  respuesta es distinta de "s". Cada decisión queda en
  registro_aprobaciones (herramienta, argumentos,
  aprobado, momento).

## Revisión de trazas

- Frecuencia: semanal, y además cada vez que se
  rechace o falle un reembolso. Las interacciones se
  guardan en trazas_agente.jsonl con registrar_traza.

- Qué se busca:
  - Herramientas invocadas varias veces seguidas
    (marcar_repeticiones_sospechosas ya las señala):
    posible bucle del agente.
  - Llamadas a generar_reembolso: confirmar que cada
    una tenga su entrada en registro_aprobaciones y que
    el monto coincida con lo pedido por el cliente.
  - Reembolsos rechazados o con timeout, y reintentos
    del agente tras un rechazo.
  - Argumentos inusuales: montos altos o pedidos que el
    cliente no mencionó, números de seguimiento
    inexistentes, peso o distancia fuera de rango.
  - Respuestas finales que afirman una acción (por
    ejemplo, "reembolso generado") sin una acción
    registrada que la respalde.

## Qué hacer ante un comportamiento inesperado

- 1. Detener el agente (interrumpir la ejecución) y no
  aprobar ninguna solicitud pendiente de reembolso.

- 2. Conservar la evidencia: trazas_agente.jsonl y
  registro_aprobaciones, sin modificarlos.

- 3. Revisar la traza de la sesión afectada: qué se
  preguntó, qué herramientas se llamaron, con qué
  argumentos y qué respondió el agente.

- 4. Si se ejecutó un reembolso indebido, avisar al
  responsable de pagos para revertirlo manualmente,
  porque la herramienta no puede deshacerlo.

- 5. Corregir la causa (prompt, descripción de la
  herramienta o validación de argumentos) y volver a
  probar con la misma entrada antes de reactivar el
  agente.

- 6. Anotar el incidente y el ajuste para tenerlo en
  cuenta en las próximas revisiones.
