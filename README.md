# YouTube Downloader 🎬

After messing around with music and media projects, I decided to make a **YouTube Downloader** using **Python**, **PyQt5**, and **yt-dlp**.
This lets you search YouTube videos directly from the app, preview thumbnails, and download audio, video, or both in different formats.

## How it works
1. Type a search query in the search bar and hit **Search**.
2. The app fetches 4 results from YouTube and displays their thumbnails and titles.
3. Click the download button under a thumbnail to download in your chosen format:
   - **Video only** → mp4/webm
   - **Audio only** → mp3/opus
   - **Video + Audio** → mp4/webm
4. Format options are selectable via the menu, and the app ensures only one format/action is active at a time.

## What I learned while making it
- **Integrating YouTube Data API v3** for search results.
- **Using yt-dlp** for flexible media downloading with format selection.
- **Dynamic thumbnail loading** and scaling with QPixmap.
- **Qt menu and checkbox logic** for mutually exclusive selections.

## Dependencies
```bash
pip install -r requirements.txt
```
This app also needs **FFmpeg**, please make sure you have it in your path.

## Files
- `youtubedownloader_ui.py` → UI code generated in Qt Designer
- `youtubedownloader.pyw` → Main downloader logic
- `requirements.txt` → All the required dependencies

## Note 📝
This one might actually get updates or bugfixes in the future since I’m planning on actively using it.
