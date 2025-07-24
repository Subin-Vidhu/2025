#!/usr/bin/env python3
"""
Spintly Office Access Monitor - FastAPI Application
Works with extracted table data and provides monitoring capabilities
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Tuple
import json
import os
from datetime import datetime, timedelta, time
import asyncio
import uvicorn
import pandas as pd

app = FastAPI(
    title="Spintly Office Access Monitor",
    description="Monitor your office access history from Spintly dashboard",
    version="1.0.0"
)

# Data models
class AccessRecord(BaseModel):
    index: int
    name: str
    datetime: str
    direction: str
    all_cells: List[str]
    parsed_datetime: Optional[datetime] = None

class AccessSummary(BaseModel):
    total_records: int
    latest_entry: Optional[AccessRecord] = None
    latest_exit: Optional[AccessRecord] = None
    today_entries: int
    today_exits: int
    current_status: str  # "In Office" or "Out of Office"

class UpdateRequest(BaseModel):
    table_data: List[Dict]

class TimeAnalysis(BaseModel):
    total_time: float
    office_time: float
    break_time: float
    target_met: bool
    difference: float
    status: str
    last_exit: Optional[str] = None
    first_entry: Optional[str] = None

class DailyTimeAnalysis(BaseModel):
    date: str
    user: str
    with_seconds: TimeAnalysis
    without_seconds: TimeAnalysis

# Constants (matching your Python script)
OFFICE_START = time(7, 30)
OFFICE_END = time(19, 30)
TARGET_TIME = 8 * 3600 + 30 * 60  # 8 hours 30 minutes in seconds (EXACT match to Python)

# Global data storage (in production, use a database)
access_data: List[AccessRecord] = []
last_updated: Optional[datetime] = None
time_analysis_cache: Dict[str, DailyTimeAnalysis] = {}

def parse_datetime(datetime_str: str) -> Optional[datetime]:
    """Parse Spintly datetime format"""
    try:
        # Format: "Jul 23, 2025, 07:38:08 AM (IST)"
        # Remove the timezone part for parsing
        clean_str = datetime_str.replace(" (IST)", "")
        return datetime.strptime(clean_str, "%b %d, %Y, %I:%M:%S %p")
    except:
        return None

def load_initial_data():
    """Load data from investigation results"""
    global access_data, last_updated

    try:
        with open('spintly_investigation_results.json', 'r') as f:
            data = json.load(f)

        table_data = data.get('currentTableData', [])
        access_records = []

        for record in table_data:
            if record.get('name') and record.get('datetime'):  # Skip empty records
                access_record = AccessRecord(
                    index=record.get('index', 0),
                    name=record.get('name', ''),
                    datetime=record.get('datetime', ''),
                    direction=record.get('direction', '').replace('• ', ''),  # Clean direction
                    all_cells=record.get('allCells', []),
                    parsed_datetime=parse_datetime(record.get('datetime', ''))
                )
                access_records.append(access_record)

        # Sort by parsed datetime (newest first)
        access_records.sort(key=lambda x: x.parsed_datetime or datetime.min, reverse=True)
        access_data = access_records
        last_updated = datetime.now()

        print(f"✅ Loaded {len(access_data)} access records")

    except Exception as e:
        print(f"⚠️ Could not load initial data: {e}")
        access_data = []

def calculate_summary() -> AccessSummary:
    """Calculate access summary from current data"""
    if not access_data:
        return AccessSummary(
            total_records=0,
            current_status="Unknown",
            today_entries=0,
            today_exits=0
        )

    # Find latest entry and exit
    latest_entry = None
    latest_exit = None

    for record in access_data:
        if "Entry" in record.direction and not latest_entry:
            latest_entry = record
        elif "Exit" in record.direction and not latest_exit:
            latest_exit = record

        if latest_entry and latest_exit:
            break

    # Count today's activities
    today = datetime.now().date()
    today_entries = 0
    today_exits = 0

    for record in access_data:
        if record.parsed_datetime and record.parsed_datetime.date() == today:
            if "Entry" in record.direction:
                today_entries += 1
            elif "Exit" in record.direction:
                today_exits += 1

    # Determine current status
    current_status = "Unknown"
    if latest_entry and latest_exit:
        if latest_entry.parsed_datetime > latest_exit.parsed_datetime:
            current_status = "In Office"
        else:
            current_status = "Out of Office"
    elif latest_entry and not latest_exit:
        current_status = "In Office"
    elif latest_exit and not latest_entry:
        current_status = "Out of Office"

    return AccessSummary(
        total_records=len(access_data),
        latest_entry=latest_entry,
        latest_exit=latest_exit,
        today_entries=today_entries,
        today_exits=today_exits,
        current_status=current_status
    )

# Time Analysis Functions (matching your Python script logic)
def truncate_seconds(dt: datetime) -> datetime:
    """Truncate seconds from datetime"""
    return dt.replace(second=0, microsecond=0)

def calculate_time_spent_detailed(records: List[AccessRecord], current_time: datetime = None, truncate: bool = False) -> Dict[str, float]:
    """Calculate time spent in office (matching your Python logic)"""
    total_time, total_office_hours_time, total_break_time = 0, 0, 0
    entry_time, first_entry_time, last_exit_time = None, None, None

    print(f"\nCalculating time for {len(records)} records")
    print(f"Current time: {current_time}")

    # Convert current_time to datetime if it's not None
    if current_time and isinstance(current_time, datetime):
        current_time = current_time.replace(tzinfo=None)  # Remove timezone if present

    # CRITICAL FIX: Sort records by datetime (oldest first) for correct time calculation
    sorted_records = sorted(records, key=lambda x: x.parsed_datetime or datetime.min)
    print(f"Sorted {len(sorted_records)} records chronologically (oldest first)")

    # Debug: Print sorted records
    for i, record in enumerate(sorted_records):
        print(f"  {i+1}. {record.parsed_datetime} - {record.direction}")

    for record in sorted_records:
        dt = truncate_seconds(record.parsed_datetime) if truncate else record.parsed_datetime
        if dt:
            dt = dt.replace(tzinfo=None)  # Remove timezone if present
        else:
            continue

        print(f"\nProcessing record: {dt} - {record.direction}")

        if 'entry' in record.direction.lower():
            if first_entry_time is None:
                first_entry_time = dt
                print(f"First entry time set to: {first_entry_time}")
            entry_time = dt
            print(f"Entry time set to: {entry_time}")
        elif 'exit' in record.direction.lower() and entry_time:
            exit_time = dt
            last_exit_time = exit_time
            duration = (exit_time - entry_time).total_seconds()
            total_time += duration
            print(f"Exit time: {exit_time}")
            print(f"Duration: {format_time_seconds(duration)}")

            # Calculate time during office hours
            entry_time_within_office_hours = max(entry_time, entry_time.replace(hour=OFFICE_START.hour, minute=OFFICE_START.minute, second=0))
            exit_time_within_office_hours = min(exit_time, exit_time.replace(hour=OFFICE_END.hour, minute=OFFICE_END.minute, second=0))

            if entry_time_within_office_hours < exit_time_within_office_hours:
                office_duration = (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()
                total_office_hours_time += office_duration
                print(f"Office hours duration: {format_time_seconds(office_duration)}")

            entry_time = None

    # Handle open entry without exit or no exit record for the day
    if entry_time and current_time:
        print(f"\nHandling open entry:")
        print(f"Entry time: {entry_time}")
        print(f"Current time: {current_time}")

        exit_time = truncate_seconds(current_time) if truncate else current_time
        last_exit_time = exit_time
        duration = (exit_time - entry_time).total_seconds()
        if duration > 0:  # Only add if duration is positive
            total_time += duration
            print(f"Duration until current time: {format_time_seconds(duration)}")

            # Office hours calculation for current open session
            entry_time_within_office_hours = max(entry_time, entry_time.replace(hour=OFFICE_START.hour, minute=OFFICE_START.minute, second=0))
            exit_time_within_office_hours = min(exit_time, exit_time.replace(hour=OFFICE_END.hour, minute=OFFICE_END.minute, second=0))

            if entry_time_within_office_hours < exit_time_within_office_hours:
                office_duration = (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()
                total_office_hours_time += office_duration
                print(f"Office hours duration until current time: {format_time_seconds(office_duration)}")

    # Handle case where we have first entry but lost track of entry_time (EXACT match to Python lines 106-126)
    elif first_entry_time and current_time and current_time.date() == first_entry_time.date():
        print(f"\nHandling first entry without exit:")
        print(f"First entry time: {first_entry_time}")
        print(f"Current time: {current_time}")

        exit_time = truncate_seconds(current_time) if truncate else current_time
        last_exit_time = exit_time
        duration = (exit_time - first_entry_time).total_seconds()
        if duration > 0:
            total_time += duration
            print(f"Duration until current time: {format_time_seconds(duration)}")

            # Office hours calculation for current open session
            entry_time_within_office_hours = max(first_entry_time, first_entry_time.replace(hour=OFFICE_START.hour, minute=OFFICE_START.minute, second=0))
            exit_time_within_office_hours = min(exit_time, exit_time.replace(hour=OFFICE_END.hour, minute=OFFICE_END.minute, second=0))

            if entry_time_within_office_hours < exit_time_within_office_hours:
                office_duration = (exit_time_within_office_hours - entry_time_within_office_hours).total_seconds()
                total_office_hours_time += office_duration
                print(f"Office hours duration until current time: {format_time_seconds(office_duration)}")

    # Calculate total break time
    if first_entry_time and last_exit_time:
        total_duration = (last_exit_time - first_entry_time).total_seconds()
        total_break_time = max(0, total_duration - total_time)  # Ensure break time is not negative
        print(f"\nFinal calculations:")
        print(f"Total duration: {format_time_seconds(total_duration)}")
        print(f"Total time: {format_time_seconds(total_time)}")
        print(f"Office hours time: {format_time_seconds(total_office_hours_time)}")
        print(f"Break time: {format_time_seconds(total_break_time)}")

    return {
        'total': total_time,
        'office': total_office_hours_time,
        'break': total_break_time,
        'last_exit': last_exit_time,
        'first_entry': first_entry_time
    }

def format_time_seconds(seconds: float) -> str:
    """Format time from seconds to hh:mm:ss"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def calculate_leave_time(office_time: float, current_time: datetime, analyzed_date: datetime) -> Tuple[datetime, bool, str, timedelta]:
    """Calculate leave time and status (matching your Python logic)"""
    time_left = max(TARGET_TIME - office_time, 0)
    is_current_day = analyzed_date.date() == current_time.date()

    difference = timedelta(seconds=int(office_time - TARGET_TIME))

    if time_left == 0:
        return current_time, True, "Target met", difference
    else:
        if is_current_day:
            leave_time = current_time + timedelta(seconds=time_left)
            if leave_time.time() > time(19, 30):  # If leave time is after office hours
                return datetime.combine(analyzed_date.date(), time(19, 30)), False, "Leave by end of day", difference
            else:
                return leave_time, False, f"Leave by {leave_time.strftime('%I:%M:%S %p')}", difference
        else:
            return current_time, False, "Target not met", difference

