// Authentication variables
const SECRET_KEY = 'PROTOS25';
let isAuthenticated = false;

// Check if user is already authenticated
window.addEventListener('DOMContentLoaded', function() {
  const savedAuth = sessionStorage.getItem('pacsAuth');
  if (savedAuth === SECRET_KEY) {
    showDashboard();
  } else {
    showAuthScreen();
  }
});

// Authentication functions
function showAuthScreen() {
  document.getElementById('authScreen').style.display = 'flex';
  document.getElementById('mainDashboard').style.display = 'none';
  isAuthenticated = false;
}

function showDashboard() {
  document.getElementById('authScreen').style.display = 'none';
  document.getElementById('mainDashboard').style.display = 'block';
  isAuthenticated = true;
  // Initialize dashboard
  load();
  setupEventListeners();
}

function logout() {
  sessionStorage.removeItem('pacsAuth');
  showAuthScreen();
  // Clear any intervals/timeouts
  if (window.refreshInterval) {
    clearInterval(window.refreshInterval);
  }
}

// Handle authentication form
document.getElementById('authForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const enteredKey = document.getElementById('secretKey').value;
  const errorDiv = document.getElementById('authError');
  
  if (enteredKey === SECRET_KEY) {
    sessionStorage.setItem('pacsAuth', SECRET_KEY);
    showDashboard();
    errorDiv.style.display = 'none';
  } else {
    errorDiv.style.display = 'block';
    document.getElementById('secretKey').value = '';
    document.getElementById('secretKey').focus();
  }
});

// Main application variables
const cardsEl = document.getElementById('cards');
const addBtn = document.getElementById('addBtn');
const refreshBtn = document.getElementById('refreshBtn');
const refreshDataBtn = document.getElementById('refreshDataBtn');
let authToken = window.DASHBOARD_TOKEN || null;
const dlg = document.getElementById('svcDialog');
const form = document.getElementById('svcForm');
const cancelBtn = document.getElementById('cancelBtn');
let services = [];
let filterMode = 'all';
let searchTerm = '';
let compact = false;
const latencyWarn = 250; // ms threshold
const latencyCritical = 800;

async function load() {
  if (!isAuthenticated) return;
  try {
    const r = await fetch('/api/services', authToken ? { headers: { 'X-Auth-Token': authToken } } : undefined);
    services = await r.json();
    render();
    updateStats();
  } catch (e) {
    console.error('Load failed', e);
  }
}

function classifyLatency(ms){
  if (ms == null) return '';
  if (ms >= latencyCritical) return 'critical';
  if (ms >= latencyWarn) return 'warn';
  return 'ok';
}

function updateStats() {
  const total = services.length;
  const up = services.filter(s => s.last_status === 'up').length;
  const down = services.filter(s => s.last_status === 'down').length;
  const latencies = services.filter(s => s.last_latency_ms > 0).map(s => s.last_latency_ms);
  const avgLatency = latencies.length ? Math.round(latencies.reduce((a, b) => a + b, 0) / latencies.length) : 0;

  document.getElementById('totalServices').textContent = total;
  document.getElementById('upServices').textContent = up;
  document.getElementById('downServices').textContent = down;
  document.getElementById('avgLatency').textContent = avgLatency + 'ms';
}

function updateSingleCard(id, service) {
  // Find the specific card element
  const cards = document.querySelectorAll('.card');
  let targetCard = null;
  
  for (const card of cards) {
    const editBtn = card.querySelector(`[data-edit="${id}"]`);
    if (editBtn) {
      targetCard = card;
      break;
    }
  }
  
  if (!targetCard) return;
  
  // Update the card content
  const errLine = service.last_error ? `<div class="error-text">Error: ${service.last_error}</div>` : '';
  const port = service.port && ![80, 443].includes(service.port) ? `:${service.port}` : '';
  
  const latencyClass = classifyLatency(service.last_latency_ms);
  const envBadge = service.env ? `<span class="env-badge">${service.env.toUpperCase()}</span>` : '';
  targetCard.innerHTML = `
    <div class="card-header-row">
      <div class="left-head">
        <div class="svc-name">${service.name}</div>
        <div class="host-line">${service.host}${port}</div>
      </div>
      ${envBadge}
    </div>
    <div class="status-badge ${service.last_status || 'unknown'}">${(service.last_status || 'unknown').toUpperCase()}</div>
    <div class="metrics">
      <div class="metric">
        <div class="metric-value">${service.last_http_status || '---'}</div>
        <div class="metric-label">HTTP</div>
      </div>
      <div class="metric latency ${latencyClass}">
        <div class="metric-value">${service.last_latency_ms != null ? service.last_latency_ms + 'ms' : '---'}</div>
        <div class="metric-label">LAT</div>
        <canvas class="sparkline" data-spark="${service.id}"></canvas>
      </div>
    </div>
    ${errLine}
    <div class="timestamp">📅 Changed: ${service.last_change ? timeago(service.last_change) : '—'} • ✅ Checked: ${service.last_checked ? timeago(service.last_checked) : '—'}</div>
    <footer>
      <button data-edit="${service.id}" class="secondary">Edit</button>
      <button data-del="${service.id}" class="danger">Delete</button>
      <button data-check="${service.id}" class="success">Check</button>
    </footer>`;
  
  // Update card class for status styling
  targetCard.className = `card ${service.last_status || 'unknown'}`;
}

