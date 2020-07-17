from pytube import YouTube, Playlist
from bs4 import BeautifulSoup
import requests, os

# This is a callback function for the Youtube object when its downloading
def dlprogress(s, c, bytes_left):
    print('Downloading [{:.1f} MB / {:.1f} MB]  {:.2%}'.format((s.filesize - bytes_left)/1000000, s.filesize/1000000,  (s.filesize - bytes_left)/s.filesize), end='\r')

# the core download function that is called by sending the link as parameter v and the directory to save to (optional)
def downloadytvid(v , dir=''):
	yt = YouTube(v, on_progress_callback=dlprogress).streams.filter(progressive=True).get_highest_resolution()
	# print('Downloading:')
	print(yt.title)
	if dir == '':
		savedpath = yt.download()
	else:
		savedpath = yt.download(dir)
	print('\nDownload Complete\nSaved to ', savedpath,'\n---')

def downloadfromfilelist():
	listfile = open("listofvids.txt")
	listofvids = listfile.readlines()
	listdown = []
	for i,v in enumerate(listofvids):
		if 'youtube.com/watch' in v:
			listdown.append(v.strip().split('&',1)[0])
	print(listdown)
	for v in listdown:
		downloadytvid(v)
	print('All Done! Enjoy youtube binging offline!')

def downloadplaylist():
	playlistpage = input('Enter or paste the playlist link:\n=> ')
	print('---')
	playlistpage = playlistpage.strip('\n').strip() + '&disable_polymer=true'
	r = requests.get(playlistpage)
	soup = BeautifulSoup(r.content, 'html.parser')
	
	playlistauthor = soup.select_one('h1', class_='pl-header-title').text.strip()
	playlisttitle = soup.find_all('h1', class_='pl-header-title')[0].text.strip()
	print(playlistauthor, '-', playlisttitle)
	savedir = os.getcwd() + '/' + playlistauthor+ ' - ' + playlisttitle

	results = soup.find(id='content')
	playlistancs = results.find_all('a', class_='pl-video-title-link', href=True)
	for anc in playlistancs:
		downloadytvid(anc['href'], savedir)
	print('All Done! Enjoy your youtube playlist offline!')


if __name__ == "__main__":
	print('\nWelcome to my LazyYoutubeDownloader program!')
	print('What would you like to download?')
	ask = input('[1]Yt Video  [2]Playlist  [3]Filelist of links\n=> ')
	if ask == '1':
		videolink = input('Enter or paste the Youtube video link:\n=> ')
		if 'youtube.com/watch' in videolink:
			downloadytvid(videolink)
		else:
			print('Oops! Not a valid yt link!')
	elif ask == '2':
		print('---')
		downloadplaylist()
	elif ask =='3':
		downloadfromfilelist()
	else:
		print('Sorry wrong input. Only 1 or 2. Try again.')
	print('Brought to you by jakfromspace')