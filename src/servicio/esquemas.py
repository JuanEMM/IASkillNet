"""El contrato del servicio de porteria: que entra y que sale de cada endpoint.

Limites de entrada (cada consulta y cada extraccion terminan en una llamada a Gemini):
- pregunta: 3 a 500 caracteres. Menos no tiene contenido; mas es un abuso o un error y
  encarece la llamada sin mejorar la respuesta.
- texto de la guia: 20 a 2000 caracteres. La guia de ejemplo tiene unos 330; 2000 deja
  margen para guias largas y corta textos que no son una guia.
"""
from pydantic import BaseModel, ConfigDict, Field

GUIA_EJEMPLO = (
    "Guia de despacho N 100231. Remitente: Agricola Los Aromos, Rancagua. "
    "Destinatario: Centro de Distribucion Santiago Sur, Av. Las Industrias 1450, "
    "San Bernardo. Chofer: Juan Perez, RUT 12.345.678-5. Patente: BXKL45. "
    "Carga: fruta fresca, 1200 kg en 40 bultos. Origen: Rancagua. Destino: Santiago."
)


class Consulta(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    pregunta: str = Field(
        min_length=3,
        max_length=500,
        description="Pregunta del guardia o del supervisor, entre 3 y 500 caracteres.",
        examples=["cuando ingreso el camion BXKL45"],
    )


class Item(BaseModel):
    atributo: str = Field(description="Nombre corto del dato, en minusculas con guion bajo.")
    valor: str = Field(description="El dato o la regla concreta tomada de la fuente.")
    calidad: int = Field(
        ge=1, le=5, description="Confianza del dato, de 1 a 5; menor a 4 es parcial o dudoso."
    )
    fuente: str = Field(
        description="Procedimiento o registro de donde sale el dato, por ejemplo ingreso-0007."
    )


class RespuestaConsulta(BaseModel):
    trace_id: str = Field(description="Identificador de la peticion, el mismo que aparece en los logs.")
    items: list[Item] = Field(
        description="Datos encontrados, cada uno con su fuente; vacia si los documentos no cubren la pregunta."
    )
    fuentes: list[str] = Field(description="Documentos recuperados del indice para responder.")


class Guia(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    texto: str = Field(
        min_length=20,
        max_length=2000,
        description="Texto de la guia de transporte, tal como lo escribe o dicta el conductor, "
                    "entre 20 y 2000 caracteres.",
        examples=[GUIA_EJEMPLO],
    )


class DatoGuia(BaseModel):
    atributo: str = Field(description="Nombre del dato extraido, por ejemplo rut o patente.")
    valor: str = Field(description="Valor extraido del texto de la guia.")
    calidad: int = Field(ge=1, le=5, description="Calidad del dato extraido, de 1 a 5.")
    requiere_confirmacion: bool = Field(
        description="true si el dato no paso la validacion por codigo (patente o RUT) o si su "
                    "calidad es menor a 4: el guardia lo confirma a mano."
    )


class RespuestaExtraccion(BaseModel):
    trace_id: str = Field(description="Identificador de la peticion, el mismo que aparece en los logs.")
    dateInput: str = Field(description="Fecha y hora de la extraccion.")
    items: list[DatoGuia] = Field(description="Datos extraidos de la guia, ya validados.")


class EstadoIngreso(BaseModel):
    patente: str = Field(description="Patente del camion, en mayusculas.")
    guia: str = Field(description="Numero de la guia de transporte del ingreso.")
    hora_ingreso: str = Field(description="Hora de ingreso de hoy, en formato HH:MM.")
    carga: str = Field(description="Tipo de carga declarada en la guia.")
    hora_salida: str | None = Field(
        default=None, description="Hora de salida de hoy, o null si sigue en planta."
    )
    en_planta: bool = Field(description="true si el camion ingreso hoy y no tiene salida registrada.")
    fuente: str = Field(description="Registro de donde sale el dato, por ejemplo ingreso-0007.")


class CampoInvalido(BaseModel):
    campo: str = Field(description="Campo que no cumple la regla.")
    problema: str = Field(description="Que regla incumple.")


class ErrorRespuesta(BaseModel):
    codigo: str = Field(description="Codigo estable del error, para que un programa lo compare.")
    mensaje: str = Field(description="Explicacion legible del error.")
    campos: list[CampoInvalido] | None = Field(
        default=None, description="Detalle por campo, si aplica."
    )
