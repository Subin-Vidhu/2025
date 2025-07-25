/**
 * Spintly API Reverse Engineering Script
 * Run this in browser console while on Spintly dashboard
 *
 * Instructions:
 * 1. Login to https://smart-access.spintly.com/dashboard/access/history
 * 2. Open DevTools (F12) -> Console tab
 * 3. Paste and run this entire script
 * 4. Follow the prompts and save the output
 */

console.log("🔍 SPINTLY API INVESTIGATION STARTED");
console.log("=====================================");

// Global storage for captured data
window.spintlyInvestigation = {
    networkRequests: [],
    authData: {},
    apiEndpoints: [],
    findings: {}
};

// Step 1: Setup Network Monitoring
console.log("\n📡 STEP 1: Setting up network monitoring...");

// Store original functions
const originalFetch = window.fetch;
const originalXHR = window.XMLHttpRequest;

// Intercept fetch requests
window.fetch = function(...args) {
    const [url, options = {}] = args;
    const requestData = {
        type: 'fetch',
        url: url.toString(),
        method: options.method || 'GET',
        headers: options.headers || {},
        body: options.body,
        timestamp: new Date().toISOString()
    };

    console.log('🌐 FETCH:', requestData.method, requestData.url);
    window.spintlyInvestigation.networkRequests.push(requestData);

    return originalFetch.apply(this, args).then(response => {
        console.log('📥 RESPONSE:', response.status, requestData.url);
        requestData.responseStatus = response.status;
        requestData.responseHeaders = Object.fromEntries(response.headers.entries());
        return response;
    }).catch(error => {
        console.log('❌ ERROR:', error.message, requestData.url);
        requestData.error = error.message;
        throw error;
    });
};

// Intercept XMLHttpRequest
window.XMLHttpRequest = function() {
    const xhr = new originalXHR();
    const originalOpen = xhr.open;
    const originalSend = xhr.send;

    xhr.open = function(method, url, ...rest) {
        this._requestData = {
            type: 'xhr',
            method: method,
            url: url.toString(),
            timestamp: new Date().toISOString(),
            headers: {}
        };
        console.log('🌐 XHR:', method, url);
        return originalOpen.apply(this, [method, url, ...rest]);
    };

    xhr.send = function(data) {
        if (this._requestData) {
            this._requestData.body = data;
            this._requestData.headers = this.getAllResponseHeaders();
            window.spintlyInvestigation.networkRequests.push(this._requestData);
        }
        return originalSend.apply(this, arguments);
    };

    return xhr;
};

console.log("✅ Network monitoring active!");

// Step 2: Extract Authentication Data
console.log("\n🔐 STEP 2: Extracting authentication data...");

// Get cookies
const cookies = {};
document.cookie.split(';').forEach(cookie => {
    const [key, value] = cookie.trim().split('=');
    if (key && value) cookies[key] = value;
});

// Get storage data
const localStorage_data = {};
for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    localStorage_data[key] = localStorage.getItem(key);
}

const sessionStorage_data = {};
for (let i = 0; i < sessionStorage.length; i++) {
    const key = sessionStorage.key(i);
    sessionStorage_data[key] = sessionStorage.getItem(key);
}

// Look for CSRF tokens
const csrfTokens = {};
document.querySelectorAll('meta').forEach(meta => {
    if (meta.name && (meta.name.toLowerCase().includes('csrf') || meta.name.toLowerCase().includes('token'))) {
        csrfTokens[meta.name] = meta.content;
    }
});

// Store auth data
window.spintlyInvestigation.authData = {
    cookies,
    localStorage: localStorage_data,
    sessionStorage: sessionStorage_data,
    csrfTokens,
    currentUrl: window.location.href,
    userAgent: navigator.userAgent,
    timestamp: new Date().toISOString()
};

console.log("🍪 Cookies found:", Object.keys(cookies).length);
console.log("💾 LocalStorage items:", Object.keys(localStorage_data).length);
console.log("🔒 SessionStorage items:", Object.keys(sessionStorage_data).length);
console.log("🛡️ CSRF tokens:", Object.keys(csrfTokens).length);

// Step 3: Analyze Current Page
console.log("\n📄 STEP 3: Analyzing current page...");

// Look for API endpoints in page source
const pageText = document.documentElement.innerHTML;
const apiPatterns = [
    /["']([^"']*\/api\/[^"']*)/gi,
    /["']([^"']*\/access\/[^"']*)/gi,
    /["']([^"']*\/history\/[^"']*)/gi,
    /url["\s]*[:=]["\s]*["']([^"']+)/gi
];

const foundEndpoints = new Set();
apiPatterns.forEach(pattern => {
    const matches = [...pageText.matchAll(pattern)];
    matches.forEach(match => foundEndpoints.add(match[1]));
});

window.spintlyInvestigation.apiEndpoints = Array.from(foundEndpoints);
console.log("🎯 Potential API endpoints found:", foundEndpoints.size);

