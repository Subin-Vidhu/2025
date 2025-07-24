/**
 * Spintly Live Time Analyzer - Browser Console Script
 * Replicates the Python time analysis logic in real-time
 * Run this on Spintly dashboard to get instant time analysis
 */

console.log("🕒 SPINTLY LIVE TIME ANALYZER");
console.log("==============================");

// Constants (matching your Python script EXACTLY)
const OFFICE_START = { hour: 7, minute: 30 };
const OFFICE_END = { hour: 19, minute: 30 };
const TARGET_TIME = 8 * 3600 + 30 * 60; // 8 hours 30 minutes in seconds (EXACT match to Python)

// Utility Functions
function parseDateTime(datetimeStr) {
    // Parse "Jul 23, 2025, 07:38:08 AM (IST)" format
    const cleanStr = datetimeStr.replace(" (IST)", "");
    return new Date(cleanStr);
}

function truncateSeconds(date) {
    const newDate = new Date(date);
    newDate.setSeconds(0, 0);
    return newDate;
}

function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function isWithinOfficeHours(date) {
    const hour = date.getHours();
    const minute = date.getMinutes();
    const timeInMinutes = hour * 60 + minute;
    const startInMinutes = OFFICE_START.hour * 60 + OFFICE_START.minute;
    const endInMinutes = OFFICE_END.hour * 60 + OFFICE_END.minute;
    return timeInMinutes >= startInMinutes && timeInMinutes <= endInMinutes;
}

function getOfficeHoursBounds(date) {
    const startTime = new Date(date);
    startTime.setHours(OFFICE_START.hour, OFFICE_START.minute, 0, 0);

    const endTime = new Date(date);
    endTime.setHours(OFFICE_END.hour, OFFICE_END.minute, 0, 0);

    return { start: startTime, end: endTime };
}