def analyze_time_for_date(date: datetime.date, current_time: datetime = None) -> Dict[str, DailyTimeAnalysis]:
    """Analyze time spent for a specific date"""
    if current_time is None:
        current_time = datetime.now()

    # Filter records for the specific date
    date_records = [record for record in access_data if record.parsed_datetime and record.parsed_datetime.date() == date]

    if not date_records:
        return {}

    # Group by user
    user_records = {}
    for record in date_records:
        if record.name not in user_records:
            user_records[record.name] = []
        user_records[record.name].append(record)

    results = {}

    for user, records in user_records.items():
        # FIXED: Always pass current time, let calculate_time_spent_detailed decide (EXACT match to Python)
        print(f"📅 Analyzing {user} for {date}")
        print(f"🕐 Current time: {current_time}")

        # Calculate with seconds - ALWAYS pass current_time (matching Python)
        with_seconds_data = calculate_time_spent_detailed(records, current_time, truncate=False)
        # Calculate without seconds - ALWAYS pass current_time (matching Python)
        without_seconds_data = calculate_time_spent_detailed(records, current_time, truncate=True)

        # Calculate leave time info for both
        leave_info_with = calculate_leave_time(with_seconds_data['office'], current_time, datetime.combine(date, datetime.min.time()))
        leave_info_without = calculate_leave_time(without_seconds_data['office'], current_time, datetime.combine(date, datetime.min.time()))

        with_seconds_analysis = TimeAnalysis(
            total_time=with_seconds_data['total'],
            office_time=with_seconds_data['office'],
            break_time=with_seconds_data['break'],
            target_met=leave_info_with[1],
            difference=leave_info_with[3].total_seconds(),
            status=leave_info_with[2],
            last_exit=with_seconds_data['last_exit'].isoformat() if with_seconds_data['last_exit'] else None,
            first_entry=with_seconds_data['first_entry'].isoformat() if with_seconds_data['first_entry'] else None
        )

        without_seconds_analysis = TimeAnalysis(
            total_time=without_seconds_data['total'],
            office_time=without_seconds_data['office'],
            break_time=without_seconds_data['break'],
            target_met=leave_info_without[1],
            difference=leave_info_without[3].total_seconds(),
            status=leave_info_without[2],
            last_exit=without_seconds_data['last_exit'].isoformat() if without_seconds_data['last_exit'] else None,
            first_entry=without_seconds_data['first_entry'].isoformat() if without_seconds_data['first_entry'] else None
        )

        results[user] = DailyTimeAnalysis(
            date=date.isoformat(),
            user=user,
            with_seconds=with_seconds_analysis,
            without_seconds=without_seconds_analysis
        )

    return results

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Main dashboard page"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Spintly Office Access Monitor</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .status-in { color: #28a745; font-weight: bold; }
            .status-out { color: #dc3545; font-weight: bold; }
            .status-unknown { color: #6c757d; font-weight: bold; }
            .entry { color: #28a745; }
            .exit { color: #dc3545; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f8f9fa; }
            .refresh-btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            .refresh-btn:hover { background: #0056b3; }
            .last-updated { color: #6c757d; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏢 Spintly Office Access Monitor</h1>

            <div class="card">
                <h2>📊 Current Status</h2>
                <div id="summary">Loading...</div>
                <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
                <div class="last-updated" id="lastUpdated"></div>
            </div>

            <div class="card">
                <h2>📋 Recent Access History</h2>
                <div id="accessHistory">Loading...</div>
            </div>

            <div class="card">
                <h2>⏱️ Time Analysis</h2>
                <div style="margin-bottom: 10px;">
                    <input type="date" id="analysisDate" value="" style="padding: 8px; margin-right: 10px;">
                    <button class="refresh-btn" onclick="loadTimeAnalysis()">📊 Analyze Time</button>
                    <button class="refresh-btn" onclick="exportCSV()" style="background: #28a745;">💾 Export CSV</button>
                </div>
                <div id="timeAnalysis">Select a date to analyze time spent</div>
            </div>
        </div>

        <script>
            async function loadSummary() {
                try {
                    const response = await fetch('/api/summary');
                    const data = await response.json();

                    const statusClass = data.current_status === 'In Office' ? 'status-in' :
                                       data.current_status === 'Out of Office' ? 'status-out' : 'status-unknown';

                    document.getElementById('summary').innerHTML = `
                        <p><strong>Current Status:</strong> <span class="${statusClass}">${data.current_status}</span></p>
                        <p><strong>Today's Activity:</strong> ${data.today_entries} entries, ${data.today_exits} exits</p>
                        <p><strong>Total Records:</strong> ${data.total_records}</p>
                        ${data.latest_entry ? `<p><strong>Latest Entry:</strong> ${data.latest_entry.datetime}</p>` : ''}
                        ${data.latest_exit ? `<p><strong>Latest Exit:</strong> ${data.latest_exit.datetime}</p>` : ''}
                    `;
                } catch (error) {
                    document.getElementById('summary').innerHTML = '<p style="color: red;">Error loading summary</p>';
                }
            }

            async function loadAccessHistory() {
                try {
                    const response = await fetch('/api/access-history?limit=20');
                    const data = await response.json();

                    let html = '<table><tr><th>Name</th><th>Date & Time</th><th>Direction</th><th>Location</th></tr>';
                    data.forEach(record => {
                        const directionClass = record.direction.includes('Entry') ? 'entry' : 'exit';
                        const location = record.all_cells[6] || '-';
                        html += `<tr>
                            <td>${record.name}</td>
                            <td>${record.datetime}</td>
                            <td class="${directionClass}">${record.direction}</td>
                            <td>${location}</td>
                        </tr>`;
                    });
                    html += '</table>';

                    document.getElementById('accessHistory').innerHTML = html;
                } catch (error) {
                    document.getElementById('accessHistory').innerHTML = '<p style="color: red;">Error loading access history</p>';
                }
            }

            async function refreshData() {
                document.getElementById('lastUpdated').innerHTML = 'Refreshing...';
                await Promise.all([loadSummary(), loadAccessHistory()]);
                document.getElementById('lastUpdated').innerHTML = `Last updated: ${new Date().toLocaleString()}`;
            }

            async function loadTimeAnalysis() {
                const dateInput = document.getElementById('analysisDate');
                const date = dateInput.value;

                if (!date) {
                    alert('Please select a date');
                    return;
                }

                try {
                    document.getElementById('timeAnalysis').innerHTML = 'Loading time analysis...';

                    const response = await fetch(`/api/time-analysis/${date}`);
                    const data = await response.json();

                    if (Object.keys(data).length === 0) {
                        document.getElementById('timeAnalysis').innerHTML = '<p>No data found for the selected date.</p>';
                        return;
                    }

                    let html = '<div style="overflow-x: auto;">';

                    // With seconds table
                    html += '<h3>📊 Time Analysis (With Seconds)</h3>';
                    html += '<table style="width: 100%; margin-bottom: 20px;"><tr><th>Name</th><th>Total Time</th><th>Office Hours</th><th>Break Time</th><th>Target</th><th>Difference</th><th>Status</th></tr>';

                    for (const [user, analysis] of Object.entries(data)) {
                        const ws = analysis.with_seconds;
                        const targetIcon = ws.target_met ? '✅' : '❌';
                        const diffSign = ws.difference >= 0 ? '+' : '-';
                        const diffTime = formatSeconds(Math.abs(ws.difference));
                        const statusColor = ws.target_met ? 'color: green' : 'color: red';

                        html += `<tr>
                            <td>${user}</td>
                            <td>${formatSeconds(ws.total_time)}</td>
                            <td>${formatSeconds(ws.office_time)}</td>
                            <td>${formatSeconds(ws.break_time)}</td>
                            <td>${targetIcon}</td>
                            <td style="${statusColor}">${diffSign}${diffTime}</td>
                            <td style="${statusColor}">${ws.status}</td>
                        </tr>`;
                    }
                    html += '</table>';

                    // Without seconds table
                    html += '<h3>📊 Time Analysis (Without Seconds)</h3>';
                    html += '<table style="width: 100%;"><tr><th>Name</th><th>Total Time</th><th>Office Hours</th><th>Break Time</th><th>Target</th><th>Difference</th><th>Status</th></tr>';

                    for (const [user, analysis] of Object.entries(data)) {
                        const wos = analysis.without_seconds;
                        const targetIcon = wos.target_met ? '✅' : '❌';
                        const diffSign = wos.difference >= 0 ? '+' : '-';
                        const diffTime = formatSeconds(Math.abs(wos.difference));
                        const statusColor = wos.target_met ? 'color: green' : 'color: red';

                        html += `<tr>
                            <td>${user}</td>
                            <td>${formatSeconds(wos.total_time)}</td>
                            <td>${formatSeconds(wos.office_time)}</td>
                            <td>${formatSeconds(wos.break_time)}</td>
                            <td>${targetIcon}</td>
                            <td style="${statusColor}">${diffSign}${diffTime}</td>
                            <td style="${statusColor}">${wos.status}</td>
                        </tr>`;
                    }
                    html += '</table></div>';

                    document.getElementById('timeAnalysis').innerHTML = html;
                } catch (error) {
                    document.getElementById('timeAnalysis').innerHTML = '<p style="color: red;">Error loading time analysis</p>';
                    console.error('Error:', error);
                }
            }

            async function exportCSV() {
                const dateInput = document.getElementById('analysisDate');
                const date = dateInput.value;

                if (!date) {
                    alert('Please select a date');
                    return;
                }

                try {
                    const response = await fetch(`/api/csv-export/${date}`);
                    const data = await response.json();

                    // Create and download CSV file
                    const blob = new Blob([data.csv_content], { type: 'text/csv' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = data.filename;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);

                    alert('CSV file downloaded successfully!');
                } catch (error) {
                    alert('Error exporting CSV');
                    console.error('Error:', error);
                }
            }

            function formatSeconds(seconds) {
                const hours = Math.floor(seconds / 3600);
                const minutes = Math.floor((seconds % 3600) / 60);
                const secs = Math.floor(seconds % 60);
                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            }

            // Set today's date as default
            document.getElementById('analysisDate').value = new Date().toISOString().split('T')[0];

            // Load data on page load
            refreshData();

            // Auto-refresh every 5 minutes
            setInterval(refreshData, 5 * 60 * 1000);
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/api/summary", response_model=AccessSummary)
async def get_summary():
    """Get access summary"""
    return calculate_summary()

@app.get("/api/access-history", response_model=List[AccessRecord])
async def get_access_history(limit: int = 50):
    """Get access history records"""
    return access_data[:limit]

@app.get("/api/latest-entry", response_model=Optional[AccessRecord])
async def get_latest_entry():
    """Get the most recent entry record"""
    for record in access_data:
        if "Entry" in record.direction:
            return record
    return None

@app.get("/api/latest-exit", response_model=Optional[AccessRecord])
async def get_latest_exit():
    """Get the most recent exit record"""
    for record in access_data:
        if "Exit" in record.direction:
            return record
    return None

@app.post("/api/update-data")
async def update_data(request: UpdateRequest):
    """Update access data with new table data from browser"""
    global access_data, last_updated

    try:
        access_records = []

        for record in request.table_data:
            if record.get('name') and record.get('datetime'):  # Skip empty records
                access_record = AccessRecord(
                    index=record.get('index', 0),
                    name=record.get('name', ''),
                    datetime=record.get('datetime', ''),
                    direction=record.get('direction', '').replace('• ', ''),
                    all_cells=record.get('allCells', []),
                    parsed_datetime=parse_datetime(record.get('datetime', ''))
                )
                access_records.append(access_record)

        # Sort by parsed datetime (newest first)
        access_records.sort(key=lambda x: x.parsed_datetime or datetime.min, reverse=True)
        access_data = access_records
        last_updated = datetime.now()

        return {
            "status": "success",
            "message": f"Updated with {len(access_data)} records",
            "last_updated": last_updated.isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating data: {str(e)}")

@app.get("/api/status")
async def get_status():
    """Get API status and last update time"""
    return {
        "status": "running",
        "total_records": len(access_data),
        "last_updated": last_updated.isoformat() if last_updated else None,
        "version": "1.0.0"
    }

@app.get("/api/time-analysis/{date}", response_model=Dict[str, DailyTimeAnalysis])
async def get_time_analysis_for_date(date: str):
    """Get detailed time analysis for a specific date (YYYY-MM-DD format)"""
    try:
        analyzed_date = datetime.strptime(date, "%Y-%m-%d").date()
        current_time = datetime.now()

        # Check cache first
        cache_key = f"{date}_{current_time.strftime('%Y-%m-%d_%H')}"  # Cache per hour
        if cache_key in time_analysis_cache:
            return time_analysis_cache[cache_key]

        results = analyze_time_for_date(analyzed_date, current_time)

        # Cache results
        time_analysis_cache[cache_key] = results

        return results
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

@app.get("/api/time-analysis/today", response_model=Dict[str, DailyTimeAnalysis])
async def get_today_time_analysis():
    """Get detailed time analysis for today"""
    today = datetime.now().date()
    return await get_time_analysis_for_date(today.isoformat())

@app.get("/api/time-analysis/range/{start_date}/{end_date}")
async def get_time_analysis_range(start_date: str, end_date: str):
    """Get time analysis for a date range"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start > end:
            raise HTTPException(status_code=400, detail="Start date must be before end date")

        results = {}
        current_date = start
        current_time = datetime.now()

        while current_date <= end:
            date_str = current_date.isoformat()
            results[date_str] = analyze_time_for_date(current_date, current_time)
            current_date += timedelta(days=1)

        return results
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

@app.get("/api/csv-export/{date}")
async def export_csv_for_date(date: str):
    """Export time analysis as CSV for a specific date"""
    try:
        analyzed_date = datetime.strptime(date, "%Y-%m-%d").date()
        current_time = datetime.now()

        results = analyze_time_for_date(analyzed_date, current_time)

        if not results:
            raise HTTPException(status_code=404, detail="No data found for the specified date")

        # Generate CSV content
        csv_lines = [
            "Date,Name,Office Time With Seconds,Office Time Without Seconds,Sign With Seconds,Difference With Seconds,Sign Without Seconds,Difference Without Seconds,Status,Message With Seconds,Message Without Seconds"
        ]

        for user, analysis in results.items():
            # Calculate signs and cap differences
            sign_with = '+' if analysis.with_seconds.difference >= 0 else '-'
            sign_without = '+' if analysis.without_seconds.difference >= 0 else '-'

            diff_with = abs(analysis.with_seconds.difference)
            diff_without = abs(analysis.without_seconds.difference)
            msg_with = ''
            msg_without = ''

            # Cap at 1 hour for positive differences
            if sign_with == '+' and diff_with > 3600:
                diff_with = 3600
                msg_with = 'Only 1 hour/day can be considered extra'
            if sign_without == '+' and diff_without > 3600:
                diff_without = 3600
                msg_without = 'Only 1 hour/day can be considered extra'

            csv_lines.append(
                f"{date},{user},{format_time_seconds(analysis.with_seconds.office_time)},{format_time_seconds(analysis.without_seconds.office_time)},{sign_with},{format_time_seconds(diff_with)},{sign_without},{format_time_seconds(diff_without)},{analysis.with_seconds.status},{msg_with},{msg_without}"
            )

        csv_content = '\n'.join(csv_lines)

        return {
            "csv_content": csv_content,
            "filename": f"spintly_time_analysis_{date}.csv"
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Load initial data on startup"""
    load_initial_data()

# Main function to run the app
def main():
    """Run the FastAPI application"""
    print("🚀 Starting Spintly Office Access Monitor")
    print("📊 Dashboard will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")

    uvicorn.run(
        "spintly_fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()