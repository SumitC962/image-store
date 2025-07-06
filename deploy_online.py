#!/usr/bin/env python3
"""
Quick Online Deployment Helper
"""

import os
import subprocess
import sys

def check_git():
    """Check if Git is installed"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git():
    """Initialize Git repository"""
    if not os.path.exists('.git'):
        subprocess.run(['git', 'init'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Initial commit'])
        print("✅ Git repository initialized")
    else:
        print("✅ Git repository already exists")

def create_env_file():
    """Create environment file for deployment"""
    env_content = """# Production Environment Variables
SECRET_KEY=your-super-secret-key-change-this-in-production
ADMIN_PASSWORD=your-secure-password-change-this
FLASK_ENV=production
FLASK_DEBUG=False
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Environment file created (.env)")

def main():
    print("🚀 Quick Online Deployment Setup")
    print("=" * 40)
    
    # Check Git
    if not check_git():
        print("❌ Git is not installed. Please install Git first:")
        print("   Download from: https://git-scm.com/downloads")
        return
    
    print("✅ Git is installed")
    
    # Initialize Git
    init_git()
    
    # Create environment file
    create_env_file()
    
    print("\n📋 Next Steps:")
    print("1. Go to https://railway.app/")
    print("2. Sign up with GitHub")
    print("3. Click 'New Project'")
    print("4. Select 'Deploy from GitHub repo'")
    print("5. Connect your repository")
    print("6. Add environment variables:")
    print("   - SECRET_KEY: your-secret-key")
    print("   - ADMIN_PASSWORD: your-password")
    print("7. Deploy!")
    print("\n🌐 Your app will be available at:")
    print("   https://your-app-name.railway.app")
    print("\n📱 You can then access from any device!")

if __name__ == '__main__':
    main() 