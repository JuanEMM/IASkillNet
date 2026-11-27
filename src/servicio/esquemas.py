"""El contrato del servicio de porteria: que entra y que sale de cada endpoint."""
from pydantic import BaseModel, Field

GUIA_EJEMPLO = (
    "Guia de despacho N 100231. Remitente: Agricola Los Aromos, Rancagua. "
    "Destinatario: Centro de Distribucion Santiago Sur, Av. Las Industrias 1450, "
    "San Bernardo. Chofer: Juan Perez, RUT 12.345.678-5. Patente: BXKL45. "
    "Carga: fruta fresca, 1200 kg en 40 bultos. Origen: Rancagua. Destino: Santiago."
)


class Consulta(BaseModel):
    pregunta: str = Field(
        description="Pregunta del guardia o del supervisor, en lenguaje natural.",
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
    texto: str = Field(
        description="Texto de la guia de transporte, tal como lo escribe o dicta el conductor.",
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
