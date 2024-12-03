#! python3
# downloads garfield minus garfield

import requests, os, bs4, shutil

#starting URL
url = 'https://garfieldminusgarfield.net/'
#Store comics in \garfield_minus_garfield
os.makedirs('garf_minus_garf', exist_ok=True)

#Site uses different img tags for newer pages
old_tag = 0
message = 0
while not url.endswith('#'):
    #Eventually it will die out so try block is necessary
    try:
    #download the page
        print('Downloading page %s...' % url)
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36' })
        res.raise_for_status()
        #Parse html with beautiful soup
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        #Find the url of the comic image
        if old_tag == 0:
            comicElem = soup.select('div.npf_col img')
        #Update old_tag counter to 1 to move to older html tags
        if comicElem == []:
            print('Could not find comic image.')
            old_tag += 1
        if old_tag == 1:
            comicElem = soup.select('div.photo img')
            if message == 0:
                print('Switching to old style')
                message += 1
        if old_tag == 0:
            #counter
            n = 0
            for imgs in comicElem:
                comicURL = comicElem[int(n)].get('src')
                n += 1
                res = requests.get(comicURL, timeout=20, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36' })
                print('Downloading image %s...' % (comicURL))
                res.raise_for_status()

                #Save image to \garf_minus_garf
                imageFile = open(os.path.join('garf_minus_garf', os.path.basename(comicURL)), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                #input()
        else:
            #counter
            n = 0
            for imgs in comicElem:
                comicURL = comicElem[int(n)].get('src')
                n += 1
                res = requests.get(comicURL, timeout=20, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36' })
                print('Downloading image %s...' % (comicURL))
                res.raise_for_status()

                #Save image to \garf_minus_garf
                imageFile = open(os.path.join('garf_minus_garf', os.path.basename(comicURL)), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
                #input() 
        
        #Get previous comic button URL
        prevLink = soup.select('a[id="next"]')[0]
        url = 'https://garfieldminusgarfield.net' + prevLink.get('href')
        print(url)
    except IndexError as e:
        print(f'An error occured: {e}')
        break
        

path = "garf_minus_garf"
counter = 1
#New name of file
newName = "garf_minus_garf"
#Loop through files in folder
for folderName, subfolders, files in os.walk(path):
    for file in files:
        #create new file name plus the counter
        newFile = newName + "_" + str(counter) + ".png"
        print(newFile)
        counter += 1
        print(f'Renaming "{file}" to "{newFile}"...')
        newFile = os.path.join(path, newFile)
        file = os.path.join(path, file)
        shutil.move(file, newFile)
print('Done')
