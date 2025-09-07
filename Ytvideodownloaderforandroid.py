from pytubefix import YouTube
import os
import subprocess

def download_to_accessible_location(url):
    """
    Download to Termux internal storage (always accessible)
    Then copy to shared storage manually
    """
    try:
        # Download to Termux internal directory first
        internal_path = os.path.expanduser("~/downloads")
        os.makedirs(internal_path, exist_ok=True)
        
        print("📱 Downloading to internal Termux storage...")
        yt = YouTube(url)
        
        print(f"🎥 Title: {yt.title}")
        
        # Download to internal location
        video_stream = yt.streams.get_highest_resolution()
        downloaded_file = video_stream.download(output_path=internal_path)
        
        print("✅ Downloaded to Termux internal storage!")
        print(f"📁 Location: {downloaded_file}")
        
        # Try to copy to shared storage
        try:
            # Attempt different shared storage paths
            shared_paths = [
                "/sdcard/Download/",
                "/storage/emulated/0/Download/",
                "/storage/self/primary/Download/"
            ]
            
            filename = os.path.basename(downloaded_file)
            
            for shared_path in shared_paths:
                try:
                    if os.path.exists(shared_path):
                        dest_file = os.path.join(shared_path, filename)
                        subprocess.run(['cp', downloaded_file, dest_file], check=True)
                        print(f"✅ Copied to shared storage: {shared_path}")
                        print("👀 Check your Gallery or File Manager!")
                        break
                except:
                    continue
            else:
                print("⚠️  Couldn't copy to shared storage, but file is saved in:")
                print(f"   {downloaded_file}")
                print("💡 You can manually copy it using a file manager")
                
        except Exception as copy_error:
            print("⚠️  File saved to Termux internal storage only")
            print(f"📁 Location: {downloaded_file}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

# Usage
url = input("Enter YouTube URL: ")
download_to_accessible_location(url)