// Main Time Calculation Function (EXACT match to your Python logic)
function calculateTimeSpent(records, currentTime = null, truncate = false, analyzedDate = null) {
    let totalTime = 0;
    let totalOfficeHoursTime = 0;
    let totalBreakTime = 0;
    let entryTime = null;
    let firstEntryTime = null;
    let lastExitTime = null;

    console.log(`\n📊 Calculating time for ${records.length} records`);
    console.log(`🕐 Current time: ${currentTime || 'Not provided'}`);
    console.log(`📅 Analyzed date: ${analyzedDate ? analyzedDate.toDateString() : 'Not provided'}`);

    // Convert current_time to remove timezone if present (matching Python)
    if (currentTime && currentTime instanceof Date) {
        currentTime = new Date(currentTime.getTime()); // Remove timezone reference
    }

    // Sort records by datetime
    records.sort((a, b) => a.parsedDateTime - b.parsedDateTime);

    for (const record of records) {
        let dt = truncate ? truncateSeconds(record.parsedDateTime) : record.parsedDateTime;
        dt = new Date(dt.getTime()); // Remove timezone reference (matching Python)

        console.log(`\n🔄 Processing: ${dt.toLocaleString()} - ${record.direction}`);

        if (record.direction.toLowerCase() === 'entry') { // EXACT match to Python
            if (!firstEntryTime) {
                firstEntryTime = dt;
                console.log(`🚪 First entry time set to: ${firstEntryTime.toLocaleString()}`);
            }
            entryTime = dt;
            console.log(`📥 Entry time set to: ${entryTime.toLocaleString()}`);
        }
        else if (record.direction.toLowerCase() === 'exit' && entryTime) { // EXACT match to Python
            const exitTime = dt;
            lastExitTime = exitTime;
            const duration = (exitTime - entryTime) / 1000; // Convert to seconds
            totalTime += duration;

            console.log(`📤 Exit time: ${exitTime.toLocaleString()}`);
            console.log(`⏱️ Duration: ${formatTime(duration)}`);

            // Calculate time during office hours (EXACT match to Python logic)
            const entryTimeWithinOfficeHours = new Date(Math.max(
                entryTime.getTime(),
                new Date(entryTime.getFullYear(), entryTime.getMonth(), entryTime.getDate(),
                        OFFICE_START.hour, OFFICE_START.minute, 0).getTime()
            ));
            const exitTimeWithinOfficeHours = new Date(Math.min(
                exitTime.getTime(),
                new Date(exitTime.getFullYear(), exitTime.getMonth(), exitTime.getDate(),
                        OFFICE_END.hour, OFFICE_END.minute, 0).getTime()
            ));

            if (entryTimeWithinOfficeHours < exitTimeWithinOfficeHours) {
                const officeDuration = (exitTimeWithinOfficeHours - entryTimeWithinOfficeHours) / 1000;
                totalOfficeHoursTime += officeDuration;
                console.log(`🏢 Office hours duration: ${formatTime(officeDuration)}`);
            }

            entryTime = null;
        }
    }

    // Handle open entry without exit or no exit record for the day (EXACT match to Python)
    if (entryTime && currentTime) {
        console.log(`\n🔓 Handling open entry:`);
        console.log(`📥 Entry time: ${entryTime.toLocaleString()}`);
        console.log(`🕐 Current time: ${currentTime.toLocaleString()}`);

        const exitTime = truncate ? truncateSeconds(currentTime) : currentTime;
        lastExitTime = exitTime;
        const duration = (exitTime - entryTime) / 1000;

        if (duration > 0) { // Only add if duration is positive (matching Python)
            totalTime += duration;
            console.log(`⏱️ Duration until current time: ${formatTime(duration)}`);

            // Office hours calculation for current open session (EXACT match to Python)
            const entryTimeWithinOfficeHours = new Date(Math.max(
                entryTime.getTime(),
                new Date(entryTime.getFullYear(), entryTime.getMonth(), entryTime.getDate(),
                        OFFICE_START.hour, OFFICE_START.minute, 0).getTime()
            ));
            const exitTimeWithinOfficeHours = new Date(Math.min(
                exitTime.getTime(),
                new Date(exitTime.getFullYear(), exitTime.getMonth(), exitTime.getDate(),
                        OFFICE_END.hour, OFFICE_END.minute, 0).getTime()
            ));

            if (entryTimeWithinOfficeHours < exitTimeWithinOfficeHours) {
                const officeDuration = (exitTimeWithinOfficeHours - entryTimeWithinOfficeHours) / 1000;
                totalOfficeHoursTime += officeDuration;
                console.log(`🏢 Office hours duration until current time: ${formatTime(officeDuration)}`);
            }
        }
    }
    // Handle case where we have first entry but lost track of entry_time (EXACT match to Python lines 106-126)
    else if (firstEntryTime && currentTime &&
             currentTime.toDateString() === firstEntryTime.toDateString()) { // FIXED: Compare with firstEntryTime.date(), not analyzedDate
        console.log(`\n🔓 Handling first entry without exit:`);
        console.log(`📥 First entry time: ${firstEntryTime.toLocaleString()}`);
        console.log(`🕐 Current time: ${currentTime.toLocaleString()}`);

        const exitTime = truncate ? truncateSeconds(currentTime) : currentTime;
        lastExitTime = exitTime;
        const duration = (exitTime - firstEntryTime) / 1000;

        if (duration > 0) {
            totalTime += duration;
            console.log(`⏱️ Duration until current time: ${formatTime(duration)}`);

            // Office hours calculation for current open session
            const entryTimeWithinOfficeHours = new Date(Math.max(
                firstEntryTime.getTime(),
                new Date(firstEntryTime.getFullYear(), firstEntryTime.getMonth(), firstEntryTime.getDate(),
                        OFFICE_START.hour, OFFICE_START.minute, 0).getTime()
            ));
            const exitTimeWithinOfficeHours = new Date(Math.min(
                exitTime.getTime(),
                new Date(exitTime.getFullYear(), exitTime.getMonth(), exitTime.getDate(),
                        OFFICE_END.hour, OFFICE_END.minute, 0).getTime()
            ));

            if (entryTimeWithinOfficeHours < exitTimeWithinOfficeHours) {
                const officeDuration = (exitTimeWithinOfficeHours - entryTimeWithinOfficeHours) / 1000;
                totalOfficeHoursTime += officeDuration;
                console.log(`🏢 Office hours duration until current time: ${formatTime(officeDuration)}`);
            }
        }
    }

    // Calculate total break time (EXACT match to Python)
    if (firstEntryTime && lastExitTime) {
        const totalDuration = (lastExitTime - firstEntryTime) / 1000;
        totalBreakTime = Math.max(0, totalDuration - totalTime); // Ensure break time is not negative

        console.log(`\n📋 Final calculations:`);
        console.log(`⏰ Total duration: ${formatTime(totalDuration)}`);
        console.log(`🕐 Total time: ${formatTime(totalTime)}`);
        console.log(`🏢 Office hours time: ${formatTime(totalOfficeHoursTime)}`);
        console.log(`☕ Break time: ${formatTime(totalBreakTime)}`);
    }

    return {
        total: totalTime,
        office: totalOfficeHoursTime,
        break: totalBreakTime,
        lastExit: lastExitTime,
        firstEntry: firstEntryTime
    };
}

