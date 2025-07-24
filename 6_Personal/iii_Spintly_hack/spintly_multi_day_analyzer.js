/**
 * Spintly Multi-Day Time Analyzer
 * Analyzes multiple days of data and generates comprehensive reports
 * Run this on Spintly dashboard to analyze date ranges
 */

console.log("📅 SPINTLY MULTI-DAY TIME ANALYZER");
console.log("===================================");

// Constants
const OFFICE_START = { hour: 7, minute: 30 };
const OFFICE_END = { hour: 19, minute: 30 };
const TARGET_TIME = 8 * 3600 + 30 * 60; // 8 hours 30 minutes in seconds (EXACT match to Python)

// Utility functions (copied from main analyzer)
function parseDateTime(datetimeStr) {
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

function getOfficeHoursBounds(date) {
    const startTime = new Date(date);
    startTime.setHours(OFFICE_START.hour, OFFICE_START.minute, 0, 0);

    const endTime = new Date(date);
    endTime.setHours(OFFICE_END.hour, OFFICE_END.minute, 0, 0);

    return { start: startTime, end: endTime };
}

function calculateTimeSpent(records, currentTime = null, truncate = false) {
    let totalTime = 0;
    let totalOfficeHoursTime = 0;
    let totalBreakTime = 0;
    let entryTime = null;
    let firstEntryTime = null;
    let lastExitTime = null;

    records.sort((a, b) => a.parsedDateTime - b.parsedDateTime);

    for (const record of records) {
        let dt = truncate ? truncateSeconds(record.parsedDateTime) : record.parsedDateTime;

        if (record.direction.toLowerCase().includes('entry')) {
            if (!firstEntryTime) {
                firstEntryTime = dt;
            }
            entryTime = dt;
        }
        else if (record.direction.toLowerCase().includes('exit') && entryTime) {
            const exitTime = dt;
            lastExitTime = exitTime;
            const duration = (exitTime - entryTime) / 1000;
            totalTime += duration;

            const officeBounds = getOfficeHoursBounds(entryTime);
            const entryWithinOfficeHours = new Date(Math.max(entryTime, officeBounds.start));
            const exitWithinOfficeHours = new Date(Math.min(exitTime, officeBounds.end));

            if (entryWithinOfficeHours < exitWithinOfficeHours) {
                const officeDuration = (exitWithinOfficeHours - entryWithinOfficeHours) / 1000;
                totalOfficeHoursTime += officeDuration;
            }

            entryTime = null;
        }
    }

    if (entryTime && currentTime) {
        const exitTime = truncate ? truncateSeconds(currentTime) : currentTime;
        lastExitTime = exitTime;
        const duration = (exitTime - entryTime) / 1000;

        if (duration > 0) {
            totalTime += duration;

            const officeBounds = getOfficeHoursBounds(entryTime);
            const entryWithinOfficeHours = new Date(Math.max(entryTime, officeBounds.start));
            const exitWithinOfficeHours = new Date(Math.min(exitTime, officeBounds.end));

            if (entryWithinOfficeHours < exitWithinOfficeHours) {
                const officeDuration = (exitWithinOfficeHours - entryWithinOfficeHours) / 1000;
                totalOfficeHoursTime += officeDuration;
            }
        }
    }
    // Handle case where we have first entry but lost track of entry_time (EXACT match to Python lines 106-126)
    else if (firstEntryTime && currentTime &&
             currentTime.toDateString() === firstEntryTime.toDateString()) {
        const exitTime = truncate ? truncateSeconds(currentTime) : currentTime;
        lastExitTime = exitTime;
        const duration = (exitTime - firstEntryTime) / 1000;

        if (duration > 0) {
            totalTime += duration;

            const officeBounds = getOfficeHoursBounds(firstEntryTime);
            const entryWithinOfficeHours = new Date(Math.max(firstEntryTime, officeBounds.start));
            const exitWithinOfficeHours = new Date(Math.min(exitTime, officeBounds.end));

            if (entryWithinOfficeHours < exitWithinOfficeHours) {
                const officeDuration = (exitWithinOfficeHours - entryWithinOfficeHours) / 1000;
                totalOfficeHoursTime += officeDuration;
            }
        }
    }

    if (firstEntryTime && lastExitTime) {
        const totalDuration = (lastExitTime - firstEntryTime) / 1000;
        totalBreakTime = Math.max(0, totalDuration - totalTime);
    }

    return {
        total: totalTime,
        office: totalOfficeHoursTime,
        break: totalBreakTime,
        lastExit: lastExitTime,
        firstEntry: firstEntryTime
    };
}

function calculateLeaveTime(officeTime, currentTime, analyzedDate) {
    const timeLeft = Math.max(TARGET_TIME - officeTime, 0);
    const isCurrentDay = analyzedDate.toDateString() === currentTime.toDateString();
    const difference = officeTime - TARGET_TIME;

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
            const endOfDay = new Date(analyzedDate);
            endOfDay.setHours(19, 30, 0, 0);

            if (leaveTime > endOfDay) {
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
                    status: `Leave by ${leaveTime.toLocaleTimeString()}`,
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

// Multi-day analysis functions
function groupDataByDate(records) {
    const groupedData = {};

    records.forEach(record => {
        if (!record.parsedDateTime) return;

        const dateKey = record.parsedDateTime.toDateString();

        if (!groupedData[dateKey]) {
            groupedData[dateKey] = {};
        }

        if (!groupedData[dateKey][record.name]) {
            groupedData[dateKey][record.name] = [];
        }

        groupedData[dateKey][record.name].push(record);
    });

    return groupedData;
}

function analyzeMultipleDays(startDate, endDate) {
    console.log(`\n📊 ANALYZING DATE RANGE: ${startDate.toDateString()} to ${endDate.toDateString()}`);
    console.log("=".repeat(60));

    // Extract table data
    const rows = document.querySelectorAll("table tbody tr");
    const rawData = [];

    rows.forEach((row, index) => {
        const cells = row.querySelectorAll("td");
        if (cells.length >= 6) {
            const datetimeStr = cells[1].innerText.trim();
            const parsedDateTime = parseDateTime(datetimeStr);

            // Filter by date range
            if (parsedDateTime >= startDate && parsedDateTime <= endDate) {
                const record = {
                    index: index,
                    name: cells[0].innerText.trim(),
                    datetime: datetimeStr,
                    direction: cells[5].innerText.trim(),
                    parsedDateTime: parsedDateTime,
                    allCells: Array.from(cells).map(cell => cell.innerText.trim())
                };
                rawData.push(record);
            }
        }
    });

    console.log(`📋 Found ${rawData.length} records in date range`);

    if (rawData.length === 0) {
        console.log("❌ No data found in the specified date range!");
        return null;
    }

    // Group by date and user
    const groupedData = groupDataByDate(rawData);
    const results = {};
    const currentTime = new Date();

    // Analyze each date
    for (const [dateStr, userData] of Object.entries(groupedData)) {
        const analyzedDate = new Date(dateStr);
        results[dateStr] = {};

        console.log(`\n📅 Analyzing ${dateStr}`);
        console.log("-".repeat(40));

        for (const [userName, userRecords] of Object.entries(userData)) {
            console.log(`👤 User: ${userName} (${userRecords.length} records)`);

            // FIXED: Always pass current time, let calculateTimeSpent decide (EXACT match to Python)
            console.log(`📅 Analyzed date: ${analyzedDate.toDateString()}`);
            console.log(`🕐 Current time: ${currentTime.toLocaleString()}`);

            // Calculate with and without seconds - ALWAYS pass currentTime (matching Python)
            const withSeconds = calculateTimeSpent(userRecords, currentTime, false);
            const withoutSeconds = calculateTimeSpent(userRecords, currentTime, true);

            results[dateStr][userName] = {
                name: userName,
                date: dateStr,
                withSeconds: withSeconds,
                withoutSeconds: withoutSeconds,
                recordCount: userRecords.length
            };
        }
    }

    return results;
}

function generateMultiDayReport(results) {
    console.log("\n📊 MULTI-DAY TIME ANALYSIS REPORT");
    console.log("==================================");

    const allUsers = new Set();
    const dateKeys = Object.keys(results).sort();

    // Collect all users
    for (const userData of Object.values(results)) {
        Object.keys(userData).forEach(user => allUsers.add(user));
    }

    // Generate report for each user
    for (const user of allUsers) {
        console.log(`\n👤 USER: ${user}`);
        console.log("=".repeat(50));

        // Table header
        console.log("┌────────────┬─────────────┬─────────────┬─────────────┬────────┬─────────────┬─────────────────────┐");
        console.log("│    Date    │ Total Time  │Office Hours │ Break Time  │ Target │ Difference  │       Status        │");
        console.log("├────────────┼─────────────┼─────────────┼─────────────┼────────┼─────────────┼─────────────────────┤");

        let totalOfficeTime = 0;
        let totalDifference = 0;
        let daysAnalyzed = 0;

        for (const dateKey of dateKeys) {
            const userData = results[dateKey][user];

            if (userData) {
                const analyzedDate = new Date(dateKey);
                const currentTime = new Date();
                const leaveInfo = calculateLeaveTime(userData.withSeconds.office, currentTime, analyzedDate);

                const dateStr = analyzedDate.toLocaleDateString('en-US', { month: 'short', day: '2-digit' });
                const totalTime = formatTime(userData.withSeconds.total);
                const officeTime = formatTime(userData.withSeconds.office);
                const breakTime = formatTime(userData.withSeconds.break);
                const target = leaveInfo.targetMet ? '✓' : '✗';
                const diffSign = leaveInfo.difference >= 0 ? '+' : '-';
                const diffTime = formatTime(Math.abs(leaveInfo.difference));
                const status = leaveInfo.status;

                console.log(`│${dateStr.padEnd(12)}│${totalTime.padEnd(13)}│${officeTime.padEnd(13)}│${breakTime.padEnd(13)}│${target.padEnd(8)}│${(diffSign + diffTime).padEnd(13)}│${status.padEnd(21)}│`);

                totalOfficeTime += userData.withSeconds.office;
                totalDifference += leaveInfo.difference;
                daysAnalyzed++;
            } else {
                const dateStr = new Date(dateKey).toLocaleDateString('en-US', { month: 'short', day: '2-digit' });
                console.log(`│${dateStr.padEnd(12)}│${'No data'.padEnd(13)}│${'No data'.padEnd(13)}│${'No data'.padEnd(13)}│${'✗'.padEnd(8)}│${'-'.padEnd(13)}│${'No records'.padEnd(21)}│`);
            }
        }

        console.log("└────────────┴─────────────┴─────────────┴─────────────┴────────┴─────────────┴─────────────────────┘");

        // Summary for user
        if (daysAnalyzed > 0) {
            const avgOfficeTime = totalOfficeTime / daysAnalyzed;
            const avgDifference = totalDifference / daysAnalyzed;
            const totalDiffSign = totalDifference >= 0 ? '+' : '-';

            console.log(`\n📈 SUMMARY FOR ${user}:`);
            console.log(`   Days analyzed: ${daysAnalyzed}`);
            console.log(`   Total office time: ${formatTime(totalOfficeTime)}`);
            console.log(`   Average daily office time: ${formatTime(avgOfficeTime)}`);
            console.log(`   Total difference: ${totalDiffSign}${formatTime(Math.abs(totalDifference))}`);
            console.log(`   Average daily difference: ${avgDifference >= 0 ? '+' : '-'}${formatTime(Math.abs(avgDifference))}`);
        }
    }
}

function exportMultiDayCSV(results) {
    console.log("\n💾 GENERATING MULTI-DAY CSV");
    console.log("============================");

    const csvData = [];
    const headers = [
        'Date', 'Name', 'Office Time With Seconds', 'Office Time Without Seconds',
        'Sign With Seconds', 'Difference With Seconds',
        'Sign Without Seconds', 'Difference Without Seconds',
        'Status', 'Message With Seconds', 'Message Without Seconds'
    ];

    csvData.push(headers.join(','));

    const dateKeys = Object.keys(results).sort();

    for (const dateKey of dateKeys) {
        const analyzedDate = new Date(dateKey);
        const currentTime = new Date();

        for (const [userName, userData] of Object.entries(results[dateKey])) {
            const withSecondsInfo = calculateLeaveTime(userData.withSeconds.office, currentTime, analyzedDate);
            const withoutSecondsInfo = calculateLeaveTime(userData.withoutSeconds.office, currentTime, analyzedDate);

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
                formatTime(userData.withSeconds.office),
                formatTime(userData.withoutSeconds.office),
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

    console.log("📋 CSV Content generated");

    // Try to download CSV file
    try {
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `spintly_multi_day_analysis_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        console.log("💾 Multi-day CSV file download initiated!");
    } catch (e) {
        console.log("⚠️ Auto-download failed, please copy the CSV content manually");
        console.log(csvContent);
    }

    return csvContent;
}

// Main execution functions
function runMultiDayAnalysis(daysBack = 7) {
    console.log(`\n🚀 STARTING MULTI-DAY ANALYSIS (${daysBack} days back)`);
    console.log("=".repeat(60));

    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - daysBack);

    try {
        const results = analyzeMultipleDays(startDate, endDate);

        if (!results) {
            return;
        }

        // Generate report
        generateMultiDayReport(results);

        // Export CSV
        const csvContent = exportMultiDayCSV(results);

        console.log("\n🎉 MULTI-DAY ANALYSIS COMPLETE!");
        console.log("================================");
        console.log("✅ Multi-day report displayed above");
        console.log("✅ CSV data generated and downloaded");

        // Store results globally
        window.spintlyMultiDayAnalysis = {
            results: results,
            csvContent: csvContent,
            dateRange: { start: startDate, end: endDate }
        };

        return results;

    } catch (error) {
        console.error("❌ Error during multi-day analysis:", error);
        console.log("Make sure you're on the Spintly access history page with data loaded.");
    }
}

function runCustomDateRangeAnalysis(startDateStr, endDateStr) {
    console.log(`\n🚀 STARTING CUSTOM DATE RANGE ANALYSIS`);
    console.log(`📅 From: ${startDateStr} To: ${endDateStr}`);
    console.log("=".repeat(60));

    try {
        const startDate = new Date(startDateStr);
        const endDate = new Date(endDateStr);

        if (startDate > endDate) {
            console.log("❌ Start date must be before end date!");
            return;
        }

        const results = analyzeMultipleDays(startDate, endDate);

        if (!results) {
            return;
        }

        // Generate report
        generateMultiDayReport(results);

        // Export CSV
        const csvContent = exportMultiDayCSV(results);

        console.log("\n🎉 CUSTOM DATE RANGE ANALYSIS COMPLETE!");
        console.log("=======================================");
        console.log("✅ Custom range report displayed above");
        console.log("✅ CSV data generated and downloaded");

        // Store results globally
        window.spintlyCustomAnalysis = {
            results: results,
            csvContent: csvContent,
            dateRange: { start: startDate, end: endDate }
        };

        return results;

    } catch (error) {
        console.error("❌ Error during custom date range analysis:", error);
        console.log("Make sure the date format is correct (YYYY-MM-DD).");
    }
}

// Helper functions for easy use
window.analyzeLastWeek = () => runMultiDayAnalysis(7);
window.analyzeLastMonth = () => runMultiDayAnalysis(30);
window.analyzeCustomRange = (start, end) => runCustomDateRangeAnalysis(start, end);

// Auto-run analysis for last 7 days
console.log("🔄 Running automatic multi-day analysis for last 7 days...");
runMultiDayAnalysis(7);