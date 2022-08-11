# -*- coding: utf-8 -*-
import click


try:
    from fastcdc.fastcdc_cy import fastcdc_cy as fastcdc
    from fastcdc.fastcdc_cy import fastcdc_cy as fastcdc_qcow2_py
except ImportError:
    from fastcdc.fastcdc_py import fastcdc_py as fastcdc
    from fastcdc.fastcdc_py import fastcdc_qcow2_py as fastcdc_qcow2_py
    click.secho("Running in pure python mode (slow)", fg="bright_magenta")

__version__ = "1.4.2"

