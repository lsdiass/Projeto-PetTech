"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import calendar
from decimal import Decimal, InvalidOperation
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
import reflex as rx

from rxconfig import config


XANO_API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:FxZRT-rM"
DEMO_LOGIN_EMAIL = "admin@pettech.local"
DEMO_LOGIN_PASSWORD = "demo-pettech"
FUSO_AGENDAMENTO = ZoneInfo("America/Sao_Paulo")
NOMES_MESES = (
    "",
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
)


def timestamp_em_milissegundos(valor: object) -> int | None:
    if isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        return int(valor)
    if not isinstance(valor, str):
        return None
    if valor.isdigit():
        return int(valor)
    try:
        data_hora = datetime.fromisoformat(valor.replace("Z", "+00:00"))
    except ValueError:
        return None
    if data_hora.tzinfo is None:
        data_hora = data_hora.replace(tzinfo=FUSO_AGENDAMENTO)
    return int(data_hora.timestamp() * 1000)


def credenciais_demo_validas(email: str, senha: str) -> bool:
    return (
        email.strip().lower() == DEMO_LOGIN_EMAIL
        and senha == DEMO_LOGIN_PASSWORD
    )


def parse_preco(valor: str) -> Decimal:
    """Converte valores monetários em formato brasileiro para Decimal."""
    valor_limpo = valor.strip().replace("R$", "").replace(" ", "")
    if "," in valor_limpo:
        valor_limpo = valor_limpo.replace(".", "").replace(",", ".")
    return Decimal(valor_limpo)


def normalizar_id(valor: object) -> str | None:
    if isinstance(valor, bool):
        return None
    if isinstance(valor, int) and valor > 0:
        return str(valor)
    if isinstance(valor, str) and valor.isdigit() and int(valor) > 0:
        return str(int(valor))
    return None


def formatar_data_hora_agendamento(valor: object) -> str | None:
    try:
        timestamp = timestamp_em_milissegundos(valor)
        if timestamp is None:
            return None
        data_hora = datetime.fromtimestamp(
            timestamp / 1000,
            tz=FUSO_AGENDAMENTO,
        )
    except (OverflowError, OSError, TypeError, ValueError):
        return None
    return data_hora.strftime("%d/%m/%Y às %H:%M")


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

class LoginDemoState(rx.State):
    email: str = ""
    senha: str = ""
    mensagem: str = ""

    @rx.event
    def set_email(self, email: str):
        self.email = email

    @rx.event
    def set_senha(self, senha: str):
        self.senha = senha

    @rx.event
    def entrar(self):
        if credenciais_demo_validas(self.email, self.senha):
            self.mensagem = ""
            return rx.redirect("/tutores")

        self.mensagem = "E-mail ou senha demonstrativos inválidos."


