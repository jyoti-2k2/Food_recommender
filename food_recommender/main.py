import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from PIL import Image, ImageTk
import random

class FoodRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍽️ Mood Food Recommender")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f8f9fa')
        
        # Center the window
        self.center_window()
        
        # Load data and images
        self.food_data = self.load_food_data()
        self.food_images = {}
        
        # Current recommendations
        self.current_recommendations = []
        
        # Create GUI
        self.create_widgets()
        
        # Load images in background
        self.root.after(100, self.load_images)
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def load_food_data(self):
        """Load food data from JSON file"""
        try:
            with open('food_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "food_data.json file not found!")
            return {}
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON in food_data.json!")
            return {}
    
    def load_images(self):
        """Load all food images"""
        try:
            for mood_category in self.food_data.values():
                for food in mood_category:
                    image_path = food.get('image', 'default_food.jpg')
                    if os.path.exists(image_path):
                        image = Image.open(image_path)
                        image = image.resize((200, 150), Image.Resampling.LANCZOS)
                        self.food_images[food['name']] = ImageTk.PhotoImage(image)
            
            # Load default image if not already loaded
            if 'default_food.jpg' not in self.food_images and os.path.exists('default_food.jpg'):
                image = Image.open('default_food.jpg')
                image = image.resize((200, 150), Image.Resampling.LANCZOS)
                self.food_images['default'] = ImageTk.PhotoImage(image)
                
        except Exception as e:
            print(f"Error loading images: {e}")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create main container with scrollbar
        main_container = tk.Frame(self.root, bg='#f8f9fa')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_container)
        
        # Mood Selection
        self.create_mood_selection(main_container)
        
        # Preferences
        self.create_preferences(main_container)
        
        # Recommendations Area
        self.create_recommendations_area(main_container)
        
        # Status Bar
        self.create_status_bar(main_container)
    
    def create_header(self, parent):
        """Create application header"""
        header_frame = tk.Frame(parent, bg='#ff6b6b', height=120)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Mood Food Recommender",
            font=('Calisto MT', 28, 'bold'),
            bg='#ff6b6b',
            fg='white',
            pady=10
        )
        title_label.pack(expand=True)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Discover perfect foods that match your current mood!",
            font=('Calisto MT', 12),
            bg='#ff6b6b',
            fg='white'
        )
        subtitle_label.pack(expand=True)
    
    def create_mood_selection(self, parent):
        """Create mood selection section"""
        mood_frame = tk.LabelFrame(
            parent,
            text="🎭 How are you feeling today?",
            font=('Arial', 14, 'bold'),
            bg='#ffffff',
            fg='#2d3436',
            padx=20,
            pady=20
        )
        mood_frame.pack(fill='x', pady=10)
        
        # Mood buttons container
        button_container = tk.Frame(mood_frame, bg='#ffffff')
        button_container.pack(expand=True)
        
        self.mood_var = tk.StringVar()
        
        # Mood descriptions
        mood_descriptions = {
            'happy': {'emoji': '😊', 'desc': 'Joyful & Cheerful'},
            'sad': {'emoji': '😔', 'desc': 'Need Comfort'},
            'stressed': {'emoji': '😰', 'desc': 'Anxious & Overwhelmed'},
            'tired': {'emoji': '😴', 'desc': 'Low Energy'}
        }
        
        # Create mood buttons
        for mood, info in mood_descriptions.items():
            frame = tk.Frame(button_container, bg='#ffffff')
            frame.pack(side='left', padx=15, pady=10)
            
            btn = tk.Radiobutton(
                frame,
                text=f"{info['emoji']} {info['desc']}",
                variable=self.mood_var,
                value=mood,
                font=('Calisto MT', 12, 'bold'),
                bg='#ffffff',
                fg='#2d3436',
                command=self.on_mood_selected,
                cursor='hand2'
            )
            btn.pack()
    
    def create_preferences(self, parent):
        """Create user preferences section"""
        pref_frame = tk.LabelFrame(
            parent,
            text="⚙️ Your Preferences",
            font=('Arial', 14, 'bold'),
            bg='#ffffff',
            fg='#2d3436',
            padx=20,
            pady=20
        )
        pref_frame.pack(fill='x', pady=10)
        
        # Dietary preferences
        tk.Label(
            pref_frame,
            text="Dietary Preferences:",
            font=('Arial', 11, 'bold'),
            bg='#ffffff',
            fg='#2d3436'
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        # Variables for checkboxes
        self.veg_var = tk.BooleanVar()
        self.healthy_var = tk.BooleanVar()
        self.quick_var = tk.BooleanVar()
        self.low_cal_var = tk.BooleanVar()
        
        # Checkboxes
        checkboxes = [
            ("🥬 Vegetarian Options", self.veg_var),
            ("💪 Healthy Choices", self.healthy_var),
            ("⚡ Quick Prep (<15 mins)", self.quick_var),
            ("🔥 Low Calorie (<300 cal)", self.low_cal_var)
        ]
        
        for i, (text, var) in enumerate(checkboxes):
            cb = tk.Checkbutton(
                pref_frame,
                text=text,
                variable=var,
                font=('Arial', 10),
                bg='#ffffff',
                fg='#2d3436',
                cursor='hand2'
            )
            cb.grid(row=1, column=i, sticky='w', padx=10)
        
        # Get Recommendations Button
        self.recommend_btn = tk.Button(
            pref_frame,
            text="🎯 Get Food Recommendations!",
            font=('Arial', 12, 'bold'),
            bg='#00b894',
            fg='white',
            command=self.generate_recommendations,
            state='disabled',
            cursor='hand2',
            padx=20,
            pady=8
        )
        self.recommend_btn.grid(row=2, column=0, columnspan=4, pady=15)
    
    def create_recommendations_area(self, parent):
        """Create recommendations display area"""
        rec_frame = tk.LabelFrame(
            parent,
            text="🍴 Your Recommendations",
            font=('Arial', 14, 'bold'),
            bg='#ffffff',
            fg='#2d3436',
            padx=20,
            pady=20
        )
        rec_frame.pack(fill='both', expand=True, pady=10)
        
        # Create canvas and scrollbar for recommendations
        self.canvas = tk.Canvas(rec_frame, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(rec_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#ffffff')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = tk.Frame(parent, bg='#dfe6e9', height=25)
        status_frame.pack(fill='x', pady=(5, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to recommend! Select your mood to begin.",
            font=('Arial', 9),
            bg='#dfe6e9',
            fg='#2d3436'
        )
        self.status_label.pack(side='left', padx=10)
    
    def on_mood_selected(self):
        """Enable recommend button when mood is selected"""
        self.recommend_btn.config(state='normal', bg='#00b894')
        mood = self.mood_var.get()
        self.status_label.config(text=f"Selected: {mood.capitalize()} mood. Click to get recommendations!")
    
    def generate_recommendations(self):
        """Generate and display food recommendations"""
        mood = self.mood_var.get()
        
        if not mood:
            messagebox.showwarning("Warning", "Please select a mood first!")
            return
        
        # Clear previous recommendations
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get recommendations based on mood
        recommendations = self.food_data.get(mood, [])
        
        if not recommendations:
            messagebox.showerror("Error", f"No recommendations found for {mood} mood!")
            return
        
        # Apply filters
        filtered_recs = self.apply_filters(recommendations)
        self.current_recommendations = filtered_recs
        
        if not filtered_recs:
            messagebox.showinfo("No Results", "No foods match your current filters. Try adjusting your preferences.")
            return
        
        # Display recommendations
        self.display_recommendations(filtered_recs, mood)
        
        # Update status
        self.status_label.config(text=f"Found {len(filtered_recs)} recommendations for {mood} mood!")
    
    def apply_filters(self, recommendations):
        """Apply user preference filters"""
        filtered = recommendations.copy()
        
        # Quick prep filter
        if self.quick_var.get():
            filtered = [food for food in filtered if int(food['prep_time'].split()[0]) <= 15]
        
        # Healthy filter (simple implementation)
        if self.healthy_var.get():
            # Consider foods with reasonable calorie count as healthy
            filtered = [food for food in filtered if int(food['calories']) < 400]
        
        # Low calorie filter
        if self.low_cal_var.get():
            filtered = [food for food in filtered if int(food['calories']) < 300]
        
        # Vegetarian filter (simplified)
        if self.veg_var.get():
            non_veg_keywords = ['chicken', 'fish', 'meat', 'beef', 'pork']
            filtered = [food for food in filtered if not any(keyword in food['ingredients'].lower() for keyword in non_veg_keywords)]
        
        return filtered
    
    def display_recommendations(self, recommendations, mood):
        """Display food recommendations in scrollable area"""
        mood_colors = {
            'happy': '#fff9c4',
            'sad': '#e3f2fd',
            'stressed': '#fce4ec',
            'tired': '#e8f5e8'
        }
        
        card_bg = mood_colors.get(mood, '#ffffff')
        
        for i, food in enumerate(recommendations):
            # Create card for each food
            card_frame = tk.Frame(
                self.scrollable_frame,
                bg=card_bg,
                relief='raised',
                bd=1,
                padx=15,
                pady=15
            )
            card_frame.pack(fill='x', pady=8, padx=5)
            
            # Food content
            self.create_food_card(card_frame, food, i+1, card_bg)
    
    def create_food_card(self, parent, food, index, bg_color):
        """Create a food recommendation card"""
        # Main content frame
        content_frame = tk.Frame(parent, bg=bg_color)
        content_frame.pack(fill='x')
        
        # Left side - Image
        left_frame = tk.Frame(content_frame, bg=bg_color)
        left_frame.pack(side='left', padx=(0, 15))
        
        # Display food image
        food_image = self.food_images.get(food['name'], self.food_images.get('default', None))
        if food_image:
            img_label = tk.Label(left_frame, image=food_image, bg=bg_color)
            img_label.pack()
        else:
            # Placeholder if no image
            placeholder = tk.Label(left_frame, text="🍽️\nNo Image", bg=bg_color, font=('Arial', 8))
            placeholder.pack()
        
        # Right side - Details
        right_frame = tk.Frame(content_frame, bg=bg_color)
        right_frame.pack(side='left', fill='x', expand=True)
        
        # Food name and basic info
        name_frame = tk.Frame(right_frame, bg=bg_color)
        name_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            name_frame,
            text=f"{index}. {food['name']}",
            font=('Arial', 16, 'bold'),
            bg=bg_color,
            fg='#2d3436'
        ).pack(side='left')
        
        # Food type and prep time
        info_text = f"📋 {food['type']} | ⏰ {food['prep_time']} | 🔥 {food['calories']} cal"
        tk.Label(
            name_frame,
            text=info_text,
            font=('Arial', 10),
            bg=bg_color,
            fg='#636e72'
        ).pack(side='left', padx=(15, 0))
        
        # Nutrition info
        nutrition = food.get('nutrition', {})
        if nutrition:
            nutrition_text = f"🍽️ Nutrition: Carbs {nutrition.get('carbs', 'N/A')} | Protein {nutrition.get('protein', 'N/A')} | Fat {nutrition.get('fat', 'N/A')}"
            tk.Label(
                right_frame,
                text=nutrition_text,
                font=('Arial', 9, 'bold'),
                bg=bg_color,
                fg='#0984e3'
            ).pack(anchor='w', pady=(0, 5))
        
        # Reason
        reason_frame = tk.Frame(right_frame, bg=bg_color)
        reason_frame.pack(fill='x', pady=5)
        
        tk.Label(
            reason_frame,
            text="💡 Why it's perfect for you:",
            font=('Arial', 10, 'bold'),
            bg=bg_color,
            fg='#2d3436'
        ).pack(anchor='w')
        
        tk.Label(
            reason_frame,
            text=food['reason'],
            font=('Arial', 9),
            bg=bg_color,
            fg='#2d3436',
            wraplength=600,
            justify='left'
        ).pack(anchor='w')
        
        # Ingredients and tips in two columns
        details_frame = tk.Frame(right_frame, bg=bg_color)
        details_frame.pack(fill='x', pady=5)
        
        # Ingredients column
        ingredients_frame = tk.Frame(details_frame, bg=bg_color)
        ingredients_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Label(
            ingredients_frame,
            text="📝 Ingredients:",
            font=('Arial', 10, 'bold'),
            bg=bg_color,
            fg='#2d3436'
        ).pack(anchor='w')
        
        tk.Label(
            ingredients_frame,
            text=food['ingredients'],
            font=('Arial', 9),
            bg=bg_color,
            fg='#2d3436',
            wraplength=300,
            justify='left'
        ).pack(anchor='w')
        
        # Tips column
        tips_frame = tk.Frame(details_frame, bg=bg_color)
        tips_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        tk.Label(
            tips_frame,
            text="👨‍🍳 Chef's Tip:",
            font=('Arial', 10, 'bold'),
            bg=bg_color,
            fg='#2d3436'
        ).pack(anchor='w')
        
        tk.Label(
            tips_frame,
            text=food['tips'],
            font=('Arial', 9),
            bg=bg_color,
            fg='#2d3436',
            wraplength=300,
            justify='left'
        ).pack(anchor='w')

def main():
    """Main function to run the application"""
    try:
        root = tk.Tk()
        app = FoodRecommenderApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Application Error", f"Failed to start application: {str(e)}")

if __name__ == "__main__":
    main()