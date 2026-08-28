# -*- coding: utf-8 -*-
# --------------------------------------------------
# 多元宇宙全球開源融合模組: LoguruMultiverse
# 產出時間: 2026-08-25 17:37:04
# --------------------------------------------------

# === [全球開源原始碼開始] ===
"""
The Loguru library provides a pre-instanced logger to facilitate dealing with logging in Python.

Just ``from loguru import logger``.
"""

import atexit as _atexit
import sys as _sys

from . import _defaults
from ._logger import Core as _Core
from ._logger import Logger as _Logger

__version__ = "0.7.3"

__all__ = ["logger"]

logger = _Logger(
    core=_Core(),
    exception=None,
    depth=0,
    record=False,
    lazy=False,
    colors=False,
    raw=False,
    capture=True,
    patchers=[],
    extra={},
)

if _defaults.LOGURU_AUTOINIT and _sys.stderr:
    logger.add(_sys.stderr)

_atexit.register(logger.remove)

# === [全球開源原始碼結束] ===

def multiverse_module_hook():
    print('-> 🚀 [本地驗證] 多元宇宙全球開源模組運行正常！')
    return True

if __name__ == '__main__':
    multiverse_module_hook()
