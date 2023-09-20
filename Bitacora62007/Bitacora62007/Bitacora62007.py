"""Welcome to Pynecone! This app is a demonstration of OpenAI's GPT."""
import pynecone as pc
from .helpers import navbar
import datetime
import os

MAX_QUESTIONS = 10

#variables de estado para el botón de opción de tag
opciones= ["Personal", "Aprendizaje ", "Módulo A", "Módulo B", "Módulo C", "Módulo D", "Otros"]

class Bitacora(pc.Model, table=True):
    """Una tabla para las actividades registradas en la base de datos."""

    descripcion: str
    observaciones: str
    paginaweb: str
    fecha: str
    tag: str


class State(pc.State):
    """The app state."""

    descripcion:str=""
    observaciones:str=""
    paginaweb:str=""     
    fecha: str= datetime.date.today().strftime("%d/%m/%Y")
    tag: str=""
    
    @pc.var
    def questions(self) -> "list[Bitacora]":
        """Get the users saved questions and answers from the database."""
        with pc.session() as session2:
            qa = (
                session2.query(Bitacora)
                # .where(Bitacora.descripcion == self.descripcion)
                # .distinct(Bitacora.observaciones)
                # .order_by(Bitacora.fecha.desc())
                .order_by(Bitacora.id.desc())
                # .limit(MAX_QUESTIONS)
                .all()
            )
            return [[q.descripcion, q.observaciones, q.fecha, q.tag, q.paginaweb] for q in qa]
            
    @pc.var
    def consultasimple(self) -> "list[Bitacora]":
        """Get the users saved questions and answers from the database."""
        with pc.session() as session3:
            qb = (
                session3.query(Bitacora)
                # .from_self(Bitacora.descripcion)
                # .where(Bitacora.descripcion == self.descripcion)
                # .distinct(Bitacora.observaciones)
                # .order_by(Bitacora.fecha.desc())
                .order_by(Bitacora.id.desc())
                # .limit(MAX_QUESTIONS)
                # .func.count
                # .all()
                # .filter_by(id=4)
                .all()
            )
            # return [[s.descripcion] for s in qb]
            return [[s.descripcion, s.observaciones, s.fecha, s.tag ] for s in qb]
            # return [[s.descripcion, s.observaciones, s.fecha, s.tag, s.paginaweb] for s in qb]

    def save_result(self):
        with pc.session() as session:
            session.add(
                Bitacora(
                descripcion=self.descripcion,
                observaciones=self.observaciones,
                paginaweb=self.paginaweb,
                fecha=self.fecha,
                tag=self.tag
                )
            )
            session.commit()
                
def index():
    return pc.center(
        navbar(),
        pc.vstack(
            pc.center(
                pc.vstack(
                    pc.form_control(
                        pc.form_label("Descripción"),
                        pc.text_area(
                            on_blur=State.set_descripcion, 
                            placeholder="Descripcion", 
                            width="100%"
                        ),
                        is_required=True
                    ),
                    pc.form_control(
                        pc.form_label("Observaciones"),

                        pc.text_area(
                            on_blur=State.set_observaciones, 
                            placeholder="Observaciones", 
                            width="100%"
                        ),
                        is_required=False
                    ),
                    pc.form_control(
                        pc.form_label("Pagina Web"), 
                        pc.text_area(
                            on_blur=State.set_paginaweb, 
                            placeholder="Pagina Web", 
                            width="100%"
                        ),
                    ),
                    pc.form_control(
                        pc.form_label("Seleccionar Tag"),
                        pc.radio_group(
                            opciones,
                            on_change=State.set_tag
                        ),
                        pc.badge("Tag seleccionado:   ", color_scheme="blue", variant="outline"),
                        pc.badge(State.tag, color_scheme="red", variant="solid"),
                    ),
                    pc.badge("Asegurarse de hacer click fuera del campo antes de salvar el registro", color_scheme="red"),                 
                    pc.button("Guardar Respuesta", on_click=State.save_result, width="100%"),
                    shadow="lg",
                    padding="1em",
                    border_radius="lg",
                    width="100%",
                ),
                width="100%",
            ),
            pc.center(
                pc.vstack(
                    pc.heading("Tabla de Registros", font_size="1.5em"),
                    pc.divider(),
                    pc.data_table(
                        data=State.questions,
                        # columns=["Descripcion", "Observaciones", "Fecha", "Tag","Pagina_Web"],
                        columns=["Descripcion", "Observaciones", "Fecha", "Tag",],
                        pagination=True,
                        search=True,
                        sort=True,
                    ),
                    shadow="lg",
                    padding="1em",
                    border_radius="lg",
                ),
            ),
            width="80%",
            spacing="2em",
        ),
        padding_top="6em",
        text_align="top",
        position="relative",
    )


def registros():
    return pc.center(
        navbar(),
        pc.vstack(
            pc.heading("Tabla de Registros", font_size="1.5em"),
            pc.divider(),
            pc.data_table(
                data=State.consultasimple,
                columns=["Descripcion", "Observaciones", "Fecha", "Tag","Pagina_Web"],
                pagination=True,
                search=True,
                sort=True,
            ),
            shadow="lg",
            padding="1em",
            border_radius="lg",
            width="80%",
        ),
        width="80%",
        spacing="2em",
        padding_top="6em",
        text_align="top",
        # position="relative",
        )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.add_page(registros)
app.compile()