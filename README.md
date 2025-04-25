# Spotify Playlist Creator

A simple application that creates Spotify playlists from a list of songs. Supports importing songs from CSV, Excel, Word, PDF, and text files.

## Installation

### Option 1: Download the Executable (Recommended for most users)
1. Go to the [Releases page](https://github.com/joeskinner353/spotify-playlist-maker/releases)
2. Download the latest `SpotifyPlaylistCreator.exe`
3. Double-click to run the program

### Option 2: Run from Source Code (For developers)
1. Install Python 3.8 or higher
2. Clone the repository:
   ```bash
   git clone https://github.com/joeskinner353/spotify-playlist-maker.git
   cd spotify-playlist-maker
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the program:
   ```bash
   python spotify_playlist_creator.py
   ```

## First-Time Setup
1. When you first run the program, it will open your web browser
2. Log in to your Spotify account
3. Click "Agree" to authorize the application
4. Return to the application window

## Usage
1. Either:
   - Paste a list of songs (one per line) into the text area
   - Click "Upload File" to import songs from a file
2. Enter a name for your playlist
3. Click "Create Playlist"

## Tips
- For better song matching, include both song name and artist:
  ```
  Shape of You - Ed Sheeran
  Bohemian Rhapsody - Queen
  ```
- Supported file formats:
  - CSV files (.csv)
  - Excel files (.xlsx)
  - Word documents (.docx)
  - PDF files (.pdf)
  - Text files (.txt)

## Updates
The program will automatically check for updates when launched. If an update is available, you'll be prompted to download it.

## Compatibility

### Python Version
This application is tested and compatible with:
- Python 3.8, 3.9, 3.10, 3.11, and 3.12

### Package Dependencies
Specific package versions are required to ensure compatibility:
```
spotipy==2.23.0
numpy==1.24.3
pandas==2.0.3
python-docx==1.0.1
PyPDF2==3.0.1
openpyxl==3.1.2
pyinstaller==6.1.0
```

The application includes built-in dependency checking and will offer to update packages to the required versions if mismatches are detected.

## Troubleshooting
- If you get authentication errors, delete the `.spotify_cache` file in the same directory as the program and try again
- Make sure you have an active internet connection
- For file import issues, check that your file is in one of the supported formats
- If you encounter package compatibility errors, the app should detect them automatically. If manual fixing is required:
  ```bash
  pip install -r requirements.txt --upgrade
  ```

## Development with Docker

1. Clone the repository:
```bash
git clone https://github.com/joeskinner353/spotify-playlist-maker.git
cd spotify-playlist-maker
```

2. Build and run with Docker:
```bash
# Allow Docker to connect to X server (on macOS, need XQuartz running)
xhost +local:docker

# Build and run
docker-compose up --build
```

3. For development, you can mount your local directory:
```bash
docker-compose up
```

This will reflect changes to the code immediately without rebuilding.