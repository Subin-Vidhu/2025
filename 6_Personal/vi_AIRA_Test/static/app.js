const cardsEl = document.getElementById('cards');
const addBtn = document.getElementById('addBtn');
const refreshBtn = document.getElementById('refreshBtn');
const refreshDataBtn = document.getElementById('refreshDataBtn');
let authToken = window.DASHBOARD_TOKEN || null;
const dlg = document.getElementById('svcDialog');
const form = document.getElementById('svcForm');
const cancelBtn = document.getElementById('cancelBtn');
let services = [];

async function load() {
  try {
    const r = await fetch('/api/services', authToken ? { headers: { 'X-Auth-Token': authToken } } : undefined);
    services = await r.json();
    render();
    updateStats();
  } catch (e) {
    console.error('Load failed', e);
  }
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
  
  targetCard.innerHTML = `
    <h3>${service.name}</h3>
    <div class="host-info">${service.host}${port}</div>
    <div class="status-badge ${service.last_status || 'unknown'}">${(service.last_status || 'unknown').toUpperCase()}</div>
    
    <div class="metrics">
      <div class="metric">
        <div class="metric-value">${service.last_http_status || '---'}</div>
        <div class="metric-label">HTTP Status</div>
      </div>
      <div class="metric">
        <div class="metric-value">${service.last_latency_ms != null ? service.last_latency_ms + 'ms' : '---'}</div>
        <div class="metric-label">Latency</div>
      </div>
    </div>
    
    ${errLine}
    
    <div class="timestamp">Last change: ${service.last_change ? timeago(service.last_change) : '—'}</div>
    <div class="timestamp">Last check: ${service.last_checked ? timeago(service.last_checked) : '—'}</div>
    
    <footer>
      <button data-edit="${service.id}" class="secondary">Edit</button>
      <button data-del="${service.id}" class="danger">Delete</button>
      <button data-check="${service.id}" class="success">Check Now</button>
    </footer>`;
  
  // Update card class for status styling
  targetCard.className = `card ${service.last_status || 'unknown'}`;
}

function render() {
  cardsEl.innerHTML = '';
  services.sort((a, b) => a.name.localeCompare(b.name));
  services.forEach(s => {
    const div = document.createElement('div');
    div.className = `card ${s.last_status || 'unknown'}`;
    
    const errLine = s.last_error ? `<div class="error-text">Error: ${s.last_error}</div>` : '';
    const port = s.port && ![80, 443].includes(s.port) ? `:${s.port}` : '';
    
    div.innerHTML = `
      <h3>${s.name}</h3>
      <div class="host-info">${s.host}${port}</div>
      <div class="status-badge ${s.last_status || 'unknown'}">${(s.last_status || 'unknown').toUpperCase()}</div>
      
      <div class="metrics">
        <div class="metric">
          <div class="metric-value">${s.last_http_status || '---'}</div>
          <div class="metric-label">HTTP Status</div>
        </div>
        <div class="metric">
          <div class="metric-value">${s.last_latency_ms != null ? s.last_latency_ms + 'ms' : '---'}</div>
          <div class="metric-label">Latency</div>
        </div>
      </div>
      
      ${errLine}
      
      <div class="timestamp">Last change: ${s.last_change ? timeago(s.last_change) : '—'}</div>
      <div class="timestamp">Last check: ${s.last_checked ? timeago(s.last_checked) : '—'}</div>
      
      <footer>
        <button data-edit="${s.id}" class="secondary">Edit</button>
        <button data-del="${s.id}" class="danger">Delete</button>
        <button data-check="${s.id}" class="success">Check Now</button>
      </footer>`;
    cardsEl.appendChild(div);
  });
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

form.addEventListener('submit', async e => {
  e.preventDefault();
  const payload = {
    id: form.id.value || form.name.value.trim(),
    name: form.name.value.trim(),
    host: form.host.value.trim(),
    port: form.port.value ? Number(form.port.value) : undefined,
    protocol: form.protocol.value,
    path: form.path.value.trim() || '/',
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

window.triggerCheckNow = async function(){
  await fetch('/api/check', authToken? {headers:{'X-Auth-Token':authToken}}: undefined);
  setTimeout(load, 2000);
};

load();
setInterval(load, 15000);
