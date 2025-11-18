import os
import requests
from PIL import Image
import io

def download_default_images():
    """Download placeholder images from Unsplash"""
    image_urls = {
        'chocolate_ice_cream.jpg': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400&h=300&fit=crop',
        'pizza_margherita.jpg': 'https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=400&h=300&fit=crop',
        'fruit_smoothie_bowl.jpg': 'https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?w=400&h=300&fit=crop',
        'sushi_platter.jpg': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop',
        'mac_cheese.jpg': 'https://images.unsplash.com/photo-1543339312-28c4996f5f27?w=400&h=300&fit=crop',
        'chicken_soup.jpg': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400&h=300&fit=crop',
        'hot_chocolate.jpg': 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400&h=300&fit=crop',
        'mashed_potatoes.jpg': 'https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?w=400&h=300&fit=crop',
        'green_tea.jpg': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=300&fit=crop',
        'dark_chocolate.jpg': 'https://images.unsplash.com/photo-1588196749597-9ff075ee6b5b?w=400&h=300&fit=crop',
        'oatmeal_berries.jpg': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=300&fit=crop',
        'avocado_toast.jpg': 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=400&h=300&fit=crop',
        'banana_smoothie.jpg': 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400&h=300&fit=crop',
        'mixed_nuts.jpg': 'https://images.unsplash.com/photo-1611854778585-e5d6d11b598b?w=400&h=300&fit=crop',
        'energy_bars.jpg': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop',
        'coffee_snack.jpg': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop',
        'default_food.jpg': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop'
    }
    
    # Create images directory
    os.makedirs('images', exist_ok=True)
    
    for filename, url in image_urls.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                image = image.resize((400, 300), Image.Resampling.LANCZOS)
                
                if filename == 'default_food.jpg':
                    image.save(filename)
                else:
                    image.save(f'images/{filename}')
                
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download: {filename}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
    
    print("Image download completed!")

if __name__ == "__main__":
    download_default_images()