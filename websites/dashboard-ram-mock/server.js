const express = require('express');
const path = require('path');
const os = require('os');

const app = express();
const PORT = process.env.PORT ? Number(process.env.PORT) : 3006;

function readSystemStats() {
  const totalMem = os.totalmem();
  const freeMem = os.freemem();
  const usedMem = totalMem - freeMem;
  const memUtil = totalMem > 0 ? (usedMem / totalMem) * 100 : 0;
  const loadAvg = os.loadavg?.()[0] ?? 0;
  const cpuCount = os.cpus()?.length || 1;
  const cpuPercent = Math.max(0, Math.min(100, (loadAvg / cpuCount) * 100));

  return {
    timestamp: new Date().toISOString(),
    memory: {
      totalBytes: totalMem,
      usedBytes: usedMem,
      freeBytes: freeMem,
      usedPercent: memUtil,
    },
    cpu: {
      loadAverage1m: loadAvg,
      cores: cpuCount,
      usagePercent: cpuPercent,
    },
  };
}

app.use(express.static(path.join(__dirname, 'public')));
app.get('/healthz', (req, res) => res.json({ ok: true, service: 'ram-dashboard' }));
app.get('/api/system-stats', (req, res) => res.json(readSystemStats()));

app.listen(PORT, '0.0.0.0', () => {
  console.log(`[ram-dashboard] http://127.0.0.1:${PORT}`);
});
