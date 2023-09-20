import pynecone as pc


def navbar():
    return pc.box(
        pc.hstack(
            pc.hstack(
                pc.image(src="/nba.png", width="50px"),
                pc.heading("Bitacora D.62007"),
                pc.flex(
                    pc.badge("2023 Bitacora", color_scheme="blue"),
                ),
            ),
            pc.menu(
                pc.menu_button(
                    "Menu", bg="black", color="white", border_radius="md", px=4, py=2
                ),
                pc.menu_list(
                    pc.link(pc.menu_item("Inicio"), href="/"),
                    pc.menu_divider(),
                    pc.link(
                        pc.menu_item(
                            pc.hstack(pc.text("Desglose de registros"), pc.icon(tag="DownloadIcon"))
                        ),
                        href="/registros",
                    ),
                ),
            ),
            justify="space-between",
            border_bottom="0.6em solid #F0F0F0",
            padding_x="10em",
            padding_y="1em",
            bg="rgba(12,255,255, 0.97)",
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="500",
    )