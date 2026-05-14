import webbrowser
import requests
import json
from datetime import datetime, timedelta
import os

API_KEY = "FzPCFzpptCiSStuAt7EnNjVeMTUXwjhME9WDbwuD"
APOD_URL = "https://api.nasa.gov/planetary/apod"
FAVORITES_FILE = "nasa_favorites.json"

def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=2)

def display_apod(data):
    print("\n" + "="*60)
    print(f"🌟 {data.get('title', 'Unknown Title').upper()}")
    print("="*60)
    print(f"📅 Date: {data.get('date')}")
    print(f"👨‍🔬 Copyright: {data.get('copyright', 'Public Domain')}")
    print(f"🎬 Media Type: {data.get('media_type', 'image').upper()}")
    print(f"\n📖 {data.get('explanation', 'No description available')}\n")
    
    return data.get("hdurl") or data.get("url")

def fetch_apod(params):
    print("🛰️ Connecting to NASA servers...")
    try:
        response = requests.get(APOD_URL, params=params)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print("❌ Error: Invalid API key.")
        elif response.status_code == 400:
            print("❌ Error: Invalid parameters or date out of range.")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return None

def open_in_browser(url):
    if url:
        confirm = input("\n🌠 Open image in browser? (y/n): ").strip().lower()
        if confirm == 'y':
            webbrowser.open(url)
            print("✅ Opening cosmic view...")
    else:
        print("❌ No media URL available.")

def add_to_favorites(data, favorites):
    favorite = {
        "title": data.get("title"),
        "date": data.get("date"),
        "url": data.get("url"),
        "hdurl": data.get("hdurl"),
        "explanation": data.get("explanation")[:100] + "..."
    }
    favorites.append(favorite)
    save_favorites(favorites)
    print("⭐ Added to favorites!")

def show_favorites(favorites):
    if not favorites:
        print("\n📚 No favorites saved yet.")
        return
    
    print("\n" + "="*60)
    print("⭐ YOUR FAVORITE COSMIC IMAGES")
    print("="*60)
    for i, fav in enumerate(favorites, 1):
        print(f"{i}. {fav['title']} ({fav['date']})")
        print(f"   {fav['explanation']}\n")

def search_range():
    print("\n🔍 Search by Date Range")
    try:
        start = input("Enter start date (YYYY-MM-DD) or press Enter for 7 days ago: ").strip()
        end = input("Enter end date (YYYY-MM-DD) or press Enter for today: ").strip()
        
        if not start:
            start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        if not end:
            end = datetime.now().strftime("%Y-%m-%d")
        
        count = input("How many images? (1-30): ").strip()
        count = int(count) if count and 1 <= int(count) <= 30 else 5
        
        params = {"api_key": API_KEY, "start_date": start, "end_date": end, "count": count}
        
        print(f"📊 Fetching {count} images from {start} to {end}...")
        response = requests.get(APOD_URL, params=params)
        
        if response.status_code == 200:
            images = response.json()
            print(f"\n✅ Found {len(images)} images!")
            
            for i, img in enumerate(images, 1):
                print(f"\n[{i}] {img.get('title')} - {img.get('date')}")
                print(f"    {img.get('explanation', 'N/A')[:80]}...")
            
            return images
        else:
            print("❌ Failed to fetch images.")
            return None
    except ValueError:
        print("❌ Invalid input.")
        return None

def main():
    print("\n" + "🚀"*20)
    print("  🌌 NASA SPACE EXPLORER - INTERACTIVE EDITION 🌌")
    print("🚀"*20)
    
    favorites = load_favorites()
    
    while True:
        print("\n📋 MENU:")
        print("1️⃣  Today's Astronomy Picture")
        print("2️⃣  Search by Specific Date")
        print("3️⃣  Search Date Range (Multiple Images)")
        print("4️⃣  View Favorites")
        print("5️⃣  Exit")
        
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == '1':
            params = {"api_key": API_KEY}
            data = fetch_apod(params)
            if data:
                url = display_apod(data)
                open_in_browser(url)
                if input("\n💾 Save to favorites? (y/n): ").strip().lower() == 'y':
                    add_to_favorites(data, favorites)
        
        elif choice == '2':
            date = input("Enter date (YYYY-MM-DD): ").strip()
            if date:
                params = {"api_key": API_KEY, "date": date}
                data = fetch_apod(params)
                if data:
                    url = display_apod(data)
                    open_in_browser(url)
                    if input("\n💾 Save to favorites? (y/n): ").strip().lower() == 'y':
                        add_to_favorites(data, favorites)
        
        elif choice == '3':
            images = search_range()
            if images:
                view = input("\nView any image? (Enter number or press Enter to skip): ").strip()
                if view and view.isdigit() and 1 <= int(view) <= len(images):
                    data = images[int(view) - 1]
                    url = display_apod(data)
                    open_in_browser(url)
                    if input("\n💾 Save to favorites? (y/n): ").strip().lower() == 'y':
                        add_to_favorites(data, favorites)
        
        elif choice == '4':
            show_favorites(favorites)
        
        elif choice == '5':
            print("\n👋 Thanks for exploring space! See you next time! 🌌")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()