// Calculate leave time and status (EXACT match to your Python logic)
function calculateLeaveTime(officeTime, currentTime, analyzedDate) {
    const timeLeft = Math.max(TARGET_TIME - officeTime, 0);
    const isCurrentDay = analyzedDate.toDateString() === currentTime.toDateString(); // EXACT match to Python

    // Create difference as timedelta equivalent (EXACT match to Python)
    const differenceSeconds = Math.floor(officeTime - TARGET_TIME);
    const difference = differenceSeconds; // Keep as seconds for now

    if (timeLeft === 0) {
        return {
            leaveTime: currentTime,
            targetMet: true,
            status: "Target met",
            difference: difference
        };
    } else {
        if (isCurrentDay) {
            const leaveTime = new Date(currentTime.getTime() + timeLeft * 1000);
            // Check if leave time is after office hours (EXACT match to Python)
            if (leaveTime.getHours() > 19 || (leaveTime.getHours() === 19 && leaveTime.getMinutes() > 30)) {
                const endOfDay = new Date(analyzedDate);
                endOfDay.setHours(19, 30, 0, 0);
                return {
                    leaveTime: endOfDay,
                    targetMet: false,
                    status: "Leave by end of day",
                    difference: difference
                };
            } else {
                return {
                    leaveTime: leaveTime,
                    targetMet: false,
                    status: `Leave by ${leaveTime.toLocaleTimeString('en-US', { hour12: true })}`, // EXACT match to Python format
                    difference: difference
                };
            }
        } else {
            return {
                leaveTime: currentTime,
                targetMet: false,
                status: "Target not met",
                difference: difference
            };
        }
    }
}

// Generate summary table (matching your Python output format)
function generateSummaryTable(timeSpent, currentTime, analyzedDate, useSeconds = true) {
    const name = timeSpent.name || 'User';
    const times = useSeconds ? timeSpent.withSeconds : timeSpent.withoutSeconds;

    const leaveInfo = calculateLeaveTime(times.office, currentTime, analyzedDate);
    const differenceStr = formatTime(Math.abs(leaveInfo.difference));
    const lastExitStr = times.lastExit ? times.lastExit.toLocaleTimeString() : "No exit";

    const isCurrentDay = analyzedDate.toDateString() === currentTime.toDateString();
    let timeLeftStr, statusColor;

    if (isCurrentDay && !leaveInfo.targetMet) {
        timeLeftStr = `-${differenceStr}`;
        statusColor = '🟡'; // Yellow
    } else if (leaveInfo.targetMet) {
        timeLeftStr = leaveInfo.difference > 0 ? `+${differenceStr}` : "00:00:00";
        statusColor = '🟢'; // Green
    } else {
        timeLeftStr = `-${differenceStr}`;
        statusColor = '🔴'; // Red
    }

    return {
        name: name,
        totalTime: formatTime(times.total),
        officeTime: formatTime(times.office),
        breakTime: formatTime(times.break),
        target: leaveInfo.targetMet ? '✓' : '✗',
        difference: `${statusColor} ${timeLeftStr}`,
        lastExit: lastExitStr,
        status: `${statusColor} ${leaveInfo.status}`
    };
}

