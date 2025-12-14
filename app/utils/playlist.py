"""Playlist generation utilities for M3U and XSPF formats."""

import tempfile
from typing import NamedTuple
from urllib.parse import quote

import xspf_lib as xspf
from seedrcc import AsyncSeedr


class PlaylistResult(NamedTuple):
    file_path: str
    filename: str


def generate_playlist_content(tracks: list[dict], playlist_type: str, playlist_title: str) -> bytes:
    """Generates the content of the playlist file."""
    if playlist_type == "xspf":
        track_list = [xspf.Track(location=t["location"], title=t["title"]) for t in tracks]
        playlist = xspf.Playlist(title=playlist_title, trackList=track_list)
        return playlist.xml_string().encode()

    # Default to M3U
    playlist_content = ["#EXTM3U"]
    for track in tracks:
        playlist_content.append(f"#EXTINF:-1,{track['title']}")
        playlist_content.append(track["location"])
    return "\n".join(playlist_content).encode()


async def _recursive_get_tracks(seedr: AsyncSeedr, contents) -> list[dict]:
    """Recursively fetches all playable tracks from a given folder's contents."""
    tracks = []
    # Sort to ensure a consistent order
    files = sorted(contents.files, key=lambda f: f.name)
    folders = sorted(contents.folders, key=lambda f: f.name)

    for file in files:
        if file.play_video or file.play_audio:
            result = await seedr.fetch_file(str(file.folder_file_id))
            if result.url:
                safe_url = quote(result.url, safe="/:&?=%")
                tracks.append({"location": safe_url, "title": result.name})

    for folder in folders:
        sub_contents = await seedr.list_contents(folder_id=str(folder.id))
        tracks.extend(await _recursive_get_tracks(seedr, sub_contents))

    return tracks


async def generate_file_playlist(
    seedr: AsyncSeedr,
    file_id: str,
    playlist_type: str = "m3u",
) -> PlaylistResult | None:
    """Generate playlist for a single file."""
    result = await seedr.fetch_file(file_id)
    if not result.url:
        return None

    safe_url = quote(result.url, safe="/:&?=%")
    tracks = [{"location": safe_url, "title": result.name}]
    playlist_content = generate_playlist_content(tracks, playlist_type, result.name)

    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=f".{playlist_type}") as temp_f:
        temp_f.write(playlist_content)
        return PlaylistResult(file_path=temp_f.name, filename=f"{result.name}.{playlist_type}")


async def generate_folder_playlist(
    seedr: AsyncSeedr,
    folder_id: str,
    playlist_type: str = "m3u",
) -> PlaylistResult | None:
    """Generate playlist for a folder."""
    root_contents = await seedr.list_contents(folder_id=folder_id)
    all_tracks = await _recursive_get_tracks(seedr, root_contents)

    if not all_tracks:
        return None

    playlist_content = generate_playlist_content(all_tracks, playlist_type, root_contents.name)

    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=f".{playlist_type}") as temp_f:
        temp_f.write(playlist_content)
        return PlaylistResult(file_path=temp_f.name, filename=f"{root_contents.name}.{playlist_type}")
