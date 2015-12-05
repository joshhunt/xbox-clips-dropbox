import os
import dropbox

app_key = os.environ.get('DROPBOX_KEY')
app_secret = os.environ.get('DROPBOX_SECRET')

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()
access_token, user_id = flow.finish(code)

print '\nAwesome!'
print 'Access token:' + access_token
print 'Save this for clips.py'

dropboxClient = dropbox.client.DropboxClient(access_token)