// Extract and process table data
function extractAndAnalyzeData() {
    console.log("\n🔍 EXTRACTING TABLE DATA");
    console.log("=========================");

    // Extract table data
    const rows = document.querySelectorAll("table tbody tr");
    const rawData = [];

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
            rawData.push(record);
        }
    });

    console.log(`📊 Extracted ${rawData.length} records`);

    if (rawData.length === 0) {
        console.log("❌ No data found! Make sure you're on the Spintly access history page.");
        return;
    }

    // Process data by date and user
    const processedData = {};
    const currentTime = new Date();

    rawData.forEach(record => {
        if (!record.name || !record.datetime) return;

        const parsedDateTime = parseDateTime(record.datetime);
        const dateKey = parsedDateTime.toDateString();
        const userName = record.name;

        if (!processedData[dateKey]) {
            processedData[dateKey] = {};
        }

        if (!processedData[dateKey][userName]) {
            processedData[dateKey][userName] = [];
        }

        processedData[dateKey][userName].push({
            ...record,
            parsedDateTime: parsedDateTime
        });
    });

    console.log(`📅 Found data for ${Object.keys(processedData).length} dates`);

    // Analyze each date
    const results = {};

    for (const [dateStr, userData] of Object.entries(processedData)) {
        const analyzedDate = new Date(dateStr);
        results[dateStr] = {};

        console.log(`\n📅 ANALYZING ${dateStr}`);
        console.log("=".repeat(50));

        for (const [userName, userRecords] of Object.entries(userData)) {
            console.log(`\n👤 User: ${userName} (${userRecords.length} records)`);

            // FIXED: Always pass current time, let calculateTimeSpent decide (EXACT match to Python)
            console.log(`📅 Analyzed date: ${analyzedDate.toDateString()}`);
            console.log(`� Current time: ${currentTime.toLocaleString()}`);

            // Calculate with seconds - ALWAYS pass currentTime (matching Python)
            const withSeconds = calculateTimeSpent(userRecords, currentTime, false, analyzedDate);
            // Calculate without seconds - ALWAYS pass currentTime (matching Python)
            const withoutSeconds = calculateTimeSpent(userRecords, currentTime, true, analyzedDate);

            results[dateStr][userName] = {
                name: userName,
                withSeconds: withSeconds,
                withoutSeconds: withoutSeconds
            };
        }
    }

    return { results, currentTime };
}

// Display results in table format
function displayResults(analysisResults) {
    const { results, currentTime } = analysisResults;

    console.log("\n🎯 TIME ANALYSIS SUMMARY");
    console.log("========================");

    for (const [dateStr, userData] of Object.entries(results)) {
        const analyzedDate = new Date(dateStr);

        console.log(`\n📅 ${dateStr}`);
        console.log("=".repeat(60));

        // With seconds table
        console.log("\n📊 WITH SECONDS:");
        console.log("┌─────────────┬─────────────┬─────────────┬─────────────┬────────┬─────────────┬─────────────┬─────────────────────┐");
        console.log("│    Name     │ Total Time  │Office Hours │ Break Time  │ Target │ Difference  │  Last Exit  │       Status        │");
        console.log("├─────────────┼─────────────┼─────────────┼─────────────┼────────┼─────────────┼─────────────┼─────────────────────┤");

        for (const [userName, timeData] of Object.entries(userData)) {
            const summary = generateSummaryTable(timeData, currentTime, analyzedDate, true);
            console.log(`│${summary.name.padEnd(13)}│${summary.totalTime.padEnd(13)}│${summary.officeTime.padEnd(13)}│${summary.breakTime.padEnd(13)}│${summary.target.padEnd(8)}│${summary.difference.padEnd(13)}│${summary.lastExit.padEnd(13)}│${summary.status.padEnd(21)}│`);
        }

        console.log("└─────────────┴─────────────┴─────────────┴─────────────┴────────┴─────────────┴─────────────┴─────────────────────┘");

        // Without seconds table
        console.log("\n📊 WITHOUT SECONDS:");
        console.log("┌─────────────┬─────────────┬─────────────┬─────────────┬────────┬─────────────┬─────────────┬─────────────────────┐");
        console.log("│    Name     │ Total Time  │Office Hours │ Break Time  │ Target │ Difference  │  Last Exit  │       Status        │");
        console.log("├─────────────┼─────────────┼─────────────┼─────────────┼────────┼─────────────┼─────────────┼─────────────────────┤");

        for (const [userName, timeData] of Object.entries(userData)) {
            const summary = generateSummaryTable(timeData, currentTime, analyzedDate, false);
            console.log(`│${summary.name.padEnd(13)}│${summary.totalTime.padEnd(13)}│${summary.officeTime.padEnd(13)}│${summary.breakTime.padEnd(13)}│${summary.target.padEnd(8)}│${summary.difference.padEnd(13)}│${summary.lastExit.padEnd(13)}│${summary.status.padEnd(21)}│`);
        }

        console.log("└─────────────┴─────────────┴─────────────┴─────────────┴────────┴─────────────┴─────────────┴─────────────────────┘");
    }

    return results;
}

