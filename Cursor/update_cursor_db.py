import sqlite3
import os
import shutil
# Your MercyHacks keys
devDeviceId = "0b917aa3-7562-4d13-8570-a68cc920dff3"
machineId = "afc6b512d1ae294689b948d65fbded94fa2245a83f3a5a0d9cce5f677efbde46"
macMachineId = "afb085e83826f0f1c208b22a5647839cfa3096cbb4c571b0e4c52e851dd26d88a6050a4dcf658b1a7274c67cef855713576cef2e0f2b190b87043eac9a60d70f"
sqmId = "{048442DE-AF03-4BC3-80AA-60DC28134A51}"
# Path to SQLite database
db_path = os.path.expandvars(r"%APPDATA%\Cursor\User\globalStorage\state.vscdb")
if os.path.exists(db_path):
    # Create backup
    backup_path = db_path + ".backup"
    shutil.copy2(db_path, backup_path)
    print(f"Created backup at {backup_path}")
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Update values
    cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'telemetry.devDeviceId'", (devDeviceId,))
    cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'telemetry.machineId'", (machineId,))
    cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'telemetry.macMachineId'", (macMachineId,))
    cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'telemetry.sqmId'", (sqmId,))
    cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'storage.serviceMachineId'", (devDeviceId,))
    # Commit changes and close
    conn.commit()
    conn.close()
    print("Successfully updated Cursor database")
else:
    print(f"Database not found at {db_path}")