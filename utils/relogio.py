"""Relógio institucional compartilhado por busca, reserva e indicadores."""

import os
from datetime import datetime
from zoneinfo import ZoneInfo


def agora_local():
    # Porto Velho; pode ser configurado para outra instituição no ambiente.
    return datetime.now(ZoneInfo(os.getenv("APP_TIMEZONE", "America/Porto_Velho")))


def hoje_local():
    return agora_local().date()
