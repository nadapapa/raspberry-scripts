import dropbox
import os
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

app_key = config["DROPBOX"]["app_key"]
app_secret = config["DROPBOX"]["app_secret"]


def dropboxAuth():
    accessTokenFileOverwrite = open("accessToken.txt", "w+")

    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    # Have the user sign in and authorize this token
    authorize_url = flow.start()
    print('1. Go to: ' + authorize_url)
    print('2. Click "Allow" (you might have to log in first)')
    print('3. Copy the authorization code.')
    code = input("Enter the authorization code here: ").strip()

    try:
        # This will fail if the user enters an invalid authorization code
        access_token, user_id = flow.finish(code)
        accessTokenFileOverwrite.write(access_token)
    except:
        print("failed authorization, restart")
        accessTokenFileOverwrite.close()
        os.remove("accessToken.txt")

    accessTokenFileOverwrite.close()


def dropboxUpload(fileToUpload):
    if not os.path.isfile("accessToken.txt"):
        dropboxAuth()

    # get access token from file
    accessTokenFileRead = open("accessToken.txt", "r")
    access_token = accessTokenFileRead.read().rstrip()
    accessTokenFileRead.close()

    # make client
    client = dropbox.client.DropboxClient(access_token)

    # upload file
    fileToUploadObject = open(fileToUpload, "rb")
    response = client.put_file(fileToUpload, fileToUploadObject)
    fileToUploadObject.close()

if __name__ == "__main__":
    import sys
    sys.exit(dropboxUpload(sys.argv[1]))