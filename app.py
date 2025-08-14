from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mental_health.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), nullable=False)  # 'user' or 'professional'
    is_admin = db.Column(db.Boolean, default=False)  # New admin flag
    
    # Professional details
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(50))
    experience = db.Column(db.String(50))
    education = db.Column(db.Text)
    bio = db.Column(db.Text)
    hourly_rate = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_email = db.Column(db.String(120), nullable=False)
    receiver_email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    attachment_path = db.Column(db.String(255))

class ChatConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, archived, blocked
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_connection_id = db.Column(db.Integer, db.ForeignKey('chat_connection.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text)
    attachment_path = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        elif current_user.user_type == 'professional':
            return redirect(url_for('professional_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        # Special handling for admin login
        if email == 'admin@example.com' and password == 'admin123':
            # Check if admin user exists, if not create it
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                try:
                    admin_user = User(
                        username='admin',
                        email='admin@example.com',
                        user_type='admin',
                        is_admin=True
                    )
                    admin_user.set_password('admin123')
                    db.session.add(admin_user)
                    db.session.commit()
                except Exception as e:
                    admin_user = User.query.filter_by(username='admin').first()
                    if not admin_user:
                        flash('Error creating admin user. Please try again.')
                        return redirect(url_for('login'))
            
            login_user(admin_user)
            flash('Welcome Admin!')
            return redirect(url_for('admin_dashboard'))
        
        # Check for test account
        if email == 'test@example.com' and password == 'password123' and user_type == 'user':
            test_user = User.query.filter_by(email='test@example.com').first()
            if not test_user:
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    user_type='user',
                    is_admin=False
                )
                test_user.set_password('password123')
                db.session.add(test_user)
                db.session.commit()
            
            login_user(test_user)
            return redirect(url_for('user_dashboard'))
        
        # Regular user login
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.user_type == user_type:
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            elif user.user_type == 'professional':
                return redirect(url_for('professional_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        flash('Invalid email, password, or user type')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('signup'))

        user = User(username=username, email=email, user_type=user_type)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    view = request.args.get('view', 'user')
    return render_template('dashboard.html', view=view)

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if current_user.is_admin or current_user.user_type != 'user':
        return redirect(url_for('home'))
    return render_template('user_dashboard.html')

@app.route('/professional/dashboard')
@login_required
def professional_dashboard():
    if current_user.is_admin or current_user.user_type != 'professional':
        return redirect(url_for('home'))
    return render_template('professional_dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/professionals')
@login_required
def professional_list():
    if current_user.user_type != 'user':
        return redirect(url_for('home'))
    return render_template('professional_list.html')

@app.route('/select_professional/<email>', methods=['POST'])
@login_required
def select_professional(email):
    if current_user.user_type != 'user':
        return redirect(url_for('home'))
    
    # Here you would typically:
    # 1. Create a connection between the user and professional
    # 2. Send notification to the professional
    # 3. Redirect to appointment scheduling
    
    flash(f'You have selected a professional. They will contact you at {email}')
    return redirect(url_for('user_dashboard'))

@app.route('/chat/<professional_email>')
@login_required
def chat(professional_email):
    if current_user.user_type != 'user':
        flash('Only users can access the chat interface.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get professional details
    professional = User.query.filter_by(email=professional_email, user_type='professional').first()
    if not professional:
        flash('Professional not found.', 'error')
        return redirect(url_for('professional_list'))
    
    # Get or create chat connection
    chat_connection = ChatConnection.query.filter_by(
        user_id=current_user.id,
        professional_id=professional.id
    ).first()
    
    if not chat_connection:
        chat_connection = ChatConnection(
            user_id=current_user.id,
            professional_id=professional.id,
            status='active'
        )
        db.session.add(chat_connection)
        db.session.commit()
    
    # Get chat messages
    messages = ChatMessage.query.filter_by(
        chat_connection_id=chat_connection.id
    ).order_by(ChatMessage.timestamp).all()
    
    return render_template('chat.html',
                         professional=professional,
                         messages=messages,
                         chat_connection=chat_connection)

@app.route('/send_message/<professional_email>', methods=['POST'])
@login_required
def send_message(professional_email):
    if current_user.user_type != 'user':
        return jsonify({'error': 'Unauthorized'}), 403
    
    message_text = request.form.get('message')
    attachment = request.files.get('attachment')
    
    if not message_text and not attachment:
        return jsonify({'error': 'No message content'}), 400
    
    # Get professional
    professional = User.query.filter_by(email=professional_email, user_type='professional').first()
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404
    
    # Get or create chat connection
    chat_connection = ChatConnection.query.filter_by(
        user_id=current_user.id,
        professional_id=professional.id
    ).first()
    
    if not chat_connection:
        chat_connection = ChatConnection(
            user_id=current_user.id,
            professional_id=professional.id,
            status='active'
        )
        db.session.add(chat_connection)
        db.session.commit()
    
    # Handle attachment if present
    attachment_path = None
    if attachment:
        # Create a unique filename
        filename = secure_filename(attachment.filename)
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        attachment_path = f'uploads/{unique_filename}'
        
        # Ensure the uploads directory exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        # Save the file
        try:
            attachment.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        except Exception as e:
            print(f"Error saving file: {e}")
            return jsonify({'error': 'Failed to save attachment'}), 500
    
    # Create message
    message = ChatMessage(
        chat_connection_id=chat_connection.id,
        sender_id=current_user.id,
        content=message_text,
        attachment_path=attachment_path
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify({
        'message': message_text,
        'attachment_path': attachment_path,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/get_messages/<professional_email>')
@login_required
def get_messages(professional_email):
    if current_user.user_type != 'user':
        return jsonify({'error': 'Unauthorized'}), 403
    
    professional = User.query.filter_by(email=professional_email, user_type='professional').first()
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404
    
    chat_connection = ChatConnection.query.filter_by(
        user_id=current_user.id,
        professional_id=professional.id
    ).first()
    
    if not chat_connection:
        return jsonify({'messages': []})
    
    messages = ChatMessage.query.filter_by(
        chat_connection_id=chat_connection.id
    ).order_by(ChatMessage.timestamp).all()
    
    return jsonify({
        'messages': [{
            'content': msg.content,
            'attachment_path': msg.attachment_path,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_sender': msg.sender_id == current_user.id
        } for msg in messages]
    })

@app.route('/resources')
@login_required
def resources():
    return render_template('resources.html')

if __name__ == '__main__':
    with app.app_context():
        # Drop all tables first
        db.drop_all()
        # Create all tables
        db.create_all()
        
        # Create test professional users if they don't exist
        professionals = [
            {
                'username': 'Dr. Sarah Johnson',
                'email': 'dr.sarah.j@example.com',
                'password': 'password123',
                'user_type': 'professional',
                'specialization': 'Clinical Psychology',
                'license_number': 'PSY-12345',
                'experience': '8 years',
                'education': 'Ph.D. in Clinical Psychology, Stanford University',
                'bio': 'Specialized in anxiety disorders and trauma therapy. Certified in CBT and EMDR.',
                'hourly_rate': '$150/hr'
            },
            {
                'username': 'Dr. Michael Chen',
                'email': 'dr.michael.c@example.com',
                'password': 'password123',
                'user_type': 'professional',
                'specialization': 'Marriage & Family Therapy',
                'license_number': 'MFT-67890',
                'experience': '12 years',
                'education': 'M.S. in Marriage & Family Therapy, UCLA',
                'bio': 'Expert in relationship counseling and family dynamics. Gottman Method certified.',
                'hourly_rate': '$140/hr'
            },
            {
                'username': 'Dr. Emily Rodriguez',
                'email': 'dr.emily.r@example.com',
                'password': 'password123',
                'user_type': 'professional',
                'specialization': 'Child Psychology',
                'license_number': 'PSY-23456',
                'experience': '10 years',
                'education': 'Ph.D. in Child Psychology, Harvard University',
                'bio': 'Specialized in child development and behavioral therapy. Play therapy certified.',
                'hourly_rate': '$160/hr'
            },
            {
                'username': 'Dr. James Wilson',
                'email': 'dr.james.w@example.com',
                'password': 'password123',
                'user_type': 'professional',
                'specialization': 'Addiction Counseling',
                'license_number': 'LADC-34567',
                'experience': '15 years',
                'education': 'M.S. in Addiction Counseling, Columbia University',
                'bio': 'Expert in substance abuse treatment and recovery support. Certified in trauma-informed care.',
                'hourly_rate': '$145/hr'
            },
            {
                'username': 'Dr. Lisa Patel',
                'email': 'dr.lisa.p@example.com',
                'password': 'password123',
                'user_type': 'professional',
                'specialization': 'Trauma Therapy',
                'license_number': 'PSY-45678',
                'experience': '9 years',
                'education': 'Ph.D. in Clinical Psychology, Yale University',
                'bio': 'Specialized in trauma recovery and PTSD treatment. EMDR certified.',
                'hourly_rate': '$155/hr'
            }
        ]
        
        for prof in professionals:
            user = User(
                username=prof['username'],
                email=prof['email'],
                user_type=prof['user_type'],
                specialization=prof['specialization'],
                license_number=prof['license_number'],
                experience=prof['experience'],
                education=prof['education'],
                bio=prof['bio'],
                hourly_rate=prof['hourly_rate']
            )
            user.set_password(prof['password'])
            db.session.add(user)
        
        # Create test user
        test_user = User(
            username='testuser',
            email='test@example.com',
            user_type='user',
            is_admin=False
        )
        test_user.set_password('password123')
        db.session.add(test_user)
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@example.com',
            user_type='admin',
            is_admin=True
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        db.session.commit()
    app.run(debug=True) 