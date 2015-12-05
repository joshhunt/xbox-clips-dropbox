import os

import xbox
import dropbox
import requests


xbox_email = os.environ.get('XBOX_EMAIL')
xbox_password = os.environ.get('XBOX_PASS')
xbox_gamertag = os.environ.get('XBOX_GAMERTAG')
dropbox_token = os.environ.get('DROPBOX_ACCESS_TOKEN')
dropbox_folder = 'Xbox Clips'

print 'Getting already saved videos from Dropbox...'
dropboxClient = dropbox.client.DropboxClient(dropbox_token)
folder_metadata = dropboxClient.metadata('/' + dropbox_folder)

existing_videos = map(lambda file: file['path'].replace('/{}/'.format(dropbox_folder), '').replace('.mp4', ''), folder_metadata['contents'])
print '...There are {} videos in the {} folder on Dropbox'.format(len(existing_videos), dropbox_folder)

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

    req = requests.post('https://api.dropboxapi.com/1/save_url/auto/{}/{}.mp4'.format(dropbox_folder, clip_id), headers={
      'Authorization': 'Bearer {}'.format(dropbox_token)
    }, data={'url': clip.media_url})

  # print ' - URL: ' + clip.media_url
