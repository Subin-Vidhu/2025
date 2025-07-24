/**
 * Spintly Data Updater Script
 * Run this in browser console on Spintly dashboard to update your FastAPI app
 */

console.log("🔄 SPINTLY DATA UPDATER");
console.log("======================");

// Extract table data
const rows = document.querySelectorAll("table tbody tr");
const tableData = [];

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

console.log(`📊 Extracted ${tableData.length} records`);

// Send data to FastAPI app
async function updateFastAPIData() {
    try {
        const response = await fetch('http://localhost:8000/api/update-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                table_data: tableData
            })
        });

        if (response.ok) {
            const result = await response.json();
            console.log("✅ SUCCESS! Data updated in FastAPI app");
            console.log(`📈 ${result.message}`);
            console.log(`🕒 Last updated: ${result.last_updated}`);

            // Show success message
            alert(`✅ Success! Updated FastAPI app with ${tableData.length} records.\n\nCheck your dashboard at http://localhost:8000`);
        } else {
            const error = await response.text();
            console.error("❌ Error updating data:", error);
            alert(`❌ Error updating data: ${error}`);
        }
    } catch (error) {
        console.error("❌ Network error:", error);
        alert(`❌ Network error: ${error.message}\n\nMake sure your FastAPI app is running at http://localhost:8000`);
    }
}

// Update the data
updateFastAPIData();

// Also log the data for manual inspection
console.log("📋 Extracted data:", tableData);