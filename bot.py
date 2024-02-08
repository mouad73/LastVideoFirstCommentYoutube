import logging
from datetime import datetime
from google_apis import create_service

# Configure logging
logging.basicConfig(filename='api_logs.txt', level=logging.INFO)

CLIENT_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtubepartner'
]

service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

channel_id = 'UC3TyojVupN-Q09L_-LEX54Q'  # The channel ID for @marouane53Too

# Log the start of the execution
logging.info(f'{datetime.now()} - Execution started')

# Flag to track if a new video has been detected and commented on
new_video_commented = False

try:
    if not new_video_commented:
        # Step 1: Get the uploads playlist ID for the channel
        playlist_response = service.channels().list(part='contentDetails', id=channel_id).execute()
        uploads_playlist_id = playlist_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Step 2: Get the latest video from the uploads playlist
        playlist_items_response = service.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=1  # Fetch only one video, which will be the latest one
        ).execute()

        latest_video_id = playlist_items_response['items'][0]['snippet']['resourceId']['videoId']

        logging.info(f'Latest video ID: {latest_video_id}')


        if latest_video_id == 'b_uQKqMr2KQ':
            logging.info('No new videos')
        else:
            # Step 3: Comment on the latest video
            request_body = {
                'snippet': {
                    'videoId': latest_video_id,
                    'topLevelComment': {
                        'snippet': {
                            'textOriginal': 'First Comment.'
                        }
                    }
                }
            }
            response = service.commentThreads().insert(
                part='snippet',
                body=request_body
            ).execute()
            logging.info(f'{datetime.now()} -  Comment posted successfully')
            logging.info(response)
            new_video_commented = True
    else:
        logging.info(f'{datetime.now()} - Already commented on a new video, skipping video check')
except Exception as e:
    # Log any exceptions that occur
    logging.error(f'An error occurred: {str(e)}')
