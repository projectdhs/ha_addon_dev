from flask import Flask, request, jsonify
import yt_dlp
import traceback

app = Flask(__name__)

potoken = "MnB5m1G6-6piznmj4-pv-4XJoq8gRPmc0D-rXpaZa4Hxm9141nltAEwmROZ-pZVCCaMQeq66Wdn6DyleuJ4dpKoWx9VPguTHs6nNwoqK_IoQJaGJLi0me48u9CxRWfw2IpBZrdShOaMC_cOaStMTkHm_"

ydl_opts = {
    "quiet": True,
    'cookiefile': '/config/.storage/ytube_cookie.txt',
    # This enforces a player client and skips unnecessary scraping to increase speed
    "extractor_args": {
        "youtube": {
            "skip": ["translated_subs", "dash"],
            "player_client": ["web_music"],
            "player_skip": ["webpage"],
        }
    },
}


ydl = yt_dlp.YoutubeDL(ydl_opts)

def get_audio_url_from_json(video_url):
    info_dict = ydl.extract_info(video_url, download=False)

    for format in info_dict.get('formats', []):
        if format.get('acodec') == 'mp4a.40.2' and format.get('vcodec') != 'none':
            return format['url']

@app.route('/api/getSongUrl', methods=['GET'])
def get_song_url():
    song_id = request.args.get('songid')
    if not song_id:
        return jsonify({'error': 'Missing songid parameter'}), 400

    video_url = f"https://music.youtube.com/watch?v={song_id}"
    audio_url = get_audio_url_from_json(video_url)

    if audio_url:
        return jsonify({'audio_url': audio_url})
    else:
        return jsonify({'error': 'Failed to extract audio URL'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6784)