// CSV Export Function
function exportToCSV(results, currentTime) {
    console.log("\n💾 GENERATING CSV DATA");
    console.log("======================");

    const csvData = [];
    const headers = [
        'Date', 'Name', 'Office Time With Seconds', 'Office Time Without Seconds',
        'Sign With Seconds', 'Difference With Seconds',
        'Sign Without Seconds', 'Difference Without Seconds',
        'Status', 'Message With Seconds', 'Message Without Seconds'
    ];

    csvData.push(headers.join(','));

    for (const [dateStr, userData] of Object.entries(results)) {
        const analyzedDate = new Date(dateStr);

        for (const [userName, timeData] of Object.entries(userData)) {
            const withSecondsInfo = calculateLeaveTime(timeData.withSeconds.office, currentTime, analyzedDate);
            const withoutSecondsInfo = calculateLeaveTime(timeData.withoutSeconds.office, currentTime, analyzedDate);

            // Calculate signs and cap differences at 1 hour for positive values
            const signWithSeconds = withSecondsInfo.difference >= 0 ? '+' : '-';
            const signWithoutSeconds = withoutSecondsInfo.difference >= 0 ? '+' : '-';

            let diffWithSeconds = Math.abs(withSecondsInfo.difference);
            let diffWithoutSeconds = Math.abs(withoutSecondsInfo.difference);
            let msgWithSeconds = '';
            let msgWithoutSeconds = '';

            // Cap at 1 hour for positive differences
            if (signWithSeconds === '+' && diffWithSeconds > 3600) {
                diffWithSeconds = 3600;
                msgWithSeconds = 'Only 1 hour/day can be considered extra';
            }
            if (signWithoutSeconds === '+' && diffWithoutSeconds > 3600) {
                diffWithoutSeconds = 3600;
                msgWithoutSeconds = 'Only 1 hour/day can be considered extra';
            }

            const row = [
                analyzedDate.toISOString().split('T')[0], // Date
                userName,
                formatTime(timeData.withSeconds.office),
                formatTime(timeData.withoutSeconds.office),
                signWithSeconds,
                formatTime(diffWithSeconds),
                signWithoutSeconds,
                formatTime(diffWithoutSeconds),
                withSecondsInfo.status,
                msgWithSeconds,
                msgWithoutSeconds
            ];

            csvData.push(row.join(','));
        }
    }

    const csvContent = csvData.join('\n');

    console.log("📋 CSV Content:");
    console.log(csvContent);

    // Try to download CSV file
    try {
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `spintly_time_analysis_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        console.log("💾 CSV file download initiated!");
    } catch (e) {
        console.log("⚠️ Auto-download failed, please copy the CSV content manually");
    }

    return csvContent;
}

// Update FastAPI function
async function updateFastAPI(results) {
    console.log("\n🚀 UPDATING FASTAPI APP");
    console.log("========================");

    try {
        // Convert results to the format expected by FastAPI
        const tableData = [];

        for (const [dateStr, userData] of Object.entries(results)) {
            for (const [userName, timeData] of Object.entries(userData)) {
                // Add records from the original data
                // This would need to be extracted from the original table data
                // For now, we'll create a simplified version
            }
        }

        const response = await fetch('http://localhost:8000/api/update-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                table_data: tableData,
                time_analysis: results
            })
        });

        if (response.ok) {
            const result = await response.json();
            console.log("✅ FastAPI updated successfully!");
            console.log(`📈 ${result.message}`);
        } else {
            console.log("❌ Failed to update FastAPI");
        }
    } catch (error) {
        console.log(`⚠️ FastAPI update failed: ${error.message}`);
        console.log("Make sure FastAPI is running at http://localhost:8000");
    }
}

// Main execution function
function runSpintlyTimeAnalysis() {
    console.log("\n🚀 STARTING SPINTLY TIME ANALYSIS");
    console.log("==================================");

    try {
        // Extract and analyze data
        const analysisResults = extractAndAnalyzeData();

        if (!analysisResults) {
            return;
        }

        // Display results
        const results = displayResults(analysisResults);

        // Export to CSV
        const csvContent = exportToCSV(results, analysisResults.currentTime);

        // Update FastAPI (optional)
        updateFastAPI(results);

        console.log("\n🎉 ANALYSIS COMPLETE!");
        console.log("=====================");
        console.log("✅ Time analysis displayed above");
        console.log("✅ CSV data generated and downloaded");
        console.log("✅ FastAPI update attempted");

        // Store results globally for further use
        window.spintlyTimeAnalysis = {
            results: results,
            csvContent: csvContent,
            currentTime: analysisResults.currentTime
        };

        return results;

    } catch (error) {
        console.error("❌ Error during analysis:", error);
        console.log("Make sure you're on the Spintly access history page with data loaded.");
    }
}

// Auto-run the analysis
console.log("🔄 Running automatic analysis...");
runSpintlyTimeAnalysis();