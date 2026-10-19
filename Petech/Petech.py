"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import httpx
import reflex as rx

from rxconfig import config


XANO_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:FxZRT-rM"


class TutorState(rx.State):
    """Estado para gerenciar o cadastro de tutores."""
    nome: str = ""
    email: str = ""
    telefone: str = ""
    processando: bool = False
    mensagem: str = ""

    def set_nome(self, nome: str):
        self.nome = nome

    def set_email(self, email: str):
        self.email = email

    def set_telefone(self, telefone: str):
        self.telefone = telefone

    def signup_tutor(self):
        """Função para processar o cadastro do tutor."""
        nome = self.nome.strip()
        if not nome:
            self.mensagem = "O nome é obrigatório."
            return

        self.processando = True
        self.mensagem = "Cadastrando..."

        url = f"{XANO_API_URL}/tutor"
        dados = {"nome": nome}
        if self.email.strip():
            dados["email"] = self.email.strip()
        if self.telefone.strip():
            dados["telefone"] = self.telefone.strip()

        try:
            response = httpx.post(
                url,
                json=dados,
                timeout=10.0
            )
            response.raise_for_status()
            tutor = response.json()
        except httpx.HTTPStatusError as error:
            try:
                err_data = error.response.json()
            except ValueError:
                err_data = None
            err_msg = (
                err_data.get("message", error.response.text)
                if isinstance(err_data, dict)
                else error.response.text
            )
            self.mensagem = f"Erro no cadastro: {err_msg}"
        except httpx.RequestError as error:
            self.mensagem = f"Erro de conexão com o Xano: {error}"
        except ValueError:
            self.mensagem = "O Xano retornou uma resposta inválida."
        else:
            if not isinstance(tutor, dict) or tutor.get("id") is None:
                self.mensagem = "O Xano não confirmou a gravação do tutor."
            else:
                self.mensagem = f"Tutor cadastrado com sucesso! ID: {tutor['id']}"
                self.nome = ""
                self.email = ""
                self.telefone = ""
        finally:
            self.processando = False

def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Cadastro de Tutor", size="8"),
            rx.text("Preencha os dados abaixo para cadastrar um novo cliente.", size="3"),
            
            rx.vstack(
                rx.text("Nome:"),
                rx.input(
                    placeholder="Digite o nome completo",
                    on_change=TutorState.set_nome,
                    value=TutorState.nome,
                    width="100%",
                ),
                rx.text("E-mail:"),
                rx.input(
                    placeholder="email@exemplo.com",
                    on_change=TutorState.set_email,
                    value=TutorState.email,
                    width="100%",
                ),
                rx.text("Telefone:"),
                rx.input(
                    placeholder="(00) 00000-0000",
                    on_change=TutorState.set_telefone,
                    value=TutorState.telefone,
                    width="100%",
                ),
                rx.button(
                    "Cadastrar",
                    on_click=TutorState.signup_tutor,
                    loading=TutorState.processando,
                    width="100%",
                    margin_top="10px",
                ),
                rx.cond(
                    TutorState.mensagem,
                    rx.text(TutorState.mensagem, color="blue", size="2"),
                ),
                width="400px",
                padding="20px",
                border="1px solid #ddd",
                border_radius="10px",
                spacing="3",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
        ),
    )


app = rx.App()
app.add_page(index)