def login() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("PetTech", size="8"),
            rx.text("Acesse o sistema de gestão do pet shop.", size="3"),
            rx.vstack(
                rx.text("E-mail:"),
                rx.input(
                    placeholder="E-mail de demonstração",
                    type="email",
                    on_change=LoginDemoState.set_email,
                    value=LoginDemoState.email,
                    width="100%",
                ),
                rx.text("Senha:"),
                rx.input(
                    placeholder="Senha de demonstração",
                    type="password",
                    on_change=LoginDemoState.set_senha,
                    value=LoginDemoState.senha,
                    width="100%",
                ),
                rx.button(
                    "Entrar",
                    on_click=LoginDemoState.entrar,
                    width="100%",
                    margin_top="10px",
                ),
                rx.cond(
                    LoginDemoState.mensagem,
                    rx.text(LoginDemoState.mensagem, color="red", size="2"),
                ),
                rx.text(
                    "Acesso demonstrativo: admin@pettech.local / demo-pettech",
                    size="2",
                ),
                rx.text(
                    "Protótipo sem autenticação real: as rotas e os dados não são protegidos.",
                    color="orange",
                    size="2",
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


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Cadastro de Tutor", size="8"),
            rx.text("Preencha os dados abaixo para cadastrar um novo cliente.", size="3"),
            rx.link("Página inicial", href="/"),
            rx.link("Cadastrar Pet", href="/pets"),
            rx.link("Cadastrar Serviço", href="/servicos"),
            rx.link("Agendar atendimento", href="/agendamentos"),
            rx.link("Consultar agendamentos", href="/agendamentos/lista"),
            
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
            rx.link("Voltar ao cadastro de tutor", href="/tutores"),
            rx.link("Cadastrar Serviço", href="/servicos"),
            rx.link("Agendar atendimento", href="/agendamentos"),
            rx.link("Consultar agendamentos", href="/agendamentos/lista"),
            rx.link("Página inicial", href="/"),
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


class AgendamentoState(rx.State):
    opcoes_pet: list[str] = []
    opcoes_servico: list[str] = []
    pets: list[dict[str, str]] = []
    servicos: list[dict[str, str]] = []
    pet_selecionado: str = ""
    servico_selecionado: str = ""
    ano: int = 0
    mes: int = 0
    titulo_mes: str = ""
    dias_calendario: list[dict[str, str]] = []
    dias_disponibilidade: list[dict[str, str]] = []
    horarios_mes: list[dict[str, str]] = []
    horarios: list[dict[str, str]] = []
    data_selecionada: str = ""
    horario_selecionado: str = ""
    carregando_dados: bool = False
    carregando_disponibilidade: bool = False
    processando: bool = False
    erro: str = ""
    aviso: str = ""
    mensagem: str = ""
    sucesso: bool = False

    def _atualizar_calendario(self):
        if self.ano < 1 or self.mes < 1:
            self.dias_calendario = []
            return

        hoje = datetime.now(FUSO_AGENDAMENTO).date()
        primeiro_dia_semana, dias_no_mes = calendar.monthrange(self.ano, self.mes)
        dias = [
            {
                "data": "",
                "numero": "",
                "habilitado": "false",
                "espaco": "true",
            }
            for _ in range(primeiro_dia_semana)
        ]
        disponibilidade = {dia["data"]: dia for dia in self.dias_disponibilidade}

        for numero in range(1, dias_no_mes + 1):
            data = f"{self.ano:04d}-{self.mes:02d}-{numero:02d}"
            dia = disponibilidade.get(data)
            habilitado = (
                dia is not None
                and dia["tem_horario_disponivel"] == "true"
                and datetime.strptime(data, "%Y-%m-%d").date() >= hoje
            )
            dias.append({
                "data": data,
                "numero": str(numero),
                "habilitado": str(habilitado).lower(),
                "espaco": "false",
            })

        self.dias_calendario = dias
        self.titulo_mes = f"{NOMES_MESES[self.mes]} {self.ano}"

    @rx.event
    def carregar_dados(self):
        self.carregando_dados = True
        self.erro = ""
        self.aviso = ""
        self.mensagem = ""
        self.pets = []
        self.servicos = []
        self.opcoes_pet = []
        self.opcoes_servico = []
        agora = datetime.now(FUSO_AGENDAMENTO)
        self.ano = agora.year
        self.mes = agora.month

        try:
            resposta_pets = httpx.get(f"{XANO_API_URL}/pet", timeout=15.0)
            resposta_pets.raise_for_status()
            pets = resposta_pets.json()
            resposta_servicos = httpx.get(
                f"{XANO_API_URL}/servico",
                timeout=15.0,
            )
            resposta_servicos.raise_for_status()
            servicos = resposta_servicos.json()
        except httpx.HTTPStatusError as error:
            self.erro = (
                "Não foi possível carregar Pets e Serviços do Xano: "
                f"HTTP {error.response.status_code}."
            )
        except httpx.RequestError as error:
            self.erro = f"Erro de conexão ao carregar Pets e Serviços: {error}"
        except ValueError:
            self.erro = "O Xano retornou uma lista de Pets ou Serviços inválida."
        else:
            if not isinstance(pets, list) or not isinstance(servicos, list):
                self.erro = "O Xano retornou uma lista de Pets ou Serviços inválida."
            else:
                pets_validos: list[dict[str, str]] = []
                servicos_validos: list[dict[str, str]] = []
                pets_invalidos = 0
                servicos_invalidos = 0
                for pet in pets:
                    if (
                        not isinstance(pet, dict)
                        or not isinstance(pet.get("id"), int)
                        or not isinstance(pet.get("tutor_id"), int)
                        or not isinstance(pet.get("nome"), str)
                        or not pet["nome"].strip()
                    ):
                        pets_invalidos += 1
                        continue
                    pets_validos.append({
                        "id": str(pet["id"]),
                        "nome": pet["nome"],
                        "tutor_id": str(pet["tutor_id"]),
                    })

                for servico in servicos:
                    if (
                        not isinstance(servico, dict)
                        or not isinstance(servico.get("id"), int)
                        or not isinstance(servico.get("nome"), str)
                        or not servico["nome"].strip()
                        or not isinstance(servico.get("duracao_minutos"), int)
                        or servico["duracao_minutos"] <= 0
                    ):
                        servicos_invalidos += 1
                        continue
                    servicos_validos.append({
                        "id": str(servico["id"]),
                        "nome": servico["nome"],
                        "duracao_minutos": str(servico["duracao_minutos"]),
                    })

                self.pets = pets_validos
                self.servicos = servicos_validos
                self.opcoes_pet = [
                    f"{pet['id']} - {pet['nome']} (Tutor {pet['tutor_id']})"
                    for pet in pets_validos
                ]
                self.opcoes_servico = [
                    f"{servico['id']} - {servico['nome']} "
                    f"({servico['duracao_minutos']} min)"
                    for servico in servicos_validos
                ]
                avisos = []
                if pets_invalidos:
                    avisos.append(f"{pets_invalidos} Pet(s) inválido(s) foram omitidos.")
                if servicos_invalidos:
                    avisos.append(
                        f"{servicos_invalidos} Serviço(s) com dados inválidos "
                        "foram omitidos."
                    )
                self.aviso = " ".join(avisos)

                if not pets_validos:
                    self.erro = (
                        "Nenhum Pet válido cadastrado. Cadastre ou corrija um Pet "
                        "antes de agendar."
                    )
                elif not servicos_validos:
                    self.erro = (
                        "Nenhum Serviço válido cadastrado. Cadastre ou corrija um "
                        "Serviço antes de agendar."
                    )

        self.carregando_dados = False
        self._atualizar_calendario()

    @rx.event
    def selecionar_pet(self, opcao: str):
        pet_id = opcao.split(" - ", 1)[0]
        if not any(pet["id"] == pet_id for pet in self.pets):
            self.erro = "Selecione um Pet cadastrado."
            return
        self.pet_selecionado = opcao
        self.erro = ""
        self.mensagem = ""

    @rx.event
    def selecionar_servico(self, opcao: str):
        servico_id = opcao.split(" - ", 1)[0]
        if not any(servico["id"] == servico_id for servico in self.servicos):
            self.erro = "Selecione um Serviço cadastrado."
            return

        self.servico_selecionado = opcao
        self.data_selecionada = ""
        self.horario_selecionado = ""
        self.horarios = []
        self.mensagem = ""
        self.sucesso = False
        self._carregar_disponibilidade()

    def _carregar_disponibilidade(self):
        if not self.servico_selecionado:
            self.dias_disponibilidade = []
            self.horarios_mes = []
            self._atualizar_calendario()
            return

        servico_id = int(self.servico_selecionado.split(" - ", 1)[0])
        self.carregando_disponibilidade = True
        self.erro = ""
        self.dias_disponibilidade = []
        self.horarios_mes = []
        try:
            response = httpx.get(
                f"{XANO_API_URL}/agendamento_disponibilidade",
                params={
                    "servico_id": servico_id,
                    "ano": self.ano,
                    "mes": self.mes,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            dados = response.json()
        except httpx.HTTPStatusError as error:
            self.erro = (
                "Erro ao consultar disponibilidade no Xano: "
                f"HTTP {error.response.status_code}."
            )
            self.dias_disponibilidade = []
            self.horarios_mes = []
        except httpx.RequestError as error:
            self.erro = f"Erro de conexão ao consultar disponibilidade: {error}"
            self.dias_disponibilidade = []
            self.horarios_mes = []
        except ValueError:
            self.erro = "O Xano retornou uma disponibilidade inválida."
            self.dias_disponibilidade = []
            self.horarios_mes = []
        else:
            dias = []
            horarios_mes = []
            if not isinstance(dados, list):
                self.erro = "O Xano retornou uma disponibilidade inválida."
            else:
                for dia in dados:
                    if (
                        not isinstance(dia, dict)
                        or not isinstance(dia.get("data"), str)
                        or not isinstance(dia.get("horarios"), list)
                        or not isinstance(
                            dia.get("tem_horario_disponivel"), bool
                        )
                    ):
                        self.erro = (
                            "O Xano retornou um dia de disponibilidade inválido."
                        )
                        break

                    horarios = []
                    for horario in dia["horarios"]:
                        if (
                            not isinstance(horario, dict)
                            or not isinstance(horario.get("hora"), str)
                            or not isinstance(horario.get("disponivel"), bool)
                        ):
                            self.erro = (
                                "O Xano retornou um horário de disponibilidade inválido."
                            )
                            break
                        data_hora = timestamp_em_milissegundos(
                            horario.get("data_hora")
                        )
                        if data_hora is None:
                            self.erro = (
                                "O Xano retornou um horário sem data válida."
                            )
                            break
                        horarios.append(
                            {
                                "data": dia["data"],
                                "data_hora": str(data_hora),
                                "hora": horario["hora"],
                                "disponivel": str(
                                    horario["disponivel"]
                                ).lower(),
                            }
                        )
                    if self.erro:
                        break
                    dias.append({
                        "data": dia["data"],
                        "tem_horario_disponivel": str(
                            dia["tem_horario_disponivel"]
                        ).lower(),
                    })
                    horarios_mes.extend(horarios)
                if not self.erro:
                    self.dias_disponibilidade = dias
                    self.horarios_mes = horarios_mes

        self.carregando_disponibilidade = False
        self._atualizar_calendario()

    def _recarregar_apos_falha(self, mensagem_erro: str):
        self._carregar_disponibilidade()
        if self.erro:
            self.erro = f"{mensagem_erro} {self.erro}"
        else:
            self.erro = mensagem_erro

    @rx.event
    def mudar_mes(self, incremento: int):
        ano = self.ano
        mes = self.mes + incremento
        if mes < 1:
            ano -= 1
            mes = 12
        elif mes > 12:
            ano += 1
            mes = 1

        agora = datetime.now(FUSO_AGENDAMENTO)
        if (ano, mes) < (agora.year, agora.month):
            return

        self.ano = ano
        self.mes = mes
        self.data_selecionada = ""
        self.horario_selecionado = ""
        self.horarios = []
        self.mensagem = ""
        self._carregar_disponibilidade()

    @rx.event
    def selecionar_dia(self, data: str):
        dia = next(
            (
                item
                for item in self.dias_disponibilidade
                if (
                    item["data"] == data
                    and item["tem_horario_disponivel"] == "true"
                )
            ),
            None,
        )
        if dia is None:
            self.erro = "Este dia não possui horários disponíveis."
            return

        self.data_selecionada = data
        self.horarios = [
            horario
            for horario in self.horarios_mes
            if horario["data"] == data
        ]
        self.horario_selecionado = ""
        self.erro = ""
        self.mensagem = ""
        self.sucesso = False

    @rx.event
    def selecionar_horario(self, data_hora: str):
        horario = next(
            (
                item
                for item in self.horarios
                if (
                    item["data_hora"] == data_hora
                    and item["disponivel"] == "true"
                )
            ),
            None,
        )
        if horario is None:
            self.erro = "Selecione um horário que ainda esteja disponível."
            return
        self.horario_selecionado = horario["data_hora"]
        self.erro = ""
        self.mensagem = ""
        self.sucesso = False

    @rx.event
    def confirmar_agendamento(self):
        if self.processando:
            return
        if not self.pet_selecionado or not self.servico_selecionado:
            self.erro = "Selecione um Pet e um Serviço antes de agendar."
            return
        if not self.data_selecionada or not self.horario_selecionado:
            self.erro = "Selecione um dia e horário disponíveis."
            return

        pet_id = int(self.pet_selecionado.split(" - ", 1)[0])
        servico_id = int(self.servico_selecionado.split(" - ", 1)[0])
        data_hora = int(self.horario_selecionado)
        self.processando = True
        self.erro = ""
        self.mensagem = "Confirmando agendamento..."
        self.sucesso = False

        try:
            response = httpx.post(
                f"{XANO_API_URL}/agendamento",
                json={
                    "pet_id": pet_id,
                    "servico_id": servico_id,
                    "data_hora": data_hora,
                },
                timeout=20.0,
            )
            response.raise_for_status()
            agendamento = response.json()
        except httpx.HTTPStatusError as error:
            self.mensagem = ""
            if error.response.status_code == 429:
                tempo_espera = error.response.headers.get("Retry-After")
                if tempo_espera and tempo_espera.isdigit():
                    self.erro = (
                        "O Xano limitou temporariamente as chamadas. "
                        f"Aguarde {tempo_espera} segundos antes de tentar novamente."
                    )
                else:
                    self.erro = (
                        "O Xano limitou temporariamente as chamadas. "
                        "Aguarde um pouco antes de tentar novamente."
                    )
            else:
                self.erro = (
                    "O Xano não confirmou o agendamento: "
                    f"HTTP {error.response.status_code}."
                )
                if error.response.status_code < 500:
                    self._recarregar_apos_falha(self.erro)
        except httpx.RequestError as error:
            self.mensagem = ""
            self.erro = f"Erro de conexão ao confirmar agendamento: {error}"
        except ValueError:
            self.mensagem = ""
            self.erro = "O Xano retornou uma confirmação inválida."
        else:
            data_hora_confirmada = (
                timestamp_em_milissegundos(agendamento.get("data_hora"))
                if isinstance(agendamento, dict)
                else None
            )
            if (
                not isinstance(agendamento, dict)
                or agendamento.get("id") is None
                or agendamento.get("pet_id") != pet_id
                or agendamento.get("servico_id") != servico_id
                or data_hora_confirmada != data_hora
                or agendamento.get("status") != "Agendado"
            ):
                self.mensagem = ""
                self.erro = (
                    "O Xano não confirmou os dados persistidos do agendamento."
                )
            else:
                self.mensagem = "Agendado com sucesso!"
                self.sucesso = True
                self.horario_selecionado = ""
                self.data_selecionada = ""
                self.horarios = []
                self._carregar_disponibilidade()
        finally:
            self.processando = False


class ListaAgendamentosState(rx.State):
    agendamentos: list[dict[str, str]] = []
    id_selecionado: str = ""
    detalhe_selecionado: dict[str, str] = {}
    carregando: bool = False
    erro: str = ""

    @rx.var
    def sem_agendamentos(self) -> bool:
        return not self.carregando and not self.erro and not self.agendamentos

    @rx.event
    def carregar_agendamentos(self):
        self.carregando = True
        self.erro = ""
        self.agendamentos = []
        self.id_selecionado = ""
        self.detalhe_selecionado = {}

        try:
            agendamentos = buscar_lista_xano("agendamento")
            pets = buscar_lista_xano("pet")
            servicos = buscar_lista_xano("servico")
            tutores = buscar_lista_xano("tutor")
        except httpx.HTTPStatusError as error:
            endpoint = error.request.url.path.rsplit("/", 1)[-1]
            self.erro = (
                f"Não foi possível carregar {endpoint} no Xano: "
                f"HTTP {error.response.status_code}."
            )
        except httpx.RequestError as error:
            endpoint = error.request.url.path.rsplit("/", 1)[-1]
            self.erro = f"Erro de conexão ao carregar {endpoint}: {error}"
        except ValueError as error:
            self.erro = str(error)
        else:
            pets_por_id = {
                item_id: pet
                for pet in pets
                if (item_id := normalizar_id(pet.get("id"))) is not None
            }
            servicos_por_id = {
                item_id: servico
                for servico in servicos
                if (item_id := normalizar_id(servico.get("id"))) is not None
            }
            tutores_por_id = {
                item_id: tutor
                for tutor in tutores
                if (item_id := normalizar_id(tutor.get("id"))) is not None
            }
            registros = []

            for agendamento in agendamentos:
                agendamento_id = normalizar_id(agendamento.get("id"))
                pet_id = normalizar_id(agendamento.get("pet_id"))
                servico_id = normalizar_id(agendamento.get("servico_id"))
                data_hora = formatar_data_hora_agendamento(
                    agendamento.get("data_hora")
                )
                status = agendamento.get("status")
                if (
                    agendamento_id is None
                    or pet_id is None
                    or servico_id is None
                    or data_hora is None
                    or not isinstance(status, str)
                    or not status.strip()
                ):
                    self.erro = (
                        "O Xano retornou um agendamento com identificadores, "
                        "data/hora ou status inválidos."
                    )
                    break

                pet = pets_por_id.get(pet_id)
                servico = servicos_por_id.get(servico_id)
                tutor_id = (
                    normalizar_id(pet.get("tutor_id"))
                    if pet is not None
                    else None
                )
                tutor = tutores_por_id.get(tutor_id or "")
                pet_nome = (
                    pet.get("nome")
                    if pet is not None and isinstance(pet.get("nome"), str)
                    else f"Pet não encontrado (ID {pet_id})"
                )
                tutor_nome = (
                    tutor.get("nome")
                    if tutor is not None
                    and isinstance(tutor.get("nome"), str)
                    else (
                        f"Tutor não encontrado (ID {tutor_id})"
                        if tutor_id
                        else "Tutor não encontrado"
                    )
                )
                servico_nome = (
                    servico.get("nome")
                    if servico is not None
                    and isinstance(servico.get("nome"), str)
                    else f"Serviço não encontrado (ID {servico_id})"
                )
                registros.append({
                    "id": agendamento_id,
                    "pet": pet_nome,
                    "tutor": tutor_nome,
                    "servico": servico_nome,
                    "data_hora": data_hora,
                    "status": status.strip(),
                    "timestamp": str(
                        timestamp_em_milissegundos(
                            agendamento.get("data_hora")
                        )
                    ),
                })

            if not self.erro:
                self.agendamentos = sorted(
                    registros,
                    key=lambda item: int(item["timestamp"]),
                    reverse=True,
                )

        self.carregando = False

    @rx.event
    def selecionar_agendamento(self, agendamento_id: str):
        agendamento = next(
            (
                item
                for item in self.agendamentos
                if item["id"] == agendamento_id
            ),
            None,
        )
        if agendamento is None:
            self.erro = "O agendamento selecionado não está na lista."
            self.id_selecionado = ""
            self.detalhe_selecionado = {}
            return

        self.id_selecionado = agendamento_id
        self.detalhe_selecionado = agendamento
        self.erro = ""

    @rx.event
    def fechar_detalhe(self):
        self.id_selecionado = ""
        self.detalhe_selecionado = {}


def buscar_lista_xano(endpoint: str) -> list[dict[str, object]]:
    response = httpx.get(f"{XANO_API_URL}/{endpoint}", timeout=15.0)
    response.raise_for_status()
    dados = response.json()
    if not isinstance(dados, list) or any(
        not isinstance(item, dict) for item in dados
    ):
        raise ValueError(
            f"O Xano retornou uma lista inválida para /{endpoint}."
        )
    return dados


def calendario_agendamento() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.button(
                "‹",
                on_click=AgendamentoState.mudar_mes(-1),
                disabled=(
                    (AgendamentoState.ano == datetime.now(FUSO_AGENDAMENTO).year)
                    & (
                        AgendamentoState.mes
                        == datetime.now(FUSO_AGENDAMENTO).month
                    )
                ),
            ),
            rx.heading(AgendamentoState.titulo_mes, size="5"),
            rx.button(
                "›",
                on_click=AgendamentoState.mudar_mes(1),
            ),
            align="center",
            justify="between",
            width="100%",
        ),
        rx.grid(
            *[
                rx.text(dia, weight="bold", align="center")
                for dia in ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
            ],
            columns="repeat(7, 1fr)",
            width="100%",
        ),
        rx.grid(
            rx.foreach(
                AgendamentoState.dias_calendario,
                lambda dia: rx.cond(
                dia["espaco"] == "true",
                    rx.box(height="40px"),
                    rx.button(
                    dia["numero"],
                    on_click=AgendamentoState.selecionar_dia(dia["data"]),
                    disabled=dia["habilitado"] != "true",
                    color_scheme=rx.cond(
                        dia["habilitado"] == "true",
                        "blue",
                        "gray",
                    ),
                    variant=rx.cond(
                        dia["data"] == AgendamentoState.data_selecionada,
                        "solid",
                        "outline",
                    ),
                        width="100%",
                    ),
                ),
            ),
            columns="repeat(7, 1fr)",
            width="100%",
        ),
        spacing="3",
        width="100%",
    )


def fluxo_agendamento() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Novo Agendamento", size="8"),
            rx.text(
                "Selecione um Pet, um Serviço, o dia e um horário disponível.",
                size="3",
            ),
            rx.hstack(
                rx.link("Cadastro de Tutor", href="/tutores"),
                rx.link("Cadastro de Pet", href="/pets"),
                rx.link("Cadastro de Serviço", href="/servicos"),
                rx.link("Consultar agendamentos", href="/agendamentos/lista"),
                spacing="4",
                wrap="wrap",
            ),
            rx.cond(
                AgendamentoState.carregando_dados,
                rx.text("Carregando Pets e Serviços..."),
                rx.vstack(
                    rx.text("Pet:"),
                    rx.select(
                        AgendamentoState.opcoes_pet,
                        value=AgendamentoState.pet_selecionado,
                        on_change=AgendamentoState.selecionar_pet,
                        placeholder="Selecione o Pet",
                        width="100%",
                    ),
                    rx.text("Serviço:"),
                    rx.select(
                        AgendamentoState.opcoes_servico,
                        value=AgendamentoState.servico_selecionado,
                        on_change=AgendamentoState.selecionar_servico,
                        placeholder="Selecione o Serviço",
                        width="100%",
                    ),
                    rx.cond(
                        (AgendamentoState.servico_selecionado != "")
                        & (AgendamentoState.pet_selecionado == ""),
                        rx.text("Selecione um Pet para visualizar o calendário."),
                    ),
                    rx.cond(
                        AgendamentoState.carregando_disponibilidade,
                        rx.text("Consultando disponibilidade..."),
                        rx.cond(
                                    (AgendamentoState.servico_selecionado != "")
                                    & (AgendamentoState.pet_selecionado != ""),
                            rx.vstack(
                                rx.heading("Selecione o dia", size="5"),
                                calendario_agendamento(),
                                rx.cond(
                                    AgendamentoState.data_selecionada != "",
                                    rx.vstack(
                                        rx.heading(
                                            "Horários disponíveis",
                                            size="5",
                                        ),
                                        rx.grid(
                                            rx.foreach(
                                                AgendamentoState.horarios,
                                                lambda horario: rx.button(
                                                    horario["hora"],
                                                    on_click=AgendamentoState
                                                    .selecionar_horario(
                                                        horario["data_hora"]
                                                    ),
                                                    disabled=(
                                                        horario["disponivel"]
                                                        != "true"
                                                    ),
                                                    color_scheme=rx.cond(
                                                        horario["disponivel"]
                                                        == "true",
                                                        "blue",
                                                        "gray",
                                                    ),
                                                    variant=rx.cond(
                                                        horario["data_hora"]
                                                        == AgendamentoState
                                                        .horario_selecionado,
                                                        "solid",
                                                        "outline",
                                                    ),
                                                ),
                                            ),
                                            columns="repeat(4, 1fr)",
                                            width="100%",
                                        ),
                                        rx.button(
                                            "Confirmar agendamento",
                                            on_click=AgendamentoState
                                            .confirmar_agendamento,
                                            loading=AgendamentoState.processando,
                                            disabled=(
                                                (
                                                    AgendamentoState
                                                    .horario_selecionado
                                                    == ""
                                                )
                                                | AgendamentoState.processando
                                            ),
                                            width="100%",
                                        ),
                                        width="100%",
                                        spacing="3",
                                    ),
                                ),
                                width="100%",
                                spacing="4",
                            ),
                        ),
                    ),
                    rx.cond(
                        AgendamentoState.erro != "",
                        rx.text(AgendamentoState.erro, color="red", size="2"),
                    ),
                    rx.cond(
                        AgendamentoState.aviso != "",
                        rx.text(
                            AgendamentoState.aviso,
                            color="orange",
                            size="2",
                        ),
                    ),
                    rx.cond(
                        AgendamentoState.mensagem != "",
                        rx.text(
                            AgendamentoState.mensagem,
                            color=rx.cond(
                                AgendamentoState.sucesso,
                                "green",
                                "blue",
                            ),
                            size="2",
                        ),
                    ),
                    width="100%",
                    max_width="600px",
                    padding="20px",
                    border="1px solid #ddd",
                    border_radius="10px",
                    spacing="3",
                ),
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
            width="100%",
        ),
    )


def lista_agendamentos() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Agendamentos", size="8"),
            rx.text(
                "Consulte os atendimentos cadastrados e seus vínculos.",
                size="3",
            ),
            rx.hstack(
                rx.link("Novo agendamento", href="/agendamentos"),
                rx.link("Cadastro de tutor", href="/tutores"),
                rx.button(
                    "Atualizar lista",
                    on_click=ListaAgendamentosState.carregar_agendamentos,
                    loading=ListaAgendamentosState.carregando,
                    disabled=ListaAgendamentosState.carregando,
                ),
                align="center",
                spacing="4",
                width="100%",
            ),
            rx.cond(
                ListaAgendamentosState.erro != "",
                rx.text(ListaAgendamentosState.erro, color="red", size="2"),
            ),
            rx.cond(
                ListaAgendamentosState.carregando,
                rx.text("Carregando agendamentos..."),
            ),
            rx.cond(
                ListaAgendamentosState.sem_agendamentos,
                rx.text("Nenhum agendamento cadastrado."),
            ),
            rx.foreach(
                ListaAgendamentosState.agendamentos,
                lambda agendamento: rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.heading(agendamento["pet"], size="4"),
                            rx.text(agendamento["servico"]),
                            rx.text(agendamento["data_hora"]),
                            rx.hstack(
                                rx.text("Status:", weight="bold"),
                                rx.text(agendamento["status"]),
                                spacing="2",
                            ),
                            align="start",
                            spacing="1",
                        ),
                        rx.spacer(),
                        rx.button(
                            "Ver detalhes",
                            on_click=ListaAgendamentosState
                            .selecionar_agendamento(agendamento["id"]),
                        ),
                        align="center",
                        width="100%",
                    ),
                    border="1px solid #ddd",
                    border_radius="10px",
                    padding="16px",
                    width="100%",
                ),
            ),
            rx.cond(
                ListaAgendamentosState.id_selecionado != "",
                rx.vstack(
                    rx.heading("Detalhes do agendamento", size="6"),
                    rx.hstack(
                        rx.text("Tutor:", weight="bold"),
                        rx.text(
                            ListaAgendamentosState
                            .detalhe_selecionado["tutor"]
                        ),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("Pet:", weight="bold"),
                        rx.text(
                            ListaAgendamentosState
                            .detalhe_selecionado["pet"]
                        ),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("Serviço:", weight="bold"),
                        rx.text(
                            ListaAgendamentosState
                            .detalhe_selecionado["servico"]
                        ),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("Data e hora:", weight="bold"),
                        rx.text(
                            ListaAgendamentosState
                            .detalhe_selecionado["data_hora"]
                        ),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("Status:", weight="bold"),
                        rx.text(
                            ListaAgendamentosState
                            .detalhe_selecionado["status"]
                        ),
                        spacing="2",
                    ),
                    rx.button(
                        "Fechar detalhes",
                        on_click=ListaAgendamentosState.fechar_detalhe,
                    ),
                    align="start",
                    width="100%",
                    border="1px solid #aaa",
                    border_radius="10px",
                    padding="20px",
                    spacing="3",
                ),
            ),
            spacing="4",
            width="100%",
            max_width="800px",
            padding="24px",
            align="start",
            min_height="85vh",
        ),
        width="100%",
    )


def cadastro_servico() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Cadastro de Serviço", size="8"),
            rx.text("Cadastre um serviço oferecido pelo estabelecimento.", size="3"),
            rx.link("Voltar ao cadastro de tutor", href="/tutores"),
            rx.link("Ir para cadastro de pet", href="/pets"),
            rx.link("Agendar atendimento", href="/agendamentos"),
            rx.link("Consultar agendamentos", href="/agendamentos/lista"),
            rx.link("Página inicial", href="/"),
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
app.add_page(login, route="/")
app.add_page(index, route="/tutores")
app.add_page(
    cadastro_pet,
    route="/pets",
    on_load=PetState.carregar_tutores,
)
app.add_page(cadastro_servico, route="/servicos")
app.add_page(
    fluxo_agendamento,
    route="/agendamentos",
    on_load=AgendamentoState.carregar_dados,
)
app.add_page(
    lista_agendamentos,
    route="/agendamentos/lista",
    on_load=ListaAgendamentosState.carregar_agendamentos,
)
