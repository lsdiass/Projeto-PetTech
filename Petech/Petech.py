"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from decimal import Decimal, InvalidOperation

import httpx
import reflex as rx

from rxconfig import config


XANO_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:FxZRT-rM"


def parse_preco(valor: str) -> Decimal:
    """Converte valores monetários em formato brasileiro para Decimal."""
    valor_limpo = valor.strip().replace("R$", "").replace(" ", "")
    if "," in valor_limpo:
        valor_limpo = valor_limpo.replace(".", "").replace(",", ".")
    return Decimal(valor_limpo)


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
            rx.link("Cadastrar Pet", href="/pets"),
            rx.link("Cadastrar Serviço", href="/servicos"),
            
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


class PetState(rx.State):
    """Estado para gerenciar o cadastro de pets."""
    opcoes_tutor: list[str] = []
    tutor_id: str = ""
    tutor_selecionado: str = ""
    nome: str = ""
    especie: str = ""
    raca: str = ""
    porte: str = ""
    observacoes_saude: str = ""
    carregando_tutores: bool = False
    processando: bool = False
    erro_tutores: str = ""
    mensagem: str = ""
    sucesso: bool = False

    @rx.event
    def carregar_tutores(self):
        """Carrega as opções de tutor antes de permitir o cadastro."""
        self.carregando_tutores = True
        self.opcoes_tutor = []
        self.tutor_id = ""
        self.tutor_selecionado = ""
        self.erro_tutores = ""

        try:
            response = httpx.get(f"{XANO_API_URL}/tutor", timeout=10.0)
            response.raise_for_status()
            tutores = response.json()
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
            self.erro_tutores = f"Erro ao carregar tutores: {err_msg}"
        except httpx.RequestError as error:
            self.erro_tutores = f"Erro de conexão ao carregar tutores: {error}"
        except ValueError:
            self.erro_tutores = "O Xano retornou uma lista de tutores inválida."
        else:
            if not isinstance(tutores, list):
                self.erro_tutores = "O Xano retornou uma lista de tutores inválida."
            else:
                opcoes_tutor = []
                for tutor in tutores:
                    tutor_id = str(tutor.get("id", "")) if isinstance(tutor, dict) else ""
                    if (
                        not isinstance(tutor, dict)
                        or not tutor_id.isdigit()
                        or not isinstance(tutor.get("nome"), str)
                        or not tutor["nome"].strip()
                    ):
                        self.erro_tutores = (
                            "O Xano retornou um tutor sem identificador ou nome válido."
                        )
                        break
                    opcoes_tutor.append(f"{tutor_id} - {tutor['nome']}")
                else:
                    self.opcoes_tutor = opcoes_tutor

                if not self.erro_tutores and not self.opcoes_tutor:
                    self.erro_tutores = (
                        "Nenhum tutor cadastrado. Cadastre um tutor antes de cadastrar um pet."
                    )
        finally:
            self.carregando_tutores = False

    @rx.event
    def set_tutor_selecionado(self, tutor_selecionado: str):
        self.tutor_selecionado = tutor_selecionado
        self.tutor_id = tutor_selecionado.split(" - ", 1)[0]
        self.mensagem = ""

    @rx.event
    def set_nome(self, nome: str):
        self.nome = nome

    @rx.event
    def set_especie(self, especie: str):
        self.especie = especie

    @rx.event
    def set_raca(self, raca: str):
        self.raca = raca

    @rx.event
    def set_porte(self, porte: str):
        self.porte = porte

    @rx.event
    def set_observacoes_saude(self, observacoes_saude: str):
        self.observacoes_saude = observacoes_saude

    @rx.event
    def registrar_pet(self):
        """Valida e envia o cadastro do pet ao Xano."""
        nome = self.nome.strip()
        especie = self.especie.strip()
        tutor_selecionado = any(
            opcao.split(" - ", 1)[0] == self.tutor_id
            for opcao in self.opcoes_tutor
        )

        if self.erro_tutores:
            self.mensagem = self.erro_tutores
            self.sucesso = False
            return
        if not tutor_selecionado:
            self.mensagem = "Selecione um tutor cadastrado."
            self.sucesso = False
            return
        if not nome:
            self.mensagem = "O nome do pet é obrigatório."
            self.sucesso = False
            return
        if not especie:
            self.mensagem = "A espécie do pet é obrigatória."
            self.sucesso = False
            return
        if self.porte not in ["Pequeno", "Médio", "Grande"]:
            self.mensagem = "Selecione um porte válido."
            self.sucesso = False
            return

        self.processando = True
        self.mensagem = "Cadastrando pet..."
        self.sucesso = False

        dados = {
            "tutor_id": int(self.tutor_id),
            "nome": nome,
            "especie": especie,
            "porte": self.porte,
        }
        if self.raca.strip():
            dados["raca"] = self.raca.strip()
        if self.observacoes_saude.strip():
            dados["observacoes_saude"] = self.observacoes_saude.strip()

        try:
            response = httpx.post(
                f"{XANO_API_URL}/pet",
                json=dados,
                timeout=10.0,
            )
            response.raise_for_status()
            pet = response.json()
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
            if not isinstance(pet, dict) or pet.get("id") is None:
                self.mensagem = "O Xano não confirmou a gravação do pet."
            elif (
                str(pet.get("tutor_id")) != self.tutor_id
                or pet.get("nome") != nome
                or pet.get("especie") != especie
                or pet.get("porte") != self.porte
                or (
                    "raca" in dados
                    and pet.get("raca") != dados["raca"]
                )
                or (
                    "observacoes_saude" in dados
                    and pet.get("observacoes_saude") != dados["observacoes_saude"]
                )
            ):
                self.mensagem = (
                    "O Xano criou um registro, mas não confirmou os dados do pet. "
                    "Verifique se o schema e o endpoint POST /pet foram atualizados "
                    "no grupo Event Logs."
                )
            else:
                self.mensagem = f"Pet cadastrado com sucesso! ID: {pet['id']}"
                self.sucesso = True
                self.nome = ""
                self.especie = ""
                self.raca = ""
                self.porte = ""
                self.observacoes_saude = ""
                self.tutor_id = ""
                self.tutor_selecionado = ""
        finally:
            self.processando = False


