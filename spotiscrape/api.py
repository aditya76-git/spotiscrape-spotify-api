import requests
from .utils import extract_id, get_timeTag, get_current_timezone, uri_to_gid, find_device_id, time_to_seconds, handle_exception
from .errors import SpotiScrapeError
import json


class GetStreams:
    """
    A class representing streaming information for a media file.

    Attributes:
        pssh (str): The Protection System Specific Header (PSSH) of the media.
        fileID (str): The ID of the media file.
        cdnURL (str): The URL of the Content Delivery Network (CDN) serving the media.

    Methods:
        __init__(pssh, fileID, cdnURL): Initializes a new instance of GetStreams.

    Example:
        pssh = "AAAAU3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAADMIARIQLiuCvgOeQaA7/TDEd2i4hhoHc3BvdGlmeSIULiuCvgOeQaA7/TDEd2i4hqt/m08="
        fileID = "2e2b82be039e41a03bfd30c47768b886ab7f9b4f"
        cdnURL = "https://audio-ak-spotify-com.akamaized.net/audio/2e2b82be039e41a03bfd30c47768b886ab7f9b4f?__token__=exp=1693291307~hmac=f6accdf053ccd5ff9a744a7dfd133d54d048f7a87afe1301c53793d86ea01876"

        streams_info = GetStreams(pssh, fileID, cdnURL)
    """

    def __init__(self, pssh, fileID, cdnURL):
        self.pssh = pssh
        self.fileID = fileID
        self.cdnURL = cdnURL


class DeviceInfo:
    """
    A class representing device information extracted from data.

    Attributes:
        list (dict): A dictionary of device information.
        prev_tracks (dict): A dictionary of previous tracks in the player state.
        next_tracks (dict): A dictionary of next tracks in the player state.
        playback_speed (dict): Playback speed information in the player state.
        playback_quality (dict): Playback quality information in the player state.
        SMARTPHONE_DEVICE_ID (str): The device ID for the smartphone.
        COMPUTER_DEVICE_ID (str): The device ID for the computer.
        ALL_DATA (dict): The complete data used to initialize the device information.
        PRIMARY_DEVICE_ID (str): The device ID of the primary device.
        ACTIVE_DEVICE_ID (str): The active device ID.

    Methods:
        __init__(data): Initializes a new instance of DeviceInfo.

    """

    def __init__(self, data: dict):
        """
        Initializes a new instance of DeviceInfo.

        Args:
            data (dict): The data containing device and player state information.
        """

        self.list = data.get("devices", {})
        self.prev_tracks = data.get("player_state", {}).get("prev_tracks", {})
        self.next_tracks = data.get("player_state", {}).get("next_tracks", {})
        self.playback_speed = data.get(
            "player_state", {}).get("playback_speed", {})
        self.playback_quality = data.get(
            "player_state", {}).get("playback_quality", {})
        self.SMARTPHONE_DEVICE_ID = find_device_id(
            data.get("devices", {}), "SMARTPHONE")
        self.COMPUTER_DEVICE_ID = find_device_id(
            data.get("devices", {}), "COMPUTER")
        self.ALL_DATA = data
        self.PRIMARY_DEVICE_ID = list(self.list.keys())[0]
        self.ACTIVE_DEVICE_ID = data.get("active_device_id", "")
        self.CURRENTLY_PLAYING_TRACK_ID = data.get("player_state", {}).get("context_uri", {}).split(":")[-1]



