# server.py
import asyncio
import http.server
import json
import threading
from core import AutonomousNode

node = AutonomousNode("TERMUX-NODE-01")

HTML_PAGE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>Autonomous Mesh Visualizer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #030712; color: #38bdf8; font-family: monospace; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
        header { padding: 12px 20px; border-bottom: 1px solid #1e293b; display: flex; justify-content: space-between; align-items: center; background: #0b0f19; }
        .node-id { font-size: 14px; color: #94a3b8; letter-spacing: 1px; }
        .grid-container { flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 10px; padding: 10px; }
        .panel { background: #0b0f19; border: 1px solid #1e293b; border-radius: 6px; padding: 15px; display: flex; flex-direction: column; overflow: hidden; position: relative; }
        .panel-title { font-size: 12px; color: #64748b; text-transform: uppercase; margin-bottom: 10px; }
        canvas { width: 100%; height: 100%; display: block; }
        .metrics-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; flex: 1; align-content: center; }
        .metric-box { background: #111827; padding: 12px; border-radius: 4px; border-left: 3px solid #38bdf8; }
        .metric-val { font-size: 24px; color: #fff; margin-top: 4px; font-weight: bold; }
        .status-indicator { display: flex; align-items: center; gap: 8px; font-size: 16px; margin-top: auto; }
        .dot { width: 10px; height: 10px; border-radius: 50%; background: #4ade80; box-shadow: 0 0 8px #4ade80; }
        .log-stream { flex: 1; overflow: hidden; display: flex; flex-direction: column; justify-content: flex-end; font-size: 12px; gap: 4px; }
        .log-line { opacity: 0.8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .log-safe { color: #4ade80; }
        .log-alert { color: #f87171; }
    </style>
</head>
<body>
    <header>
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 8px; height: 8px; background: #4ade80; border-radius: 50%;"></div>
            <span style="font-weight: bold; color: #fff; letter-spacing: 2px;">CORE MESH</span>
        </div>
        <div class="node-id" id="header-id">NODE-01</div>
    </header>
    <div class="grid-container">
        <div class="panel">
            <div class="panel-title">Neural Activity Matrix</div>
            <canvas id="neuralCanvas"></canvas>
        </div>
        <div class="panel">
            <div class="panel-title">Core Metrics</div>
            <div class="metrics-grid">
                <div class="metric-box">
                    <div style="color: #94a3b8; font-size: 10px;">CYCLE</div>
                    <div class="metric-val" id="m-cycle">0</div>
                </div>
                <div class="metric-box" style="border-left-color: #4ade80;">
                    <div style="color: #94a3b8; font-size: 10px;">TASKS</div>
                    <div class="metric-val" id="m-tasks">0</div>
                </div>
            </div>
            <div class="status-indicator">
                <div class="dot"></div>
                <span id="m-status" style="color: #fff;">SYNCING</span>
            </div>
        </div>
        <div class="panel">
            <div class="panel-title">Entropy & Waveform</div>
            <canvas id="waveCanvas"></canvas>
        </div>
        <div class="panel">
            <div class="panel-title">Guardrail Intercept Stream</div>
            <div class="log-stream" id="logStream">
                <div class="log-line log-safe">[INIT] Mesh link established.</div>
            </div>
        </div>
    </div>
    <script>
        function setupCanvas(canvas) {
            const ctx = canvas.getContext('2d');
            canvas.width = canvas.parentElement.clientWidth - 30;
            canvas.height = canvas.parentElement.clientHeight - 40;
            return ctx;
        }
        const nCanvas = document.getElementById('neuralCanvas');
        const nCtx = setupCanvas(nCanvas);
        const wCanvas = document.getElementById('waveCanvas');
        const wCtx = setupCanvas(wCanvas);

        let particles = Array.from({ length: 20 }, () => ({
            x: Math.random() * nCanvas.width, y: Math.random() * nCanvas.height,
            vx: (Math.random() - 0.5) * 1.5, vy: (Math.random() - 0.5) * 1.5, radius: Math.random() * 2 + 1
        }));

        function drawNeural() {
            nCtx.clearRect(0, 0, nCanvas.width, nCanvas.height);
            nCtx.fillStyle = '#38bdf8';
            particles.forEach((p, i) => {
                p.x += p.vx; p.y += p.vy;
                if (p.x < 0 || p.x > nCanvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > nCanvas.height) p.vy *= -1;
                nCtx.beginPath(); nCtx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); nCtx.fill();
                for (let j = i + 1; j < particles.length; j++) {
                    let p2 = particles[j], dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                    if (dist < 60) {
                        nCtx.strokeStyle = `rgba(56, 189, 248, ${1 - dist / 60})`;
                        nCtx.lineWidth = 0.5; nCtx.beginPath(); nCtx.moveTo(p.x, p.y); nCtx.lineTo(p2.x, p2.y); nCtx.stroke();
                    }
                }
            });
            requestAnimationFrame(drawNeural);
        }
        drawNeural();

        let waveOffset = 0;
        function drawWave() {
            wCtx.clearRect(0, 0, wCanvas.width, wCanvas.height);
            wCtx.strokeStyle = '#38bdf8'; wCtx.lineWidth = 1.5; wCtx.beginPath();
            for (let x = 0; x < wCanvas.width; x++) {
                let y = wCanvas.height / 2 + Math.sin(x * 0.03 + waveOffset) * 12;
                if (x === 0) wCtx.moveTo(x, y); else wCtx.lineTo(x, y);
            }
            wCtx.stroke(); waveOffset += 0.05;
            requestAnimationFrame(drawWave);
        }
        drawWave();

        async function fetchState() {
            try {
                let res = await fetch('/status');
                let data = await res.json();
                document.getElementById('header-id').innerText = data.node_id;
                document.getElementById('m-cycle').innerText = data.state.current_cycle;
                document.getElementById('m-tasks').innerText = data.state.tasks_done;
                document.getElementById('m-status').innerText = data.state.status.toUpperCase();
                let stream = document.getElementById('logStream');
                if (data.state.logs && data.state.logs.length > 0) {
                    let html = '';
                    data.state.logs.slice(0, 4).reverse().forEach(log => {
                        let isAlert = log.includes('攔截') || log.includes('拒絕');
                        html += `<div class="log-line ${isAlert ? 'log-alert' : 'log-safe'}">${log}</div>`;
                    });
                    stream.innerHTML = html;
                }
            } catch (e) {}
        }
        setInterval(fetchState, 500);
    </script>
</body>
</html>
"""


class DashboardHandler(http.server.BaseHTTPRequestHandler):

  def do_GET(self):
    if self.path == "/status":
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      self.wfile.write(
          json.dumps({"node_id": node.node_id, "state": node.state}).encode(
              "utf-8"
          )
      )
    else:
      self.send_response(200)
      self.send_header("Content-type", "text/html; charset=utf-8")
      self.end_headers()
      self.wfile.write(HTML_PAGE.encode("utf-8"))

  def log_message(self, format, *args):
    pass


if __name__ == "__main__":
  threading.Thread(
      target=lambda: asyncio.run(node.run_mind_loop()), daemon=True
  ).start()
  server = http.server.HTTPServer(("0.0.0.0", 8081), DashboardHandler)
  print("🌐 視覺化動態面板已啟動！請在瀏覽器打開：http://127.0.0.1:8080")
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    node.is_active = False

