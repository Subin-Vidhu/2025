# Railway Reservation System

A comprehensive railway ticket booking and management system built with Python, Streamlit, and SQLite. This application provides a complete solution for managing train schedules, seat reservations, and passenger information through an intuitive web interface.

## 🚆 Features

### Core Functionality
- **Train Management**: Add, view, search, and delete trains
- **Seat Reservation**: Intelligent seat booking system with different seat types
- **Ticket Management**: Book and cancel tickets with passenger details
- **Search System**: Find trains by train number or route (source-destination)
- **Seat Visualization**: View real-time seat availability and passenger information

### Seat Categories
- **Window Seats**: Premium seats with window view
- **Aisle Seats**: Easy access seats near the aisle
- **Middle Seats**: Standard seats between window and aisle

## 🛠 Technology Stack

- **Frontend**: Streamlit (Web Interface)
- **Backend**: Python
- **Database**: SQLite
- **Data Processing**: Pandas

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Installation

1. **Clone or Download the Project**
   ```bash
   # Navigate to the project directory
   cd railway-reservation-streamlit-main
   ```

2. **Install Required Dependencies**
   ```bash
   pip install streamlit pandas sqlite3
   ```
   
   > **Note**: `sqlite3` comes pre-installed with Python, but if you encounter issues, you may need to install it separately.

3. **Run the Application**
   ```bash
   streamlit run main.py
   ```

4. **Access the Application**
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - The application will start automatically

## 📊 Database Schema

The system uses SQLite with the following tables:

### Users Table
```sql
CREATE TABLE users (
    username TEXT,
    password TEXT
)
```

### Employees Table
```sql
CREATE TABLE employees (
    employee_id TEXT,
    password TEXT,
    designation TEXT
)
```

### Trains Table
```sql
CREATE TABLE trains (
    train_number TEXT,
    train_name TEXT,
    departure_date TEXT,
    starting_destination TEXT,
    ending_destination TEXT
)
```

### Dynamic Seat Tables (per train)
```sql
CREATE TABLE seats_{train_number} (
    seat_number INTEGER PRIMARY KEY,
    seat_type TEXT,
    booked INTEGER,
    passenger_name TEXT,
    passenger_age INTEGER,
    passenger_gender TEXT
)
```

## 🎯 How to Use

### 1. Adding a New Train
- Select "Add Train" from the sidebar
- Fill in the train details:
  - Train Number
  - Train Name
  - Departure Date
  - Starting Destination
  - Ending Destination
- Click "Add Train" to save

### 2. Viewing Trains
- Select "View Trains" to see all available trains in a tabular format

### 3. Searching for Trains
- **By Train Number**: Enter the train number and click search
- **By Route**: Enter starting and ending destinations

### 4. Booking a Ticket
- Select "Book Ticket" from the sidebar
- Enter:
  - Train Number
  - Passenger Details (Name, Age, Gender)
  - Preferred Seat Type (Window/Aisle/Middle)
- System automatically assigns the next available seat of the requested type

### 5. Cancelling a Ticket
- Select "Cancel Ticket"
- Enter Train Number and Seat Number
- Confirm cancellation

### 6. Viewing Seat Layout
- Select "View Seats"
- Enter Train Number
- View detailed seat information including passenger details for booked seats

## 🎨 Seat Allocation Logic

The system uses an intelligent seat numbering system:
- **Seats 1-50** per train
- **Window Seats**: Positions ending in 0, 4, 5, 9
- **Aisle Seats**: Positions ending in 2, 3, 6, 7
- **Middle Seats**: Positions ending in 1, 8

## 📁 File Structure

```
railway-reservation-streamlit-main/
├── main.py              # Main application file
├── railway_system.db    # SQLite database (auto-generated)
└── README.md           # This documentation file
```

## 🔧 Key Functions

### Database Management
- `create_DB_if_Not_available()`: Initializes database tables
- `create_seat_table()`: Creates seat layout for each train

### Train Operations
- `add_train()`: Adds new train to the system
- `delete_train()`: Removes train and associated seat data
- `search_train_by_train_number()`: Find specific train
- `search_trains_by_destinations()`: Find trains by route

### Booking Operations
- `book_ticket()`: Reserve seat with passenger details
- `cancel_tickets()`: Cancel existing reservation
- `allocate_next_available_seat()`: Smart seat assignment
- `view_seats()`: Display seat availability and passenger info

### Utility Functions
- `categorize_seat()`: Determines seat type based on position
- `train_functions()`: Main UI controller

## 🚨 Error Handling

The system includes comprehensive error handling for:
- Invalid train numbers
- Unavailable seats
- Missing passenger information
- Database connection issues
- Duplicate train entries

## 🔮 Future Enhancements

Potential improvements for the system:
- User authentication and role-based access
- Payment integration
- Email confirmation system
- Train schedule management
- Waiting list functionality
- Mobile responsiveness
- Advanced reporting features
- Multi-class seat categories (1AC, 2AC, 3AC, Sleeper)

## 📝 Usage Examples

### Example 1: Adding a Train
```
Train Number: 12345
Train Name: Express Special
Departure Date: 2025-09-21
Starting Destination: New York
Ending Destination: Boston
```

### Example 2: Booking a Ticket
```
Train Number: 12345
Seat Type: Window
Passenger Name: John Doe
Passenger Age: 30
Passenger Gender: Male
```

## 🐛 Troubleshooting

### Common Issues:
1. **Database not found**: The database is auto-created on first run
2. **Streamlit not found**: Run `pip install streamlit`
3. **Port already in use**: Use `streamlit run main.py --server.port 8502`

## 📄 License

This project is created for educational purposes as part of the "Master Python Railway Reservation System Project" course.

## 🤝 Contributing

This is an educational project. Feel free to fork and enhance for learning purposes.

## 📞 Support

For issues or questions related to this railway reservation system, please refer to the course materials or create an issue in the project repository.

---

**Note**: This is a demonstration system for educational purposes. For production use, additional security measures, data validation, and error handling should be implemented.


---

[Course Certificate](Master%20Python%20Railway%20Reservation%20System%20Project%202025.pdf)