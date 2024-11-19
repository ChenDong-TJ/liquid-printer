import os
import glob

def count_images():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_dir = os.path.dirname(script_dir)
    # Look for PNG files in the downloads directory
    downloads_dir = os.path.expanduser("~/Downloads")
    pattern = os.path.join(downloads_dir, "pixel-art-*.png")
    
    # Count matching files
    image_files = glob.glob(pattern)
    count = len(image_files)
    
    print(f"Found {count} pixel art images in downloads folder")
    
    # Print the list of files
    if count > 0:
        print("\nImage files:")
        for file in image_files:
            print(f"- {os.path.basename(file)}")

if __name__ == "__main__":
    count_images()