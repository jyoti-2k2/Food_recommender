import os
import subprocess
import sys

def setup_application():
    """Setup the food recommendation application"""
    print("Setting up Mood Food Recommender...")
    
    # Install requirements
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Download images
    print("Downloading food images...")
    try:
        import download_images
        download_images.download_default_images()
    except Exception as e:
        print(f"Note: Could not download images automatically: {e}")
        print("You can manually add food images to the 'images' folder.")
    
    print("\n✅ Setup completed!")
    print("🎯 Run the application with: python main.py")
    print("📁 Make sure these files are in the same folder:")
    print("   - main.py")
    print("   - food_data.json") 
    print("   - images/ folder with food images")

if __name__ == "__main__":
    setup_application()