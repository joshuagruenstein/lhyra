from imgurpython import ImgurClient

CLIENT_ID = '3fa744e80ad2ae7'
CLIENT_SECRET = '59ba07338b6f4c79d0a9701134051a2bffdb2c95'

images = ["../c++/progress.png", "../c++/relative_plot.png"]

client = ImgurClient(CLIENT_ID, CLIENT_SECRET)

for image in images:
	response = client.upload_from_path(image, anon=True)
	print(response["link"])