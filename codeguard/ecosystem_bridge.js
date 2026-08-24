// ==============================================================
// Ecosystem Bridge - Node.js 跨語言專案橋接與設定讀取模組
// ==============================================================

const fs = require('fs');
const path = 'ecosystem_config.json';

function loadPythonEcosystemConfig() {
    console.log("==============================================================");
    console.log(" 🌐 [JS 跨語言模組] 正在嘗試讀取 Genesis-Core-Eternity 設定...");
    console.log("==============================================================");

    try {
        if (fs.existsSync(path)) {
            const rawData = fs.readFileSync(path, 'utf8');
            const config = JSON.parse(rawData);
            console.log(`-> 🟢 [讀取成功] 專案名稱: ${config.app_name}`);
            console.log(`-> 🟢 [讀取成功] 運行環境: ${config.environment}`);
            console.log(`-> 🟢 [讀取成功] 除錯模式: ${config.debug_mode}`);
        } else {
            console.log("-> ⚠️ [檔案不存在] 找不到 Python 建立的設定檔，請先執行 Python 初始化。");
        }
    } catch (error) {
        console.error("-> 🔴 [讀取錯誤] 解析設定檔時發生例外:", error.message);
    }
    console.log("==============================================================");
}

// 執行橋接測試
loadPythonEcosystemConfig();