function render() {
  cardsEl.innerHTML = '';
  const term = searchTerm.toLowerCase();
  services.sort((a,b)=> a.name.localeCompare(b.name));
  const now = Date.now();
  const filtered = services.filter(s => {
    if (term && !(`${s.name} ${s.host}`.toLowerCase().includes(term))) return false;
    if (filterMode === 'up' && s.last_status !== 'up') return false;
    if (filterMode === 'down' && s.last_status !== 'down') return false;
    if (filterMode === 'unknown' && s.last_status !== 'unknown') return false;
    if (filterMode === 'slow' && !(s.last_latency_ms >= latencyWarn)) return false;
    if (filterMode === 'changed') {
      if (!s.last_change) return false;
      const diff = now - new Date(s.last_change).getTime();
      if (diff > 10*60*1000) return false; // 10m window
    }
    return true;
  });
  filtered.forEach(s => {
    const div = document.createElement('div');
    div.className = `card ${s.last_status || 'unknown'}`;
    const errLine = s.last_error ? `<div class="error-text">Error: ${s.last_error}</div>` : '';
    const port = s.port && ![80, 443].includes(s.port) ? `:${s.port}` : '';
    const latencyClass = classifyLatency(s.last_latency_ms);
    const envBadge = s.env ? `<span class="env-badge">${s.env.toUpperCase()}</span>` : '';
    div.innerHTML = `
      <div class="card-header-row">
        <div class="left-head">
          <div class="svc-name">${s.name}</div>
          <div class="host-line">${s.host}${port}</div>
        </div>
        ${envBadge}
      </div>
      <div class="status-badge ${s.last_status || 'unknown'}">${(s.last_status || 'unknown').toUpperCase()}</div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-value">${s.last_http_status || '---'}</div>
          <div class="metric-label">HTTP</div>
        </div>
        <div class="metric latency ${latencyClass}">
          <div class="metric-value">${s.last_latency_ms != null ? s.last_latency_ms + 'ms' : '---'}</div>
          <div class="metric-label">LAT</div>
          <canvas class="sparkline" data-spark="${s.id}"></canvas>
        </div>
      </div>
      ${errLine}
      <div class="timestamp">📅 Changed: ${s.last_change ? timeago(s.last_change) : '—'} • ✅ Checked: ${s.last_checked ? timeago(s.last_checked) : '—'}</div>
      <footer>
        <button data-edit="${s.id}" class="secondary">Edit</button>
        <button data-del="${s.id}" class="danger">Delete</button>
        <button data-check="${s.id}" class="success">Check</button>
      </footer>`;
    cardsEl.appendChild(div);
  });
  // after mount fetch history for visible services for sparklines
  filtered.forEach(s=> loadHistorySpark(s.id));
}

async function loadHistorySpark(id){
  try {
    const r = await fetch('/api/history/' + id);
    if(!r.ok) return;
    const data = await r.json();
    const canvas = document.querySelector(`canvas[data-spark="${id}"]`);
    if(!canvas) return;
    const values = data.latency_ms || [];
    drawSparkline(canvas, values);
  } catch(e){ console.warn('spark failed', e); }
}

