import PyInstaller.__main__
import os
import shutil
from version import VERSION

# Clean previous builds
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

PyInstaller.__main__.run([
    'spotify_playlist_creator.py',
    '--onefile',
    '--windowed',
    '--name=SpotifyPlaylistCreator',
    '--add-data=version.py:.',
    '--icon=icon.ico',  # Add an icon file if you have one
])

# Copy version file to dist directory
shutil.copy('version.py', 'dist/version.py') 