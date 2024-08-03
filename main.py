import yt_dlp
import os
import subprocess

def list_formats(url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        # Print all formats for debugging
        print("All formats extracted:", formats)
        return formats

def filter_video_formats(formats):
    # Filter out audio-only formats
    video_formats = [fmt for fmt in formats if fmt.get('height') is not None]
    return video_formats

def choose_format(formats):
    print("Available video formats:")
    for i, fmt in enumerate(formats):
        format_str = f"{fmt['format_id']}: {fmt['format']} - {fmt.get('height', 'N/A')}p - {fmt.get('tbr', 'N/A')} kbps"
        print(f"{i + 1}. {format_str}")

    choice = int(input("Select a format by number: ").strip()) - 1
    if 0 <= choice < len(formats):
        return formats[choice]['format_id']
    else:
        print("Invalid choice. Defaulting to best format.")
        return None

def download_video_and_audio(url, path='.'):
    # Ensure the output path exists
    if not os.path.exists(path):
        os.makedirs(path)

    # Get available formats
    formats = list_formats(url)
    if not formats:
        print("No formats available.")
        return

    # Filter out video formats
    video_formats = filter_video_formats(formats)
    if not video_formats:
        print("No video formats available.")
        return

    # Let user choose format
    selected_format = choose_format(video_formats)

    # Specify the path to ffmpeg if it's not in the system PATH
    ffmpeg_path = 'C:/ffmpeg/bin/'  # Update this to your actual ffmpeg bin directory

    # yt-dlp options for downloading video and audio separately
    ydl_opts = {
        'format': f'{selected_format}/best',  # Download selected video
        'outtmpl': os.path.join(path, 'video.mp4'),  # Save video as video.mp4
        'noplaylist': True,  # Download a single video
        'verbose': True,  # Verbose output for debugging
        'ffmpeg_location': ffmpeg_path,  # Ensure ffmpeg path is correct
    }

    try:
        print(f"Downloading video from URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"An error occurred while downloading video: {e}")
        return

    ydl_opts['format'] = 'bestaudio/best'  # Download best audio

    try:
        print(f"Downloading audio from URL: {url}")
        ydl_opts['outtmpl'] = os.path.join(path, 'audio.mp4')  # Save audio as audio.mp4
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"An error occurred while downloading audio: {e}")
        return

    # Merge video and audio with ffmpeg
    video_file = os.path.join(path, 'video.mp4')
    audio_file = os.path.join(path, 'audio.mp4')
    output_file = os.path.join(path, 'output.mp4')

    ffmpeg_command = [
        os.path.join(ffmpeg_path, 'ffmpeg.exe'),
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_file
    ]

    try:
        print(f"Merging video and audio into {output_file}")
        subprocess.run(ffmpeg_command, check=True)
        print("Merge completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while merging: {e}")

def main():
    while True:
        print("\nMenu:")
        print("1. Download Video and Audio, then Merge")
        print("2. Exit")

        choice = input("Enter your choice (1/2): ").strip()

        if choice == '1':
            url = input("Enter the video URL: ").strip()
            if url:
                print(f"URL received: {url}")  # Debug: Print the URL
                download_video_and_audio(url)
            else:
                print("URL cannot be empty.")
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
