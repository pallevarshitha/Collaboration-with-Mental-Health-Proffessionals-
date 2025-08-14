# Mental Health Collaboration Platform

A comprehensive Flask-based web application designed to connect mental health professionals with clients, providing a secure and user-friendly platform for mental health support and collaboration.

## 🌟 Features

### User Management & Authentication
- **Multi-role User System**: Support for clients, professionals, and administrators
- **Secure Authentication**: Password hashing and session management
- **Role-based Access Control**: Different dashboards and permissions for each user type

### Professional Directory
- **Professional Profiles**: Detailed information including specialization, experience, education, and hourly rates
- **Search & Selection**: Easy browsing and selection of mental health professionals
- **Professional Verification**: License numbers and credentials display

### Chat & Communication
- **Real-time Chat Interface**: WhatsApp-style chat interface for client-professional communication
- **File Sharing**: Support for images, videos, and documents
- **Media Handling**: Automatic video playback, image previews, and document downloads
- **Chat History**: Persistent message storage and retrieval

### Wellness Resources
- **Stress Relief Videos**: Curated YouTube content for stress management
- **Yoga & Exercise**: Guided yoga sessions and workout routines
- **Mental Health Education**: Access to helpful resources and exercises

### Modern UI/UX
- **Responsive Design**: Mobile-friendly interface
- **Clean Interface**: Modern, intuitive design with smooth animations
- **Accessibility**: Easy navigation and user experience

## 🚀 Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login for session management
- **Frontend**: HTML5, CSS3, JavaScript
- **File Handling**: Werkzeug for secure file uploads
- **Styling**: Custom CSS with modern design principles

## 📁 Project Structure

```
mental_health/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── login.html       # User authentication
│   ├── user_dashboard.html      # Client dashboard
│   ├── professional_list.html   # Professional directory
│   ├── chat.html        # Chat interface
│   └── resources.html   # Wellness resources
├── uploads/              # File storage directory
└── instance/             # Database files
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/mental-health-platform.git
cd mental-health-platform
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Access the Platform
Open your web browser and navigate to:
```
http://localhost:5000
```

## 👥 User Types & Access

### Client Users
- **Login**: `test@example.com` / `password123`
- **Features**: Browse professionals, start chats, access wellness resources

### Professional Users
- **Features**: Profile management, client communication, appointment scheduling

### Admin Users
- **Login**: `admin@example.com` / `admin123`
- **Features**: User management, platform oversight, system administration

## 🔐 Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- Secure file upload handling
- SQL injection protection

## 📱 Key Functionalities

### Chat System
- Real-time messaging between clients and professionals
- File attachment support (images, videos, documents)
- Message history and persistence
- Professional profile integration

### Professional Directory
- Comprehensive professional profiles
- Specialization-based filtering
- Contact and availability information
- Direct chat initiation

### Wellness Resources
- Curated YouTube video collections
- Stress relief and meditation content
- Yoga and exercise routines
- Mental health education materials

## 🎯 Use Cases

- **Mental Health Clinics**: Professional-client communication platform
- **Individual Therapists**: Client management and communication
- **Mental Health Organizations**: Resource sharing and professional networking
- **Educational Institutions**: Mental health training and resource distribution

## 🔧 Customization

The platform is designed for easy extension and modification:
- Modular Flask application structure
- Configurable user roles and permissions
- Customizable professional profile fields
- Extensible chat functionality
- Flexible resource management system

## 🤝 Contributing

We welcome contributions! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask community for the excellent web framework
- Mental health professionals for domain expertise
- Open source contributors for inspiration and tools

## 📞 Support

For support or questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation and FAQ sections

---

**Note**: This platform is designed for educational and demonstration purposes. For production use in mental health services, please ensure compliance with relevant healthcare regulations and data protection laws. 