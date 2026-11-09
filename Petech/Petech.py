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
    """Estado para gerenciar cadastro, listagem e edição de tutores."""
    nome: str = ""
    email: str = ""
    telefone: str = ""
    processando: bool = False
    mensagem: str = ""
    tutores: list[dict[str, str]] = []
    tem_tutores: bool = False
    carregando_tutores: bool = False
    erro_lista: str = ""
    tutor_id_edicao: str = ""
    nome_edicao: str = ""
    email_edicao: str = ""
    telefone_edicao: str = ""
    editando: bool = False
    processando_edicao: bool = False
    mensagem_edicao: str = ""
    sucesso_edicao: bool = False
    tutor_id_exclusao: str = ""
    processando_exclusao: bool = False
    mensagem_exclusao: str = ""
    sucesso_exclusao: bool = False

    def set_nome(self, nome: str):
        self.nome = nome

    def set_email(self, email: str):
        self.email = email

    def set_telefone(self, telefone: str):
        self.telefone = telefone

    def set_nome_edicao(self, nome: str):
        self.nome_edicao = nome

    def set_email_edicao(self, email: str):
        self.email_edicao = email

    def set_telefone_edicao(self, telefone: str):
        self.telefone_edicao = telefone

    def carregar_tutores(self):
        """Carrega os tutores existentes para a lista de edição."""
        self.carregando_tutores = True
        self.erro_lista = ""

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
            self.erro_lista = f"Erro ao carregar tutores: {err_msg}"
            self.tutores = []
            self.tem_tutores = False
        except httpx.RequestError as error:
            self.erro_lista = f"Erro de conexão ao carregar tutores: {error}"
            self.tutores = []
            self.tem_tutores = False
        except ValueError:
            self.erro_lista = "O Xano retornou uma lista de tutores inválida."
            self.tutores = []
            self.tem_tutores = False
        else:
            if not isinstance(tutores, list):
                self.erro_lista = "O Xano retornou uma lista de tutores inválida."
                self.tutores = []
                self.tem_tutores = False
            else:
                tutores_validos: list[dict[str, str]] = []
                for tutor in tutores:
                    if not isinstance(tutor, dict):
                        self.erro_lista = (
                            "O Xano retornou um tutor com dados inválidos."
                        )
                        break

                    tutor_id = normalizar_id(tutor.get("id"))
                    nome = tutor.get("nome")
                    email = tutor.get("email")
                    telefone = tutor.get("telefone")
                    if (
                        tutor_id is None
                        or not isinstance(nome, str)
                        or not nome.strip()
                        or (email is not None and not isinstance(email, str))
                        or (
                            telefone is not None
                            and not isinstance(telefone, str)
                        )
                    ):
                        self.erro_lista = (
                            "O Xano retornou um tutor sem identificador "
                            "ou com dados inválidos."
                        )
                        break

                    tutores_validos.append(
                        {
                            "id": tutor_id,
                            "nome": nome.strip(),
                            "email": email or "",
                            "telefone": telefone or "",
                        }
                    )

                if self.erro_lista:
                    self.tutores = []
                    self.tem_tutores = False
                else:
                    self.tutores = tutores_validos
                    self.tem_tutores = bool(tutores_validos)
                    if not self.tutores:
                        self.erro_lista = "Nenhum tutor cadastrado."
        finally:
            self.carregando_tutores = False

    def iniciar_edicao(self, tutor_id: str):
        tutor = next(
            (item for item in self.tutores if item["id"] == tutor_id),
            None,
        )
        if tutor is None:
            self.erro_lista = "Não foi possível localizar o tutor selecionado."
            return

        self.tutor_id_edicao = tutor["id"]
        self.nome_edicao = tutor["nome"]
        self.email_edicao = tutor["email"]
        self.telefone_edicao = tutor["telefone"]
        self.mensagem_edicao = ""
        self.sucesso_edicao = False
        self.editando = True

    def cancelar_edicao(self):
        if self.processando_edicao:
            return
        self.editando = False
        self.tutor_id_edicao = ""
        self.nome_edicao = ""
        self.email_edicao = ""
        self.telefone_edicao = ""
        self.mensagem_edicao = ""
        self.sucesso_edicao = False

    def iniciar_exclusao(self, tutor_id: str):
        if self.processando_exclusao or self.processando_edicao:
            return
        if not any(tutor["id"] == tutor_id for tutor in self.tutores):
            self.erro_lista = "Não foi possível localizar o tutor selecionado."
            return
        self.tutor_id_exclusao = tutor_id
        self.mensagem_exclusao = ""
        self.sucesso_exclusao = False

    def cancelar_exclusao(self):
        if self.processando_exclusao:
            return
        self.tutor_id_exclusao = ""
        self.mensagem_exclusao = ""
        self.sucesso_exclusao = False

    def confirmar_exclusao(self):
        tutor_id = normalizar_id(self.tutor_id_exclusao)
        if tutor_id is None:
            self.mensagem_exclusao = "Selecione um tutor válido para excluir."
            self.sucesso_exclusao = False
            return

        self.processando_exclusao = True
        self.mensagem_exclusao = "Excluindo tutor..."
        self.sucesso_exclusao = False
        try:
            response = httpx.delete(
                f"{XANO_API_URL}/tutor/{tutor_id}",
                timeout=10.0,
            )
            response.raise_for_status()
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
            self.mensagem_exclusao = f"Erro ao excluir tutor: {err_msg}"
        except httpx.RequestError as error:
            self.mensagem_exclusao = (
                f"Erro de conexão com o Xano: {error}"
            )
        else:
            resultado = None
            if response.content:
                try:
                    resultado = response.json()
                except ValueError:
                    resultado = None

            exclusao_confirmada = (
                isinstance(resultado, dict)
                and normalizar_id(resultado.get("id")) == tutor_id
                and resultado.get("deleted") is True
            )
            if not exclusao_confirmada:
                try:
                    verificacao = httpx.get(
                        f"{XANO_API_URL}/tutor/{tutor_id}",
                        timeout=10.0,
                    )
                    verificacao.raise_for_status()
                except httpx.HTTPStatusError as error:
                    if error.response.status_code == 404:
                        exclusao_confirmada = True
                    else:
                        self.mensagem_exclusao = (
                            "O Xano respondeu à exclusão, mas não foi possível "
                            "verificar se o tutor foi removido."
                        )
                except httpx.RequestError as error:
                    self.mensagem_exclusao = (
                        "A solicitação de exclusão foi enviada, mas não foi "
                        f"possível confirmar o resultado: {error}"
                    )
                else:
                    self.mensagem_exclusao = (
                        "O tutor ainda consta no Xano; a exclusão não foi "
                        "confirmada."
                    )

            if not exclusao_confirmada:
                if not self.mensagem_exclusao or (
                    self.mensagem_exclusao == "Excluindo tutor..."
                ):
                    self.mensagem_exclusao = (
                        "O Xano não confirmou a exclusão do tutor."
                    )
            else:
                self.tutores = [
                    tutor
                    for tutor in self.tutores
                    if tutor["id"] != tutor_id
                ]
                self.tem_tutores = bool(self.tutores)
                self.erro_lista = (
                    "" if self.tem_tutores else "Nenhum tutor cadastrado."
                )
                self.tutor_id_exclusao = ""
                self.mensagem_exclusao = "Tutor excluído com sucesso."
                self.sucesso_exclusao = True
                if self.tutor_id_edicao == tutor_id:
                    self.editando = False
                    self.tutor_id_edicao = ""
                    self.nome_edicao = ""
                    self.email_edicao = ""
                    self.telefone_edicao = ""
                    self.mensagem_edicao = ""
                    self.sucesso_edicao = False
        finally:
            self.processando_exclusao = False

    def salvar_edicao(self):
        tutor_id = normalizar_id(self.tutor_id_edicao)
        nome = self.nome_edicao.strip()
        email = self.email_edicao.strip() or None
        telefone = self.telefone_edicao.strip() or None
        if tutor_id is None:
            self.mensagem_edicao = "Selecione um tutor válido para editar."
            self.sucesso_edicao = False
            return
        if not nome:
            self.mensagem_edicao = "O nome é obrigatório."
            self.sucesso_edicao = False
            return

        self.processando_edicao = True
        self.mensagem_edicao = "Salvando alterações..."
        self.sucesso_edicao = False
        dados = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
        }

        try:
            response = httpx.patch(
                f"{XANO_API_URL}/tutor/{tutor_id}",
                json=dados,
                timeout=10.0,
            )
            response.raise_for_status()
            tutor_atualizado = response.json()
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
            self.mensagem_edicao = f"Erro ao alterar tutor: {err_msg}"
        except httpx.RequestError as error:
            self.mensagem_edicao = f"Erro de conexão com o Xano: {error}"
        except ValueError:
            self.mensagem_edicao = "O Xano retornou uma resposta inválida."
        else:
            dados_confirmados = (
                isinstance(tutor_atualizado, dict)
                and normalizar_id(tutor_atualizado.get("id")) == tutor_id
                and tutor_atualizado.get("nome") == nome
                and tutor_atualizado.get("email") == email
                and tutor_atualizado.get("telefone") == telefone
            )
            if not dados_confirmados:
                self.mensagem_edicao = (
                    "O Xano não confirmou a alteração dos dados do tutor."
                )
            else:
                self.mensagem_edicao = "Tutor alterado com sucesso."
                self.sucesso_edicao = True
                self.tutores = [
                    {
                        "id": tutor_id,
                        "nome": nome,
                        "email": email or "",
                        "telefone": telefone or "",
                    }
                    if tutor["id"] == tutor_id
                    else tutor
                    for tutor in self.tutores
                ]
        finally:
            self.processando_edicao = False

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
            tutor_id = (
                normalizar_id(tutor.get("id"))
                if isinstance(tutor, dict)
                else None
            )
            if tutor_id is None:
                self.mensagem = "O Xano não confirmou a gravação do tutor."
            else:
                self.mensagem = f"Tutor cadastrado com sucesso! ID: {tutor_id}"
                self.nome = ""
                self.email = ""
                self.telefone = ""
                self.tutores = [
                    item for item in self.tutores if item["id"] != tutor_id
                ]
                self.tutores.append(
                    {
                        "id": tutor_id,
                        "nome": nome,
                        "email": dados.get("email", ""),
                        "telefone": dados.get("telefone", ""),
                    }
                )
                self.tem_tutores = True
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


