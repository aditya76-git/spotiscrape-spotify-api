
![Logo](https://i.imgur.com/qtyX2iLh.png)

# SpotiScrape - Unofficial Spotify API on RAPIDAPI
- Unlock Spotify Music Database and seamlessly access and extract music data from Spotify’s vast catalog with SpotiScrape, the ultimate API for developers and music enthusiasts.

- Our API provides a wide range of functionalities to enhance your Spotify experience. Whether you’re a developer building a music application or a music enthusiast looking for advanced features, our API has you covered.




## Details

- Retrieve a curated list of recommended tracks
- Add or remove artists from your library
- Access artist information, which includes Discography, Merchandise, Profile, Related Content, Sharing Info, Stats and Visuals
- Get time-synced lyrics in both timestamp and LRC format
- Retrieve liked songs
- Get top artists and tracks based on your listening pattern
- Obtain playlist information
- Access user profile details, including following and followers information
- Retrieve recently played songs
- Obtain track information
- Get user details

#### Search

```http
POST /search
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `query` | `string` | **Required**. Search Query |  |
| `filter` | `string` | **Optional**. albums, artists, audiobooks, episodes, genre, playlist, podcasts, user. |  |

Retrieves search data based on the provided query.

#### Get Track Info

```http
POST /get-track-info
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `trackID` | `string` | **Required**. trackID of the Spotify Song |  |

Retrieves Track Info

#### Get Credits

```http
POST /get-credits
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `trackID` | `string` | **Required**. trackID of a spotify song |  |

Retrieves credits of a song based on the trackID.

#### Get Recommended Tracks

```http
POST /get-recommended-tracks
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `trackID` | `string` | **Required**. trackID of a spotify song |  |

Retrieves recommended tracks of a based on the trackID.

#### Add Artist To Library

```http
POST /add-artist-to-library
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `sp_dc` | `string` | **Required**. Spotify sp_dc cookie value. | Grab sp_dc cookie value from https://te.legra.ph/How-to-get-Spotify-sp-dc-cookie-07-11 |1
| `artistID` | `string` | **Required**. trackID of a spotify song |  |

Adds artist to your library i.e. follow a artist on Spotify

#### Remove Artist From Library

```http
POST /remove-artist-from-library
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `sp_dc` | `string` | **Required**. Spotify sp_dc cookie value. | Grab sp_dc cookie value from https://te.legra.ph/How-to-get-Spotify-sp-dc-cookie-07-11 |1
| `artistID` | `string` | **Required**. trackID of a spotify song |  |

Removes artist from your library i.e. unfollow a artist on Spotify

#### Get Detailed Artist Info

```http
POST /get-artist-info
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `artistID` | `string` | **Required**. artistID of a spotify song |  |

Retrieves Artist Info based on the artistID.

#### Get Artist Discography

```http
POST /get-artist-info
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `artistID` | `string` | **Required**. artistID of a spotify song |  |
| `filter` | `string` | **Required**. discography |  |

Retrieves Artist Discography Info based on the artistID.

#### Get Artist Merchandise

```http
POST /get-artist-info
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `artistID` | `string` | **Required**. artistID of a spotify song |  |
| `filter` | `string` | **Required**. goods |  |

Retrieves Artist Merchandise Info based on the artistID.

#### Get Artist Profile

```http
POST /get-artist-info
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `artistID` | `string` | **Required**. artistID of a spotify song |  |
| `filter` | `string` | **Required**. profile |  |

Retrieves Artist Profile Info based on the artistID.

#### Get Artist Related Content

```http
POST /get-artist-info
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `artistID` | `string` | **Required**. artistID of a spotify song |  |
| `filter` | `string` | **Required**. relatedContent |  |

Retrieves Artist Related Content Info based on the artistID.

#### Get Artist Info Sharing Info

```http
POST /get-artist-info
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `artistID` | `string` | **Required**. artistID of a spotify song |  |
| `filter` | `string` | **Required**. sharingInfo |  |

Retrieves Artist Sharing Info Info based on the artistID.

#### Get Artist Info Stats

```http
POST /get-artist-info
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `artistID` | `string` | **Required**. artistID of a spotify song |  |
| `filter` | `string` | **Required**. stats |  |

Retrieves Artist Stats Info Info based on the artistID.

#### Get Artist Info Visuals

```http
POST /get-artist-info
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `artistID` | `string` | **Required**. artistID of a spotify song |  |
| `filter` | `string` | **Required**. visuals |  |

Retrieves Artist Visuals Info Info based on the artistID.

#### Get Lyrics

```http
POST /get-lyrics
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `sp_dc` | `string` | **Required**. Spotify sp_dc cookie value. | Grab sp_dc cookie value from https://te.legra.ph/How-to-get-Spotify-sp-dc-cookie-07-11 |1
| `trackID` | `string` | **Required**. trackID of a spotify song |  |

Retrieves Lyrics data based on the trackID

#### Get Liked Songs

```http
POST /get-liked-songs
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `sp_dc` | `string` | **Required**. Spotify sp_dc cookie value. | Grab sp_dc cookie value from https://te.legra.ph/How-to-get-Spotify-sp-dc-cookie-07-11 |1
| `limit` | `string` | **Optional**. Limit value of results, default value is 25 |  |
| `offset` | `string` | **Optional**. Offset value of result, default value is 0 |  |

Retrieves Lyrics data in timestamp or LRC format based on the trackID

#### Get Top Artists

```http
POST /get-top-artists
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `sp_dc` | `string` | **Required**. Spotify sp_dc cookie value. | Grab sp_dc cookie value from https://te.legra.ph/How-to-get-Spotify-sp-dc-cookie-07-11 |1
| `limit` | `string` | **Optional**. Limit value of results, default value is 25 |  |
| `offset` | `string` | **Optional**. Offset value of result, default value is 0 |  |

Retrieves Top Artist data based on the songs Listened by the user

#### Get Top Tracks

```http
POST /get-top-tracks
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `sp_dc` | `string` | **Required**. Spotify sp_dc cookie value. | Grab sp_dc cookie value from https://te.legra.ph/How-to-get-Spotify-sp-dc-cookie-07-11 |1
| `limit` | `string` | **Optional**. Limit value of results, default value is 25 |  |
| `offset` | `string` | **Optional**. Offset value of result, default value is 0 |  |

Retrieves Top Tracks data based on the songs Listened by the user

#### Get Playlist Info

```http
POST /get-playlist-info
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `playlistID` | `string` | **Required**. playlistID of a Spotify Playlist |  |
| `limit` | `string` | **Optional**. Limit value of results, default value is 25 |  |
| `offset` | `string` | **Optional**. Offset value of result, default value is 0 |  |

Retrieves Songs in a Playlist data based on the playlistID

#### Get User Followers Details

```http
POST /get-user-followers-details
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `playlistID` | `string` | **Required**. playlistID of a Spotify Playlist |  |
| `userID` | `string` | **Optional**. UserID of a Spotify User |  |

Retrieves User's Followers data based on the userID, if userID not provided then returns data for the user authenticated with the sp_dc cookie value

#### Get User Following Details

```http
POST /get-user-following-details
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `playlistID` | `string` | **Required**. playlistID of a Spotify Playlist |  |
| `userID` | `string` | **Optional**. UserID of a Spotify User |  |

Retrieves User's Following data based on the userID, if userID not provided then returns data for the user authenticated with the sp_dc cookie value

#### Get Recently Played Songs

```http
POST /get-recently-played-songs
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `sp_dc` | `string` | **Required**. Spotify sp_dc cookie value. | Grab sp_dc cookie value from https://te.legra.ph/How-to-get-Spotify-sp-dc-cookie-07-11 |1
| `limit` | `string` | **Optional**. Limit value of results, default value is 50 |  |
| `offset` | `string` | **Optional**. Offset value of result, default value is 0 |  |

Retrieves User's Recently played songs based on the sp_dc cookie value

#### Get Home Page Details

```http
POST /get-home-page-details
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `sp_dc` | `string` | **Required**. Spotify sp_dc cookie value. | Grab sp_dc cookie value from https://te.legra.ph/How-to-get-Spotify-sp-dc-cookie-07-11 |1
| `timezone` | `string` | **Required**. timezone, example Asia/Calcutta |  |

Retrieves User's Home Page details

#### Get Users Details

```http
POST /get-users-details
```

| Parameter | Type | Description | Help |
| :-------- | :--- | :---------- | :--- |
| `sp_dc` | `string` | **Required**. Spotify sp_dc cookie value. | Grab sp_dc cookie value from https://te.legra.ph/How-to-get-Spotify-sp-dc-cookie-07-11 |1

Retrieves User's details


## Try It Out

- Copyright © 2023 - [SpotiScrape]([https://rapidapi.com/user/conan7612](https://rapidapi.com/conan7612/api/spotiscrape))

## Authors

- Copyright © 2023 - [conan7612](https://rapidapi.com/user/conan7612)