// Step 4: Extract Table Data (Current Method)
console.log("\n📊 STEP 4: Extracting current table data...");

const tableData = [];
const rows = document.querySelectorAll("table tbody tr");
rows.forEach((row, index) => {
    const cells = row.querySelectorAll("td");
    if (cells.length >= 6) {
        const record = {
            index: index,
            name: cells[0].innerText.trim(),
            datetime: cells[1].innerText.trim(),
            direction: cells[5].innerText.trim(),
            allCells: Array.from(cells).map(cell => cell.innerText.trim())
        };
        tableData.push(record);
    }
});

window.spintlyInvestigation.currentTableData = tableData;
console.log("📋 Table records extracted:", tableData.length);

console.log("\n✅ INITIAL SETUP COMPLETE!");
console.log("==========================================");
console.log("🔄 Now please REFRESH the page or navigate to access history");
console.log("📞 After page loads, run: window.spintlyInvestigation.analyze()");

// Analysis Functions
window.spintlyInvestigation.analyze = function() {
    console.log("\n🔍 ANALYZING CAPTURED DATA");
    console.log("============================");

    const requests = this.networkRequests;
    console.log(`📊 Total requests captured: ${requests.length}`);

    // Filter for API-like requests
    const apiRequests = requests.filter(req =>
        req.url.includes('/api/') ||
        req.url.includes('/access') ||
        req.url.includes('/history') ||
        req.url.includes('.json') ||
        req.method !== 'GET' ||
        req.url.includes('ajax')
    );

    console.log(`🎯 API-like requests: ${apiRequests.length}`);

    // Display each API request
    apiRequests.forEach((req, index) => {
        console.log(`\n--- API Request ${index + 1} ---`);
        console.log(`${req.method} ${req.url}`);
        console.log(`Type: ${req.type}`);
        console.log(`Status: ${req.responseStatus || 'pending'}`);
        if (req.headers && Object.keys(req.headers).length > 0) {
            console.log(`Headers:`, req.headers);
        }
        if (req.body) {
            console.log(`Body:`, req.body);
        }
    });

    this.findings.apiRequests = apiRequests;

    // Generate curl commands
    this.generateCurlCommands();

    // Export all data
    this.exportData();

    return apiRequests;
};

window.spintlyInvestigation.generateCurlCommands = function() {
    console.log("\n🔧 GENERATING CURL COMMANDS");
    console.log("=============================");

    const apiRequests = this.findings.apiRequests || [];
    const curlCommands = [];

    apiRequests.forEach((req, index) => {
        let curl = `curl -X ${req.method} "${req.url}"`;

        // Add common headers
        curl += ` \\\n  -H "User-Agent: ${this.authData.userAgent}"`;
        curl += ` \\\n  -H "Accept: application/json, text/plain, */*"`;
        curl += ` \\\n  -H "Accept-Language: en-US,en;q=0.9"`;

        // Add cookies
        const cookieString = Object.entries(this.authData.cookies)
            .map(([key, value]) => `${key}=${value}`)
            .join('; ');
        if (cookieString) {
            curl += ` \\\n  -H "Cookie: ${cookieString}"`;
        }

        // Add request headers
        if (req.headers && typeof req.headers === 'object') {
            Object.entries(req.headers).forEach(([key, value]) => {
                if (value && !key.toLowerCase().includes('cookie')) {
                    curl += ` \\\n  -H "${key}: ${value}"`;
                }
            });
        }

        // Add body data
        if (req.body) {
            if (typeof req.body === 'string') {
                curl += ` \\\n  -d '${req.body}'`;
            } else {
                curl += ` \\\n  -d '${JSON.stringify(req.body)}'`;
            }
            curl += ` \\\n  -H "Content-Type: application/json"`;
        }

        curlCommands.push(curl);

        console.log(`\n--- CURL Command ${index + 1} ---`);
        console.log(curl);
    });

    this.findings.curlCommands = curlCommands;
    return curlCommands;
};

window.spintlyInvestigation.exportData = function() {
    console.log("\n📤 EXPORTING DATA");
    console.log("==================");

    const exportData = {
        timestamp: new Date().toISOString(),
        authData: this.authData,
        networkRequests: this.networkRequests,
        apiEndpoints: this.apiEndpoints,
        currentTableData: this.currentTableData,
        findings: this.findings
    };

    const jsonString = JSON.stringify(exportData, null, 2);

    console.log("📋 Copy this data and save it to investigation_results.json:");
    console.log("=".repeat(60));
    console.log(jsonString);
    console.log("=".repeat(60));

    // Try to download as file (may not work in all browsers)
    try {
        const blob = new Blob([jsonString], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'spintly_investigation_results.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        console.log("💾 File download initiated!");
    } catch (e) {
        console.log("⚠️ Auto-download failed, please copy the JSON manually");
    }

    return exportData;
};