class SpotiScrape:
    """
    A class for scraping data from the Spotify WEB-API.
    """

    def __init__(self, sp_dc):
        """
        Initializes a new instance of SpotiScrape.

        Args:
            sp_dc (str): The Spotify sp_dc value for authentication.
        """
        self.session = requests.Session()
        self.sp_dc = sp_dc
        self.setup_headers()


    def setup_headers(self):
        self.access_token, self.client_id = self.get_access_token()
        self.client_token = self.get_authorization()
        self.session.cookies.update({'sp_dc': self.sp_dc})
        self.session.headers.update({
            'authorization': f'Bearer {self.access_token}',
            'client-token': self.client_token,
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            ),
            'sec-ch-ua-platform': '"Windows"',
            'referer': 'https://open.spotify.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
        })

    def get_authorization(self):
        """
        Sets up the HTTP headers for the session.

        This method initializes necessary headers for the HTTP session, including access tokens, client tokens, user agent, and other headers.

        """
        
        headers = {
            'authority': 'clienttoken.spotify.com',
            'accept': 'application/json',
            'accept-language': 'en,en-US;q=0.9,en-IN;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://open.spotify.com',
            'referer': 'https://open.spotify.com/',
            'sec-ch-ua': (
                '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"'
            ),
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            ),
        }

        json_data = {
            'client_data': {
                'client_version': '1.2.16.562.g2a214ff8',
                'client_id': self.client_id,
                'js_sdk_data': {
                    'device_brand': 'unknown',
                    'device_model': 'unknown',
                    'os': 'windows',
                    'os_version': 'NT 10.0',
                    'device_id': '00000000000000000000000000000000',
                    'device_type': 'computer',
                },
            },
        }

        response = requests.post(
            'https://clienttoken.spotify.com/v1/clienttoken', headers=headers, json=json_data
        ).json()

        return response['granted_token']['token']

    def get_access_token(self):
        """
        Retrieves the access token and client ID for the session.

        This method sends a request to the Spotify API to obtain the access token and client ID required for authentication and authorization.

        Returns:
            tuple: A tuple containing the access token and client ID.

        Raises:
            SpotiScrapeError: If there's an issue with the request or if unauthorized due to sp_dc cookie value.

        Note:
            The sp_dc value must be set in the session cookies before calling this method.
        """
        self.session.cookies.update({'sp_dc': self.sp_dc})

        headers = {
            'authority': 'open.spotify.com',
            'accept': (
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
            ),
            'accept-language': 'en,en-US;q=0.9,en-IN;q=0.8',
            'cache-control': 'max-age=0',
            'sec-ch-ua': (
                '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"'
            ),
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            ),
        }

        params = {
            'reason': 'transport',
            'productType': 'web_player',
        }

        response = self.session.get(
            'https://open.spotify.com/get_access_token', params=params, headers=headers
        ).json()

        if "error" in response:
            raise SpotiScrapeError("Unauthorized. Check sp_dc cookie value")

        return response['accessToken'], response['clientId']

    def get_track_info(self, trackURL):
        """
        Retrieves information about a track from its URL.

        Args:
            trackURL (str): The URL of the track.

        Returns:
            dict: Information about the track.

        Raises:
            SpotiScrapeError: If there's an issue with retrieving track information or the track URL is invalid.
        """

        trackID = extract_id(trackURL)

        params = {
            'ids': trackID,
            'market': 'from_token',
        }

        response = self.session.get(
            'https://api.spotify.com/v1/tracks', params=params
        ).json()

        if not len(response['tracks']) < 0:
            raise SpotiScrapeError("Error Retriving Track Info. Check Track URL")

        return response['tracks'][0]


    def search(self, query, filter=None):
        """
        Searches for content on Spotify based on the provided query.

        Args:
            query (str): The search query.
            filter (str, optional): The type of filter to apply to the search results. Default is None.

        Returns:
            dict or list: Search results based on the provided filter.

        Raises:
            SpotiScrapeError: If there's an issue with the search or the specified filter is not found.
        """
        params = {
            'operationName': 'searchDesktop',
            'variables': '{{"searchTerm":"{}","offset":0,"limit":10,"numberOfTopResults":5,"includeAudiobooks":true}}'.format(query),
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"130115162add6f3499d2f88ead8a37a7cad1d4d2314f3a206377035e7d26b74c"}}',
        }

        response = self.session.get(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params).json()

        del response['data']['searchV2']['chipOrder']

        if filter:
            if filter in response['data']['searchV2']:

                filtered_dict = {
                    filter: response['data']['searchV2'][filter]
                }
                return filtered_dict

            else:
                raise SpotiScrapeError("Filter {} not Found. Available Filters - {}".format(
                    filter, "topResults, albums, artists, episodes, genres, playlists, podcasts, audiobooks, users"))
        else:
            return response['data']['searchV2']['topResults']['itemsV2']


    def get_poster_url(self, trackURL):
        """
        Retrieves the poster URL for a track.

        Args:
            trackURL (str): The URL of the track.

        Returns:
            str: The URL of the track's poster.

        Raises:
            SpotiScrapeError: If there's an issue retrieving the poster URL or if the track URL is invalid.
        """

        trackID = extract_id(trackURL)
        params = {
            'operationName': 'getTrack',
            'variables': '{{"uri":"spotify:track:{}"}}'.format(trackID),
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"e101aead6d78faa11d75bec5e36385a07b2f1c4a0420932d374d89ee17c70dd6"}}',
        }

        response = self.session.get(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params)
        try:
            response = response.json()
            posterURL = response['data']['trackUnion']['albumOfTrack']['coverArt']['sources'][-1]['url']
            return posterURL
        
        except Exception as e:

            handle_exception(response, e, "Error retrieving Poster URL. Check Track URL or response format.")
        
        

    def get_lyrics(self, trackURL, format=None):
        """
        Retrieves lyrics for a track.

        Args:
            trackURL (str): The URL of the track.
            format (str, optional): The format of the lyrics. Default is None.

        Returns:
            dict: Lyrics information based on the specified format. ("lrc" can be a format)

        Raises:
            SpotiScrapeError: If there's an issue retrieving lyrics or if the track URL is invalid.
        """
        self.session.headers.update({'app-platform': 'WebPlayer'})

        trackID = extract_id(trackURL)
        posterURL = self.get_poster_url(trackURL)

        params = {
            'format': 'json',
            'vocalRemoval': 'false',
            'market': 'from_token',
        }

        posterID = posterURL.split("/")[-1]

        response = self.session.get(
            'https://spclient.wg.spotify.com/color-lyrics/v2/track/{}/image/https%3A%2F%2Fi.scdn.co%2Fimage%2F{}'.format(
                trackID, posterID),
            params=params,
        )

        if format == "lrc":

            try:
                response = response.json()

                new_lines = []

                for lines in response['lyrics']['lines']:
                    new_lines.append({
                        'timeTag': get_timeTag(lines['startTimeMs']),
                        'words': lines['words'],
                        'syllables': lines['syllables']
                    })
                del response['lyrics']['lines']

                response['lyrics']['lines'] = new_lines
                return response
            
            except Exception as e:

                handle_exception(response, e, "Error parsing lyrics format. Check Track URL or response format.")

        else:
            return response.json()

    def get_recommended_tracks(self, trackURL):
        """
        Retrieves recommended tracks based on the given track URL.

        Args:
            trackURL (str): The URL of the track.

        Returns:
            list: Recommended tracks based on the provided track URL.

        Raises:
            SpotiScrapeError: If there's an issue retrieving recommended tracks or if the track URL is invalid.
        """

        trackID = extract_id(trackURL)
        params = {
            'operationName': 'internalLinkRecommenderTrack',
            'variables': '{{"uri":"spotify:track:{}","strategy":"ORGANIC_TRAFFIC"}}'.format(trackID),
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"97f52864d50ba62ab761a7bff47f1a9921d9e357316f7d60ad84ae3788eea4cf"}}',
        }

        response = self.session.get(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params)
        
        try:
            response = response.json()
            return response['data']['seoRecommended']['items']
        except Exception as e:

            handle_exception(response, e, "Error retrieving recommended tracks. Check track URL or response format.")




        
    def get_track_credits(self, trackURL):
        """
        Retrieves credits information for a track.

        Args:
            trackURL (str): The URL of the track.

        Returns:
            dict: Credits information for the provided track URL.

        Raises:
            SpotiScrapeError: If there's an issue retrieving track credits or if the track URL is invalid.
        """
        trackID = extract_id(trackURL)

        self.session.headers.update({'app-platform': 'WebPlayer', })

        response = self.session.get(
            f'https://spclient.wg.spotify.com/track-credits-view/v0/experimental/{trackID}/credits')
        
        try:
            response = response.json()
            return response
        except Exception as e:
            handle_exception(response, e, "Error retrieving recommended tracks. Check track URL or response format.")

   


    def get_artist_info(self, artistURL, filter=None, topTracks=None):
        """
        Retrieves artist information for the given artist URL.

        Args:
            artistURL (str): The URL of the artist.
            filter (str, optional): Filter to narrow down the artist information. Default is None. (Available Filters - discography, goods, profile, relatedContent, sharingInfo, stats, visuals)
            topTracks (bool, optional): Whether to retrieve the artist's top tracks. Default is None.

        Returns:
            dict or list: Artist information based on the provided options.

        Raises:
            SpotiScrapeError: If there's an issue retrieving artist information or if the artist URL is invalid.
        """
        artistID = extract_id(artistURL)

        params = {
            'operationName': 'queryArtistOverview',
            'variables': '{{"uri":"spotify:artist:{}","locale":"","includePrerelease":false}}'.format(artistID),
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"35648a112beb1794e39ab931365f6ae4a8d45e65396d641eeda94e4003d41497"}}',
        }

        response = self.session.get(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params)
        
        try:

            response = response.json()

            if filter:
                if filter in response['data']['artistUnion']:
                    return response['data']['artistUnion'][filter]
                else:
                    raise SpotiScrapeError("Filter not Found in Response")
            elif topTracks == True:
                return response['data']['artistUnion']['discography']['topTracks']
            else:
                return response['data']['artistUnion']
            
        except Exception as e:
            
            handle_exception(response, e, "Error retrieving artist information. Check artist URL or response format.")
            
        


    def get_home_page_info(self):
        """
        Retrieves information about the user's home page.

        Returns:
            dict: Information about the user's home page, including greeting and sections.

        Raises:
            SpotiScrapeError: If there's an issue retrieving home page information.
        """
        self.session.headers.update({'app-platform': 'WebPlayer'})

        time_zone = get_current_timezone()

        params = {
            'operationName': 'home',
            'variables': '{{"timeZone":"{}"}}'.format(time_zone),
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"3099d0901548aa93509318763519c57acd1a0bb533a9793ff57732fe8b91504a"}}',
        }

        data = {

        }

        response = self.session.get(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params)
        
        try:

            response = response.json()

            data['greeting'] = response['data']['home']['greeting']
            data['sections'] = response['data']['home']['sectionContainer']['sections']

        except Exception as e:
            handle_exception(response, e, "Error retrieving home page information. Check response format.")

        return data



    def get_user_details(self):
        """
        Retrieves details of the authenticated user.

        Returns:
            dict: Details of the authenticated user.

        Raises:
            SpotiScrapeError: If there's an issue retrieving user details.
        """
        self.session.headers.update({'app-platform': 'WebPlayer'})

        response = self.session.get('https://api.spotify.com/v1/me')

        try:
            response = response.json()
            return response
        
        except Exception as e:

            handle_exception(response, e, "Error retrieving user details. Check authentication or response status.")




    def get_recently_played(self, offset=0, limit=50):
        """
        Retrieves recently played tracks for the authenticated user.

        Args:
            offset (int, optional): The offset for pagination. Default is 0.
            limit (int, optional): The number of tracks to retrieve. Default is 50.

        Returns:
            dict: Recently played tracks information.

        Raises:
            SpotiScrapeError: If there's an issue retrieving recently played tracks or user details.
        """
        self.session.headers.update({'app-platform': 'WebPlayer'})

        userID = self.get_user_details()['uri'].split(":")[-1]

        params = {
            'format': 'json',
            'filter': 'default,collection-new-episodes',
            'market': 'from_token',
        }

        if offset and limit:
            params['offset'] = str(offset)
            params['limit'] = str(limit)

        else:
            params['offset'] = "0"
            params['limit'] = "50"

        try:

            response = response.json()

            response = self.session.get(
                f'https://spclient.wg.spotify.com/recently-played/v3/user/{userID}/recently-played',
                params=params
            )

        except Exception as e:
            handle_exception(response, e, "Error retrieving user details. Check response format.")



    def get_liked_songs(self, offset=0, limit=25):
        """
        Retrieves liked songs (library tracks) for the authenticated user.

        Args:
            offset (int, optional): The offset for pagination. Default is 0.
            limit (int, optional): The number of tracks to retrieve. Default is 25.

        Returns:
            list: List of liked songs (library tracks) information.

        Raises:
            SpotiScrapeError: If there's an issue retrieving liked songs or if the response format is unexpected.
        """
        self.session.headers.update({'app-platform': 'WebPlayer'})

        params = {
            'operationName': 'fetchLibraryTracks',
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"8474ec383b530ce3e54611fca2d8e3da57ef5612877838b8dbf00bd9fc692dfb"}}',
        }

        if offset and limit:
            params['variables'] = '{{"offset":{},"limit":{}}}'.format(
                offset, limit)


        response = self.session.get(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params)
        
        try:
            response = response.json()

            return response['data']['me']['library']['tracks']
        
        except Exception as e:

            handle_exception(response, e, "Error retrieving liked songs. Check response format.")



    def get_playlist_info(self, playlistURL, offset=0, limit=25):
        """
        Retrieves playlist information for the given playlist URL.

        Args:
            playlistURL (str): URL of the playlist.
            offset (int, optional): The offset for pagination. Default is 0.
            limit (int, optional): The number of tracks to retrieve. Default is 25.

        Returns:
            dict: Playlist information.

        Raises:
            SpotiScrapeError: If there's an issue retrieving playlist information or if the response format is unexpected.
        """
        playlistID = extract_id(playlistURL)

        self.session.headers.update({'app-platform': 'WebPlayer'})

        params = {
            'operationName': 'fetchPlaylist',
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"5534e86cc2181b9e70be86ae26d514abd8d828be2ee56e5f8b7882dd70204c62"}}',
        }

        if offset and limit:
            params['variables'] = '{{"uri":"spotify:playlist:{}","offset":{},"limit":{}}}'.format(
                playlistID, offset, limit)

        response = self.session.get(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params)
        
        try:
            response = response.json()

            return response['data']['playlistV2']

        except Exception as e:

            handle_exception(response, e, "Error retrieving playlist information. Check response format.")



    def get_user_profile_details(self, userURL=None, limit=10):
        """
        Retrieves profile details for the given user URL or authenticated user.

        Args:
            userURL (str, optional): URL of the user's profile. Default is None (authenticated user).
            limit (int, optional): The maximum number of playlists, artists, and episodes to retrieve. Default is 10.

        Returns:
            dict: User profile details.

        Raises:
            SpotiScrapeError: If there's an issue retrieving user profile details or if the response format is unexpected.
        """
        self.session.headers.update({'app-platform': 'WebPlayer'})

        if userURL is None:
            userID = userID = self.get_user_details()['uri'].split(":")[-1]
        else:
            userID = extract_id(userURL)


        params = {
            'market': 'from_token',
        }

        if limit:
            params['playlist_limit'] = str(limit)
            params['artist_limit'] = str(limit)
            params['episode_limit'] = str(limit)

        response = self.session.get(
            f'https://spclient.wg.spotify.com/user-profile-view/v3/profile/{userID}',
            params=params
        )

        try:

            response = response.json()
            return response

        except Exception as e:
            handle_exception(response, e, "Error retrieving user profile details. Check response format.")
    

    def get_top(self, type="tracks", offset=0, limit=10):
        """
        Retrieves the user's top tracks or artists.

        Args:
            type (str, optional): The type of data to retrieve. Either "tracks" or "artists". Default is "tracks".
            offset (int, optional): The index of the first item to return. Default is 0.
            limit (int, optional): The maximum number of items to return. Default is 10.

        Returns:
            dict: User's top tracks or artists.

        Raises:
            SpotiScrapeError: If there's an issue retrieving top tracks or artists or if the response format is unexpected.
        """
        self.session.headers.update({'app-platform': 'WebPlayer'})

        if type is None:
            type = "tracks"

        params = {
            'time_range': 'short_term',
        }

        if limit and offset:
            params['limit'] = str(limit)
            params['offset'] = str(offset)
        else:
            params['offset'] = "0"
            params['limit'] = "10"

        response = self.session.get(
            f'https://api.spotify.com/v1/me/top/{type}', params=params)
        
        try:

            response = response.json()
            return response
        
        except Exception as e:
            handle_exception(response, e, "Error retrieving top tracks or artists. Check response format.")

   


    def get_top_artists(self, offset=0, limit=10):
        """
        Retrieves the user's top artists.

        Args:
            offset (int, optional): The index of the first artist to return. Default is 0.
            limit (int, optional): The maximum number of artists to return. Default is 10.

        Returns:
            dict: User's top artists.

        Raises:
            SpotiScrapeError: If there's an issue retrieving top artists or if the response format is unexpected.
        """
        return self.get_top(type="artists", offset=offset, limit=limit)

    def get_top_tracks(self, offset=0, limit=10):
        """
        Retrieves the user's top tracks.

        Args:
            offset (int, optional): The index of the first track to return. Default is 0.
            limit (int, optional): The maximum number of tracks to return. Default is 10.

        Returns:
            dict: User's top tracks.

        Raises:
            SpotiScrapeError: If there's an issue retrieving top tracks or if the response format is unexpected.
        """
        return self.get_top(type="tracks", offset=offset, limit=limit)

    def get_connections(self, userURL=None, type=None):
        """
        Retrieves user's connections (followings or followers).

        Args:
            userURL (str, optional): URL of the user's profile. If not provided, uses the authenticated user's profile.
            type (str, optional): Type of connections to retrieve. Can be 'following' or 'followers'. Default is 'following'.

        Returns:
            dict: User's connections.

        Raises:
            SpotiScrapeError: If there's an issue retrieving connections or if the response format is unexpected.
        """

        # Set the headers for the session
        self.session.headers.update({'app-platform': 'WebPlayer'})

        if userURL is None:
            userID = self.get_user_details()['uri'].split(":")[-1]
        else:
            userID = extract_id(userURL)

        if type is None:
            type = "following"

        params = {
            'market': 'from_token',
        }

        response = self.session.get(
            f'https://spclient.wg.spotify.com/user-profile-view/v3/profile/{userID}/{type}',
            params=params
        )

        try:

            response = response.json()
            return response
        
        except Exception as e:

            handle_exception(response, e, "Error retrieving user's connections. Check track URL or response format.")


    def artist_operation(self, artistURL, operation_name):
        """
        Perform a specific operation on an artist.

        Args:
            artistURL (str): URL of the artist's profile.
            operation_name (str): Name of the operation to perform, e.g., "addToLibrary" or "removeFromLibrary".

        Returns:
            dict: Response from the artist operation API.

        Raises:
            SpotiScrapeError: If there's an issue with the operation or the response format is unexpected.
        """

        self.session.headers.update({'app-platform': 'WebPlayer'})

        artistID = extract_id(artistURL)

        json_data = {
            'variables': {
                'uris': [
                    'spotify:artist:{}'.format(artistID),
                ],
            },
            'operationName': operation_name,
            'extensions': {
                'persistedQuery': {
                    'version': 1,
                    'sha256Hash': '656c491c3f65d9d08d259be6632f4ef1931540ebcf766488ed17f76bb9156d15' if operation_name == "addToLibrary" else "1103bfd4b9d80275950bff95ef6d41a02cec3357e8f7ecd8974528043739677c",
                },
            },
        }

        response = self.session.post(
            'https://api-partner.spotify.com/pathfinder/v1/query', json=json_data)
        
        try:
            response = response.json()

            return response
        
        except Exception as e:
            handle_exception(response, e, "Error Performing Artist Operation. Check track URL or response format.")


    def follow_artist(self, artistURL):
        """
        Follow an artist.

        Args:
            artistURL (str): URL of the artist's profile.

        Returns:
            str: Confirmation message if the artist is followed successfully.

        Raises:
            SpotiScrapeError: If there's an error while following the artist.
        """
        

        try:
            response = self.artist_operation(artistURL, "addToLibrary")
            return("Artist Followed")

        except Exception as e:

            handle_exception(response, e, "Error Following Artist. Check Artist URL or response format.")
            



    def unfollow_artist(self, artistURL):
        """
        Unfollow an artist.

        Args:
            artistURL (str): URL of the artist's profile.

        Returns:
            str: Confirmation message if the artist is unfollowed successfully.

        Raises:
            SpotiScrapeError: If there's an error while unfollowing the artist.
        """
        try:
            response = self.artist_operation(artistURL, "removeFromLibrary")
            return("Artist UnFollowed")

        except Exception as e:

            handle_exception(response, e, "Error UnFollowing Artist. Check Artist URL or response format.")


    def devices(self):
        """
        Get Devices Connected with the Authenticated Account.

        Args:
            device_id (str): The unique identifier for the device.

        Returns:
            DeviceInfo: An object containing information about the connected device.

        Raises:
            SpotiScrapeError: If there's an error while connecting the device.
        """
        self.session.headers.update(
            {'x-spotify-connection-id': 'Y2FlODljOGUtNDA3Zi00ZTQ2LTk3YjItMDZhYmJlNzA4OWMxK2RlYWxlcit0Y3A6Ly9nYWUyLWRlYWxlci1hLWxjcHMuZ2FlMi5zcG90aWZ5Lm5ldDo1NzAwK0M3QUYyRUNBNUFBNDEwN0ZEQTExODVDMTRGNDhGOTA0NjIxNDc5MDA0RTM4NDBDQjI3RTI0QzdDN0UxMEI3QkM='})

        json_data = {
            'member_type': 'CONNECT_STATE',
            'device': {
                'device_info': {
                    'capabilities': {
                        'can_be_player': False,
                        'hidden': True,
                        'needs_full_player_state': True,
                    },
                },
            },
        }

        response = self.session.put(
            'https://gae2-spclient.spotify.com/connect-state/v1/devices/hobs_1244c7ff01cd7cfcab51e39d2fb5573e71b',
            json=json_data,
        )

        try:
            response = response.json()

            return DeviceInfo(response)
        
        except Exception as e:

            handle_exception(response, e, "Error Retriving Device Info. Check Response Format")

      

    def get_artist_discography_all(self, artistURL, limit=0, offset=50):
        """
        Get the complete discography of an artist.

        Args:
            artistURL (str): The URL of the artist on Spotify.
            limit (int, optional): The maximum number of items to retrieve per request. Default is 0
            offset (int, optional): The offset to start retrieving items. Default is 50

        Returns:
            dict: A dictionary containing the complete discography information of the artist.

        Raises:
            SpotiScrapeError: If there's an error while retrieving the artist's discography.
        """
        self.session.headers.update({'app-platform': 'WebPlayer'})

        artistID = extract_id(artistURL)

        params = {
            'operationName': 'queryArtistDiscographyAll',
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"35a699e12a728c1a02f5bf67121a50f87341e65054e13126c03b7697fbd26692"}}',
        }

        if offset and limit:
            params['variables'] = '{{"uri":"spotify:artist:{}","offset":{},"limit":{}}}'.format(
                artistID, offset, limit)
        else:
            params['variables'] = '{{"uri":"spotify:artist:{}","offset":0,"limit":50}}'.format(
                artistID)

        response = self.session.get(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params)
        
        try:
            response = response.json()

            return response['data']['artistUnion']['discography']
        
        except Exception as e:
            handle_exception(response, e, "Error retrieving artist discography. Check artist URL or response format.")

    def get_track_metadata(self, trackURL):
        """
        Retrieve metadata for a specific track.

        Args:
            trackURL (str): The URL of the track on Spotify.

        Returns:
            dict: A dictionary containing metadata information about the track.

        Raises:
            SpotiScrapeError: If there's an error while retrieving track metadata.
        """
        self.session.headers.update({'accept': 'application/json'})

        trackID = extract_id(trackURL)

        params = {
            'market': 'from_token',
        }

        gid = uri_to_gid(trackID)

        response = self.session.get(
            f'https://spclient.wg.spotify.com/metadata/4/track/{gid}',
            params=params
        )

        try:

            response = response.json()
            return response
        
        except Exception as e:
            handle_exception(response, e, "Error retrieving track metadata. Check track URL or response format.")

    

    def get_cdnURL(self, fileID):
        """
        Retrieve the CDN URL for a given file ID.

        Args:
            fileID (str): The ID of the audio file.

        Returns:
            str: The CDN URL for the audio file.
        """
        params = {
            'version': '10000000',
            'product': '9',
            'platform': '39',
            'alt': 'json',
        }

        response = self.session.get(
            f'https://gae2-spclient.spotify.com/storage-resolve/v2/files/audio/interactive/10/{fileID}',
            params=params,
        )

        try:
            response = response.json()
            return response['cdnurl'][-1]
        
        except Exception as e:

            handle_exception(response, e, "Error retrieving CDN URL. Check track URL or response format.")




    def get_file_id(self, trackURL, format=None):
        """
        Retrieve the file ID for a track's audio file.

        Args:
            trackURL (str): The URL of the track on Spotify.
            format (str, optional): The desired audio format. Defaults to None.

        Returns:
            str: The file ID of the audio file.
        """
        files = self.get_track_metadata(trackURL)['file']
        if format is not None:
            for file in files:
                if file['format'] == format:
                    fileID = file['file_id']
        else:
            for file in files:
                if file['format'] == "MP4_128":
                    fileID = file['file_id']

        return fileID


    def get_pssh(self, fileID):
        """
        Retrieve the PSSH data for a given file ID.

        Args:
            fileID (str): The ID of the audio file.

        Returns:
            str: The PSSH data.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }
        response = requests.get(
            f'https://seektables.scdn.co/seektable/{fileID}.json', headers=headers)
        
        try:
            response = response.json()

            return response['pssh']
        
        except Exception as e:

            handle_exception(response, e, "Error retrieving PSSH. Check track URL or response format.")


    def get_streams(self, trackURL, format=None):
        """
        Get audio stream information for a track.

        Args:
            trackURL (str): The URL of the track on Spotify.
            format (str, optional): The desired audio format. Defaults to None.

        Returns:
            GetStreams: An instance of the GetStreams class containing stream details.
        """
        fileID = self.get_file_id(trackURL, format)
        pssh = self.get_pssh(fileID)
        cdnURL = self.get_cdnURL(fileID)
        return GetStreams(pssh, fileID, cdnURL)

    def add_to_queue(self, trackURL):

        """
        Add a track to the queue.

        Args:
            trackURL (str): The URL of the track to be added.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """

        deviceID = self.devices().ACTIVE_DEVICE_ID if self.devices().ACTIVE_DEVICE_ID.strip() != "" else self.devices().PRIMARY_DEVICE_ID

        trackID = extract_id(trackURL)

        json_data = {
            'command': {
                'track': {
                    'uri': 'spotify:track:{}'.format(trackID),
                    'metadata': {
                        'is_queued': 'true',
                    },
                    'provider': 'queue',
                },
                'endpoint': 'add_to_queue',
            },
        }

        response = self.session.post(
            'https://gae2-spclient.spotify.com/connect-state/v1/player/command/from/{}/to/{}'.format(
                deviceID, deviceID),
            json=json_data,
        )

        try:

            response = response.json()
            return response
        
        except Exception as e:

            handle_exception(response, e, "Error Adding Track to Queue. Check track URL or response format.")
        
    def move_items_in_playlist(self, playlistURL, trackURL, newPosition):
        """
        Move a track within a playlist to a new position.

        Args:
            playlistURL (str): The URL of the playlist.
            trackURL (str): The URL of the track to be moved.
            newPosition (int): The new position for the track.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """
        self.session.headers.update({'app-platform': 'WebPlayer'})

        trackID = extract_id(trackURL)
        playlistID = extract_id(playlistURL)

        complete_playlist_data = self.get_playlist_info(playlistURL)[
            'content']['items']

        trackID_suffix = "track:{}".format(trackID)

        for track in complete_playlist_data:
            item_data = track['itemV2']['data']
            if item_data['uri'].endswith(trackID_suffix):
                track_to_move_uid = track['uid']
                break

        # print(track_to_move_uid)

        new_position_uid = complete_playlist_data[int(newPosition)]['uid']

        # print(new_position_uid)

        json_data = {
            'variables': {
                'playlistUri': 'spotify:playlist:{}'.format(playlistID),
                'uids': [
                    track_to_move_uid,
                ],
                'newPosition': {
                    'moveType': 'BEFORE_UID',
                    'fromUid': new_position_uid,
                },
            },
            'operationName': 'moveItemsInPlaylist',
            'extensions': {
                'persistedQuery': {
                    'version': 1,
                    'sha256Hash': '06f8c6722ac42c1669ba2cf19e44e9bc2caf303255a3ceeed758d4366c76742f',
                },
            },
        }

        response = self.session.post(
            'https://api-partner.spotify.com/pathfinder/v1/query', json=json_data)

        try:

            response = response.json()
            return response
        
        except Exception as e:
            handle_exception(response, e, "Error Moving Track to New Position. Check track URL, playlistURL or response format.")
  

    def reorder_items_in_playlist(self, playlistURL, oldPosition, newPosition):

        """
        Reorder tracks within a playlist.

        Args:
            playlistURL (str): The URL of the playlist.
            oldPosition (int): The current position of the track.
            newPosition (int): The new position for the track.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """

        self.session.headers.update({'app-platform': 'WebPlayer'})

        playlistID = extract_id(playlistURL)

        complete_playlist_data = self.get_playlist_info(playlistURL)[
            'content']['items']

        old_position_uid = complete_playlist_data[int(oldPosition) - 1]['uid']

        new_position_uid = complete_playlist_data[int(newPosition)]['uid']

        # print(new_position_uid)

        json_data = {
            'variables': {
                'playlistUri': 'spotify:playlist:{}'.format(playlistID),
                'uids': [
                    old_position_uid,
                ],
                'newPosition': {
                    'moveType': 'BEFORE_UID',
                    'fromUid': new_position_uid,
                },
            },
            'operationName': 'moveItemsInPlaylist',
            'extensions': {
                'persistedQuery': {
                    'version': 1,
                    'sha256Hash': '06f8c6722ac42c1669ba2cf19e44e9bc2caf303255a3ceeed758d4366c76742f',
                },
            },
        }

        response = self.session.post(
            'https://api-partner.spotify.com/pathfinder/v1/query', json=json_data)
        
        try:
            response = response.json()
            return response
        
        except Exception as e:

            handle_exception(response, e, "Error Reordering Track in Playlist. Check track URL, playlistURL or response format.")



    def liked_songs_operation(self, trackURL, operation_name):

        """
        Perform an operation on liked songs (add or remove).

        Args:
            trackURL (str): The URL of the track.
            operation_name (str): The operation to perform ("addToLibrary" or "removeFromLibrary").

        Returns:
            dict: The JSON response indicating the success of the operation.
        """

        trackID = extract_id(trackURL)

        #operation_name = addToLibrary or removeFromLibrary

        json_data = {
            'variables': {
                'uris': [
                    'spotify:track:{}'.format(trackID),
                ],
            },
            'operationName': operation_name,
            'extensions': {
                'persistedQuery': {
                    'version': 1,
                    'sha256Hash': '1103bfd4b9d80275950bff95ef6d41a02cec3357e8f7ecd8974528043739677c' if operation_name == "removeFromLibrary" else "656c491c3f65d9d08d259be6632f4ef1931540ebcf766488ed17f76bb9156d15",
                },
            },
        }

        response = self.session.post(
            'https://api-partner.spotify.com/pathfinder/v1/query', json=json_data)
        
        try:
            response = response.json()

        except Exception as e:

            handle_exception(response, e, "Error Operating on Liked Songs. Check track URL or response format.")

        return response


    def like_song(self, trackURL):
        """
        Like a song by adding it to your library.

        Args:
            trackURL (str): The URL of the track.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """
        res = self.liked_songs_operation(trackURL, "addToLibrary")

        return res

    def unlike_song(self, trackURL):
        """
        Unlike a song by removing it from your library.

        Args:
            trackURL (str): The URL of the track.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """
        res = self.liked_songs_operation(trackURL, "removeFromLibrary")

        return res

    def remove_track_from_playlist(self, trackURL, playlistURL):
        """
        Remove a track from a playlist.

        Args:
            trackURL (str): The URL of the track to be removed.
            playlistURL (str): The URL of the playlist.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """
        

        playlistID = extract_id(playlistURL)
        trackID = extract_id(trackURL)

        complete_playlist_data = self.get_playlist_info(playlistURL)[
            'content']['items']

        trackID_suffix = "track:{}".format(trackID)

        track_to_remove_uid = ""

        for track in complete_playlist_data:
            item_data = track['itemV2']['data']
            if item_data['uri'].endswith(trackID_suffix):
                track_to_remove_uid += track['uid']
                break

        json_data = {
            'variables': {
                'playlistUri': 'spotify:playlist:{}'.format(playlistID),
                'uids': [
                    track_to_remove_uid,
                ],
            },
            'operationName': "removeFromPlaylist",
            'extensions': {
                'persistedQuery': {
                    'version': 1,
                    'sha256Hash': "c0202852f3743f013eb453bfa15637c9da2d52a437c528960f4d10a15f6dfb49",
                },
            },
        }

        response = self.session.post(
            'https://api-partner.spotify.com/pathfinder/v1/query', json=json_data)

        try:

            response = response.json()
            return response
        
        except Exception as e:

            handle_exception(response, e, "Error Removing Track From Playlist. Check playlist URL or response format.")


    def add_track_to_playlist(self, trackURL, playlistURL, positon=None):

        """
        Add a track to a playlist.

        Args:
            trackURL (str): The URL of the track to be added.
            playlistURL (str): The URL of the playlist.
            positon (str): The position to add the track (TOP, BOTTOM, or None).

        Returns:
            dict: The JSON response indicating the success of the operation.
        """

        if positon not in ["TOP", "BOTTOM", None]:
            raise SpotiScrapeError(
                "Invalid Position Choose from TOP or BOTTOM")

        if positon is None:
            position_suffix = "TOP"
        else:
            position_suffix = positon

        playlistID = extract_id(playlistURL)
        trackID = extract_id(trackURL)

        json_data = {
            'variables': {
                'uris': [
                    'spotify:track:{}'.format(trackID),
                ],
                'playlistUri': 'spotify:playlist:{}'.format(playlistID),
                'newPosition': {
                    'moveType': '{}_OF_PLAYLIST'.format(position_suffix),
                    'fromUid': None,
                },
            },
            'operationName': 'addToPlaylist',
            'extensions': {
                'persistedQuery': {
                    'version': 1,
                    'sha256Hash': '200b7618afd05364c4aafb95e2070249ed87ee3f08fc4d2f1d5d04fdf1a516d9',
                },
            },
        }


        response = self.session.post(
            'https://api-partner.spotify.com/pathfinder/v1/query', json=json_data)
        
        try:
            response = response.json()
            return response

        except Exception as e:

            handle_exception(response, e, "Error Adding Track to Playlist. Check track URL or response format.")

    def edit_playlist_details(self, playlistURL, newTitle, newDescription=None):

        """
        Edit playlist details.

        Args:
            playlistURL (str): The URL of the playlist.
            newTitle (str): The new title for the playlist.
            newDescription (str, optional): The new description for the playlist.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """
        self.session.headers.update({'app-platform': 'WebPlayer'})

        playlistID = extract_id(playlistURL)

        json_data = {
            'deltas': [
                {
                    'ops': [
                        {
                            'kind': 6,
                            'updateListAttributes': {
                                'newAttributes': {
                                    'values': {
                                        'name': newTitle,
                                        'description': newDescription if newDescription is not None else "",
                                        'formatAttributes': [],
                                        'pictureSize': [],
                                    },
                                    'noValue': [],
                                },
                            },
                        },
                    ],
                    'info': {
                        'source': {
                            'client': 5,
                        },
                    },
                },
            ],
            'wantResultingRevisions': False,
            'wantSyncResult': False,
            'nonces': [],
        }

        response = self.session.post(
            'https://spclient.wg.spotify.com/playlist/v2/playlist/{}/changes'.format(playlistID), json=json_data
        )

        try:
            response = response.json()
            return response
        
        except Exception as e:
        
            handle_exception(response, e, "Error Editing Playlist Details. Check playlist URL or response format.")

    def manage_player(self, trackURL, operation_name):
        """
        Manage the player's state (play or pause).

        Args:
            trackURL (str): The URL of the track.
            operation_name (str): The operation to perform ("play" or "pause").

        Returns:
            dict: The JSON response indicating the success of the operation.
        """

        trackID = extract_id(trackURL)

        if operation_name.lower() not in ["play", "pause"]:
            raise SpotiScrapeError(
                "Invalid Operation for Player Choose from pause or play")

        deviceID = self.devices().ACTIVE_DEVICE_ID if self.devices().ACTIVE_DEVICE_ID.strip() != "" else self.devices().PRIMARY_DEVICE_ID

        json_data = {
            'command': {
                'options': {
                    'license': 'on-demand',
                    'skip_to': {
                        'track_index': 0,
                        'track_uri': 'spotify:track:{}'.format(trackID),
                    },
                    'player_options_override': {},
                },
                'endpoint': operation_name,
            },
        }

        response = self.session.post(
            'https://gae2-spclient.spotify.com/connect-state/v1/player/command/from/{}/to/{}'.format(
                deviceID, deviceID),
            json=json_data,
        )

        try:

            response = response.json()
            return response

        except Exception as e:

            handle_exception(response, e, "Error {}ing Player. Check track URL or response format.".format(operation_name))


     

    def play_song(self):
        """
        Play a song on the player.

        Args:
            trackURL (str): The URL of the track.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """
        trackURL = "https://open.spotify.com/track/{}".format(self.devices().CURRENTLY_PLAYING_TRACK_ID)
        res = self.manage_player(trackURL, "play")

        return res

    def pause_song(self):
        """
        Pause a song on the player.

        Args:
            trackURL (str): The URL of the track.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """
        trackURL = "https://open.spotify.com/track/{}".format(self.devices().CURRENTLY_PLAYING_TRACK_ID)
        res = self.manage_player(trackURL, "pause")

        return res

    def pin_playlist(self, playlistURL):
        """
        Pin a playlist to your library.

        Args:
            playlistURL (str): The URL of the playlist.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """
        self.session.headers.update({'app-platform': 'WebPlayer'})

        playlistID = extract_id(playlistURL)

        json_data = {
            'variables': {
                'uri': 'spotify:playlist:{}'.format(playlistID),
            },
            'operationName': 'pinLibraryItem',
            'extensions': {
                'persistedQuery': {
                    'version': 1,
                    'sha256Hash': 'b90ca9015c5e9928a5a14d74fb5fd528255905c8aa607db449097332725caa8b',
                },
            },
        }

        response = self.session.post(
            'https://api-partner.spotify.com/pathfinder/v1/query', json=json_data)
        
        try:
            response = response.json()

        except Exception as e:
            
            handle_exception(response, e, "Error Pining Playlist. Check playlist URL or response format.")



    def unpin_playlist(self, playlistURL):

        """
        Unpin a playlist from your library.

        Args:
            playlistURL (str): The URL of the playlist.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """

        self.session.headers.update({'app-platform': 'WebPlayer'})

        playlistID = extract_id(playlistURL)

        json_data = {
            'variables': {
                'uri': 'spotify:playlist:{}'.format(playlistID),
            },
            'operationName': 'unpinLibraryItem',
            'extensions': {
                'persistedQuery': {
                    'version': 1,
                    'sha256Hash': 'bb5cefe831e624d7d5daa76cf9c2d3bfebb2998a329ce595003cf59740ebd0d4',
                },
            },
        }

        response = self.session.post(
            'https://api-partner.spotify.com/pathfinder/v1/query', json=json_data)
        
        try:
            response = response.json()
            return response
        
        except Exception as e:

            handle_exception(response, e, "Error UnPining Playlist. Check playlist URL or response format.")



    def seek_player(self, seek_to):
        seek_to_sec = time_to_seconds(seek_to)
        json_data = {
            'command': {
                'value': int(seek_to_sec),
                'endpoint': 'seek_to',
            },
        }

        response = self.session.post(
            'https://gae2-spclient.spotify.com/connect-state/v1/player/command/from/14bcc06b67c73b7e662e652c9d74875a606887e1/to/14bcc06b67c73b7e662e652c9d74875a606887e1',
            json=json_data,
        ).json()

        return response

    def enable_repeat(self):
        """
        Enable repeating of the current context (album, playlist, etc.).

        Returns:
            dict: The JSON response indicating the success of the operation.
        """

        deviceID = self.devices().ACTIVE_DEVICE_ID if self.devices().ACTIVE_DEVICE_ID.strip() != "" else self.devices().PRIMARY_DEVICE_ID

        json_data = {
            'command': {
                'repeating_context': True,
                'repeating_track': False,
                'endpoint': 'set_options',
            },
        }

        response = self.session.post(
            'https://gae2-spclient.spotify.com/connect-state/v1/player/command/from/{}/to/{}'.format(
                deviceID, deviceID),
            json=json_data,
        )
        try:

            response = response.json()

            return response
        
        except Exception as e:

            handle_exception(response, e, "Error Enabling Repeat on Player. Check response format.")



    def enable_repeat_one(self):
        """
        Enable repeating of the current track.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """

        deviceID = self.devices().ACTIVE_DEVICE_ID if self.devices().ACTIVE_DEVICE_ID.strip() != "" else self.devices().PRIMARY_DEVICE_ID

        json_data = {
            'command': {
                'repeating_context': True,
                'repeating_track': True,
                'endpoint': 'set_options',
            },
        }

        response = self.session.post(
            'https://gae2-spclient.spotify.com/connect-state/v1/player/command/from/{}/to/{}'.format(
                deviceID, deviceID),
            json=json_data,
        )

        try:

            response = response.json()

            return response
        
        except Exception as e:

            handle_exception(response, e, "Error Enabling Repeat of the current track on Player. Check response format.")


    def disable_repeat(self):
        """
        Disable repeating of both context and track.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """

        deviceID = self.devices().ACTIVE_DEVICE_ID if self.devices().ACTIVE_DEVICE_ID.strip() != "" else self.devices().PRIMARY_DEVICE_ID

        json_data = {
            'command': {
                'repeating_context': False,
                'repeating_track': False,
                'endpoint': 'set_options',
            },
        }

        response = self.session.post(
            'https://gae2-spclient.spotify.com/connect-state/v1/player/command/from/{}/to/{}'.format(
                deviceID, deviceID),
            json=json_data,
        )

        try:

            response = response.json()

            return response
        
        except Exception as e:

            handle_exception(response, e, "Error Disabing Repeat on Player. Check response format.")



    def enable_shuffle(self):
        """
        Enable shuffling of the current context.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """

        deviceID = self.devices().ACTIVE_DEVICE_ID if self.devices().ACTIVE_DEVICE_ID.strip() != "" else self.devices().PRIMARY_DEVICE_ID

        json_data = {
            'command': {
                'value': True,
                'endpoint': 'set_shuffling_context',
            },
        }

        response = self.session.post(
            'https://gae2-spclient.spotify.com/connect-state/v1/player/command/from/{}/to/{}'.format(
                deviceID, deviceID),
            json=json_data,
        )
        
        try:

            response = response.json()

            return response
        
        except Exception as e:

            handle_exception(response, e, "Error Enabling Shuffle on Player. Check response format.")
    
    def disable_shuffle(self):
        """
        Disable shuffling of the current context.

        Returns:
            dict: The JSON response indicating the success of the operation.
        """

        deviceID = self.devices().ACTIVE_DEVICE_ID if self.devices().ACTIVE_DEVICE_ID.strip() != "" else self.devices().PRIMARY_DEVICE_ID

        json_data = {
            'command': {
                'value': False,
                'endpoint': 'set_shuffling_context',
            },
        }

        response = self.session.post(
            'https://gae2-spclient.spotify.com/connect-state/v1/player/command/from/{}/to/{}'.format(
                deviceID, deviceID),
            json=json_data,
        )

        try:

            response = response.json()

            return response
        
        except Exception as e:

            handle_exception(response, e, "Error Disabling Shuffle on Player. Check response format.")
            

    def get_public_playlists(self, userURL=None, offset=0, limit=200):
        """
        Get public playlists of a user.

        Args:
            userURL (str, optional): The URL of the user's profile. If None, gets your playlists.
            offset (int, optional): The offset of playlists to start from. Default is 0
            limit (int, optional): The maximum number of playlists to retrieve. Default is 200

        Returns:
            dict: The JSON response containing the public playlists.
        """

        self.session.headers.update({'app-platform': 'WebPlayer'})

        if userURL is None:
            userID = self.get_user_details()['uri'].split(":")[-1]
        else:
            userID = extract_id(userURL)

        params = {
            'market': 'from_token',
        }

        if offset and limit:
            params['offset'] = str(offset)
            params['limit'] = str(limit)

        else:
            params['offset'] = "0"
            params['limit'] = "200"

        response = self.session.get(
            'https://spclient.wg.spotify.com/user-profile-view/v3/profile/{}/playlists'.format(userID),
            params=params,
        )

        try:
            response = response.json()
            return response
        
        except Exception as e:
            handle_exception(response, e, "Error Getting Public Playlist of USER. Check user URL or response format.")

    def get_account_info(self):

        self.session.headers.update({'app-platform': 'WebPlayer'})

        params = {
            'market': 'from_token',
        }

        response = self.session.get(
            'https://spclient.wg.spotify.com/melody/v1/product_state', params=params)
        
        try:

            response = response.json()
            return response
        
        except Exception as e:

            handle_exception(response, e, "Error retrieving Account Info of Authenticated. Check response format.")


    def get_library(self, offset=0, limit=50):

        """
        Get Libraray Data of the autheticated user's account.

        offset (int, optional): The offset for pagination. Default is 0.
        limit (int, optional): The number of tracks to retrieve. Default is 50.

        Returns:
            dict: The JSON response containing account information.
        """

        self.session.headers.update({'app-platform': 'WebPlayer'})

        params = {
            'operationName': 'libraryV2',
            'variables': '{"filters":[],"order":"Creator","textFilter":"","features":["LIKED_SONGS","YOUR_EPISODES"],"limit":50,"offset":0,"flatten":false,"expandedFolders":[],"folderUri":null,"includeFoldersWhenFlattening":true}',
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"93662a816ebf38ab32f6028512e584c53c4b71d6aad920ce6039a4a62236574e"}}',
        }

        if limit and offset:
            variables_dict = json.loads(params['variables'])
            variables_dict['limit'] = int(limit)
            variables_dict['offset'] = int(offset)

            updated_variables_json = json.dumps(variables_dict)

            params['variables'] = updated_variables_json

        response = self.session.get(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params)
        
        try:
            response = response.json()
            return response
        except Exception as e:
            handle_exception(response, e, "Error retrieving Libraray Data of the autheticated user's account. Check response format.")



    def are_artists_in_library(self, artistURLs):
        """
        Check if artists are in the user's library.

        Args:
            artistURLs (str or list): The URLs of the artists to check. If str provided then split by a + for the urls or else provide a list of artistURLs

        Returns:
            dict: The JSON response indicating whether the tracks are in the library.
        """

        params = {
            'operationName': 'areArtistsInLibrary',
            'variables': '{"uris":[]}',
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"bb7f6d46598f5a2d0148a6418ff148d8613112af87a55c4cb6df33d69acc3038"}}',
        }

        variables_dict = json.loads(params['variables'])

        if isinstance(artistURLs, str):
            artistURLs = artistURLs.split("+")

        additional_uris = artistURLs
        variables_dict['uris'].extend(additional_uris)
        updated_variables_json = json.dumps(variables_dict)
        params['variables'] = updated_variables_json

        data = {
            'data': []
        }

        response = self.session.get(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params)

        try:
            response = response.json()
            for index in range(len(response['data']['artists'])):
                artist_entry = {
                    '__typename': "Artist",
                    'saved': response['data']['artists'][index]['saved'],
                    'id': extract_id(artistURLs[index])
                }
                data['data'].append(artist_entry)

            return data
        
        except Exception as e:

            handle_exception(response, e, "Error Checking If Artists are in Library. Check artist URLs or response format.")

    def are_tracks_in_library(self, trackURLs):

        """
        Check if tracks are in the user's library.

        Args:
            trackURLs (str or list): The URLs of the tracks to check. If str provided then split by a + for the urls or else provide a list of trackURLs

        Returns:
            dict: The JSON response indicating whether the tracks are in the library.
        """

        params = {
            'operationName': 'areTracksInLibrary',
            'variables': '{"uris":[]}',
            'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"2b51d510cac8d1262d8ed3d44af70e45a41b3c4d94c454483e779dcae6dc890e"}}',
        }

        variables_dict = json.loads(params['variables'])

        if isinstance(trackURLs, str):
            trackURLs = trackURLs.split("+")

        additional_uris = trackURLs
        variables_dict['uris'].extend(additional_uris)
        updated_variables_json = json.dumps(variables_dict)
        params['variables'] = updated_variables_json

        data = {
            'data': []
        }

        response = self.session.get(
            'https://api-partner.spotify.com/pathfinder/v1/query', params=params)

        try:

            response = response.json()
            for index in range(len(response['data']['tracks'])):
                artist_entry = {
                    '__typename': "Track",
                    'saved': response['data']['tracks'][index]['saved'],
                    'id': extract_id(trackURLs[index])
                }
                data['data'].append(artist_entry)

            return data
        
        except Exception as e:
            
            handle_exception(response, e, "Error Checking If Tracks are in Library. Check track URL or response format.")

        