class ClienteAuthState(rx.State):
    nome: str = ""
    cpf: str = ""
    telefone: str = ""
    email: str = ""
    senha: str = ""
    confirmar_senha: str = ""
    mensagem: str = ""
    processando: bool = False
    nome_cliente: str = ""
    cpf_cliente: str = ""
    telefone_cliente: str = ""
    email_cliente: str = ""
    pets_cliente: list[dict[str, str]] = []
    agendamentos_ativos_cliente: list[dict[str, str]] = []
    agendamentos_historico_cliente: list[dict[str, str]] = []
    carregando_dashboard: bool = False
    formulario_pet_cliente_aberto: bool = False
    processando_pet_cliente: bool = False
    mensagem_pet_cliente: str = ""
    sucesso_pet_cliente: bool = False
    pet_cliente_nome: str = ""
    pet_cliente_especie: str = ""
    pet_cliente_raca: str = ""
    pet_cliente_porte: str = ""
    pet_cliente_observacoes: str = ""
    formulario_agendamento_cliente_aberto: bool = False
    carregando_servicos_cliente: bool = False
    servicos_cliente: list[dict[str, str]] = []
    opcoes_servicos_cliente: list[str] = []
    opcoes_pets_agendamento_cliente: list[str] = []
    pet_agendamento_cliente: str = ""
    servico_agendamento_cliente: str = ""
    ano_agendamento_cliente: int = 0
    mes_agendamento_cliente: int = 0
    titulo_mes_agendamento_cliente: str = ""
    dias_calendario_agendamento_cliente: list[dict[str, str]] = []
    dias_disponibilidade_agendamento_cliente: list[dict[str, str]] = []
    horarios_mes_agendamento_cliente: list[dict[str, str]] = []
    horarios_agendamento_cliente: list[dict[str, str]] = []
    data_agendamento_cliente: str = ""
    horario_agendamento_cliente: str = ""
    carregando_disponibilidade_cliente: bool = False
    processando_agendamento_cliente: bool = False
    mensagem_agendamento_cliente: str = ""
    erro_agendamento_cliente: str = ""
    sucesso_agendamento_cliente: bool = False
    _auth_token: str = ""
    _tutor_id: str = ""

    def _limpar_dados_dashboard(self):
        self.nome_cliente = ""
        self.cpf_cliente = ""
        self.telefone_cliente = ""
        self.email_cliente = ""
        self.pets_cliente = []
        self.opcoes_pets_agendamento_cliente = []
        self.agendamentos_ativos_cliente = []
        self.agendamentos_historico_cliente = []
        self.formulario_pet_cliente_aberto = False
        self.formulario_agendamento_cliente_aberto = False
        self.servicos_cliente = []
        self.opcoes_servicos_cliente = []
        self.pet_agendamento_cliente = ""
        self.servico_agendamento_cliente = ""
        self.dias_calendario_agendamento_cliente = []
        self.dias_disponibilidade_agendamento_cliente = []
        self.horarios_mes_agendamento_cliente = []
        self.horarios_agendamento_cliente = []
        self.data_agendamento_cliente = ""
        self.horario_agendamento_cliente = ""
        self.pet_cliente_nome = ""
        self.pet_cliente_especie = ""
        self.pet_cliente_raca = ""
        self.pet_cliente_porte = ""
        self.pet_cliente_observacoes = ""
        self.mensagem_pet_cliente = ""
        self.sucesso_pet_cliente = False
        self.processando_pet_cliente = False
        self.erro_agendamento_cliente = ""
        self.mensagem_agendamento_cliente = ""
        self.sucesso_agendamento_cliente = False
        self.processando_agendamento_cliente = False
        self.carregando_servicos_cliente = False
        self.carregando_disponibilidade_cliente = False

    def _processar_resposta_dashboard(self, dados: object) -> bool:
        if not isinstance(dados, dict):
            return False

        tutor = dados.get("tutor")
        pets = dados.get("pets")
        agendamentos = dados.get("agendamentos")
        if (
            not isinstance(tutor, dict)
            or normalizar_id(tutor.get("id")) != self._tutor_id
            or not isinstance(tutor.get("nome"), str)
            or not tutor["nome"].strip()
            or not isinstance(tutor.get("cpf"), str)
            or not tutor["cpf"].strip()
            or not isinstance(tutor.get("telefone"), str)
            or not tutor["telefone"].strip()
            or not isinstance(tutor.get("email"), str)
            or not tutor["email"].strip()
            or not isinstance(pets, list)
            or not isinstance(agendamentos, list)
        ):
            return False

        pets_validos: list[dict[str, str]] = []
        for pet in pets:
            if not isinstance(pet, dict) or normalizar_id(pet.get("id")) is None:
                return False

            nome = pet.get("nome")
            especie = pet.get("especie")
            porte = pet.get("porte")
            raca = pet.get("raca")
            if (
                not isinstance(nome, str)
                or not nome.strip()
                or not isinstance(especie, str)
                or not especie.strip()
                or not isinstance(porte, str)
                or not porte.strip()
                or (raca is not None and not isinstance(raca, str))
            ):
                return False

            pets_validos.append(
                {
                    "id": normalizar_id(pet.get("id")) or "",
                    "nome": nome.strip(),
                    "especie": especie.strip(),
                    "raca": (
                        raca.strip()
                        if isinstance(raca, str) and raca.strip()
                        else "Não informada"
                    ),
                    "porte": porte.strip(),
                }
            )

        ativos: list[dict[str, str]] = []
        historico: list[dict[str, str]] = []
        for agendamento in agendamentos:
            if (
                not isinstance(agendamento, dict)
                or normalizar_id(agendamento.get("id")) is None
            ):
                return False

            pet_nome = agendamento.get("pet_nome")
            servico_nome = agendamento.get("servico_nome")
            status = agendamento.get("status")
            data_hora = formatar_data_hora_agendamento(
                agendamento.get("data_hora")
            )
            if (
                not isinstance(pet_nome, str)
                or not pet_nome.strip()
                or not isinstance(servico_nome, str)
                or not servico_nome.strip()
                or not isinstance(status, str)
                or status not in (
                    "Agendado",
                    "Em Andamento",
                    "Concluído",
                    "Cancelado",
                )
                or data_hora is None
            ):
                return False

            item = {
                "pet_nome": pet_nome.strip(),
                "servico_nome": servico_nome.strip(),
                "data_hora": data_hora,
                "status": status,
            }
            if status in ("Agendado", "Em Andamento"):
                ativos.append(item)
            else:
                historico.append(item)

        self.nome_cliente = tutor["nome"].strip()
        self.cpf_cliente = tutor["cpf"].strip()
        self.telefone_cliente = tutor["telefone"].strip()
        self.email_cliente = tutor["email"].strip()
        self.email = self.email_cliente
        self.pets_cliente = pets_validos
        self.opcoes_pets_agendamento_cliente = [
            f"{pet['id']} - {pet['nome']}" for pet in pets_validos
        ]
        self.agendamentos_ativos_cliente = ativos
        self.agendamentos_historico_cliente = historico
        self.formulario_pet_cliente_aberto = False
        self.formulario_agendamento_cliente_aberto = False
        self.mensagem_pet_cliente = ""
        self.mensagem_agendamento_cliente = ""
        self.erro_agendamento_cliente = ""
        return True

    @rx.event
    def alternar_formulario_pet_cliente(self):
        if self.processando_pet_cliente:
            return
        self.formulario_pet_cliente_aberto = not self.formulario_pet_cliente_aberto
        self.mensagem_pet_cliente = ""
        self.sucesso_pet_cliente = False

    @rx.event
    def set_pet_cliente_nome(self, valor: str):
        self.pet_cliente_nome = valor

    @rx.event
    def set_pet_cliente_especie(self, valor: str):
        self.pet_cliente_especie = valor

    @rx.event
    def set_pet_cliente_raca(self, valor: str):
        self.pet_cliente_raca = valor

    @rx.event
    def set_pet_cliente_porte(self, valor: str):
        self.pet_cliente_porte = valor

    @rx.event
    def set_pet_cliente_observacoes(self, valor: str):
        self.pet_cliente_observacoes = valor

    @rx.event
    def cadastrar_pet_cliente(self):
        if self.processando_pet_cliente:
            return
        if not self._auth_token or not self._tutor_id:
            self.mensagem = "Sua sessão expirou. Entre novamente."
            return rx.redirect("/cliente")

        nome = self.pet_cliente_nome.strip()
        especie = self.pet_cliente_especie.strip()
        raca = self.pet_cliente_raca.strip()
        porte = self.pet_cliente_porte
        observacoes = self.pet_cliente_observacoes.strip()
        if not nome:
            self.mensagem_pet_cliente = "O nome do Pet é obrigatório."
        elif not especie:
            self.mensagem_pet_cliente = "A espécie do Pet é obrigatória."
        elif porte not in ("Pequeno", "Médio", "Grande"):
            self.mensagem_pet_cliente = "Selecione um porte válido."
        else:
            self.mensagem_pet_cliente = ""
        if self.mensagem_pet_cliente:
            self.sucesso_pet_cliente = False
            return

        self.processando_pet_cliente = True
        self.mensagem_pet_cliente = "Cadastrando Pet..."
        self.sucesso_pet_cliente = False
        dados = {
            "nome": nome,
            "especie": especie,
            "porte": porte,
            "raca": raca or None,
            "observacoes_saude": observacoes or None,
        }
        try:
            response = httpx.post(
                f"{XANO_API_URL}/cliente/sessao/pets",
                headers={"Authorization": f"Bearer {self._auth_token}"},
                json=dados,
                timeout=15.0,
            )
            response.raise_for_status()
            pet = response.json()
        except httpx.HTTPStatusError as error:
            if error.response.status_code in (401, 403):
                self._auth_token = ""
                self._tutor_id = ""
                self._limpar_dados_dashboard()
                self.mensagem = "Sua sessão expirou. Entre novamente."
                return rx.redirect("/cliente")
            self.mensagem_pet_cliente = self._mensagem_erro_http(
                error,
                "Não foi possível cadastrar o Pet",
            )
        except httpx.RequestError as error:
            self.mensagem_pet_cliente = (
                f"Erro de conexão ao cadastrar o Pet: {error}"
            )
        except ValueError:
            self.mensagem_pet_cliente = (
                "O Xano retornou uma confirmação de Pet inválida."
            )
        else:
            pet_id = normalizar_id(pet.get("id")) if isinstance(pet, dict) else None
            confirmado = (
                isinstance(pet, dict)
                and pet_id is not None
                and normalizar_id(pet.get("tutor_id")) == self._tutor_id
                and pet.get("nome") == nome
                and pet.get("especie") == especie
                and pet.get("porte") == porte
                and (pet.get("raca") or "") == raca
                and (pet.get("observacoes_saude") or "") == observacoes
            )
            if not confirmado or pet_id is None:
                self.mensagem_pet_cliente = (
                    "O Xano não confirmou os dados persistidos do Pet."
                )
            else:
                self.pets_cliente = [
                    *self.pets_cliente,
                    {
                        "id": pet_id,
                        "nome": nome,
                        "especie": especie,
                        "raca": raca or "Não informada",
                        "porte": porte,
                    },
                ]
                self.opcoes_pets_agendamento_cliente = [
                    *self.opcoes_pets_agendamento_cliente,
                    f"{pet_id} - {nome}",
                ]
                self.mensagem_pet_cliente = "Pet cadastrado com sucesso!"
                self.sucesso_pet_cliente = True
                self.formulario_pet_cliente_aberto = False
                self.pet_cliente_nome = ""
                self.pet_cliente_especie = ""
                self.pet_cliente_raca = ""
                self.pet_cliente_porte = ""
                self.pet_cliente_observacoes = ""
                if self.formulario_agendamento_cliente_aberto:
                    self._atualizar_opcoes_pets_agendamento_cliente()
        finally:
            self.processando_pet_cliente = False

    def _atualizar_opcoes_pets_agendamento_cliente(self):
        self.opcoes_pets_agendamento_cliente = [
            f"{pet['id']} - {pet['nome']}" for pet in self.pets_cliente
        ]
        if self.pet_agendamento_cliente and not any(
            opcao == self.pet_agendamento_cliente
            for opcao in self.opcoes_pets_agendamento_cliente
        ):
            self.pet_agendamento_cliente = ""

    def _limpar_agendamento_cliente(self):
        self.pet_agendamento_cliente = ""
        self.servico_agendamento_cliente = ""
        self.servicos_cliente = []
        self.opcoes_servicos_cliente = []
        self.opcoes_pets_agendamento_cliente = []
        self.dias_calendario_agendamento_cliente = []
        self.dias_disponibilidade_agendamento_cliente = []
        self.horarios_mes_agendamento_cliente = []
        self.horarios_agendamento_cliente = []
        self.data_agendamento_cliente = ""
        self.horario_agendamento_cliente = ""
        self.erro_agendamento_cliente = ""
        self.mensagem_agendamento_cliente = ""
        self.sucesso_agendamento_cliente = False

    @rx.event
    def alternar_agendamento_cliente(self):
        if self.processando_agendamento_cliente:
            return
        if self.formulario_agendamento_cliente_aberto:
            self.formulario_agendamento_cliente_aberto = False
            self._limpar_agendamento_cliente()
            return
        if not self._auth_token or not self._tutor_id:
            self.mensagem = "Sua sessão expirou. Entre novamente."
            return rx.redirect("/cliente")
        if not self.pets_cliente:
            self.erro_agendamento_cliente = (
                "Cadastre um Pet antes de solicitar um Agendamento."
            )
            return

        self.formulario_agendamento_cliente_aberto = True
        self._limpar_agendamento_cliente()
        self.pet_agendamento_cliente = (
            f"{self.pets_cliente[0]['id']} - {self.pets_cliente[0]['nome']}"
        )
        self._atualizar_opcoes_pets_agendamento_cliente()
        agora = datetime.now(FUSO_AGENDAMENTO)
        self.ano_agendamento_cliente = agora.year
        self.mes_agendamento_cliente = agora.month
        self._carregar_servicos_cliente()

    def _carregar_servicos_cliente(self):
        self.carregando_servicos_cliente = True
        self.erro_agendamento_cliente = ""
        try:
            response = httpx.get(f"{XANO_API_URL}/servico", timeout=15.0)
            response.raise_for_status()
            servicos = response.json()
        except httpx.HTTPStatusError as error:
            self.erro_agendamento_cliente = (
                "Não foi possível carregar os Serviços: "
                f"HTTP {error.response.status_code}."
            )
        except httpx.RequestError as error:
            self.erro_agendamento_cliente = (
                f"Erro de conexão ao carregar Serviços: {error}"
            )
        except ValueError:
            self.erro_agendamento_cliente = (
                "O Xano retornou uma lista de Serviços inválida."
            )
        else:
            if not isinstance(servicos, list):
                self.erro_agendamento_cliente = (
                    "O Xano retornou uma lista de Serviços inválida."
                )
            else:
                servicos_validos: list[dict[str, str]] = []
                opcoes: list[str] = []
                for servico in servicos:
                    if not isinstance(servico, dict):
                        continue
                    servico_id = normalizar_id(servico.get("id"))
                    nome = servico.get("nome")
                    duracao = servico.get("duracao_minutos")
                    if (
                        servico_id is None
                        or not isinstance(nome, str)
                        or not nome.strip()
                        or isinstance(duracao, bool)
                        or not isinstance(duracao, int)
                        or duracao <= 0
                    ):
                        continue
                    nome = nome.strip()
                    servicos_validos.append(
                        {
                            "id": servico_id,
                            "nome": nome,
                            "duracao_minutos": str(duracao),
                        }
                    )
                    opcoes.append(f"{servico_id} - {nome} ({duracao} min)")
                self.servicos_cliente = servicos_validos
                self.opcoes_servicos_cliente = opcoes
                if not servicos_validos:
                    self.erro_agendamento_cliente = (
                        "Não há Serviços válidos disponíveis para agendamento."
                    )
        finally:
            self.carregando_servicos_cliente = False

    @rx.event
    def selecionar_pet_agendamento_cliente(self, opcao: str):
        pet_id = opcao.split(" - ", 1)[0]
        pet = next(
            (item for item in self.pets_cliente if item["id"] == pet_id),
            None,
        )
        if pet is None:
            self.erro_agendamento_cliente = "Selecione um Pet da sua conta."
            return
        if opcao not in self.opcoes_pets_agendamento_cliente:
            self.erro_agendamento_cliente = "Selecione um Pet da sua conta."
            return
        self.pet_agendamento_cliente = opcao
        self.erro_agendamento_cliente = ""

    @rx.event
    def selecionar_servico_agendamento_cliente(self, opcao: str):
        servico_id = opcao.split(" - ", 1)[0]
        if not any(item["id"] == servico_id for item in self.servicos_cliente):
            self.erro_agendamento_cliente = "Selecione um Serviço válido."
            return
        self.servico_agendamento_cliente = opcao
        self.data_agendamento_cliente = ""
        self.horario_agendamento_cliente = ""
        self.horarios_agendamento_cliente = []
        self.mensagem_agendamento_cliente = ""
        self.sucesso_agendamento_cliente = False
        self._carregar_disponibilidade_cliente()

    def _atualizar_calendario_agendamento_cliente(self):
        if self.ano_agendamento_cliente < 1 or self.mes_agendamento_cliente < 1:
            self.dias_calendario_agendamento_cliente = []
            return

        hoje = datetime.now(FUSO_AGENDAMENTO).date()
        primeiro_dia_semana, dias_no_mes = calendar.monthrange(
            self.ano_agendamento_cliente,
            self.mes_agendamento_cliente,
        )
        dias = [
            {
                "data": "",
                "numero": "",
                "habilitado": "false",
                "espaco": "true",
            }
            for _ in range(primeiro_dia_semana)
        ]
        disponibilidade = {
            dia["data"]: dia
            for dia in self.dias_disponibilidade_agendamento_cliente
        }
        for numero in range(1, dias_no_mes + 1):
            data = (
                f"{self.ano_agendamento_cliente:04d}-"
                f"{self.mes_agendamento_cliente:02d}-{numero:02d}"
            )
            dia = disponibilidade.get(data)
            habilitado = (
                dia is not None
                and dia["tem_horario_disponivel"] == "true"
                and datetime.strptime(data, "%Y-%m-%d").date() >= hoje
            )
            dias.append(
                {
                    "data": data,
                    "numero": str(numero),
                    "habilitado": str(habilitado).lower(),
                    "espaco": "false",
                }
            )

        self.dias_calendario_agendamento_cliente = dias
        self.titulo_mes_agendamento_cliente = (
            f"{NOMES_MESES[self.mes_agendamento_cliente]} "
            f"{self.ano_agendamento_cliente}"
        )

    def _carregar_disponibilidade_cliente(self):
        if not self.servico_agendamento_cliente:
            self.dias_disponibilidade_agendamento_cliente = []
            self.horarios_mes_agendamento_cliente = []
            self._atualizar_calendario_agendamento_cliente()
            return

        servico_id = self.servico_agendamento_cliente.split(" - ", 1)[0]
        self.carregando_disponibilidade_cliente = True
        self.erro_agendamento_cliente = ""
        self.dias_disponibilidade_agendamento_cliente = []
        self.horarios_mes_agendamento_cliente = []
        try:
            response = httpx.get(
                f"{XANO_API_URL}/agendamento_disponibilidade",
                params={
                    "servico_id": int(servico_id),
                    "ano": self.ano_agendamento_cliente,
                    "mes": self.mes_agendamento_cliente,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            dados = response.json()
        except httpx.HTTPStatusError as error:
            self.erro_agendamento_cliente = (
                "Erro ao consultar disponibilidade: "
                f"HTTP {error.response.status_code}."
            )
        except httpx.RequestError as error:
            self.erro_agendamento_cliente = (
                f"Erro de conexão ao consultar disponibilidade: {error}"
            )
        except ValueError:
            self.erro_agendamento_cliente = (
                "O Xano retornou uma disponibilidade inválida."
            )
        else:
            if not isinstance(dados, list):
                self.erro_agendamento_cliente = (
                    "O Xano retornou uma disponibilidade inválida."
                )
            else:
                dias: list[dict[str, str]] = []
                horarios_mes: list[dict[str, str]] = []
                for dia in dados:
                    if (
                        not isinstance(dia, dict)
                        or not isinstance(dia.get("data"), str)
                        or not isinstance(dia.get("horarios"), list)
                        or not isinstance(
                            dia.get("tem_horario_disponivel"), bool
                        )
                    ):
                        self.erro_agendamento_cliente = (
                            "O Xano retornou um dia de disponibilidade inválido."
                        )
                        break
                    horarios: list[dict[str, str]] = []
                    for horario in dia["horarios"]:
                        if (
                            not isinstance(horario, dict)
                            or not isinstance(horario.get("hora"), str)
                            or not isinstance(horario.get("disponivel"), bool)
                        ):
                            self.erro_agendamento_cliente = (
                                "O Xano retornou um horário de disponibilidade inválido."
                            )
                            break
                        data_hora = timestamp_em_milissegundos(
                            horario.get("data_hora")
                        )
                        if data_hora is None:
                            self.erro_agendamento_cliente = (
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
                    if self.erro_agendamento_cliente:
                        break
                    dias.append(
                        {
                            "data": dia["data"],
                            "tem_horario_disponivel": str(
                                dia["tem_horario_disponivel"]
                            ).lower(),
                        }
                    )
                    horarios_mes.extend(horarios)
                if not self.erro_agendamento_cliente:
                    self.dias_disponibilidade_agendamento_cliente = dias
                    self.horarios_mes_agendamento_cliente = horarios_mes

        self.carregando_disponibilidade_cliente = False
        self._atualizar_calendario_agendamento_cliente()

    @rx.event
    def mudar_mes_agendamento_cliente(self, incremento: int):
        ano = self.ano_agendamento_cliente
        mes = self.mes_agendamento_cliente + incremento
        if mes < 1:
            ano -= 1
            mes = 12
        elif mes > 12:
            ano += 1
            mes = 1
        agora = datetime.now(FUSO_AGENDAMENTO)
        if (ano, mes) < (agora.year, agora.month):
            return
        self.ano_agendamento_cliente = ano
        self.mes_agendamento_cliente = mes
        self.data_agendamento_cliente = ""
        self.horario_agendamento_cliente = ""
        self.horarios_agendamento_cliente = []
        self.mensagem_agendamento_cliente = ""
        self._carregar_disponibilidade_cliente()

    @rx.event
    def selecionar_dia_agendamento_cliente(self, data: str):
        dia = next(
            (
                item
                for item in self.dias_disponibilidade_agendamento_cliente
                if item["data"] == data
                and item["tem_horario_disponivel"] == "true"
            ),
            None,
        )
        if dia is None:
            self.erro_agendamento_cliente = (
                "Este dia não possui horários disponíveis."
            )
            return
        self.data_agendamento_cliente = data
        self.horarios_agendamento_cliente = [
            horario
            for horario in self.horarios_mes_agendamento_cliente
            if horario["data"] == data
        ]
        self.horario_agendamento_cliente = ""
        self.erro_agendamento_cliente = ""
        self.mensagem_agendamento_cliente = ""

    @rx.event
    def selecionar_horario_agendamento_cliente(self, data_hora: str):
        horario = next(
            (
                item
                for item in self.horarios_agendamento_cliente
                if item["data_hora"] == data_hora
                and item["disponivel"] == "true"
            ),
            None,
        )
        if horario is None:
            self.erro_agendamento_cliente = (
                "Selecione um horário que ainda esteja disponível."
            )
            return
        self.horario_agendamento_cliente = horario["data_hora"]
        self.erro_agendamento_cliente = ""
        self.mensagem_agendamento_cliente = ""

    @rx.event
    def confirmar_agendamento_cliente(self):
        if self.processando_agendamento_cliente:
            return
        if not self._auth_token or not self._tutor_id:
            self.mensagem = "Sua sessão expirou. Entre novamente."
            return rx.redirect("/cliente")
        pet_id = self.pet_agendamento_cliente.split(" - ", 1)[0]
        servico_id = self.servico_agendamento_cliente.split(" - ", 1)[0]
        pet = next(
            (
                item
                for item in self.pets_cliente
                if item["id"] == pet_id
            ),
            None,
        )
        servico = next(
            (
                item
                for item in self.servicos_cliente
                if item["id"] == servico_id
            ),
            None,
        )
        horario = next(
            (
                item
                for item in self.horarios_agendamento_cliente
                if item["data_hora"] == self.horario_agendamento_cliente
                and item["disponivel"] == "true"
            ),
            None,
        )
        if pet is None:
            self.erro_agendamento_cliente = "Selecione um Pet da sua conta."
            return
        if servico is None:
            self.erro_agendamento_cliente = "Selecione um Serviço válido."
            return
        if not self.data_agendamento_cliente or horario is None:
            self.erro_agendamento_cliente = (
                "Selecione um dia e horário disponíveis."
            )
            return

        pet_id_int = int(pet_id)
        servico_id_int = int(servico_id)
        data_hora_int = int(horario["data_hora"])
        self.processando_agendamento_cliente = True
        self.erro_agendamento_cliente = ""
        self.mensagem_agendamento_cliente = "Confirmando Agendamento..."
        self.sucesso_agendamento_cliente = False
        try:
            response = httpx.post(
                f"{XANO_API_URL}/cliente/sessao/agendamentos",
                headers={"Authorization": f"Bearer {self._auth_token}"},
                json={
                    "pet_id": pet_id_int,
                    "servico_id": servico_id_int,
                    "data_hora": data_hora_int,
                },
                timeout=20.0,
            )
            response.raise_for_status()
            agendamento = response.json()
        except httpx.HTTPStatusError as error:
            self.mensagem_agendamento_cliente = ""
            if error.response.status_code in (401, 403):
                self._auth_token = ""
                self._tutor_id = ""
                self._limpar_dados_dashboard()
                self.mensagem = "Sua sessão expirou. Entre novamente."
                return rx.redirect("/cliente")
            erro_confirmacao = self._mensagem_erro_http(
                error,
                "Não foi possível confirmar o Agendamento",
            )
            if error.response.status_code == 429:
                tempo_espera = error.response.headers.get("Retry-After")
                if tempo_espera and tempo_espera.isdigit():
                    erro_confirmacao = (
                        "O Xano limitou temporariamente as chamadas. "
                        f"Aguarde {tempo_espera} segundos antes de tentar novamente."
                    )
                else:
                    erro_confirmacao = (
                        "O Xano limitou temporariamente as chamadas. "
                        "Aguarde um pouco antes de tentar novamente."
                    )
            if error.response.status_code < 500 and error.response.status_code != 429:
                self._carregar_disponibilidade_cliente()
                if self.erro_agendamento_cliente:
                    erro_confirmacao = (
                        f"{erro_confirmacao} {self.erro_agendamento_cliente}"
                    )
            self.erro_agendamento_cliente = erro_confirmacao
        except httpx.RequestError as error:
            self.mensagem_agendamento_cliente = ""
            self.erro_agendamento_cliente = (
                f"Erro de conexão ao confirmar Agendamento: {error}"
            )
        except ValueError:
            self.mensagem_agendamento_cliente = ""
            self.erro_agendamento_cliente = (
                "O Xano retornou uma confirmação de Agendamento inválida."
            )
        else:
            data_hora_confirmada = (
                timestamp_em_milissegundos(agendamento.get("data_hora"))
                if isinstance(agendamento, dict)
                else None
            )
            if (
                not isinstance(agendamento, dict)
                or normalizar_id(agendamento.get("id")) is None
                or normalizar_id(agendamento.get("pet_id")) != pet_id
                or normalizar_id(agendamento.get("servico_id")) != servico_id
                or data_hora_confirmada != data_hora_int
                or agendamento.get("status") != "Agendado"
            ):
                self.mensagem_agendamento_cliente = ""
                self.erro_agendamento_cliente = (
                    "O Xano não confirmou os dados persistidos do Agendamento."
                )
            else:
                self.agendamentos_ativos_cliente = [
                    {
                        "pet_nome": pet["nome"],
                        "servico_nome": servico["nome"],
                        "data_hora": formatar_data_hora_agendamento(
                            data_hora_int
                        )
                        or "",
                        "status": "Agendado",
                    },
                    *self.agendamentos_ativos_cliente,
                ]
                self.mensagem_agendamento_cliente = "Agendado com sucesso!"
                self.sucesso_agendamento_cliente = True
                self.horario_agendamento_cliente = ""
                self.data_agendamento_cliente = ""
                self.horarios_agendamento_cliente = []
                self._carregar_disponibilidade_cliente()
        finally:
            self.processando_agendamento_cliente = False

    def set_nome(self, nome: str):
        self.nome = nome

    def set_cpf(self, cpf: str):
        self.cpf = cpf

    def set_telefone(self, telefone: str):
        self.telefone = telefone

    def set_email(self, email: str):
        self.email = email

    def set_senha(self, senha: str):
        self.senha = senha

    def set_confirmar_senha(self, senha: str):
        self.confirmar_senha = senha

    def _mensagem_erro_http(
        self,
        error: httpx.HTTPStatusError,
        contexto: str,
    ) -> str:
        try:
            dados_erro = error.response.json()
        except ValueError:
            dados_erro = None

        mensagem = (
            dados_erro.get("message")
            if isinstance(dados_erro, dict)
            else None
        )
        if (
            error.response.status_code == 404
            and mensagem == "Unable to locate request."
        ):
            return (
                f"{contexto}: o endpoint de conta do cliente ainda não foi "
                "publicado no Xano. Publique os scripts da change e tente novamente."
            )
        if not isinstance(mensagem, str) or not mensagem.strip():
            mensagem = error.response.text.strip()
        if not mensagem:
            mensagem = f"HTTP {error.response.status_code}"
        return f"{contexto}: {mensagem}"

    def _processar_resposta_autenticacao(self, dados: object) -> bool:
        if not isinstance(dados, dict):
            return False

        token = dados.get("authToken")
        tutor = dados.get("tutor")
        if (
            not isinstance(token, str)
            or not token
            or not isinstance(tutor, dict)
            or normalizar_id(tutor.get("id")) is None
            or not isinstance(tutor.get("nome"), str)
            or not tutor["nome"].strip()
        ):
            return False

        self._auth_token = token
        self._tutor_id = normalizar_id(tutor.get("id")) or ""
        self.nome_cliente = tutor["nome"]
        return True

    def entrar(self):
        email = self.email.strip().lower()
        if not email or not self.senha:
            self.mensagem = "Informe seu e-mail e sua senha."
            return

        self.processando = True
        self.mensagem = "Validando acesso..."
        self._auth_token = ""
        self._tutor_id = ""
        self._limpar_dados_dashboard()

        try:
            response = httpx.post(
                f"{XANO_API_URL}/cliente/login",
                json={"email": email, "senha": self.senha},
                timeout=10.0,
            )
            response.raise_for_status()
            dados = response.json()
        except httpx.HTTPStatusError as error:
            self.senha = ""
            self.mensagem = self._mensagem_erro_http(
                error,
                "Não foi possível entrar",
            )
        except httpx.RequestError as error:
            self.senha = ""
            self.mensagem = f"Erro de conexão com o Xano: {error}"
        except ValueError:
            self.senha = ""
            self.mensagem = "O Xano retornou uma resposta de login inválida."
        else:
            self.senha = ""
            if not self._processar_resposta_autenticacao(dados):
                self.mensagem = "O Xano não confirmou a autenticação."
            else:
                self.email = email
                self.mensagem = ""
                return rx.redirect("/cliente/inicio")
        finally:
            self.processando = False

    def cadastrar(self):
        nome = self.nome.strip()
        cpf = self.cpf.strip()
        telefone = self.telefone.strip()
        email = self.email.strip().lower()
        if not nome or not cpf or not telefone or not email or not self.senha:
            self.mensagem = "Preencha todos os campos."
            return
        if len(self.senha) < 8:
            self.mensagem = "A senha deve ter pelo menos 8 caracteres."
            return
        if self.senha != self.confirmar_senha:
            self.mensagem = "A confirmação de senha não corresponde."
            return

        self.processando = True
        self.mensagem = "Criando sua conta..."
        self._auth_token = ""
        self._tutor_id = ""
        self._limpar_dados_dashboard()

        try:
            response = httpx.post(
                f"{XANO_API_URL}/cliente/cadastro",
                json={
                    "nome": nome,
                    "cpf": cpf,
                    "telefone": telefone,
                    "email": email,
                    "senha": self.senha,
                },
                timeout=10.0,
            )
            response.raise_for_status()
            dados = response.json()
        except httpx.HTTPStatusError as error:
            self.senha = ""
            self.confirmar_senha = ""
            self.mensagem = self._mensagem_erro_http(
                error,
                "Não foi possível criar a conta",
            )
        except httpx.RequestError as error:
            self.senha = ""
            self.confirmar_senha = ""
            self.mensagem = f"Erro de conexão com o Xano: {error}"
        except ValueError:
            self.senha = ""
            self.confirmar_senha = ""
            self.mensagem = "O Xano retornou uma resposta de cadastro inválida."
        else:
            self.senha = ""
            self.confirmar_senha = ""
            if not self._processar_resposta_autenticacao(dados):
                self.mensagem = "O Xano não confirmou a criação da conta."
            else:
                self.nome = nome
                self.cpf = ""
                self.telefone = telefone
                self.email = email
                self.mensagem = ""
                return rx.redirect("/cliente/inicio")
        finally:
            self.processando = False

    def carregar_conta(self):
        if not self._auth_token or not self._tutor_id:
            self._limpar_dados_dashboard()
            self.mensagem = "Entre na sua conta para acessar o dashboard."
            return rx.redirect("/cliente")

        self.carregando_dashboard = True
        self.mensagem = ""
        try:
            response = httpx.get(
                f"{XANO_API_URL}/cliente/sessao/dashboard",
                headers={"Authorization": f"Bearer {self._auth_token}"},
                timeout=10.0,
            )
            response.raise_for_status()
            dados = response.json()
        except httpx.HTTPStatusError as error:
            if error.response.status_code in (401, 403):
                self.mensagem = "Sua sessão expirou. Entre novamente."
                self._auth_token = ""
                self._tutor_id = ""
                self._limpar_dados_dashboard()
                return rx.redirect("/cliente")
            else:
                self.mensagem = self._mensagem_erro_http(
                    error,
                    "Não foi possível carregar seu dashboard",
                )
                self._limpar_dados_dashboard()
        except httpx.RequestError as error:
            self.mensagem = f"Erro de conexão ao carregar seu dashboard: {error}"
            self._limpar_dados_dashboard()
        except ValueError:
            self.mensagem = "O Xano retornou os dados do dashboard em formato inválido."
            self._limpar_dados_dashboard()
        else:
            if not self._processar_resposta_dashboard(dados):
                self.mensagem = (
                    "O Xano retornou dados incompletos ou inválidos para o dashboard."
                )
                self._limpar_dados_dashboard()
        finally:
            self.carregando_dashboard = False

    def sair(self):
        self._auth_token = ""
        self._tutor_id = ""
        self._limpar_dados_dashboard()
        self.senha = ""
        self.confirmar_senha = ""
        self.mensagem = ""
        return rx.redirect("/cliente")


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
                rx.link("Acesso do cliente", href="/cliente"),
                width="400px",
                padding="20px",
                class_name="pettech-card",
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


def cliente_login() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Área do cliente", size="8"),
            rx.text("Entre com sua conta PetTech.", size="3"),
            rx.link("Voltar à página inicial", href="/"),
            rx.vstack(
                rx.text("E-mail:"),
                rx.input(
                    placeholder="email@exemplo.com",
                    type="email",
                    on_change=ClienteAuthState.set_email,
                    value=ClienteAuthState.email,
                    width="100%",
                ),
                rx.text("Senha:"),
                rx.input(
                    placeholder="Sua senha",
                    type="password",
                    on_change=ClienteAuthState.set_senha,
                    value=ClienteAuthState.senha,
                    width="100%",
                ),
                rx.button(
                    "Entrar",
                    on_click=ClienteAuthState.entrar,
                    loading=ClienteAuthState.processando,
                    width="100%",
                    margin_top="10px",
                ),
                rx.cond(
                    ClienteAuthState.mensagem,
                    rx.text(
                        ClienteAuthState.mensagem,
                        color="red",
                        size="2",
                    ),
                ),
                rx.link("Ainda não tenho conta. Cadastrar", href="/cliente/cadastro"),
                width="100%",
                max_width="420px",
                padding="20px",
                class_name="pettech-card",
                spacing="3",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
        ),
    )


def cadastro_cliente() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Criar conta de cliente", size="8"),
            rx.text("Preencha seus dados para acessar a área do cliente.", size="3"),
            rx.link("Já tenho conta", href="/cliente"),
            rx.vstack(
                rx.text("Nome completo:"),
                rx.input(
                    placeholder="Digite seu nome completo",
                    on_change=ClienteAuthState.set_nome,
                    value=ClienteAuthState.nome,
                    width="100%",
                ),
                rx.text("CPF:"),
                rx.input(
                    placeholder="000.000.000-00",
                    on_change=ClienteAuthState.set_cpf,
                    value=ClienteAuthState.cpf,
                    width="100%",
                ),
                rx.text("Telefone:"),
                rx.input(
                    placeholder="(00) 00000-0000",
                    type="tel",
                    on_change=ClienteAuthState.set_telefone,
                    value=ClienteAuthState.telefone,
                    width="100%",
                ),
                rx.text("E-mail:"),
                rx.input(
                    placeholder="email@exemplo.com",
                    type="email",
                    on_change=ClienteAuthState.set_email,
                    value=ClienteAuthState.email,
                    width="100%",
                ),
                rx.text("Senha (mínimo de 8 caracteres):"),
                rx.input(
                    placeholder="Crie uma senha",
                    type="password",
                    on_change=ClienteAuthState.set_senha,
                    value=ClienteAuthState.senha,
                    width="100%",
                ),
                rx.text("Confirme sua senha:"),
                rx.input(
                    placeholder="Digite a senha novamente",
                    type="password",
                    on_change=ClienteAuthState.set_confirmar_senha,
                    value=ClienteAuthState.confirmar_senha,
                    width="100%",
                ),
                rx.button(
                    "Criar conta",
                    on_click=ClienteAuthState.cadastrar,
                    loading=ClienteAuthState.processando,
                    width="100%",
                    margin_top="10px",
                ),
                rx.cond(
                    ClienteAuthState.mensagem,
                    rx.text(
                        ClienteAuthState.mensagem,
                        color="red",
                        size="2",
                    ),
                ),
                width="100%",
                max_width="420px",
                padding="20px",
                class_name="pettech-card",
                spacing="3",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
        ),
    )


def calendario_agendamento_cliente() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.button(
                "‹",
                on_click=ClienteAuthState.mudar_mes_agendamento_cliente(-1),
            ),
            rx.heading(
                ClienteAuthState.titulo_mes_agendamento_cliente,
                size="4",
            ),
            rx.button(
                "›",
                on_click=ClienteAuthState.mudar_mes_agendamento_cliente(1),
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
                ClienteAuthState.dias_calendario_agendamento_cliente,
                lambda dia: rx.cond(
                    dia["espaco"] == "true",
                    rx.box(height="40px"),
                    rx.button(
                        dia["numero"],
                        on_click=ClienteAuthState.selecionar_dia_agendamento_cliente(
                            dia["data"]
                        ),
                        disabled=dia["habilitado"] != "true",
                        color_scheme=rx.cond(
                            dia["habilitado"] == "true",
                            "blue",
                            "gray",
                        ),
                        variant=rx.cond(
                            dia["data"] == ClienteAuthState.data_agendamento_cliente,
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


def formulario_pet_cliente() -> rx.Component:
    return rx.vstack(
        rx.text("Nome:"),
        rx.input(
            placeholder="Nome do Pet",
            value=ClienteAuthState.pet_cliente_nome,
            on_change=ClienteAuthState.set_pet_cliente_nome,
            width="100%",
        ),
        rx.text("Espécie:"),
        rx.input(
            placeholder="Ex.: Cão ou Gato",
            value=ClienteAuthState.pet_cliente_especie,
            on_change=ClienteAuthState.set_pet_cliente_especie,
            width="100%",
        ),
        rx.text("Raça (opcional):"),
        rx.input(
            placeholder="Raça do Pet",
            value=ClienteAuthState.pet_cliente_raca,
            on_change=ClienteAuthState.set_pet_cliente_raca,
            width="100%",
        ),
        rx.text("Porte:"),
        rx.select(
            ["Pequeno", "Médio", "Grande"],
            value=ClienteAuthState.pet_cliente_porte,
            on_change=ClienteAuthState.set_pet_cliente_porte,
            placeholder="Selecione o porte",
            width="100%",
        ),
        rx.text("Observações de saúde e comportamento (opcional):"),
        rx.text_area(
            placeholder="Alergias, cuidados especiais ou observações",
            value=ClienteAuthState.pet_cliente_observacoes,
            on_change=ClienteAuthState.set_pet_cliente_observacoes,
            width="100%",
        ),
        rx.button(
            "Salvar Pet",
            on_click=ClienteAuthState.cadastrar_pet_cliente,
            loading=ClienteAuthState.processando_pet_cliente,
            width="100%",
        ),
        rx.cond(
            ClienteAuthState.mensagem_pet_cliente,
            rx.text(
                ClienteAuthState.mensagem_pet_cliente,
                color=rx.cond(
                    ClienteAuthState.sucesso_pet_cliente,
                    "green",
                    "red",
                ),
                size="2",
            ),
        ),
        width="100%",
        spacing="3",
    )


def formulario_agendamento_cliente() -> rx.Component:
    return rx.vstack(
        rx.heading("Novo Agendamento", size="5"),
        rx.text("Pet:"),
        rx.select(
            ClienteAuthState.opcoes_pets_agendamento_cliente,
            value=ClienteAuthState.pet_agendamento_cliente,
            on_change=ClienteAuthState.selecionar_pet_agendamento_cliente,
            placeholder="Selecione um Pet",
            width="100%",
        ),
        rx.text("Serviço:"),
        rx.cond(
            ClienteAuthState.carregando_servicos_cliente,
            rx.text("Carregando Serviços..."),
            rx.select(
                ClienteAuthState.opcoes_servicos_cliente,
                value=ClienteAuthState.servico_agendamento_cliente,
                on_change=ClienteAuthState.selecionar_servico_agendamento_cliente,
                placeholder="Selecione um Serviço",
                width="100%",
            ),
        ),
        rx.cond(
            ClienteAuthState.servico_agendamento_cliente != "",
            rx.cond(
                ClienteAuthState.carregando_disponibilidade_cliente,
                rx.text("Consultando disponibilidade..."),
                rx.vstack(
                    rx.heading("Selecione o dia", size="5"),
                    calendario_agendamento_cliente(),
                    rx.cond(
                        ClienteAuthState.data_agendamento_cliente != "",
                        rx.vstack(
                            rx.heading("Horários disponíveis", size="5"),
                            rx.grid(
                                rx.foreach(
                                    ClienteAuthState.horarios_agendamento_cliente,
                                    lambda horario: rx.button(
                                        horario["hora"],
                                        on_click=ClienteAuthState.selecionar_horario_agendamento_cliente(
                                            horario["data_hora"]
                                        ),
                                        disabled=horario["disponivel"] != "true",
                                        color_scheme=rx.cond(
                                            horario["disponivel"] == "true",
                                            "blue",
                                            "gray",
                                        ),
                                        variant=rx.cond(
                                            horario["data_hora"]
                                            == ClienteAuthState.horario_agendamento_cliente,
                                            "solid",
                                            "outline",
                                        ),
                                    ),
                                ),
                                columns="repeat(4, 1fr)",
                                width="100%",
                            ),
                            rx.button(
                                "Confirmar Agendamento",
                                on_click=ClienteAuthState.confirmar_agendamento_cliente,
                                loading=ClienteAuthState.processando_agendamento_cliente,
                                disabled=(
                                    (ClienteAuthState.horario_agendamento_cliente == "")
                                    | ClienteAuthState.processando_agendamento_cliente
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
            ClienteAuthState.erro_agendamento_cliente,
            rx.text(
                ClienteAuthState.erro_agendamento_cliente,
                color="red",
                size="2",
            ),
        ),
        rx.cond(
            ClienteAuthState.mensagem_agendamento_cliente,
            rx.text(
                ClienteAuthState.mensagem_agendamento_cliente,
                color=rx.cond(
                    ClienteAuthState.sucesso_agendamento_cliente,
                    "green",
                    "blue",
                ),
                size="2",
            ),
        ),
        width="100%",
        spacing="3",
    )


def inicio_cliente() -> rx.Component:
    dados_cadastrais = rx.vstack(
        rx.heading("Seus dados cadastrais", size="5"),
        rx.grid(
            rx.vstack(
                rx.text("Nome", color="#718078", size="2"),
                rx.text(ClienteAuthState.nome_cliente, weight="bold"),
                align="start",
            ),
            rx.vstack(
                rx.text("CPF", color="#718078", size="2"),
                rx.text(ClienteAuthState.cpf_cliente, weight="bold"),
                align="start",
            ),
            rx.vstack(
                rx.text("Telefone", color="#718078", size="2"),
                rx.text(ClienteAuthState.telefone_cliente, weight="bold"),
                align="start",
            ),
            rx.vstack(
                rx.text("E-mail", color="#718078", size="2"),
                rx.text(ClienteAuthState.email_cliente, weight="bold"),
                align="start",
            ),
            columns="repeat(auto-fit, minmax(180px, 1fr))",
            spacing="4",
            width="100%",
        ),
        width="100%",
        align="start",
        class_name="pettech-card",
        padding="24px",
    )
    pets = rx.vstack(
        rx.heading("Seus Pets", size="5"),
        rx.cond(
            ClienteAuthState.carregando_dashboard,
            rx.text("Carregando seus Pets..."),
            rx.vstack(
                rx.cond(
                    ClienteAuthState.pets_cliente,
                    rx.grid(
                        rx.foreach(
                            ClienteAuthState.pets_cliente,
                            lambda pet: rx.vstack(
                                rx.heading(pet["nome"], size="4"),
                                rx.text(f"Espécie: {pet['especie']}"),
                                rx.text(f"Raça: {pet['raca']}"),
                                rx.text(f"Porte: {pet['porte']}"),
                                align="start",
                                width="100%",
                                class_name="pettech-card",
                                padding="16px",
                            ),
                        ),
                        columns="repeat(auto-fit, minmax(220px, 1fr))",
                        spacing="4",
                        width="100%",
                    ),
                    rx.text("Você ainda não possui Pets cadastrados."),
                ),
                rx.button(
                    rx.cond(
                        ClienteAuthState.formulario_pet_cliente_aberto,
                        "Fechar cadastro de Pet",
                        rx.cond(
                            ClienteAuthState.pets_cliente,
                            "Cadastrar outro Pet",
                            "Cadastrar primeiro Pet",
                        ),
                    ),
                    on_click=ClienteAuthState.alternar_formulario_pet_cliente,
                    disabled=ClienteAuthState.processando_pet_cliente,
                ),
                rx.cond(
                    ClienteAuthState.formulario_pet_cliente_aberto,
                    formulario_pet_cliente(),
                ),
                rx.cond(
                    ClienteAuthState.mensagem_pet_cliente
                    & ~ClienteAuthState.formulario_pet_cliente_aberto,
                    rx.text(
                        ClienteAuthState.mensagem_pet_cliente,
                        color=rx.cond(
                            ClienteAuthState.sucesso_pet_cliente,
                            "green",
                            "red",
                        ),
                        size="2",
                    ),
                ),
                width="100%",
                spacing="3",
            ),
        ),
        width="100%",
        align="start",
        class_name="pettech-card",
        padding="24px",
    )
    agendamentos_ativos = rx.vstack(
        rx.heading("Agendamentos ativos", size="5"),
        rx.cond(
            ClienteAuthState.carregando_dashboard,
            rx.text("Carregando Agendamentos..."),
            rx.vstack(
                rx.cond(
                    ClienteAuthState.agendamentos_ativos_cliente,
                    rx.grid(
                        rx.foreach(
                            ClienteAuthState.agendamentos_ativos_cliente,
                            lambda agendamento: rx.vstack(
                                rx.heading(agendamento["servico_nome"], size="4"),
                                rx.text(f"Pet: {agendamento['pet_nome']}"),
                                rx.text(f"Data e hora: {agendamento['data_hora']}"),
                                rx.text(f"Status: {agendamento['status']}"),
                                align="start",
                                width="100%",
                                class_name="pettech-card",
                                padding="16px",
                            ),
                        ),
                        columns="repeat(auto-fit, minmax(220px, 1fr))",
                        spacing="4",
                        width="100%",
                    ),
                    rx.text("Você não possui Agendamentos ativos."),
                ),
                rx.button(
                    rx.cond(
                        ClienteAuthState.formulario_agendamento_cliente_aberto,
                        "Fechar Agendamento",
                        rx.cond(
                            ClienteAuthState.agendamentos_ativos_cliente,
                            "Agendar outro atendimento",
                            "Agendar atendimento",
                        ),
                    ),
                    on_click=ClienteAuthState.alternar_agendamento_cliente,
                    disabled=ClienteAuthState.processando_agendamento_cliente,
                ),
                rx.cond(
                    ClienteAuthState.formulario_agendamento_cliente_aberto,
                    formulario_agendamento_cliente(),
                ),
                rx.cond(
                    ClienteAuthState.erro_agendamento_cliente
                    & ~ClienteAuthState.formulario_agendamento_cliente_aberto,
                    rx.text(
                        ClienteAuthState.erro_agendamento_cliente,
                        color="red",
                        size="2",
                    ),
                ),
                rx.cond(
                    ClienteAuthState.mensagem_agendamento_cliente
                    & ~ClienteAuthState.formulario_agendamento_cliente_aberto,
                    rx.text(
                        ClienteAuthState.mensagem_agendamento_cliente,
                        color=rx.cond(
                            ClienteAuthState.sucesso_agendamento_cliente,
                            "green",
                            "blue",
                        ),
                        size="2",
                    ),
                ),
                width="100%",
                spacing="3",
            ),
        ),
        width="100%",
        align="start",
        class_name="pettech-card",
        padding="24px",
    )
    agendamentos_historico = rx.vstack(
        rx.heading("Histórico de Agendamentos", size="5"),
        rx.cond(
            ClienteAuthState.agendamentos_historico_cliente,
            rx.grid(
                rx.foreach(
                    ClienteAuthState.agendamentos_historico_cliente,
                    lambda agendamento: rx.vstack(
                        rx.heading(agendamento["servico_nome"], size="4"),
                        rx.text(f"Pet: {agendamento['pet_nome']}"),
                        rx.text(f"Data e hora: {agendamento['data_hora']}"),
                        rx.text(f"Status: {agendamento['status']}"),
                        align="start",
                        width="100%",
                        class_name="pettech-card",
                        padding="16px",
                    ),
                ),
                columns="repeat(auto-fit, minmax(220px, 1fr))",
                spacing="4",
                width="100%",
            ),
            rx.text("Você ainda não possui Agendamentos no histórico."),
        ),
        width="100%",
        align="start",
        class_name="pettech-card",
        padding="24px",
    )

    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("Meu dashboard", size="8"),
                    rx.text(
                        f"Olá, {ClienteAuthState.nome_cliente}",
                        size="4",
                    ),
                    align="start",
                    spacing="1",
                ),
                rx.spacer(),
                rx.button("Sair", on_click=ClienteAuthState.sair),
                width="100%",
                align="center",
                wrap="wrap",
            ),
            rx.cond(
                ClienteAuthState.carregando_dashboard,
                rx.text("Carregando seus dados..."),
                rx.cond(
                    ClienteAuthState.mensagem,
                    rx.text(
                        ClienteAuthState.mensagem,
                        color="red",
                        size="2",
                    ),
                    rx.vstack(
                        dados_cadastrais,
                        pets,
                        agendamentos_ativos,
                        agendamentos_historico,
                        width="100%",
                        align="stretch",
                        spacing="5",
                    ),
                ),
            ),
            spacing="4",
            width="100%",
            max_width="1100px",
            margin="0 auto",
            padding="32px 16px",
            align="stretch",
        ),
        max_width="1200px",
        width="100%",
    )


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Cadastro de Tutor", size="8"),
            rx.text(
                rx.cond(
                    TutorState.editando,
                    "Altere os dados do tutor selecionado.",
                    "Preencha os dados abaixo para cadastrar um novo cliente.",
                ),
                size="3",
            ),
            rx.link("Página inicial", href="/"),
            rx.link("Cadastrar Pet", href="/pets"),
            rx.link("Cadastrar Serviço", href="/servicos"),
            rx.link("Agendar atendimento", href="/agendamentos"),
            rx.link("Consultar agendamentos", href="/agendamentos/lista"),
            
            rx.vstack(
                rx.cond(
                    TutorState.editando,
                    rx.vstack(
                        rx.heading("Editar Tutor", size="5"),
                        rx.text("Nome:"),
                        rx.input(
                            placeholder="Digite o nome completo",
                            on_change=TutorState.set_nome_edicao,
                            value=TutorState.nome_edicao,
                            width="100%",
                        ),
                        rx.text("E-mail:"),
                        rx.input(
                            placeholder="email@exemplo.com",
                            type="email",
                            on_change=TutorState.set_email_edicao,
                            value=TutorState.email_edicao,
                            width="100%",
                        ),
                        rx.text("Telefone:"),
                        rx.input(
                            placeholder="(00) 00000-0000",
                            on_change=TutorState.set_telefone_edicao,
                            value=TutorState.telefone_edicao,
                            width="100%",
                        ),
                        rx.hstack(
                            rx.button(
                                "Salvar alterações",
                                on_click=TutorState.salvar_edicao,
                                loading=TutorState.processando_edicao,
                            ),
                            rx.button(
                                "Cancelar",
                                on_click=TutorState.cancelar_edicao,
                                disabled=TutorState.processando_edicao,
                                variant="outline",
                            ),
                        ),
                        rx.cond(
                            TutorState.mensagem_edicao,
                            rx.text(
                                TutorState.mensagem_edicao,
                                color=rx.cond(
                                    TutorState.sucesso_edicao,
                                    "green",
                                    "red",
                                ),
                                size="2",
                            ),
                        ),
                        width="100%",
                        spacing="3",
                    ),
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
                            rx.text(
                                TutorState.mensagem, color="blue", size="2"
                            ),
                        ),
                        width="100%",
                        spacing="3",
                    ),
                ),
                width="400px",
                padding="20px",
                class_name="pettech-card",
                border="1px solid #ddd",
                border_radius="10px",
                spacing="3",
            ),
            rx.heading("Tutores cadastrados", size="5"),
            rx.cond(
                TutorState.carregando_tutores,
                rx.text("Carregando tutores..."),
                rx.cond(
                    TutorState.tem_tutores,
                    rx.vstack(
                        rx.foreach(
                            TutorState.tutores,
                            lambda tutor: rx.hstack(
                                rx.vstack(
                                    rx.text(tutor["nome"], weight="bold"),
                                    rx.text(
                                        rx.cond(
                                            tutor["email"] != "",
                                            tutor["email"],
                                            "E-mail não informado",
                                        ),
                                        size="2",
                                    ),
                                    rx.text(
                                        rx.cond(
                                            tutor["telefone"] != "",
                                            tutor["telefone"],
                                            "Telefone não informado",
                                        ),
                                        size="2",
                                    ),
                                    align="start",
                                ),
                                rx.button(
                                    "Editar",
                                    on_click=TutorState.iniciar_edicao(
                                        tutor["id"]
                                    ),
                                    disabled=(
                                        TutorState.processando_edicao
                                        | TutorState.processando_exclusao
                                    ),
                                ),
                                rx.button(
                                    "Excluir",
                                    on_click=TutorState.iniciar_exclusao(
                                        tutor["id"]
                                    ),
                                    disabled=(
                                        TutorState.processando_edicao
                                        | TutorState.processando_exclusao
                                    ),
                                    color_scheme="red",
                                ),
                                rx.cond(
                                    TutorState.tutor_id_exclusao
                                    == tutor["id"],
                                    rx.vstack(
                                        rx.text(
                                            "Confirma a exclusão deste tutor? "
                                            "A ação não poderá ser desfeita.",
                                            color="red",
                                            size="2",
                                        ),
                                        rx.hstack(
                                            rx.button(
                                                "Confirmar exclusão",
                                                on_click=(
                                                    TutorState.confirmar_exclusao
                                                ),
                                                loading=(
                                                    TutorState.processando_exclusao
                                                ),
                                                color_scheme="red",
                                            ),
                                            rx.button(
                                                "Cancelar",
                                                on_click=(
                                                    TutorState.cancelar_exclusao
                                                ),
                                                disabled=(
                                                    TutorState.processando_exclusao
                                                ),
                                                variant="outline",
                                            ),
                                        ),
                                        align="start",
                                        width="100%",
                                    ),
                                ),
                                justify="between",
                                align="center",
                                wrap="wrap",
                                width="100%",
                                padding="12px",
                                class_name="pettech-card",
                                border="1px solid #ddd",
                                border_radius="8px",
                            ),
                        ),
                        width="100%",
                        max_width="600px",
                    ),
                    rx.text(TutorState.erro_lista),
                ),
            ),
            rx.cond(
                TutorState.mensagem_exclusao,
                rx.text(
                    TutorState.mensagem_exclusao,
                    color=rx.cond(
                        TutorState.sucesso_exclusao,
                        "green",
                        rx.cond(
                            TutorState.processando_exclusao,
                            "blue",
                            "red",
                        ),
                    ),
                    size="2",
                ),
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
        ),
    )


class PetState(rx.State):
    """Estado para gerenciar cadastro e alteração de pets."""
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
    pets: list[dict[str, str]] = []
    tem_pets: bool = False
    carregando_pets: bool = False
    erro_lista_pets: str = ""
    pet_id_edicao: str = ""
    tutor_id_edicao: str = ""
    tutor_selecionado_edicao: str = ""
    nome_edicao: str = ""
    especie_edicao: str = ""
    raca_edicao: str = ""
    porte_edicao: str = ""
    observacoes_saude_edicao: str = ""
    editando: bool = False
    processando_edicao: bool = False
    mensagem_edicao: str = ""
    sucesso_edicao: bool = False
    pet_id_exclusao: str = ""
    processando_exclusao: bool = False
    mensagem_exclusao: str = ""
    sucesso_exclusao: bool = False

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
    def carregar_pets(self):
        """Carrega os pets existentes para a lista de edição."""
        self.carregando_pets = True
        self.erro_lista_pets = ""

        try:
            response = httpx.get(f"{XANO_API_URL}/pet", timeout=10.0)
            response.raise_for_status()
            pets = response.json()
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
            self.erro_lista_pets = f"Erro ao carregar pets: {err_msg}"
            self.pets = []
            self.tem_pets = False
        except httpx.RequestError as error:
            self.erro_lista_pets = f"Erro de conexão ao carregar pets: {error}"
            self.pets = []
            self.tem_pets = False
        except ValueError:
            self.erro_lista_pets = "O Xano retornou uma lista de pets inválida."
            self.pets = []
            self.tem_pets = False
        else:
            if not isinstance(pets, list):
                self.erro_lista_pets = "O Xano retornou uma lista de pets inválida."
                self.pets = []
                self.tem_pets = False
            else:
                pets_validos: list[dict[str, str]] = []
                registros_incompletos = 0
                for pet in pets:
                    if not isinstance(pet, dict):
                        registros_incompletos += 1
                        continue

                    pet_id = normalizar_id(pet.get("id"))
                    if pet_id is None:
                        registros_incompletos += 1
                        continue

                    tutor_id = normalizar_id(pet.get("tutor_id")) or ""
                    nome = pet.get("nome")
                    nome = nome.strip() if isinstance(nome, str) else ""
                    especie = pet.get("especie")
                    especie = especie.strip() if isinstance(especie, str) else ""
                    porte = pet.get("porte")
                    porte = (
                        porte
                        if porte in ["Pequeno", "Médio", "Grande"]
                        else ""
                    )
                    raca = pet.get("raca")
                    raca = raca.strip() if isinstance(raca, str) else ""
                    observacoes = pet.get("observacoes_saude")
                    observacoes = (
                        observacoes.strip()
                        if isinstance(observacoes, str)
                        else ""
                    )
                    dados_incompletos = not all(
                        [tutor_id, nome, especie, porte]
                    )
                    if dados_incompletos:
                        registros_incompletos += 1

                    pets_validos.append(
                        {
                            "id": pet_id,
                            "tutor_id": tutor_id,
                            "nome": nome.strip(),
                            "especie": especie.strip(),
                            "raca": raca or "",
                            "porte": porte,
                            "observacoes_saude": observacoes or "",
                            "dados_incompletos": (
                                "true" if dados_incompletos else "false"
                            ),
                        }
                    )

                self.pets = pets_validos
                self.tem_pets = bool(pets_validos)
                if registros_incompletos:
                    self.erro_lista_pets = (
                        f"{registros_incompletos} pet(s) com dados obrigatórios "
                        "incompletos. Use Editar para preencher os campos ausentes."
                    )
                elif not pets_validos:
                    self.erro_lista_pets = "Nenhum pet cadastrado."
        finally:
            self.carregando_pets = False

    @rx.event
    def iniciar_edicao(self, pet_id: str):
        pet = next((item for item in self.pets if item["id"] == pet_id), None)
        if pet is None:
            self.erro_lista_pets = "Não foi possível localizar o pet selecionado."
            return

        tutor_selecionado = next(
            (
                opcao
                for opcao in self.opcoes_tutor
                if opcao.split(" - ", 1)[0] == pet["tutor_id"]
            ),
            "",
        )
        if pet["tutor_id"] and not tutor_selecionado:
            self.mensagem_edicao = (
                "O tutor deste pet não está disponível. Atualize a lista de tutores."
            )
            self.sucesso_edicao = False
            return

        self.pet_id_edicao = pet["id"]
        self.tutor_id_edicao = pet["tutor_id"]
        self.tutor_selecionado_edicao = tutor_selecionado
        self.nome_edicao = pet["nome"]
        self.especie_edicao = pet["especie"]
        self.raca_edicao = pet["raca"]
        self.porte_edicao = pet["porte"]
        self.observacoes_saude_edicao = pet["observacoes_saude"]
        self.mensagem_edicao = ""
        self.sucesso_edicao = False
        self.editando = True

    @rx.event
    def set_tutor_selecionado_edicao(self, tutor_selecionado: str):
        self.tutor_selecionado_edicao = tutor_selecionado
        self.tutor_id_edicao = tutor_selecionado.split(" - ", 1)[0]

    @rx.event
    def set_nome_edicao(self, nome: str):
        self.nome_edicao = nome

    @rx.event
    def set_especie_edicao(self, especie: str):
        self.especie_edicao = especie

    @rx.event
    def set_raca_edicao(self, raca: str):
        self.raca_edicao = raca

    @rx.event
    def set_porte_edicao(self, porte: str):
        self.porte_edicao = porte

    @rx.event
    def set_observacoes_saude_edicao(self, observacoes_saude: str):
        self.observacoes_saude_edicao = observacoes_saude

    @rx.event
    def cancelar_edicao(self):
        if self.processando_edicao:
            return
        self.editando = False
        self.pet_id_edicao = ""
        self.tutor_id_edicao = ""
        self.tutor_selecionado_edicao = ""
        self.nome_edicao = ""
        self.especie_edicao = ""
        self.raca_edicao = ""
        self.porte_edicao = ""
        self.observacoes_saude_edicao = ""
        self.mensagem_edicao = ""
        self.sucesso_edicao = False

    @rx.event
    def salvar_edicao(self):
        pet_id = normalizar_id(self.pet_id_edicao)
        tutor_id = normalizar_id(self.tutor_id_edicao)
        nome = self.nome_edicao.strip()
        especie = self.especie_edicao.strip()
        raca = self.raca_edicao.strip() or None
        porte = self.porte_edicao
        observacoes = self.observacoes_saude_edicao.strip() or None
        tutor_valido = any(
            opcao.split(" - ", 1)[0] == self.tutor_id_edicao
            for opcao in self.opcoes_tutor
        )

        if pet_id is None:
            self.mensagem_edicao = "Selecione um pet válido para editar."
        elif tutor_id is None or not tutor_valido:
            self.mensagem_edicao = "Selecione um tutor cadastrado."
        elif not nome:
            self.mensagem_edicao = "O nome do pet é obrigatório."
        elif not especie:
            self.mensagem_edicao = "A espécie do pet é obrigatória."
        elif porte not in ["Pequeno", "Médio", "Grande"]:
            self.mensagem_edicao = "Selecione um porte válido."
        else:
            self.mensagem_edicao = ""

        if self.mensagem_edicao:
            self.sucesso_edicao = False
            return

        self.processando_edicao = True
        self.mensagem_edicao = "Salvando alterações..."
        self.sucesso_edicao = False
        dados = {
            "tutor_id": int(tutor_id),
            "nome": nome,
            "especie": especie,
            "raca": raca,
            "porte": porte,
            "observacoes_saude": observacoes,
        }

        try:
            response = httpx.patch(
                f"{XANO_API_URL}/pet/{pet_id}",
                json=dados,
                timeout=10.0,
            )
            response.raise_for_status()
            pet_atualizado = response.json()
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
            self.mensagem_edicao = f"Erro ao alterar pet: {err_msg}"
        except httpx.RequestError as error:
            self.mensagem_edicao = f"Erro de conexão com o Xano: {error}"
        except ValueError:
            self.mensagem_edicao = "O Xano retornou uma resposta inválida."
        else:
            dados_confirmados = (
                isinstance(pet_atualizado, dict)
                and normalizar_id(pet_atualizado.get("id")) == pet_id
                and normalizar_id(pet_atualizado.get("tutor_id")) == tutor_id
                and pet_atualizado.get("nome") == nome
                and pet_atualizado.get("especie") == especie
                and pet_atualizado.get("raca") == raca
                and pet_atualizado.get("porte") == porte
                and pet_atualizado.get("observacoes_saude") == observacoes
            )
            if not dados_confirmados:
                self.mensagem_edicao = (
                    "O Xano não confirmou a alteração dos dados do pet."
                )
            else:
                self.mensagem_edicao = "Pet alterado com sucesso."
                self.sucesso_edicao = True
                self.pets = [
                    {
                        "id": pet_id,
                        "tutor_id": tutor_id,
                        "nome": nome,
                        "especie": especie,
                        "raca": raca or "",
                        "porte": porte,
                        "observacoes_saude": observacoes or "",
                        "dados_incompletos": "false",
                    }
                    if pet["id"] == pet_id
                    else pet
                    for pet in self.pets
                ]
                registros_incompletos = sum(
                    pet["dados_incompletos"] == "true" for pet in self.pets
                )
                self.erro_lista_pets = (
                    f"{registros_incompletos} pet(s) com dados obrigatórios "
                    "incompletos. Use Editar para preencher os campos ausentes."
                    if registros_incompletos
                    else ""
                )
        finally:
            self.processando_edicao = False

    @rx.event
    def iniciar_exclusao(self, pet_id: str):
        if self.processando_edicao or self.processando_exclusao:
            return
        if not any(pet["id"] == pet_id for pet in self.pets):
            self.erro_lista_pets = "Não foi possível localizar o pet selecionado."
            return
        self.pet_id_exclusao = pet_id
        self.mensagem_exclusao = ""
        self.sucesso_exclusao = False

    @rx.event
    def cancelar_exclusao(self):
        if self.processando_exclusao:
            return
        self.pet_id_exclusao = ""
        self.mensagem_exclusao = ""
        self.sucesso_exclusao = False

    @rx.event
    def confirmar_exclusao(self):
        pet_id = normalizar_id(self.pet_id_exclusao)
        if pet_id is None:
            self.mensagem_exclusao = "Selecione um pet válido para excluir."
            self.sucesso_exclusao = False
            return

        self.processando_exclusao = True
        self.mensagem_exclusao = "Excluindo pet..."
        self.sucesso_exclusao = False
        try:
            response = httpx.delete(
                f"{XANO_API_URL}/pet/{pet_id}",
                timeout=10.0,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            try:
                err_data = error.response.json()
            except ValueError:
                err_data = None
            err_msg = (
                err_data.get("message", "").strip()
                if isinstance(err_data, dict)
                and isinstance(err_data.get("message"), str)
                else ""
            )
            if not err_msg:
                err_msg = error.response.text.strip()
            if not err_msg:
                err_msg = f"Xano retornou HTTP {error.response.status_code}."
            self.mensagem_exclusao = f"Erro ao excluir pet: {err_msg}"
        except httpx.RequestError as error:
            self.mensagem_exclusao = f"Erro de conexão com o Xano: {error}"
        else:
            resultado = None
            if response.content:
                try:
                    resultado = response.json()
                except ValueError:
                    resultado = None

            exclusao_confirmada = (
                isinstance(resultado, dict)
                and normalizar_id(resultado.get("id")) == pet_id
                and resultado.get("deleted") is True
            )
            if not exclusao_confirmada:
                try:
                    verificacao = httpx.get(
                        f"{XANO_API_URL}/pet/{pet_id}",
                        timeout=10.0,
                    )
                    verificacao.raise_for_status()
                except httpx.HTTPStatusError as error:
                    if error.response.status_code == 404:
                        exclusao_confirmada = True
                    else:
                        self.mensagem_exclusao = (
                            "O Xano respondeu à exclusão, mas não foi possível "
                            "verificar se o pet foi removido."
                        )
                except httpx.RequestError as error:
                    self.mensagem_exclusao = (
                        "A solicitação de exclusão foi enviada, mas não foi "
                        f"possível confirmar o resultado: {error}"
                    )
                else:
                    self.mensagem_exclusao = (
                        "O pet ainda consta no Xano; a exclusão não foi "
                        "confirmada."
                    )

            if not exclusao_confirmada:
                if self.mensagem_exclusao == "Excluindo pet...":
                    self.mensagem_exclusao = (
                        "O Xano não confirmou a exclusão do pet."
                    )
            else:
                self.pets = [
                    pet for pet in self.pets if pet["id"] != pet_id
                ]
                self.tem_pets = bool(self.pets)
                registros_incompletos = sum(
                    pet["dados_incompletos"] == "true" for pet in self.pets
                )
                self.erro_lista_pets = (
                    f"{registros_incompletos} pet(s) com dados obrigatórios "
                    "incompletos. Use Editar para preencher os campos ausentes."
                    if registros_incompletos
                    else (
                        "" if self.tem_pets else "Nenhum pet cadastrado."
                    )
                )
                self.pet_id_exclusao = ""
                self.mensagem_exclusao = "Pet excluído com sucesso."
                self.sucesso_exclusao = True
                if self.pet_id_edicao == pet_id:
                    self.editando = False
                    self.pet_id_edicao = ""
                    self.tutor_id_edicao = ""
                    self.tutor_selecionado_edicao = ""
                    self.nome_edicao = ""
                    self.especie_edicao = ""
                    self.raca_edicao = ""
                    self.porte_edicao = ""
                    self.observacoes_saude_edicao = ""
                    self.mensagem_edicao = ""
                    self.sucesso_edicao = False
        finally:
            self.processando_exclusao = False

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
                pet_id = normalizar_id(pet.get("id"))
                if pet_id is not None:
                    self.pets.append(
                        {
                            "id": pet_id,
                            "tutor_id": self.tutor_id,
                            "nome": nome,
                            "especie": especie,
                            "raca": dados.get("raca", ""),
                            "porte": self.porte,
                            "observacoes_saude": dados.get(
                                "observacoes_saude", ""
                            ),
                        }
                    )
                    self.tem_pets = True
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
            rx.cond(
                PetState.editando,
                rx.vstack(
                    rx.heading("Editar Pet", size="5"),
                    rx.text("Tutor responsável:"),
                    rx.select(
                        PetState.opcoes_tutor,
                        value=PetState.tutor_selecionado_edicao,
                        on_change=PetState.set_tutor_selecionado_edicao,
                        placeholder="Selecione um tutor",
                        width="100%",
                    ),
                    rx.text("Nome:"),
                    rx.input(
                        value=PetState.nome_edicao,
                        on_change=PetState.set_nome_edicao,
                        width="100%",
                    ),
                    rx.text("Espécie:"),
                    rx.input(
                        value=PetState.especie_edicao,
                        on_change=PetState.set_especie_edicao,
                        width="100%",
                    ),
                    rx.text("Raça (opcional):"),
                    rx.input(
                        value=PetState.raca_edicao,
                        on_change=PetState.set_raca_edicao,
                        width="100%",
                    ),
                    rx.text("Porte:"),
                    rx.select(
                        ["Pequeno", "Médio", "Grande"],
                        value=PetState.porte_edicao,
                        on_change=PetState.set_porte_edicao,
                        placeholder="Selecione o porte",
                        width="100%",
                    ),
                    rx.text("Observações de saúde e comportamento (opcional):"),
                    rx.text_area(
                        value=PetState.observacoes_saude_edicao,
                        on_change=PetState.set_observacoes_saude_edicao,
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            "Salvar alterações",
                            on_click=PetState.salvar_edicao,
                            loading=PetState.processando_edicao,
                        ),
                        rx.button(
                            "Cancelar",
                            on_click=PetState.cancelar_edicao,
                            disabled=PetState.processando_edicao,
                            variant="outline",
                        ),
                    ),
                    rx.cond(
                        PetState.mensagem_edicao,
                        rx.text(
                            PetState.mensagem_edicao,
                            color=rx.cond(
                                PetState.sucesso_edicao,
                                "green",
                                "red",
                            ),
                            size="2",
                        ),
                    ),
                    width="100%",
                    max_width="600px",
                    padding="20px",
                    class_name="pettech-card",
                    border="1px solid #ddd",
                    border_radius="10px",
                    spacing="3",
                ),
                rx.text(""),
            ),
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
                class_name="pettech-card",
                border="1px solid #ddd",
                border_radius="10px",
                spacing="3",
            ),
            rx.heading("Pets cadastrados", size="5"),
            rx.cond(
                PetState.carregando_pets,
                rx.text("Carregando pets..."),
                rx.cond(
                    PetState.tem_pets,
                    rx.vstack(
                        rx.cond(
                            PetState.erro_lista_pets,
                            rx.text(
                                PetState.erro_lista_pets,
                                color="orange",
                                size="2",
                            ),
                        ),
                        rx.foreach(
                            PetState.pets,
                            lambda pet: rx.hstack(
                                rx.vstack(
                                    rx.text(
                                        rx.cond(
                                            pet["nome"] != "",
                                            pet["nome"],
                                            "Nome não informado",
                                        ),
                                        weight="bold",
                                    ),
                                    rx.text(
                                        rx.cond(
                                            pet["especie"] != "",
                                            pet["especie"],
                                            "Espécie não informada",
                                        )
                                        + " · "
                                        + rx.cond(
                                            pet["porte"] != "",
                                            pet["porte"],
                                            "Porte não informado",
                                        )
                                    ),
                                    rx.text(
                                        rx.cond(
                                            pet["tutor_id"] != "",
                                            "Tutor ID: " + pet["tutor_id"],
                                            "Tutor não informado",
                                        ),
                                        size="2",
                                    ),
                                    rx.text(
                                        rx.cond(
                                            pet["raca"] != "",
                                            "Raça: " + pet["raca"],
                                            "Raça não informada",
                                        ),
                                        size="2",
                                    ),
                                    rx.cond(
                                        pet["dados_incompletos"] == "true",
                                        rx.text(
                                            "Dados incompletos — edite para preencher",
                                            color="orange",
                                            size="2",
                                        ),
                                    ),
                                    align="start",
                                ),
                                rx.button(
                                    "Editar",
                                    on_click=PetState.iniciar_edicao(pet["id"]),
                                    disabled=(
                                        PetState.processando_edicao
                                        | PetState.processando_exclusao
                                    ),
                                ),
                                rx.button(
                                    "Excluir",
                                    on_click=PetState.iniciar_exclusao(pet["id"]),
                                    disabled=(
                                        PetState.processando_edicao
                                        | PetState.processando_exclusao
                                    ),
                                    color_scheme="red",
                                ),
                                rx.cond(
                                    PetState.pet_id_exclusao == pet["id"],
                                    rx.vstack(
                                        rx.text(
                                            "Confirma a exclusão deste pet? "
                                            "Agendamentos vinculados impedem "
                                            "a exclusão.",
                                            color="red",
                                            size="2",
                                        ),
                                        rx.hstack(
                                            rx.button(
                                                "Confirmar exclusão",
                                                on_click=(
                                                    PetState.confirmar_exclusao
                                                ),
                                                loading=(
                                                    PetState.processando_exclusao
                                                ),
                                                color_scheme="red",
                                            ),
                                            rx.button(
                                                "Cancelar",
                                                on_click=(
                                                    PetState.cancelar_exclusao
                                                ),
                                                disabled=(
                                                    PetState.processando_exclusao
                                                ),
                                                variant="outline",
                                            ),
                                        ),
                                        align="start",
                                        width="100%",
                                    ),
                                ),
                                justify="between",
                                align="center",
                                wrap="wrap",
                                width="100%",
                                padding="12px",
                                class_name="pettech-card",
                                border="1px solid #ddd",
                                border_radius="8px",
                            ),
                        ),
                        width="100%",
                        max_width="600px",
                    ),
                    rx.text(PetState.erro_lista_pets),
                ),
            ),
            rx.cond(
                PetState.mensagem_exclusao,
                rx.text(
                    PetState.mensagem_exclusao,
                    color=rx.cond(
                        PetState.sucesso_exclusao,
                        "green",
                        rx.cond(
                            PetState.processando_exclusao,
                            "blue",
                            "red",
                        ),
                    ),
                    size="2",
                ),
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
        ),
    )


class ServicoState(rx.State):
    """Estado para gerenciar cadastro e alteração de serviços."""
    nome: str = ""
    descricao: str = ""
    preco: str = ""
    duracao_minutos: str = ""
    processando: bool = False
    mensagem: str = ""
    sucesso: bool = False
    servicos: list[dict[str, str]] = []
    tem_servicos: bool = False
    carregando_servicos: bool = False
    erro_lista_servicos: str = ""
    servico_id_edicao: str = ""
    nome_edicao: str = ""
    descricao_edicao: str = ""
    preco_edicao: str = ""
    duracao_minutos_edicao: str = ""
    editando: bool = False
    processando_edicao: bool = False
    mensagem_edicao: str = ""
    sucesso_edicao: bool = False
    servico_id_exclusao: str = ""
    processando_exclusao: bool = False
    mensagem_exclusao: str = ""
    sucesso_exclusao: bool = False

    @rx.event
    def carregar_servicos(self):
        """Carrega os serviços existentes para a lista de edição."""
        self.carregando_servicos = True
        self.erro_lista_servicos = ""

        try:
            response = httpx.get(f"{XANO_API_URL}/servico", timeout=10.0)
            response.raise_for_status()
            servicos = response.json()
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
            self.erro_lista_servicos = f"Erro ao carregar serviços: {err_msg}"
            self.servicos = []
            self.tem_servicos = False
        except httpx.RequestError as error:
            self.erro_lista_servicos = (
                f"Erro de conexão ao carregar serviços: {error}"
            )
            self.servicos = []
            self.tem_servicos = False
        except ValueError:
            self.erro_lista_servicos = (
                "O Xano retornou uma lista de serviços inválida."
            )
            self.servicos = []
            self.tem_servicos = False
        else:
            if not isinstance(servicos, list):
                self.erro_lista_servicos = (
                    "O Xano retornou uma lista de serviços inválida."
                )
                self.servicos = []
                self.tem_servicos = False
            else:
                servicos_validos: list[dict[str, str]] = []
                registros_incompletos = 0
                for servico in servicos:
                    if not isinstance(servico, dict):
                        registros_incompletos += 1
                        continue

                    servico_id = normalizar_id(servico.get("id"))
                    if servico_id is None:
                        registros_incompletos += 1
                        continue

                    nome = servico.get("nome")
                    nome = nome.strip() if isinstance(nome, str) else ""
                    descricao = servico.get("descricao")
                    descricao = (
                        descricao.strip() if isinstance(descricao, str) else ""
                    )
                    try:
                        preco = Decimal(str(servico.get("preco")))
                        preco_valido = preco.is_finite() and preco > 0
                    except (InvalidOperation, TypeError, ValueError):
                        preco = Decimal("NaN")
                        preco_valido = False
                    duracao = servico.get("duracao_minutos")
                    duracao_valida = (
                        isinstance(duracao, int)
                        and not isinstance(duracao, bool)
                        and duracao > 0
                    )
                    dados_incompletos = not (
                        nome and preco_valido and duracao_valida
                    )
                    if dados_incompletos:
                        registros_incompletos += 1

                    servicos_validos.append(
                        {
                            "id": servico_id,
                            "nome": nome,
                            "descricao": descricao,
                            "preco": format(preco, "f") if preco_valido else "",
                            "preco_exibicao": (
                                f"R$ {preco:.2f}".replace(".", ",")
                                if preco_valido
                                else "Valor não informado"
                            ),
                            "duracao_minutos": (
                                str(duracao) if duracao_valida else ""
                            ),
                            "dados_incompletos": (
                                "true" if dados_incompletos else "false"
                            ),
                        }
                    )

                self.servicos = servicos_validos
                self.tem_servicos = bool(servicos_validos)
                if registros_incompletos:
                    self.erro_lista_servicos = (
                        f"{registros_incompletos} serviço(s) com dados obrigatórios "
                        "incompletos. Use Editar para preencher os campos ausentes."
                    )
                elif not servicos_validos:
                    self.erro_lista_servicos = "Nenhum serviço cadastrado."
        finally:
            self.carregando_servicos = False

    @rx.event
    def iniciar_edicao(self, servico_id: str):
        servico = next(
            (item for item in self.servicos if item["id"] == servico_id),
            None,
        )
        if servico is None:
            self.erro_lista_servicos = (
                "Não foi possível localizar o serviço selecionado."
            )
            return

        self.servico_id_edicao = servico["id"]
        self.nome_edicao = servico["nome"]
        self.descricao_edicao = servico["descricao"]
        self.preco_edicao = servico["preco"].replace(".", ",")
        self.duracao_minutos_edicao = servico["duracao_minutos"]
        self.mensagem_edicao = ""
        self.sucesso_edicao = False
        self.editando = True

    @rx.event
    def set_nome_edicao(self, nome: str):
        self.nome_edicao = nome

    @rx.event
    def set_descricao_edicao(self, descricao: str):
        self.descricao_edicao = descricao

    @rx.event
    def set_preco_edicao(self, preco: str):
        self.preco_edicao = preco

    @rx.event
    def set_duracao_minutos_edicao(self, duracao_minutos: str):
        self.duracao_minutos_edicao = duracao_minutos

    @rx.event
    def cancelar_edicao(self):
        if self.processando_edicao:
            return
        self.editando = False
        self.servico_id_edicao = ""
        self.nome_edicao = ""
        self.descricao_edicao = ""
        self.preco_edicao = ""
        self.duracao_minutos_edicao = ""
        self.mensagem_edicao = ""
        self.sucesso_edicao = False

    @rx.event
    def salvar_edicao(self):
        servico_id = normalizar_id(self.servico_id_edicao)
        nome = self.nome_edicao.strip()
        descricao = self.descricao_edicao.strip() or None

        if servico_id is None:
            self.mensagem_edicao = "Selecione um serviço válido para editar."
            self.sucesso_edicao = False
            return
        if not nome:
            self.mensagem_edicao = "O nome do serviço é obrigatório."
            self.sucesso_edicao = False
            return

        try:
            preco = parse_preco(self.preco_edicao)
        except (InvalidOperation, ValueError):
            self.mensagem_edicao = "Informe um valor válido, por exemplo 35,00."
            self.sucesso_edicao = False
            return
        if not preco.is_finite() or preco <= 0:
            self.mensagem_edicao = "O valor deve ser maior que zero."
            self.sucesso_edicao = False
            return

        try:
            duracao_minutos = int(self.duracao_minutos_edicao.strip())
        except ValueError:
            self.mensagem_edicao = (
                "Informe a duração em minutos como número inteiro."
            )
            self.sucesso_edicao = False
            return
        if duracao_minutos <= 0:
            self.mensagem_edicao = "A duração deve ser maior que zero."
            self.sucesso_edicao = False
            return

        self.processando_edicao = True
        self.mensagem_edicao = "Salvando alterações..."
        self.sucesso_edicao = False
        dados = {
            "nome": nome,
            "descricao": descricao,
            "preco": float(preco),
            "duracao_minutos": duracao_minutos,
        }

        try:
            response = httpx.patch(
                f"{XANO_API_URL}/servico/{servico_id}",
                json=dados,
                timeout=10.0,
            )
            response.raise_for_status()
            servico_atualizado = response.json()
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
            self.mensagem_edicao = f"Erro ao alterar serviço: {err_msg}"
        except httpx.RequestError as error:
            self.mensagem_edicao = f"Erro de conexão com o Xano: {error}"
        except ValueError:
            self.mensagem_edicao = "O Xano retornou uma resposta inválida."
        else:
            if isinstance(servico_atualizado, dict):
                try:
                    preco_persistido = Decimal(
                        str(servico_atualizado.get("preco"))
                    )
                except (InvalidOperation, TypeError, ValueError):
                    preco_persistido = Decimal("NaN")
                duracao_persistida = servico_atualizado.get(
                    "duracao_minutos"
                )
                dados_confirmados = (
                    normalizar_id(servico_atualizado.get("id")) == servico_id
                    and servico_atualizado.get("nome") == nome
                    and servico_atualizado.get("descricao") == descricao
                    and preco_persistido.is_finite()
                    and preco_persistido == preco
                    and isinstance(duracao_persistida, int)
                    and not isinstance(duracao_persistida, bool)
                    and duracao_persistida == duracao_minutos
                )
            else:
                dados_confirmados = False

            if not dados_confirmados:
                self.mensagem_edicao = (
                    "O Xano não confirmou a alteração dos dados do serviço."
                )
            else:
                self.mensagem_edicao = "Serviço alterado com sucesso."
                self.sucesso_edicao = True
                self.servicos = [
                    {
                        "id": servico_id,
                        "nome": nome,
                        "descricao": descricao or "",
                        "preco": format(preco, "f"),
                        "preco_exibicao": (
                            f"R$ {preco:.2f}".replace(".", ",")
                        ),
                        "duracao_minutos": str(duracao_minutos),
                        "dados_incompletos": "false",
                    }
                    if servico["id"] == servico_id
                    else servico
                    for servico in self.servicos
                ]
                registros_incompletos = sum(
                    servico["dados_incompletos"] == "true"
                    for servico in self.servicos
                )
                self.erro_lista_servicos = (
                    f"{registros_incompletos} serviço(s) com dados obrigatórios "
                    "incompletos. Use Editar para preencher os campos ausentes."
                    if registros_incompletos
                    else ""
                )
        finally:
            self.processando_edicao = False

    @rx.event
    def iniciar_exclusao(self, servico_id: str):
        if self.processando_edicao or self.processando_exclusao:
            return
        if not any(
            servico["id"] == servico_id for servico in self.servicos
        ):
            self.erro_lista_servicos = (
                "Não foi possível localizar o serviço selecionado."
            )
            return
        self.servico_id_exclusao = servico_id
        self.mensagem_exclusao = ""
        self.sucesso_exclusao = False

    @rx.event
    def cancelar_exclusao(self):
        if self.processando_exclusao:
            return
        self.servico_id_exclusao = ""
        self.mensagem_exclusao = ""
        self.sucesso_exclusao = False

    @rx.event
    def confirmar_exclusao(self):
        servico_id = normalizar_id(self.servico_id_exclusao)
        if servico_id is None:
            self.mensagem_exclusao = (
                "Selecione um serviço válido para excluir."
            )
            self.sucesso_exclusao = False
            return

        self.processando_exclusao = True
        self.mensagem_exclusao = "Excluindo serviço..."
        self.sucesso_exclusao = False
        try:
            response = httpx.delete(
                f"{XANO_API_URL}/servico/{servico_id}",
                timeout=10.0,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            try:
                err_data = error.response.json()
            except ValueError:
                err_data = None
            err_msg = (
                err_data.get("message", "").strip()
                if isinstance(err_data, dict)
                and isinstance(err_data.get("message"), str)
                else ""
            )
            if not err_msg:
                err_msg = error.response.text.strip()
            if not err_msg:
                err_msg = f"Xano retornou HTTP {error.response.status_code}."
            self.mensagem_exclusao = (
                f"Erro ao excluir serviço: {err_msg}"
            )
        except httpx.RequestError as error:
            self.mensagem_exclusao = f"Erro de conexão com o Xano: {error}"
        else:
            resultado = None
            if response.content:
                try:
                    resultado = response.json()
                except ValueError:
                    resultado = None

            exclusao_confirmada = (
                isinstance(resultado, dict)
                and normalizar_id(resultado.get("id")) == servico_id
                and resultado.get("deleted") is True
            )
            if not exclusao_confirmada:
                try:
                    verificacao = httpx.get(
                        f"{XANO_API_URL}/servico/{servico_id}",
                        timeout=10.0,
                    )
                    verificacao.raise_for_status()
                except httpx.HTTPStatusError as error:
                    if error.response.status_code == 404:
                        exclusao_confirmada = True
                    else:
                        self.mensagem_exclusao = (
                            "O Xano respondeu à exclusão, mas não foi possível "
                            "verificar se o serviço foi removido."
                        )
                except httpx.RequestError as error:
                    self.mensagem_exclusao = (
                        "A solicitação de exclusão foi enviada, mas não foi "
                        f"possível confirmar o resultado: {error}"
                    )
                else:
                    self.mensagem_exclusao = (
                        "O serviço ainda consta no Xano; a exclusão não foi "
                        "confirmada."
                    )

            if not exclusao_confirmada:
                if self.mensagem_exclusao == "Excluindo serviço...":
                    self.mensagem_exclusao = (
                        "O Xano não confirmou a exclusão do serviço."
                    )
            else:
                self.servicos = [
                    servico
                    for servico in self.servicos
                    if servico["id"] != servico_id
                ]
                self.tem_servicos = bool(self.servicos)
                registros_incompletos = sum(
                    servico["dados_incompletos"] == "true"
                    for servico in self.servicos
                )
                self.erro_lista_servicos = (
                    f"{registros_incompletos} serviço(s) com dados obrigatórios "
                    "incompletos. Use Editar para preencher os campos ausentes."
                    if registros_incompletos
                    else (
                        "" if self.tem_servicos else "Nenhum serviço cadastrado."
                    )
                )
                self.servico_id_exclusao = ""
                self.mensagem_exclusao = "Serviço excluído com sucesso."
                self.sucesso_exclusao = True
                if self.servico_id_edicao == servico_id:
                    self.editando = False
                    self.servico_id_edicao = ""
                    self.nome_edicao = ""
                    self.descricao_edicao = ""
                    self.preco_edicao = ""
                    self.duracao_minutos_edicao = ""
                    self.mensagem_edicao = ""
                    self.sucesso_edicao = False
        finally:
            self.processando_exclusao = False

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
                servico_id = normalizar_id(servico.get("id"))
                if servico_id is not None:
                    self.servicos.append(
                        {
                            "id": servico_id,
                            "nome": nome,
                            "descricao": descricao,
                            "preco": format(preco, "f"),
                            "preco_exibicao": (
                                f"R$ {preco:.2f}".replace(".", ",")
                            ),
                            "duracao_minutos": str(duracao_minutos),
                            "dados_incompletos": "false",
                        }
                    )
                    self.tem_servicos = True
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
                    class_name="pettech-card",
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
                    class_name="pettech-card",
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
                    class_name="pettech-card",
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
            rx.cond(
                ServicoState.editando,
                rx.vstack(
                    rx.heading("Editar Serviço", size="5"),
                    rx.text("Nome:"),
                    rx.input(
                        value=ServicoState.nome_edicao,
                        on_change=ServicoState.set_nome_edicao,
                        width="100%",
                    ),
                    rx.text("Descrição (opcional):"),
                    rx.text_area(
                        value=ServicoState.descricao_edicao,
                        on_change=ServicoState.set_descricao_edicao,
                        width="100%",
                    ),
                    rx.text("Valor (R$):"),
                    rx.input(
                        type="text",
                        input_mode="decimal",
                        value=ServicoState.preco_edicao,
                        on_change=ServicoState.set_preco_edicao,
                        width="100%",
                    ),
                    rx.text("Duração média (minutos):"),
                    rx.input(
                        type="number",
                        min="1",
                        step="1",
                        value=ServicoState.duracao_minutos_edicao,
                        on_change=ServicoState.set_duracao_minutos_edicao,
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            "Salvar alterações",
                            on_click=ServicoState.salvar_edicao,
                            loading=ServicoState.processando_edicao,
                        ),
                        rx.button(
                            "Cancelar",
                            on_click=ServicoState.cancelar_edicao,
                            disabled=ServicoState.processando_edicao,
                            variant="outline",
                        ),
                    ),
                    rx.cond(
                        ServicoState.mensagem_edicao,
                        rx.text(
                            ServicoState.mensagem_edicao,
                            color=rx.cond(
                                ServicoState.sucesso_edicao,
                                "green",
                                "red",
                            ),
                            size="2",
                        ),
                    ),
                    width="100%",
                    max_width="600px",
                    padding="20px",
                    class_name="pettech-card",
                    border="1px solid #ddd",
                    border_radius="10px",
                    spacing="3",
                ),
                rx.text(""),
            ),
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
                class_name="pettech-card",
                border="1px solid #ddd",
                border_radius="10px",
                spacing="3",
            ),
            rx.heading("Serviços cadastrados", size="5"),
            rx.cond(
                ServicoState.carregando_servicos,
                rx.text("Carregando serviços..."),
                rx.cond(
                    ServicoState.tem_servicos,
                    rx.vstack(
                        rx.cond(
                            ServicoState.erro_lista_servicos,
                            rx.text(
                                ServicoState.erro_lista_servicos,
                                color="orange",
                                size="2",
                            ),
                        ),
                        rx.foreach(
                            ServicoState.servicos,
                            lambda servico: rx.hstack(
                                rx.vstack(
                                    rx.text(
                                        rx.cond(
                                            servico["nome"] != "",
                                            servico["nome"],
                                            "Nome não informado",
                                        ),
                                        weight="bold",
                                    ),
                                    rx.text(
                                        rx.cond(
                                            servico["descricao"] != "",
                                            servico["descricao"],
                                            "Sem descrição",
                                        ),
                                        size="2",
                                    ),
                                    rx.text(
                                        servico["preco_exibicao"]
                                        + " · "
                                        + rx.cond(
                                            servico["duracao_minutos"] != "",
                                            servico["duracao_minutos"] + " min",
                                            "Duração não informada",
                                        )
                                    ),
                                    rx.cond(
                                        servico["dados_incompletos"] == "true",
                                        rx.text(
                                            "Dados incompletos — edite para preencher",
                                            color="orange",
                                            size="2",
                                        ),
                                    ),
                                    align="start",
                                ),
                                rx.button(
                                    "Editar",
                                    on_click=ServicoState.iniciar_edicao(
                                        servico["id"]
                                    ),
                                    disabled=(
                                        ServicoState.processando_edicao
                                        | ServicoState.processando_exclusao
                                    ),
                                ),
                                rx.button(
                                    "Excluir",
                                    on_click=ServicoState.iniciar_exclusao(
                                        servico["id"]
                                    ),
                                    disabled=(
                                        ServicoState.processando_edicao
                                        | ServicoState.processando_exclusao
                                    ),
                                    color_scheme="red",
                                ),
                                rx.cond(
                                    ServicoState.servico_id_exclusao
                                    == servico["id"],
                                    rx.vstack(
                                        rx.text(
                                            "Confirma a exclusão deste serviço? "
                                            "Agendamentos vinculados impedem "
                                            "a exclusão.",
                                            color="red",
                                            size="2",
                                        ),
                                        rx.hstack(
                                            rx.button(
                                                "Confirmar exclusão",
                                                on_click=(
                                                    ServicoState.confirmar_exclusao
                                                ),
                                                loading=(
                                                    ServicoState.processando_exclusao
                                                ),
                                                color_scheme="red",
                                            ),
                                            rx.button(
                                                "Cancelar",
                                                on_click=(
                                                    ServicoState.cancelar_exclusao
                                                ),
                                                disabled=(
                                                    ServicoState.processando_exclusao
                                                ),
                                                variant="outline",
                                            ),
                                        ),
                                        align="start",
                                        width="100%",
                                    ),
                                ),
                                justify="between",
                                align="center",
                                wrap="wrap",
                                width="100%",
                                padding="12px",
                                class_name="pettech-card",
                                border="1px solid #ddd",
                                border_radius="8px",
                            ),
                        ),
                        width="100%",
                        max_width="600px",
                    ),
                    rx.text(ServicoState.erro_lista_servicos),
                ),
            ),
            rx.cond(
                ServicoState.mensagem_exclusao,
                rx.text(
                    ServicoState.mensagem_exclusao,
                    color=rx.cond(
                        ServicoState.sucesso_exclusao,
                        "green",
                        rx.cond(
                            ServicoState.processando_exclusao,
                            "blue",
                            "red",
                        ),
                    ),
                    size="2",
                ),
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
        ),
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;500;600;700;800&family=Poppins:wght@500;600;700&display=swap",
        "/pettech.css",
    ],
    style={
        rx.container: {
            "max_width": "1120px",
            "padding": "32px 24px",
        },
        rx.heading: {
            "font_family": "Poppins, sans-serif",
            "color": "#26352F",
            "font_weight": "600",
            "letter_spacing": "-0.02em",
        },
        rx.text: {
            "font_family": "Nunito Sans, sans-serif",
            "color": "#40514B",
            "line_height": "1.6",
        },
        rx.button: {
            "border_radius": "12px",
            "font_family": "Nunito Sans, sans-serif",
            "font_weight": "700",
            "box_shadow": "0 4px 12px rgba(38, 53, 47, 0.10)",
            "transition": "all 160ms ease",
        },
        rx.input: {
            "border_color": "#D9E1DC",
            "border_radius": "12px",
            "background_color": "#FFFFFF",
            "font_family": "Nunito Sans, sans-serif",
        },
        rx.text_area: {
            "border_color": "#D9E1DC",
            "border_radius": "12px",
            "background_color": "#FFFFFF",
            "font_family": "Nunito Sans, sans-serif",
        },
        rx.link: {
            "color": "#52796F",
            "font_family": "Nunito Sans, sans-serif",
            "font_weight": "700",
        },
        "::selection": {
            "background_color": "#DCE9E2",
            "color": "#26352F",
        },
    },
)
app.add_page(login, route="/")
app.add_page(cliente_login, route="/cliente")
app.add_page(cadastro_cliente, route="/cliente/cadastro")
app.add_page(
    inicio_cliente,
    route="/cliente/inicio",
    on_load=ClienteAuthState.carregar_conta,
)
app.add_page(
    index,
    route="/tutores",
    on_load=TutorState.carregar_tutores,
)
app.add_page(
    cadastro_pet,
    route="/pets",
    on_load=[PetState.carregar_tutores, PetState.carregar_pets],
)
app.add_page(
    cadastro_servico,
    route="/servicos",
    on_load=ServicoState.carregar_servicos,
)
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