def cadastro_pet() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Cadastro de Pet", size="8"),
            rx.text("Preencha os dados do pet e selecione seu tutor responsável.", size="3"),
            rx.link("Voltar ao cadastro de tutor", href="/"),
            rx.link("Cadastrar Serviço", href="/servicos"),
            rx.vstack(
                rx.text("Tutor responsável:"),
                rx.cond(
                    PetState.carregando_tutores,
                    rx.text("Carregando tutores..."),
                    rx.select(
                        PetState.opcoes_tutor,
                        value=PetState.tutor_selecionado,
                        on_change=PetState.set_tutor_selecionado,
                        placeholder="Selecione um tutor",
                        width="100%",
                    ),
                ),
                rx.cond(
                    PetState.erro_tutores,
                    rx.text(PetState.erro_tutores, color="red", size="2"),
                ),
                rx.text("Nome:"),
                rx.input(
                    placeholder="Nome do pet",
                    on_change=PetState.set_nome,
                    value=PetState.nome,
                    width="100%",
                ),
                rx.text("Espécie:"),
                rx.input(
                    placeholder="Ex.: Cão ou Gato",
                    on_change=PetState.set_especie,
                    value=PetState.especie,
                    width="100%",
                ),
                rx.text("Raça (opcional):"),
                rx.input(
                    placeholder="Raça do pet",
                    on_change=PetState.set_raca,
                    value=PetState.raca,
                    width="100%",
                ),
                rx.text("Porte:"),
                rx.select(
                    ["Pequeno", "Médio", "Grande"],
                    value=PetState.porte,
                    on_change=PetState.set_porte,
                    placeholder="Selecione o porte",
                    width="100%",
                ),
                rx.text("Observações de saúde e comportamento (opcional):"),
                rx.text_area(
                    placeholder="Alergias, cuidados especiais ou observações",
                    on_change=PetState.set_observacoes_saude,
                    value=PetState.observacoes_saude,
                    width="100%",
                ),
                rx.button(
                    "Cadastrar Pet",
                    on_click=PetState.registrar_pet,
                    loading=PetState.processando,
                    width="100%",
                    margin_top="10px",
                ),
                rx.cond(
                    PetState.mensagem,
                    rx.text(
                        PetState.mensagem,
                        color=rx.cond(PetState.sucesso, "green", "red"),
                        size="2",
                    ),
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


class ServicoState(rx.State):
    """Estado para gerenciar o cadastro de serviços."""
    nome: str = ""
    descricao: str = ""
    preco: str = ""
    duracao_minutos: str = ""
    processando: bool = False
    mensagem: str = ""
    sucesso: bool = False

    @rx.event
    def set_nome(self, nome: str):
        self.nome = nome

    @rx.event
    def set_descricao(self, descricao: str):
        self.descricao = descricao

    @rx.event
    def set_preco(self, preco: str):
        self.preco = preco

    @rx.event
    def set_duracao_minutos(self, duracao_minutos: str):
        self.duracao_minutos = duracao_minutos

    @rx.event
    def registrar_servico(self):
        """Valida e envia o cadastro do serviço ao Xano."""
        nome = self.nome.strip()
        descricao = self.descricao.strip()
        if not nome:
            self.mensagem = "O nome do serviço é obrigatório."
            self.sucesso = False
            return

        try:
            preco = parse_preco(self.preco)
        except (InvalidOperation, ValueError):
            self.mensagem = "Informe um valor válido, por exemplo 35,00."
            self.sucesso = False
            return
        if not preco.is_finite() or preco <= 0:
            self.mensagem = "O valor deve ser maior que zero."
            self.sucesso = False
            return

        try:
            duracao_minutos = int(self.duracao_minutos.strip())
        except ValueError:
            self.mensagem = "Informe a duração em minutos como número inteiro."
            self.sucesso = False
            return
        if duracao_minutos <= 0:
            self.mensagem = "A duração deve ser maior que zero."
            self.sucesso = False
            return

        self.processando = True
        self.mensagem = "Cadastrando serviço..."
        self.sucesso = False

        dados = {
            "nome": nome,
            "preco": float(preco),
            "duracao_minutos": duracao_minutos,
        }
        if descricao:
            dados["descricao"] = descricao

        try:
            response = httpx.post(
                f"{XANO_API_URL}/servico",
                json=dados,
                timeout=10.0,
            )
            response.raise_for_status()
            servico = response.json()
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
            if not isinstance(servico, dict):
                dados_confirmados = False
            else:
                try:
                    preco_persistido = Decimal(str(servico.get("preco")))
                    dados_confirmados = (
                        servico.get("id") is not None
                        and servico.get("nome") == nome
                        and preco_persistido == preco
                        and servico.get("duracao_minutos") == duracao_minutos
                        and (
                            not descricao
                            or servico.get("descricao") == descricao
                        )
                    )
                except (InvalidOperation, TypeError, ValueError):
                    dados_confirmados = False

            if not dados_confirmados:
                self.mensagem = (
                    "O Xano não confirmou a gravação dos dados do serviço. "
                    "Verifique o schema e o endpoint POST /servico."
                )
            else:
                self.mensagem = (
                    f"Serviço cadastrado com sucesso! ID: {servico['id']}"
                )
                self.sucesso = True
                self.nome = ""
                self.descricao = ""
                self.preco = ""
                self.duracao_minutos = ""
        finally:
            self.processando = False


def cadastro_servico() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Cadastro de Serviço", size="8"),
            rx.text("Cadastre um serviço oferecido pelo estabelecimento.", size="3"),
            rx.link("Voltar ao cadastro de tutor", href="/"),
            rx.link("Ir para cadastro de pet", href="/pets"),
            rx.vstack(
                rx.text("Nome:"),
                rx.input(
                    placeholder="Ex.: Banho, Tosa Higiênica",
                    on_change=ServicoState.set_nome,
                    value=ServicoState.nome,
                    width="100%",
                ),
                rx.text("Descrição (opcional):"),
                rx.text_area(
                    placeholder="Detalhes sobre o serviço",
                    on_change=ServicoState.set_descricao,
                    value=ServicoState.descricao,
                    width="100%",
                ),
                rx.text("Valor (R$):"),
                rx.input(
                    placeholder="Ex.: 35,00",
                    type="text",
                    input_mode="decimal",
                    on_change=ServicoState.set_preco,
                    value=ServicoState.preco,
                    width="100%",
                ),
                rx.text("Duração média (minutos):"),
                rx.input(
                    placeholder="Ex.: 60",
                    type="number",
                    min="1",
                    step="1",
                    on_change=ServicoState.set_duracao_minutos,
                    value=ServicoState.duracao_minutos,
                    width="100%",
                ),
                rx.button(
                    "Cadastrar Serviço",
                    on_click=ServicoState.registrar_servico,
                    loading=ServicoState.processando,
                    width="100%",
                    margin_top="10px",
                ),
                rx.cond(
                    ServicoState.mensagem,
                    rx.text(
                        ServicoState.mensagem,
                        color=rx.cond(ServicoState.sucesso, "green", "red"),
                        size="2",
                    ),
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
app.add_page(
    cadastro_pet,
    route="/pets",
    on_load=PetState.carregar_tutores,
)
app.add_page(cadastro_servico, route="/servicos")