function drawSparkline(canvas, values){
  if(!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width = canvas.clientWidth || 80;
  const h = canvas.height = canvas.clientHeight || 14;
  ctx.clearRect(0,0,w,h);
  if(!values.length) return;
  const max = Math.max(...values);
  const min = Math.min(...values);
  const span = max - min || 1;
  ctx.strokeStyle = '#00b5e6';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  values.forEach((v,i)=>{
    const x = (i/(values.length-1))* (w-2) +1;
    const y = h - ((v-min)/span)* (h-2) -1;
    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  });
  ctx.stroke();
}

function timeago(ts){
  try {
    const d = new Date(ts);
    const diff = (Date.now() - d.getTime()) / 1000;
    if (diff < 60) return `${Math.floor(diff)}s ago`;
    if (diff < 3600) return `${Math.floor(diff/60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff/3600)}h ago`;
    return d.toLocaleString();
  } catch { return ts; }
}

cardsEl.addEventListener('click', e => {
  const edit = e.target.dataset.edit;
  const del = e.target.dataset.del;
  const check = e.target.dataset.check;
  if (edit) openEdit(edit);
  if (del) remove(del);
  if (check) checkSingle(check);
});

function openEdit(id){
  const svc = services.find(s => s.id === id) || {};
  form.id.value = svc.id || '';
  form.name.value = svc.name || '';
  form.host.value = svc.host || '';
  form.port.value = svc.port || '';
  form.protocol.value = svc.protocol || 'https';
  form.path.value = svc.path || '/';
  form.env.value = svc.env || '';
  form.active.checked = svc.active !== false;
  document.getElementById('formTitle').textContent = svc.id ? 'Edit Service' : 'New Service';
  dlg.showModal();
}

async function remove(id){
  if (!confirm('Delete service?')) return;
  await fetch('/api/services/' + id, { method: 'DELETE' });
  await load();
}

async function checkSingle(id){
  const button = document.querySelector(`[data-check="${id}"]`);
  const card = button.closest('.card');
  const originalText = button.textContent;
  
  try {
    // Update button and card state
    button.textContent = 'Checking...';
    button.disabled = true;
    card.classList.add('checking');
    
    // Trigger the check
    await fetch('/api/check/' + id, authToken ? { headers: { 'X-Auth-Token': authToken } } : undefined);
    
    // Wait for check to complete, then fetch only this service's updated data
    setTimeout(async () => {
      try {
        const r = await fetch(`/api/services/${id}`, authToken ? { headers: { 'X-Auth-Token': authToken } } : undefined);
        
        if (r.ok) {
          const updatedService = await r.json();
          
          // Update only this service in our local array
          const index = services.findIndex(s => s.id === id);
          if (index !== -1) {
            services[index] = updatedService;
            // Re-render only this specific card
            updateSingleCard(id, updatedService);
            updateStats();
          }
        } else {
          console.error('Service not found after check');
        }
      } catch (e) {
        console.error('Failed to update single service', e);
      }
      
      // Restore button and remove checking state
      card.classList.remove('checking');
      button.textContent = originalText;
      button.disabled = false;
    }, 2500);
    
  } catch (e) {
    console.error('Single check failed', e);
    card.classList.remove('checking');
    button.textContent = originalText;
    button.disabled = false;
  }
}

// Setup event listeners (called after authentication)
function setupEventListeners() {
  // Form submission
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const payload = {
      id: form.id.value || form.name.value.trim(),
      name: form.name.value.trim(),
      host: form.host.value.trim(),
      port: form.port.value ? Number(form.port.value) : undefined,
      protocol: form.protocol.value,
      path: form.path.value.trim() || '/',
    env: form.env.value.trim(),
      active: form.active.checked
    };
    await fetch('/api/services', {
      method: 'POST',
      headers: Object.assign({'Content-Type': 'application/json'}, authToken? {'X-Auth-Token':authToken}: {}),
      body: JSON.stringify(payload)
    });
    dlg.close();
    await load();
  });

  cancelBtn.onclick = () => dlg.close();
  addBtn.onclick = () => openEdit('');

  // Refresh Data: Just reload current data from server (fast)
  refreshDataBtn.onclick = () => load();

  // Check All: Trigger new health checks for all services (slow)
  refreshBtn.onclick = async () => {
    refreshBtn.textContent = '🔄 Checking...';
    refreshBtn.disabled = true;
    try {
      await triggerCheckNow();
    } finally {
      refreshBtn.textContent = '🔄 Check All';
      refreshBtn.disabled = false;
    }
  };

  // Filtering & search
  document.addEventListener('click', e=>{
    if(e.target.classList && e.target.classList.contains('filt')){
      document.querySelectorAll('.filt').forEach(b=>b.classList.remove('active'));
      e.target.classList.add('active');
      filterMode = e.target.dataset.filter;
      render();
    }
  });
  
  const searchInput = document.getElementById('searchInput');
  if(searchInput){
    searchInput.addEventListener('input', ()=>{ searchTerm = searchInput.value; render(); });
  }
  
  const compactToggle = document.getElementById('compactToggle');
  if(compactToggle){
    compactToggle.addEventListener('change', ()=>{ compact = compactToggle.checked; document.body.classList.toggle('compact', compact); });
  }

  // Keyboard shortcuts
  document.addEventListener('keydown', e=>{
    if(!isAuthenticated) return; // Don't handle shortcuts if not authenticated
    if(e.ctrlKey && e.key.toLowerCase()==='k'){ e.preventDefault(); searchInput && searchInput.focus(); }
    else if(e.key==='r'){ refreshDataBtn.click(); }
    else if(e.key==='a'){ refreshBtn.click(); }
    else if(e.key==='n'){ addBtn.click(); }
    else if(e.key==='u'){ setFilterKey('up'); }
    else if(e.key==='d'){ setFilterKey('down'); }
    else if(e.key==='c'){ setFilterKey('changed'); }
    else if(e.key==='l'){ setFilterKey('slow'); }
    else if(e.key==='?'){ setFilterKey('unknown'); }
  });

  // Start auto-refresh
  window.refreshInterval = setInterval(load, 15000);
}

window.triggerCheckNow = async function(){
  await fetch('/api/check', authToken? {headers:{'X-Auth-Token':authToken}}: undefined);
  setTimeout(load, 2000);
};

function setFilterKey(mode){
  const btn = document.querySelector(`.filt[data-filter="${mode}"]`);
  if(btn){ btn.click(); }
}

// Initialization is now handled by the authentication system
