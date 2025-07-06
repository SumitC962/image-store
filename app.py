from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
from werkzeug.utils import secure_filename
import os
import shutil
from datetime import datetime
import zipfile
from io import BytesIO
import mimetypes
import hashlib

# Try to import optional dependencies
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    FLASK_LIMITER_AVAILABLE = True
except ImportError:
    FLASK_LIMITER_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from passlib.hash import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Initialize rate limiter if available
if FLASK_LIMITER_AVAILABLE:
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
else:
    # Create a dummy limiter decorator
    class DummyLimiter:
        def limit(self, limit_string):
            def decorator(f):
                return f
            return decorator
    limiter = DummyLimiter()

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Password hash
if BCRYPT_AVAILABLE:
    ADMIN_PASSWORD_HASH = bcrypt.hash('admin123')
else:
    # Fallback to SHA256 if bcrypt is not available
    ADMIN_PASSWORD_HASH = hashlib.sha256('admin123'.encode()).hexdigest()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_folder_path(folder_name):
    return os.path.join(UPLOAD_FOLDER, secure_filename(folder_name))

def validate_image_content(file):
    """Validate that the file is actually an image by checking MIME type"""
    if not file or not file.filename:
        return False
    
    # Check file extension
    if not allowed_file(file.filename):
        return False
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(file.filename)
    if not mime_type or not mime_type.startswith('image/'):
        return False
    
    return True

@app.route('/')
def index():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    folders = []
    if os.path.exists(UPLOAD_FOLDER):
        for item in os.listdir(UPLOAD_FOLDER):
            item_path = os.path.join(UPLOAD_FOLDER, item)
            if os.path.isdir(item_path):
                files = [f for f in os.listdir(item_path) if allowed_file(f)]
                folders.append({
                    'name': item,
                    'file_count': len(files),
                    'files': files
                })
    
    return render_template('index.html', folders=folders)

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        password = request.form['password']
        if BCRYPT_AVAILABLE:
            if bcrypt.verify(password, ADMIN_PASSWORD_HASH):
                session['authenticated'] = True
                return redirect(url_for('index'))
            else:
                flash('Invalid password!', 'error')
        else:
            # Fallback to SHA256 verification
            if hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
                session['authenticated'] = True
                return redirect(url_for('index'))
            else:
                flash('Invalid password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/create_folder', methods=['POST'])
def create_folder():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    folder_name = request.form['folder_name'].strip()
    if folder_name:
        folder_path = get_folder_path(folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            flash(f'Folder "{folder_name}" created successfully!', 'success')
        else:
            flash(f'Folder "{folder_name}" already exists!', 'error')
    
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    folder_name = request.form['folder']
    if 'file' not in request.files:
        flash('No file selected!', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(url_for('index'))
    
    if file and validate_image_content(file):
        folder_path = get_folder_path(folder_name)
        if os.path.exists(folder_path):
            filename = secure_filename(file.filename or '')
            # Add timestamp to avoid filename conflicts
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}{ext}"
            
            file_path = os.path.join(folder_path, filename)
            file.save(file_path)
            
            # Compress and optimize image if PIL is available
            if PIL_AVAILABLE:
                try:
                    with Image.open(file_path) as img:
                        # Convert to RGB if necessary
                        if img.mode in ('RGBA', 'LA', 'P'):
                            img = img.convert('RGB')
                        
                        # Resize if too large (max 1920x1080)
                        max_size = (1920, 1080)
                        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                            img.thumbnail(max_size, Image.Resampling.LANCZOS)
                        
                        # Save with optimization
                        img.save(file_path, optimize=True, quality=85)
                        
                except Exception as e:
                    # If image processing fails, keep original file
                    pass
                flash(f'File "{filename}" uploaded and optimized successfully!', 'success')
            else:
                flash(f'File "{filename}" uploaded successfully!', 'success')
        else:
            flash('Invalid folder!', 'error')
    else:
        flash('Invalid file type! Allowed types: ' + ', '.join(ALLOWED_EXTENSIONS), 'error')
    
    return redirect(url_for('index'))

@app.route('/download/<folder_name>/<filename>')
def download_file(folder_name, filename):
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    folder_path = get_folder_path(folder_name)
    file_path = os.path.join(folder_path, filename)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('File not found!', 'error')
        return redirect(url_for('index'))

@app.route('/delete/<folder_name>/<filename>')
def delete_file(folder_name, filename):
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    folder_path = get_folder_path(folder_name)
    file_path = os.path.join(folder_path, filename)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        flash(f'File "{filename}" deleted successfully!', 'success')
    else:
        flash('File not found!', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_folder/<folder_name>')
def delete_folder(folder_name):
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    folder_path = get_folder_path(folder_name)
    
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        flash(f'Folder "{folder_name}" deleted successfully!', 'success')
    else:
        flash('Folder not found!', 'error')
    
    return redirect(url_for('index'))

@app.route('/download_folder/<folder_name>')
def download_folder(folder_name):
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    folder_path = get_folder_path(folder_name)
    
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Create a zip file in memory
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zf.write(file_path, arcname)
        
        memory_file.seek(0)
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'{folder_name}.zip'
        )
    else:
        flash('Folder not found!', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 