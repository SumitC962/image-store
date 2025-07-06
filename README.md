# Secure Image Storage Website

A password-protected web application for securely storing and organizing your images with folder-based organization.

## Features

- 🔐 **Password Protection**: Secure access with password authentication
- 📁 **Folder Organization**: Create and manage folders to organize your images
- 📤 **Upload Images**: Drag and drop or browse to upload images
- 📥 **Download Images**: Download individual images or entire folders as ZIP
- 🗑️ **Delete Files**: Remove individual images or entire folders
- 🎨 **Modern UI**: Beautiful, responsive design with drag-and-drop functionality
- 🔒 **Secure**: File validation and secure filename handling

## Supported Image Formats

- PNG
- JPG/JPEG
- GIF
- BMP
- WebP
- TIFF

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Development Installation

1. **Clone or download this project**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the website**:
   - Open your web browser
   - Go to: `http://localhost:5000`
   - Default password: `admin123`

### Production Deployment

#### Option 1: Docker (Recommended)

1. **Build the Docker image**:
   ```bash
   docker build -t secure-image-storage .
   ```

2. **Run the container**:
   ```bash
   docker run -d -p 8000:8000 --name image-storage secure-image-storage
   ```

3. **Access the website**:
   - Go to: `http://localhost:8000`
   - Default password: `admin123`

#### Option 2: Gunicorn

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run with Gunicorn**:
   ```bash
   gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
   ```

3. **Access the website**:
   - Go to: `http://localhost:8000`

## Usage

### First Time Setup

1. Visit `http://localhost:5000`
2. Enter the password: `admin123`
3. Create your first folder
4. Start uploading images!

### Managing Your Images

- **Create Folders**: Use the "Create New Folder" section to organize your images
- **Upload Images**: Select a folder and upload images using the upload area
- **Download Images**: Click the download button next to any image
- **Download All**: Download an entire folder as a ZIP file
- **Delete Images**: Remove individual images or entire folders

### Security Features

- **Password Protection**: Secure bcrypt hashing with rate limiting
- **File Validation**: MIME type checking and secure filename handling
- **Image Optimization**: Automatic compression and resizing
- **Rate Limiting**: Protection against brute force attacks
- **Session Security**: HTTP-only cookies with secure flags
- **Maximum file size limits**: 16MB (configurable)
- **Content Validation**: Ensures uploaded files are actual images

## Customization

### Changing the Password

To change the default password:

1. **Using Environment Variables (Recommended)**:
   ```bash
   export ADMIN_PASSWORD=your_new_password
   ```

2. **Or edit config.py**:
   ```python
   ADMIN_PASSWORD = 'your_new_password'
   ```

3. **Restart the application**

### Changing File Size Limits

To modify the maximum file size:

1. **Using Environment Variables (Recommended)**:
   ```bash
   export MAX_FILE_SIZE=33554432  # 32MB in bytes
   ```

2. **Or edit config.py**:
   ```python
   MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB max file size
   ```

### Adding More Image Formats

To support additional image formats:

1. **Edit config.py**:
   ```python
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff', 'svg'}
   ```

## File Structure

```
PDF_MOD/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── start_production.py    # Production startup script
├── Dockerfile            # Docker containerization
├── .dockerignore         # Docker ignore file
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with styling
│   ├── login.html        # Login page
│   └── index.html        # Main dashboard
├── uploads/              # Image storage directory (created automatically)
└── logs/                 # Application logs (created automatically)
```

## Security Notes

- **Change the default password** before using in production
- **Use environment variables** for sensitive configuration
- **Enable HTTPS** in production environments
- **Regularly backup** your `uploads/` directory
- **Monitor logs** for suspicious activity
- **Use Docker** for isolated deployment
- **Set up rate limiting** to prevent brute force attacks

## Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Make sure you've installed the requirements: `pip install -r requirements.txt`

2. **Permission errors**:
   - Ensure the application has write permissions to create the `uploads/` directory

3. **Port already in use**:
   - Change the port in `app.py` line: `app.run(debug=True, host='0.0.0.0', port=5000)`

4. **Large files not uploading**:
   - Check the `MAX_CONTENT_LENGTH` setting in `app.py`

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please check the troubleshooting section above or create an issue in the project repository. 