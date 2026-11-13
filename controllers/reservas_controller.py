
from datetime import datetime


PRIORIDADE_NORMAL = 1
PRIORIDADE_AULA_PRATICA = 2
PRIORIDADE_EVENTO = 3


def classificar_prioridade(necessita_equipamentos, evento_institucional=False):
    if evento_institucional:
        return PRIORIDADE_EVENTO

    if necessita_equipamentos:
        return PRIORIDADE_AULA_PRATICA

    return PRIORIDADE_NORMAL


def converter_horario(horario):
    try:
        inicio, fim = horario.split(" - ")

        inicio = datetime.strptime(inicio.strip(), "%H:%M").time()
        fim = datetime.strptime(fim.strip(), "%H:%M").time()

        if inicio >= fim:
            raise ValueError("O horário final deve ser posterior ao inicial.")

        return inicio, fim

    except (ValueError, AttributeError):
        raise ValueError("Horário inválido. Utilize o formato HH:MM - HH:MM.")


def horarios_se_sobrepoem(horario1, horario2):
    inicio1, fim1 = converter_horario(horario1)
    inicio2, fim2 = converter_horario(horario2)

    return inicio1 < fim2 and fim1 > inicio2


def buscar_conflitos(reservas, sala_id, data, horario):
    conflitos = []

    for reserva in reservas:
        if reserva.get("status") in ("Negada", "Cancelada"):
            continue

        mesma_sala = reserva.get("sala_id") == sala_id
        mesma_data = reserva.get("data") == data

        if not mesma_sala or not mesma_data:
            continue

        if horarios_se_sobrepoem(reserva.get("horario", ""), horario):
            conflitos.append(reserva)

    return conflitos


def avaliar_solicitacao(
    reservas,
    sala_id,
    data,
    horario,
    necessita_equipamentos,
    evento_institucional=False
):
    prioridade = classificar_prioridade(
        necessita_equipamentos,
        evento_institucional
    )

    conflitos = buscar_conflitos(
        reservas,
        sala_id,
        data,
        horario
    )

    return {
        "prioridade": prioridade,
        "conflitos": conflitos,
        "precisa_coordenador": len(conflitos) > 0
    }
