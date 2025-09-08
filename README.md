# Writoria - Where Words Come Alive

Writoria is a full-featured blogging platform built with Django that enables writers to create, share, and engage with content. The platform combines modern design with powerful features to create an immersive writing experience.


## 🌟 Features

### Content Creation
- Rich text editor for writing blog posts
- Support for multiple images in posts with captions
- Category-based post organization
- Draft saving and preview functionality
- Featured image support for posts

### User Engagement
- Heart-based voting system (giving "life" to posts)
- Bookmark system for saving favorite posts
- Nested commenting system with replies
- User profiles with customizable avatars and bios

### Content Discovery
- Category-based filtering
- Full-text search functionality
- Recent posts showcase
- Pagination support
- User-specific post collections

### User Experience
- Responsive design for all devices
- Dark/Light theme toggle
- Animated star background
- Intuitive navigation
- Mobile-friendly interface

### Security & Authentication
- Secure user authentication system
- Protected routes for authenticated users
- CSRF protection
- Secure password handling

### API Integration
- Dual server architecture with Django and Flask
- Flask API handles contact form submissions
- Bidirectional sync between Django and Flask
- CORS enabled for secure cross-origin requests

## 🔧 Technology Stack

- **Backend**: Django 5.2
- **API Server**: Flask with SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development)
- **UI Framework**: Bootstrap 5.3
- **Icons**: Font Awesome 6.0
- **Image Processing**: Pillow
- **Markdown Support**: marked.js
- **API Integration**: requests, flask-cors

## 📁 Project Structure

```
writoria/
├── Django/                 # Django application
│   ├── core/              # Main application
│   │   ├── models.py      # Database models
│   │   ├── views.py       # View controllers
│   │   ├── urls.py        # URL routing
│   │   ├── forms.py       # Form definitions
│   │   ├── admin.py       # Admin interface
│   │   └── services/      # API client services
│   ├── chat/              # Chat functionality
│   ├── static/            # Static files
│   ├── templates/         # HTML templates
│   └── media/             # User-uploaded files
├── Flask/                 # Flask API server
│   └── flask_app/         # Flask application
│       ├── app.py         # API endpoints
│       └── database.db    # SQLite database
├── manage.py              # Django management
└── requirements.txt       # Dependencies
```

## 🔑 Core Models

- **BlogPost**: Main content model with title, content, images, and category
- **UserProfile**: Extended user profile with avatar and bio
- **Comment**: Nested comment system with replies
- **Vote**: Handles the "life" voting system
- **Bookmark**: User's saved posts
- **BlogImage**: Multiple images per post with captions

## 🔌 API Endpoints

### Flask API (localhost:5000)
- `POST /api/contact`
  - Handles contact form submissions
  - Stores messages in Flask database
  - Forwards data to Django API
  - Returns success/error status

### Django API (localhost:8000) 
- `POST /api/contact/`
  - Receives synced contact data from Flask
  - Stores messages in Django database
  - Handles error cases and validation

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## 🌐 Features in Detail

### Blog Post Creation
- Rich text editor with markdown support
- Multiple image upload with drag-and-drop
- Category selection
- Auto-saving drafts
- Custom URLs with slugs

### User System
- Custom user profiles
- Avatar upload
- Bio and website fields
- Activity tracking
- Post management

### Engagement Features
- Heart-based voting ("giving life")
- Nested comments
- Post bookmarking
- User following (coming soon)

## 👥 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ✨ Acknowledgments

- Built with Django and Bootstrap
- Icons by Font Awesome
- Community contributors and feedback 
