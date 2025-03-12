import tkinter as tk
from tkinter import filedialog, messagebox
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import docx
import PyPDF2
import os
import sys
import requests
from version import VERSION

class SpotifyPlaylistCreator:
    def __init__(self):
        self.version = VERSION
        self.sp = None
        self.check_for_updates()
        
        # Show first-time setup message if .spotify_cache doesn't exist
        if not os.path.exists('.spotify_cache'):
            messagebox.showinfo("First Time Setup",
                "Welcome to Spotify Playlist Creator!\n\n"
                "On the next step, your web browser will open.\n"
                "Please log in to your Spotify account and authorize the application.\n"
                "After authorizing, return to this window.")
        
        self.setup_spotify()
        self.create_gui()

    def check_for_updates(self):
        try:
            # Replace with your GitHub repo API URL
            response = requests.get('https://api.github.com/repos/joeskinner353/spotify-playlist-maker/releases/latest')
            latest_version = response.json()['tag_name']
            
            if latest_version > self.version:
                if messagebox.askyesno("Update Available", 
                    f"Version {latest_version} is available. Current version is {self.version}.\nWould you like to update?"):
                    self.open_download_page()
        except:
            # Silently fail if unable to check for updates
            pass

    def open_download_page(self):
        import webbrowser
        webbrowser.open('https://github.com/joeskinner353/spotify-playlist-maker/releases/latest')

    def setup_spotify(self):
        try:
            # Spotify API credentials
            client_id = 'e33e4e614926406e991d332035699a43'
            client_secret = 'c465ba7b3cb0481c8ce8b6079c34f2d4'
            redirect_uri = 'http://localhost:8888/callback'
            
            scope = 'playlist-modify-public'
            
            # Get the application directory (works for both source and compiled versions)
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            # Set up cache path in the application directory
            cache_path = os.path.join(application_path, '.spotify_cache')
            
            auth_manager = SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope,
                open_browser=True,
                cache_path=cache_path,
                show_dialog=True
            )
            
            # Try to get existing token first
            try:
                token = auth_manager.get_cached_token()
            except:
                token = None
            
            # If no valid token, start new auth flow
            if not token:
                try:
                    token = auth_manager.get_access_token(as_dict=False)
                except Exception as auth_error:
                    messagebox.showerror(
                        "Authentication Error",
                        "Failed to complete authentication. Please try again.\n"
                        "Make sure to complete the Spotify login in your browser."
                    )
                    raise auth_error
            
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            
            # Verify connection by getting current user
            try:
                user = self.sp.current_user()
                if not user:
                    raise Exception("Failed to get user information")
            except Exception as e:
                # If verification fails, clear cache and try again
                if os.path.exists(cache_path):
                    os.remove(cache_path)
                messagebox.showerror(
                    "Authentication Error",
                    "Failed to verify Spotify connection. Please restart the application and try again."
                )
                raise
            
        except Exception as e:
            error_msg = str(e)
            if "No token info" in error_msg:
                error_msg = "Authentication failed. Please try again and make sure to complete the Spotify login process."
            
            messagebox.showerror(
                "Authentication Error",
                f"Failed to authenticate with Spotify. Please try again.\n"
                f"If the problem persists:\n"
                f"1. Delete the .spotify_cache file if it exists\n"
                f"2. Restart the application\n"
                f"3. Make sure to complete the Spotify login in your browser\n\n"
                f"Error: {error_msg}"
            )
            raise  # Re-raise the exception to close the app if authentication fails

    def create_gui(self):
        self.window = tk.Tk()
        self.window.title("Spotify Playlist Creator")
        self.window.geometry("600x400")

        # Text area for manual input
        self.text_label = tk.Label(self.window, text="Paste song list here (one song per line):")
        self.text_label.pack(pady=5)
        
        self.text_area = tk.Text(self.window, height=10, width=50)
        self.text_area.pack(pady=10)

        # File upload button
        self.upload_button = tk.Button(self.window, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=5)

        # Playlist name entry
        self.playlist_label = tk.Label(self.window, text="Enter playlist name:")
        self.playlist_label.pack(pady=5)
        
        self.playlist_entry = tk.Entry(self.window, width=40)
        self.playlist_entry.pack(pady=5)

        # Create playlist button
        self.create_button = tk.Button(self.window, text="Create Playlist", command=self.create_playlist)
        self.create_button.pack(pady=10)

        self.window.mainloop()

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("All Supported Files", "*.csv *.xlsx *.docx *.pdf *.txt"),
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
                ("Word files", "*.docx"),
                ("PDF files", "*.pdf"),
                ("Text files", "*.txt")
            ]
        )
        
        if not file_path:
            return

        songs = self.read_file(file_path)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "\n".join(songs))

    def read_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        songs = []

        try:
            if ext == '.csv':
                df = pd.read_csv(file_path)
                songs = df.iloc[:, 0].tolist()  # Assumes songs are in first column
            elif ext == '.xlsx':
                df = pd.read_excel(file_path)
                songs = df.iloc[:, 0].tolist()
            elif ext == '.docx':
                doc = docx.Document(file_path)
                songs = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
            elif ext == '.pdf':
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        songs.extend(page.extract_text().split('\n'))
            elif ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    songs = file.read().splitlines()
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {str(e)}")
            return []

        return [song.strip() for song in songs if song.strip()]

    def create_playlist(self):
        songs = self.text_area.get(1.0, tk.END).splitlines()
        songs = [song.strip() for song in songs if song.strip()]
        
        if not songs:
            messagebox.showerror("Error", "No songs provided!")
            return

        playlist_name = self.playlist_entry.get().strip()
        if not playlist_name:
            messagebox.showerror("Error", "Please enter a playlist name!")
            return

        try:
            # Create playlist
            user_id = self.sp.current_user()['id']
            playlist = self.sp.user_playlist_create(user_id, playlist_name)
            
            # Search and add songs
            track_uris = []
            not_found = []
            
            for song in songs:
                results = self.sp.search(q=song, type='track', limit=1)
                if results['tracks']['items']:
                    track_uris.append(results['tracks']['items'][0]['uri'])
                else:
                    not_found.append(song)

            if track_uris:
                self.sp.playlist_add_items(playlist['id'], track_uris)

            # Show results
            message = f"Playlist '{playlist_name}' created successfully!\n"
            if not_found:
                message += f"\nCouldn't find these songs:\n" + "\n".join(not_found)
            
            messagebox.showinfo("Success", message)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating playlist: {str(e)}")

if __name__ == "__main__":
    app = SpotifyPlaylistCreator() 