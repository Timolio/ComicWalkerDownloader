import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm
from colorama import Fore, Style, init

def fetch_episode_details(url):
    # Запрос HTML-контента
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    })
    response.raise_for_status()
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
    if not script_tag:
        raise ValueError("JSON script tag not found")

    json_data = json.loads(script_tag.string)
    title = json_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['work']['title']
    latest_episodes = json_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['firstEpisodes']['result']

    current_episode_code = json_data['query']['episodeCode']

    episodes_data = {
        'episodes': []
    }

    for ep in latest_episodes:
        episodes_data['episodes'].append({
            'episode_no': ep['internal']['episodeNo'],
            'id': ep.get('id'),
            'title': ep.get('title'),
            'manga_title': title
        })
        if ep.get('code') == current_episode_code:
            episodes_data['current_ep'] = ep['internal']['episodeNo']

    return episodes_data

def download_and_decrypt_image(url, drm_hash, output_path):
    """
    Download and decrypt an image from the given URL.
    :param url: URL of the image to download.
    :param drm_hash: DRM hash to decrypt the image.
    :param output_path: Path to save the decrypted image.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        encrypted_data = response.content
        decrypted_data = bytes([b ^ drm_hash[i % len(drm_hash)] for i, b in enumerate(encrypted_data)])

        with open(output_path, "wb") as f:
            f.write(decrypted_data)
    else:
        print(Fore.RED + f"[ERROR] Failed to download image. HTTP Status Code: {response.status_code}" + Style.RESET_ALL)

def download_episode_pages(episode_id, manga_title, chapter_no):
    """
    Download all pages of a specific episode.
    :param episode_id: ID of the episode to download.
    :param manga_title: Title of the manga.
    :param chapter_no: Chapter number.
    """
    data = requests.get(
        f'https://comic-walker.com/api/contents/viewer?episodeId={episode_id}&imageSizeType=width%3A768',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }
    ).json()

    if not data.get("manuscripts"):
        print(Fore.RED + "[ERROR] No pages available for chapter {chapter_no}" + Style.RESET_ALL)
        return

    manga_folder = f"{manga_title.replace(' ', '_')}"
    chapter_folder = os.path.join(manga_folder, f"Chapter_{chapter_no}")

    if not os.path.exists(chapter_folder):
        os.makedirs(chapter_folder)
    
    pages = data["manuscripts"]
    for page in tqdm(pages, desc=f"Downloading", unit="page", colour="CYAN"):
        drm_hash = bytes.fromhex(page["drmHash"])
        url = page["drmImageUrl"]
        page_number = page["page"]
        output_path = os.path.join(chapter_folder, f"page_{page_number}.webp")
        download_and_decrypt_image(url, drm_hash, output_path)
    
    return chapter_folder

def download_chapter(base_url, chapter_no):
    """
    Download a specific chapter by its number.
    :param base_url: Base URL to fetch episode details.
    :param chapter_no: Chapter number to download.
    """
    ep_data = fetch_episode_details(base_url)
    eps = ep_data.get('episodes')
    if not eps:
        print(Fore.RED + "[ERROR] No episodes found" + Style.RESET_ALL)
        return
    
    if chapter_no is None:
        chapter_no = ep_data.get('current_ep')

    for ep in eps:
        if ep['episode_no'] == chapter_no:
            print(Fore.GREEN + f"[INFO] Manga Title: \"{ep['manga_title']}\"" + Style.RESET_ALL)
            print(Fore.GREEN + f"[INFO] Chapter Title: \"{ep['title']}\"" + Style.RESET_ALL)

            # Confirm download
            print(Fore.YELLOW + f"\n[CONFIRMATION] Downloading {ep['title']} of \"{ep['manga_title']}\"." + Style.RESET_ALL)

            file_path = download_episode_pages(ep['id'], ep['manga_title'], ep['episode_no'])

            # Success message
            print(Fore.GREEN + "\n[SUCCESS] Download complete!" + Style.RESET_ALL)
            print(Fore.GREEN + f"[INFO] File saved to: {file_path}" + Style.RESET_ALL)
            return
    
    print(f"Chapter {chapter_no} not found.")

if __name__ == "__main__":
    init()
    print(Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + "          COMIC WALKER DOWNLOADER v1.0" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print()

    while True:
        # Step 1: Get the chapter url
        print(Fore.GREEN + "[INFO] Please provide the link to the chapter:" + Style.RESET_ALL)
        url = input(Fore.WHITE + "> " + Style.RESET_ALL)

        # Step 2: Get the chapter number
        print(Fore.GREEN + "\n[INFO] Enter the chapter number to download (Leave blank for the current chapter):" + Style.RESET_ALL)
        chapter_input = input(Fore.WHITE + "> " + Style.RESET_ALL)
        chapter_number = int(chapter_input) if chapter_input else None

        print(Fore.GREEN + "\n[INFO] Fetching chapter details..." + Style.RESET_ALL)
        download_chapter(url, chapter_number)

        # Ask if the user wants to download another chapter
        print(Fore.BLUE + "\n[QUESTION] Do you want to download another chapter? (y/n):" + Style.RESET_ALL)
        choice = input(Fore.WHITE + "> " + Style.RESET_ALL)
        if choice.lower() != 'y':
            print(Fore.MAGENTA + "\n[EXIT] Thank you for using Comic Walker Downloader!" + Style.RESET_ALL)
            break