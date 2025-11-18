from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_images():
    """Create simple placeholder images for the food recommender"""
    
    # Create images directory
    os.makedirs('images', exist_ok=True)
    
    # Food items and their colors
    food_items = {
        'chocolate_ice_cream': ('Chocolate\nIce Cream', '#8B4513'),
        'pizza_margherita': ('Pizza\nMargherita', '#FF6347'),
        'fruit_smoothie_bowl': ('Fruit\nSmoothie Bowl', '#FF69B4'),
        'sushi_platter': ('Sushi\nPlatter', '#DC143C'),
        'mac_cheese': ('Mac &\nCheese', '#FFD700'),
        'chicken_soup': ('Chicken\nSoup', '#DAA520'),
        'hot_chocolate': ('Hot\nChocolate', '#8B4513'),
        'mashed_potatoes': ('Mashed\nPotatoes', '#F5F5DC'),
        'green_tea': ('Green\nTea', '#32CD32'),
        'dark_chocolate': ('Dark\nChocolate', '#2F4F4F'),
        'oatmeal_berries': ('Oatmeal\nBerries', '#DEB887'),
        'avocado_toast': ('Avocado\nToast', '#9ACD32'),
        'banana_smoothie': ('Banana\nSmoothie', '#FFFF00'),
        'mixed_nuts': ('Mixed\nNuts', '#A0522D'),
        'energy_bars': ('Energy\nBars', '#D2691E'),
        'coffee_snack': ('Coffee &\nSnack', '#8B4513')
    }
    
    for filename, (text, color) in food_items.items():
        # Create a new image with a nice background
        img = Image.new('RGB', (400, 300), color=color)
        draw = ImageDraw.Draw(img)
        
        # Add food emoji
        draw.text((200, 100), "🍽️", fill='white', anchor="mm", font_size=40)
        
        # Add food name
        draw.text((200, 180), text, fill='white', anchor="mm", font_size=20, 
                 stroke_width=1, stroke_fill='black')
        
        # Add decorative border
        draw.rectangle([5, 5, 395, 295], outline='white', width=3)
        
        # Save image
        img.save(f'images/{filename}.jpg')
        print(f"Created: images/{filename}.jpg")
    
    # Create default food image
    default_img = Image.new('RGB', (400, 300), color='#4682B4')
    draw = ImageDraw.Draw(default_img)
    draw.text((200, 150), "🍽️\nFood Image\nNot Available", fill='white', 
             anchor="mm", font_size=24, align='center')
    default_img.save('default_food.jpg')
    print("Created: default_food.jpg")
    
    print("\n✅ All sample images created successfully!")
    print("🎯 You can now run: python main.py")

if __name__ == "__main__":
    create_sample_images()