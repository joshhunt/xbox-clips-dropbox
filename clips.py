import os

import xbox
import dropbox
import requests

xbox_email = os.environ.get('XBOX_EMAIL')
xbox_password = os.environ.get('XBOX_PASS')
xbox_gamertag = os.environ.get('XBOX_GAMERTAG')
dropbox_token = os.environ.get('DROPBOX_ACCESS_TOKEN')

print 'Getting already saved videos from Dropbox...'
dropboxClient = dropbox.client.DropboxClient(dropbox_token)
folder_metadata = dropboxClient.metadata('/Xbox Clips')

existing_videos = map(lambda file: file['path'].replace('/Xbox Clips/', '').replace('.mp4', ''), folder_metadata['contents'])
print '...There are {} videos in the Xbox Clips on dropbox'.format(len(existing_videos))

print ''
print 'Authenticating to Xbox and getting gamer profile...'
xbox.client.authenticate(login=xbox_email, password=xbox_password)
gt = xbox.GamerProfile.from_gamertag(xbox_gamertag)

print 'Getting clips...'
clips = list(gt.clips())
print '...got {} Xbox clips!'.format(len(clips))

for clip in clips:
  clip_id = clip.clip_id.lower()

  if clip_id in existing_videos:
    foo = 1 # no nothing
  else:
    print 'Saving video to dropbox', clip_id

    req = requests.post('https://api.dropboxapi.com/1/save_url/auto/Xbox Clips/{}.mp4'.format(clip_id), headers={
      'Authorization': 'Bearer {}'.format(dropbox_token)
    }, data={'url': clip.media_url})

  # print ' - URL: ' + clip.media_url
