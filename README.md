

![Logo](https://i.imgur.com/qtyX2iLh.png)
<div style="text-align:center;">
  <a href="https://github.com/aditya76-git">aditya76-git</a> /
  <a href="https://github.com/aditya76-git/spotiscrape-spotify-api">spotiscrape-spotify-api</a>
</div>

<br />

<!-- <img src="https://i.imgur.com/y3L6XfN.png" align="right" /> -->

# SpotiScrape - SPOTIFY API
Unlock Spotify Music Database and seamlessly access and extract music data from Spotify’s vast catalog with SpotiScrape, the ultimate API for developers and music enthusiasts.

Access Account Information, User Details, Search Content, Manipulate Playlists, Control Player, Get Track and Playlist Information all with SpotiScrape



## 📋Details

- 👤 ACCOUNT INFORMATION
  - [Get Account Data](#get-account-data)
- 🏠 USER LIBRARY
  - [Get Home Page Data](#get-home-page-data)
  - [Get Library Data](#get-library-data)
- 🧑 USER
  - [Get User Profile Details](#get-user-profile-details)
  - [Get Top Artists](#get-top-artists)
  - [Get Top Tracks](#get-top-tracks)
  - [Get Connections (Followings or Followers)](#get-connections)
  - [Check if artist(s) are in the user's library](#check-artists)
  - [Check if track(s) are in the user's library](#check-tracks)
- 🎵 TRACK
  - [Get Track Info](#get-track-info)
  - [Get Poster URL](#get-poster-url)
  - [Get Recommended Tracks](#get-recommended-tracks)
  - [Get Track Metadata](#get-track-metadata)
  - [Get Streaming URL, PSSH, fileID of Track](#get-streaming-data)
  - [Get Track Credits](#get-track-credits)
- 🔍 SEARCH
  - [Get Search Info](#get-search-info)
- 🎶 LYRICS
  - [Get Lyrics Info](#get-lyrics-info)
- 🎤 ARTIST
  - [Get Artist Info](#get-artist-info)
  - [Get Artist Discography](#get-artist-discography)
  - [Follow Artist](#follow-artist)
  - [UnFollow Artist](#unfollow-artist)
- 🎧 PLAYER
  - [Get Recently Played](#get-recently-played)
  - [Get Liked Songs](#get-liked-songs)
  - [Add to Queue](#add-to-queue)
  - [Like Song](#like-song)
  - [UnLike Song](#unlike-song)
  - [Play Song](#play-song)
  - [Pause Song](#pause-song)
  - [Enable Repeat On Player](#enable-repeat)
  - [Enable Repeat of Current Track On Player](#enable-repeat-one)
  - [Disable Repeat On Player](#disable-repeat)
  - [Enable Shuffle on Player](#enable-shuffle)
  - [Disable Shuffle on Player](#disable-shuffle)
  - [Get Devices Info](#get-device-info)
- 📃 PLAYLIST
  - [Get Playlist Info](#get-playlist-info)
  - [Move Items in Playlist](#move-items-in-playlist)
  - [Re-Order Items in Playlist](#reorder-items-in-playlist)
  - [Add Track to Playlist](#add-track-to-playlist)
  - [Remove Track from Playlist](#remove-track-from-playlist)
  - [Pin Playlist](#pin-playlist)
  - [UnPin Playlist](#unpin-playlist)
  - [List Public Playlists of a User](#list-public-playlist)
  - [Edit Playlist Details](#edit-playlist-details)


## ⚠️ Disclaimer

Please note that the `spotiscrape` package is provided as-is and is not officially endorsed or supported by `Spotify`. While we have taken care to ensure that the package interacts with the Spotify API in a secure and compliant manner, we cannot guarantee the safety of your Spotify account.

By using the `spotiscrape` package, you acknowledge and agree that you are responsible for any actions taken with your Spotify account, and you use the package at your own risk. We recommend using the package responsibly

We are not liable for any potential consequences that may arise from using the `spotiscrape` package, including but not limited to `account suspension`, `data loss`, or any other `issues` related to your `Spotify` account.

It's important to exercise `caution` and ensure that you keep your `sensitive information`, such as the `sp_dc` cookie, `private` and `secure`. If you have any concerns or questions, please refer to the documentation or seek assistance from the community.







## ⚙️Installation

Open your terminal or command prompt and enter the following command:



```bash
pip install git+https://github.com/aditya76-git/spotiscrape-spotify-api@main
```
> **Note:** To use spotiscrape you need to have a Active Spotify Account 

## 🚀Initialization

To get started, you need to initialize an instance of the `SpotiScrape` class by passing your Spotify DC Cookie as an argument. Make sure to replace `"YOUR_SPOTIFY_DC_COOKIE"` with your actual `Spotify DC Cookie`.


```python3
spotify = SpotiScrape("YOUR_SPOTIFY_DC_COOKIE")
```

## 🔍 How to Find sp_dc cookie?

- `sp_dc` cookie is required to authenticate against `Spotify` in order to have access to the required services.
- Using any extensions like `Cookie-Editor` can easily help you find it
- [Extension Link - Chrome WEB Store](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

![Finding the sp_dc Cookie Value](https://camo.githubusercontent.com/d71ac89c29072c5e913e78900892a918030cfe9d1fe7bc1c1f9a00d59a0d39ae/68747470733a2f2f696b2e696d6167656b69742e696f2f67797a766c6177647a2f50726f6a656374732f7379726963732f6f734e587537373537485f4c70654830726650512e706e67 "Finding the sp_dc Cookie Value")


> **Note:** While cookies can contain sensitive information, the sp_dc cookie value is required for authentication and direct communication with the Spotify API within the scope of this open-source project. Rest assured that your sp_dc cookie will not be sent to any external server; it is solely used for interacting with Spotify's services through the project's codebase. However, caution is advised when sharing this cookie value outside the context of this project, as it could potentially lead to unauthorized access to your Spotify account.


## 👤ACCOUNT INFORMATION
#### <a id="get-account-data"></a>➡️ Get Account Data

```python3
spotify.get_account_info()
```


Get Account Information of the authenticated User

## 🏠USER LIBRARY
#### <a id="get-home-page-data"></a>➡️ Get Home Page Data

```python3
spotify.get_home_page_info()
```

Retrieves information about the user's home page.

#### <a id="get-library-data"></a>➡️ Get Library Data

```python3
spotify.get_library(offset=0, limit=20)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `offset` | `int` | **Optional**. The offset for pagination. Default is 0. |0  |
| `limit` | `int` | **Optional**. The number of tracks to retrieve. Default is 50. |20  |

Get Libraray Data of the autheticated user's account.

## 🧑USER


#### <a id="get-user-profile-details"></a>➡️ Get User Profile Details

```python3
spotify.get_user_profile_details(userURL="https://open.spotify.com/user/31m4en72cpcracygwoxaiitbr2ba", limit=10)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `userURL` | `string` | **Optional**. URL of the user's profile. Default is None (authenticated user). |  https://open.spotify.com/user/31m4en72cpcracygwoxaiitbr2ba or None|
| `limit` | `int` | **Optional**. The maximum number of playlists, artists, and episodes to retrieve. Default is 10. | 5 |

Retrieves profile details for the given user URL or authenticated user.

#### <a id="get-top-artists"></a>➡️ Get Top Artists

```python3
spotify.get_top_artists(offset=0, limit=10)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `offset` | `int` | **Optional**. The offset for pagination. Default is 0. |0  |
| `limit` | `int` | **Optional**. The number of tracks to retrieve. Default is 10. |5  |

Retrieves the authenticated user's top Artists.

#### <a id="get-top-tracks"></a>➡️ Get Top Tracks

```python3
spotify.get_top_tracks(offset=0, limit=10)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `offset` | `int` | **Optional**. The offset for pagination. Default is 0. |0  |
| `limit` | `int` | **Optional**. The number of tracks to retrieve. Default is 10. |5  |

Retrieves the authenticated user's top Tracks.

#### <a id="get-connections"></a>➡️ Get Connections (Followings or Followers)

```python3
spotify.get_connections(userURL="https://open.spotify.com/user/31m4en72cpcracygwoxaiitbr2ba" , type="following")
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `userURL` | `str` | **Optional**. URL of the user's profile. If not provided, uses the authenticated user's profile. | https://open.spotify.com/user/31m4en72cpcracygwoxaiitbr2ba  |
| `type` | `str` | **Optional**. Type of connections to retrieve. Can be 'following' or 'followers'. Default is 'following'. |followers  |

Retrieves user's connections (followings or followers).

#### <a id="check-artists"></a>➡️ Check if artist(s) are in the user's library.
Check if you are following the artists or not

```python3
spotify.are_artists_in_library(artistURLs)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `artistURLs` | `str` | **Required**. The URLs of the artists to check. If str provided then split by a + for the urls or else provide a list of artistURLs | https://link1.com/1+https://link1.com/2  |

Check if artists are in the user's library.

#### <a id="check-tracks"></a>➡️ Check if track(s) are in the user's library.
Check if you liked the songs or not

```python3
spotify.are_tracks_in_library(trackURLs)
```


| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURLs` | `str` | **Required**. The URLs of the tracks to check. If str provided then split by a + for the urls or else provide a list of artistURLs | https://link1.com/1+https://link1.com/2  |


Check if tracks are in the user's library.
## 🎵TRACK
#### <a id="get-track-info"></a>➡️ Get Track Info

```python3
spotify.get_track_info(trackURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURL` | `str` | **Required**. Spotify Track URL | https://open.spotify.com/track/3taCbWWTilb7eNMsAzOBq4

Retrieves information about a track from its URL.

#### <a id="get-poster-url"></a>➡️ Get Poster URL

```python3
spotify.get_poster_url(trackURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURL` | `str` | **Required**. trackURL of a spotify song | https://open.spotify.com/track/3taCbWWTilb7eNMsAzOBq4 |

Retrieves the poster URL for a track.

#### <a id="get-recommended-tracks"></a>➡️ Get Recommended Tracks

```python3
spotify.get_recommended_tracks(trackURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURL` | `str` | **Required**. trackURL of a spotify song. | https://open.spotify.com/track/3taCbWWTilb7eNMsAzOBq4 |

Retrieves recommended tracks based on the given track URL.

#### <a id="get-track-metadata"></a>➡️ Get Track Metadata

```python3
spotify.get_track_metadata(trackURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURL` | `str` | **Required**. trackURL of a spotify song. | https://open.spotify.com/track/3taCbWWTilb7eNMsAzOBq4 |

Retrieve metadata for a specific track.

#### <a id="get-streaming-data"></a>➡️ Get Streaming URL, PSSH, fileID of Track

```python3
spotify.get_streams(trackURL, format="MP4_128").fileID
```
```python3
spotify.get_streams(trackURL, format="MP4_128").cdnURL
```
```python3
spotify.get_streams(trackURL, format="MP4_128").fileID
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURL` | `str` | **Required**. trackURL of a spotify song. | https://open.spotify.com/track/3taCbWWTilb7eNMsAzOBq4 |
| `format` | `str` | **Optional**. Default is MP4_128 (128Kbps Audio)| MP4_128 |

Retrieve Streaming URL, PSSH, fileID of Track

#### <a id="get-track-credits"></a>➡️ Get Track Credits

```python3
spotify.get_track_credits(trackURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURL` | `str` | **Required**. trackURL of a spotify song. | https://open.spotify.com/track/3taCbWWTilb7eNMsAzOBq4 |

Retrieves credits information for a track.

## 🔍SEARCH
#### <a id="get-search-info"></a>➡️ Search

```python3
spotify.search(query, filter="artists")
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `query` | `str` | **Required**. Query to search for | Ed Sheeran |
| `filter` | `str` | **Optional**. The type of filter to apply to the search results. Default is None. Can be topResults, albums, artists, episodes, genres, playlists, podcasts, audiobooks, users | artists |

Searches for content on Spotify based on the provided query.
## 🎶LYRICS
#### <a id="get-lyrics-info"></a>➡️ Get Lyrics

```python3
spotify.get_lyrics(trackURL, format="lrc")
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURL` | `str` | **Required**. trackURL of a spotify song | https://open.spotify.com/track/3taCbWWTilb7eNMsAzOBq4 |
| `format` | `str` or `None` | **Optional**. format to get lyrics timestamp in | None or lrc |

Retrieves lyrics for a track.


## 🎤ARTIST
#### <a id="get-artist-info"></a>➡️ Get Artist Info

```python3
spotify.get_artist_info(artistURL, filter="profile")
spotify.get_artist_info(artistURL, topTracks=True)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `artistURL` | `str` | **Required**. artistURL of a Spotify Artist |https://open.spotify.com/artist/00FQb4jTyendYWaN8pK0wa  |
| `filter` | `str` | **Optional**. Filter to narrow down the artist information. |discography, goods, profile, relatedContent, sharingInfo, stats, visuals  |
| `topTracks` | `bool` | **Optional**. Whether to retrieve the artist's top tracks. Default is None.  |True|

Note: filter and topTracks can't be applied at the same time
Retrieves artist information for the given artist URL.

#### <a id="get-artist-discography"></a>➡️ Get Artist Discography

```python3
spotify.get_artist_discography_all(artistURL, limit=0, offset=50)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `artistURL` | `str` | **Required**. artistURL of a Spotify Artist |https://open.spotify.com/artist/00FQb4jTyendYWaN8pK0wa  |
| `offset` | `int` | **Optional**. The offset for pagination. Default is 0. |0  |
| `limit` | `int` | **Optional**. The number of tracks to retrieve. Default is 50. |20  |



Retrieves the complete discography of an artist.

#### <a id="follow-artist"></a>➡️ Follow Artist

```python3
spotify.follow_artist(artistURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `artistURL` | `str` | **Required**. artistURL of a spotify Artist | https://open.spotify.com/artist/00FQb4jTyendYWaN8pK0wa  |

Follow an artist.

#### <a id="unfollow-artist"></a>➡️ UnFollow Artist

```python3
spotify.unfollow_artist(artistURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `artistURL` | `str` | **Required**. artistURL of a spotify Artist | https://open.spotify.com/artist/00FQb4jTyendYWaN8pK0wa  |

UnFollow an artist.

## 🎧PLAYER
#### <a id="get-recently-played"></a>➡️ Get Recently Played

```python3
spotify.get_recently_played(offset=0, limit=50)
```
| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `offset` | `int` | **Optional**. The offset for pagination. Default is 0. |0  |
| `limit` | `int` | **Optional**. The number of tracks to retrieve. Default is 50. |20  |

Retrieves recently played tracks for the authenticated user.

#### <a id="get-liked-songs"></a>➡️ Get Liked Songs

```python3
spotify.get_liked_songs(offset=0, limit=50)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `offset` | `int` | **Optional**. The offset for pagination. Default is 0. |0  |
| `limit` | `int` | **Optional**. The number of tracks to retrieve. Default is 50. |20  |

Retrieves liked songs for the authenticated user.


#### <a id="add-to-queue"></a>➡️ Add to Queue

```python3
spotify.add_to_queue(trackURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `artistURL` | `str` | **Required**. trackURL of a spotify Track | https://open.spotify.com/track/3taCbWWTilb7eNMsAzOBq4  |

Add a track to the queue.

#### <a id="like-song"></a>➡️ Like Song

```python3
spotify.like_song(trackURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURL` | `str` | **Required**. trackURL of a spotify Track | https://open.spotify.com/track/6MlIIJwO4FxnOlrpOrS4hU  |

Like a Song

#### <a id="unlike-song"></a>➡️ UnLike Song

```python3
spotify.unlike_song(trackURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURL` | `str` | **Required**. trackURL of a spotify Track | https://open.spotify.com/track/6MlIIJwO4FxnOlrpOrS4hU  |

UnLike a Song

#### <a id="play-song"></a>➡️ Play Song

```python3
spotify.play_song()
```

Play/Resume currently playing song on the player.

#### <a id="pause-song"></a>➡️ Pause Song

```python3
spotify.pause_song()
```

Pause currently playing song on the player.

#### <a id="enable-repeat"></a>➡️ Enable Repeat On Player

```python3
spotify.enable_repeat()
```


Enable repeating of the current context

#### <a id="enable-repeat-one"></a>➡️ Enable Repeat of Current Track On Player

```python3
spotify.enable_repeat_one()
```

Enable repeating of the current track.

#### <a id="disable-repeat"></a>➡️ Disable Repeat On Player

```python3
spotify.disable_repeat()
```

Disable repeating.

#### <a id="enable-shuffle"></a>➡️ Enable Shuffle on Player

```python3
spotify.enable_shuffle()
```

Enable shuffling of the current context.

#### <a id="disable-shuffle"></a>➡️ Disable Shuffle on Player

```python3
spotify.disable_shuffle()
```

Disable shuffling of the current context.


#### <a id="get-device-info"></a>➡️ Devices

```python3
spotify.devices().prev_tracks
```
```python3
spotify.devices().next_tracks
```
```python3
spotify.devices().playback_speed
```
```python3
spotify.devices().playback_quality
```

Get Devices Connected with the Authenticated Account and other Information like `list`, `prev_tracks`, `next_tracks`, `playback_speed`, `playback_quality`, `SMARTPHONE_DEVICE_ID`, `COMPUTER_DEVICE_ID`, `ALL_DATA`, `PRIMARY_DEVICE_ID`, `ACTIVE_DEVICE_ID`

## 📃PLAYLIST

#### <a id="get-playlist-info"></a>➡️ Get Playlist Info

```python3
spotify.get_playlist_info(playlistURL, offset=0, limit=20)
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `playlistURL` | `string` | **Required**. playlistURL of a spotify Playlist | https://open.spotify.com/playlist/33P0GdndkqEel2IgwNwb9F |
| `offset` | `int` | **Optional**. The offset for pagination. Default is 0. |0  |
| `limit` | `int` | **Optional**. The number of tracks to retrieve. Default is 25. |20  |

Retrieves playlist information for the given playlist URL.

#### <a id="move-items-in-playlist"></a>➡️ Move Items in Playlist

```python3
spotify.move_items_in_playlist(playlistURL, trackURL, 5)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `playlistURL` | `str` | **Required**. playlistURL of a spotify Playlist | https://open.spotify.com/playlist/33P0GdndkqEel2IgwNwb9F  |
| `trackURL` | `str` | **Required**. trackURL of a spotify track to be moved | https://open.spotify.com/track/6MlIIJwO4FxnOlrpOrS4hU  |
| `newPosition` | `int` | **Required**. The new position for the track | https://open.spotify.com/track/6MlIIJwO4FxnOlrpOrS4hU  |

Move a track within a playlist to a new position.

#### <a id="reorder-items-in-playlist"></a>➡️ Re-Order Items in Playlist

```python3
spotify.reorder_items_in_playlist(playlistURL, 1, 5)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `playlistURL` | `str` | **Required**. playlistURL of a spotify Playlist | https://open.spotify.com/playlist/33P0GdndkqEel2IgwNwb9F  |
| `oldPosition` | `int` | **Required**. The current position of the track | 1  |
| `newPosition` | `int` | **Required**. The new position for the track | 5  |

Reorder tracks within a playlist.


#### <a id="add-track-to-playlist"></a>➡️ Add Track to Playlist

```python3
spotify.add_track_to_playlist(trackURL, playlistURL, position="TOP")
```

```python3
spotify.add_track_to_playlist(trackURL, playlistURL, position="BOTTOM")
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURL` | `str` | **Required**. trackURL of a spotify Track  to be added | https://open.spotify.com/track/6MlIIJwO4FxnOlrpOrS4hU  |
| `playlistURL` | `str` | **Required**. playlistURL of a spotify Track | https://open.spotify.com/playlist/33P0GdndkqEel2IgwNwb9F  |
| `position` | `str` | **Required**. The position to add the track (TOP, BOTTOM, or None) Defaults to TOP | BOTTOM  |

Add a track to a playlist. (TOP or BOTTOM - Defaults to TOP)


#### <a id="remove-track-from-playlist"></a>➡️ Remove Track from Playlist

```python3
spotify.remove_track_from_playlist(trackURL, playlistURL)
```


| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `trackURL` | `str` | **Required**. trackURL of a spotify Track to be removed | https://open.spotify.com/track/6MlIIJwO4FxnOlrpOrS4hU  |
| `playlistURL` | `str` | **Required**. playlistURL of a spotify Track | https://open.spotify.com/playlist/33P0GdndkqEel2IgwNwb9F  |

Remove a track from a playlist.

#### <a id="pin-playlist"></a>➡️ Pin Playlist

```python3
spotify.pin_playlist(playlistURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `playlistURL` | `str` | **Required**. playlistURL of a spotify Track | https://open.spotify.com/playlist/33P0GdndkqEel2IgwNwb9F  |

Pin a playlist to your library.

#### <a id="unpin-playlist"></a>➡️ UnPin Playlist

```python3
spotify.unpin_playlist(playlistURL)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `playlistURL` | `str` | **Required**. playlistURL of a spotify Track | https://open.spotify.com/playlist/33P0GdndkqEel2IgwNwb9F  |

Unpin a playlist from your library.

#### <a id="list-public-playlist"></a>➡️ List Public Playlists of a User

```python3
spotify.get_public_playlists(userURL="https://open.spotify.com/user/31m4en72cpcracygwoxaiitbr2ba" , offset=0, limit=10)
```

| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `userURL` | `str` | **Required**. The URL of the user's profile. If None, gets authenticated User Public Playlists | https://open.spotify.com/user/31m4en72cpcracygwoxaiitbr2ba or None  |
| `offset` | `int` | **Optional**. The offset for pagination. Default is 0. |0  |
| `limit` | `int` | **Optional**. The maximum number of playlists to retrieve. Default is 200 |20  |

Get public playlists of a user.

#### <a id="edit-playlist-details"></a>➡️ Edit Playlist Details

```python3
spotify.edit_playlist_details(playlistURL, newTitle, newDescription="New Description Edited Using Spotiscrape")
```

```python3
spotify.edit_playlist_details(playlistURL, newTitle)
```


| Parameter | Type | Description | Example |
| :-------- | :--- | :---------- | :--- |
| `playlistURL` | `str` | **Required**. playlistURL of a spotify Track | https://open.spotify.com/playlist/33P0GdndkqEel2IgwNwb9F  |
| `newTitle` | `str` | **Required**. The new title for the playlist. | PHONK  |
| `newDescription` | `str` or `None` | **Optional**. The new description for the playlist. | New Description Edited Using Spotiscrape Default to Blank  |

Edit playlist details.

## 🌟 Show Your Support

- If you find this project useful or interesting, please consider giving it a star on GitHub. It's a simple way to show your support and help others discover the project.


![Github Stars](https://img.shields.io/github/stars/aditya76-git/spotiscrape-spotify-api?style=social "Github Stars")

## 👨‍💻Developement

Thank you for your interest in contributing to this project! There are several ways you can get involved:

- **Opening Issues**: If you encounter a bug, have a feature request, or want to suggest an improvement, please open an issue. We appreciate your feedback!
- **Cloning the Project**: To work on the project locally, you can clone the repository by running:
```bash
git clone https://github.com/aditya76-git/spotiscrape-spotify-api.git
```
- **Sending Pull Requests**: If you'd like to contribute directly to the codebase, you can fork the repository, make your changes, and then send a pull request. We welcome your contributions!




## 💻Authors

- Copyright © 2023 - [aditya76-git](https://github.com/aditya76-git) / [spotiscrape-spotify-api](https://github.com/aditya76-git/spotiscrape-spotify-api)
