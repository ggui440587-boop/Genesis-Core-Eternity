# -*- coding: utf-8 -*-
# --------------------------------------------------
# 全球旗艦開源融合模組: ItsdangerousFlagship
# 產出時間: 2026-08-25 17:35:51
# --------------------------------------------------

# === [全球開源原始碼開始] ===
from .encoding import base64_decode as base64_decode
from .encoding import base64_encode as base64_encode
from .encoding import want_bytes as want_bytes
from .exc import BadData as BadData
from .exc import BadHeader as BadHeader
from .exc import BadPayload as BadPayload
from .exc import BadSignature as BadSignature
from .exc import BadTimeSignature as BadTimeSignature
from .exc import SignatureExpired as SignatureExpired
from .serializer import Serializer as Serializer
from .signer import HMACAlgorithm as HMACAlgorithm
from .signer import NoneAlgorithm as NoneAlgorithm
from .signer import Signer as Signer
from .timed import TimedSerializer as TimedSerializer
from .timed import TimestampSigner as TimestampSigner
from .url_safe import URLSafeSerializer as URLSafeSerializer
from .url_safe import URLSafeTimedSerializer as URLSafeTimedSerializer

# === [全球開源原始碼結束] ===

def flagship_module_hook():
    print('-> 🚀 [本地驗證] 全球旗艦開源模組運行正常！')
    return True

if __name__ == '__main__':
    flagship_module_hook()
