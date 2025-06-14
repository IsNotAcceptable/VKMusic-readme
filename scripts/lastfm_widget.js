const fs = require('fs');
const axios = require('axios');
const { DateTime } = require('luxon');

const LASTFM_API_KEY = process.env.LASTFM_API_KEY;
const LASTFM_USERNAME = process.env.LASTFM_USERNAME;
const OUTPUT_PATH = '../assets/lastfm_widget.svg';

// Кэш для баз64 обложек
const imageCache = new Map();

async function fetchImageAsBase64(url) {
    if (!url) return null;
    
    try {
        const response = await axios.get(url, {
            responseType: 'arraybuffer',
            timeout: 5000
        });
        return `data:${response.headers['content-type']};base64,${response.data.toString('base64')}`;
    } catch (error) {
        console.error('Ошибка загрузки обложки:', error.message);
        return null;
    }
}

async function getTrackInfo() {
    try {
        const url = `https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=${LASTFM_USERNAME}&api_key=${LASTFM_API_KEY}&format=json&limit=1`;
        const response = await axios.get(url, { timeout: 5000 });
        
        if (!response.data?.recenttracks?.track?.length) {
            return null;
        }

        const track = response.data.recenttracks.track[0];
        let imageUrl = '';

        // Ищем обложку (приоритет: extralarge > large > medium)
        const sizes = ['extralarge', 'large', 'medium'];
        for (const size of sizes) {
            const img = track.image?.find(img => img.size === size);
            if (img?.['#text']) {
                imageUrl = img['#text'];
                break;
            }
        }

        // Получаем base64 обложки
        let imageBase64 = '';
        if (imageUrl) {
            if (imageCache.has(imageUrl)) {
                imageBase64 = imageCache.get(imageUrl);
            } else {
                imageBase64 = await fetchImageAsBase64(imageUrl);
                if (imageBase64) {
                    imageCache.set(imageUrl, imageBase64);
                }
            }
        }

        return {
            name: track.name || 'Неизвестный трек',
            artist: track.artist?.['#text'] || 'Неизвестный исполнитель',
            nowPlaying: track['@attr']?.nowplaying === 'true',
            imageBase64: imageBase64
        };
        
    } catch (error) {
        console.error('Ошибка Last.fm API:', error.message);
        return null;
    }
}

function generateSVG(track) {
    const fallbackTrack = {
        name: 'Нет данных о треке',
        artist: 'Проверьте настройки Last.fm',
        nowPlaying: false,
        imageBase64: ''
    };
    
    const { name, artist, nowPlaying, imageBase64 } = track || fallbackTrack;
    const time = DateTime.now().toFormat('HH:mm');
    const bgColor = '#9400D3';

    return `
<svg width="400" height="100" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <!-- Фон -->
    <rect width="100%" height="100%" fill="${bgColor}" rx="5"/>
    
    <!-- Обложка -->
    <rect x="10" y="10" width="80" height="80" fill="rgba(0,0,0,0.2)" rx="5"/>
    ${imageBase64 ? `
    <image href="${imageBase64}" x="10" y="10" width="80" height="80" preserveAspectRatio="xMidYMid cover" rx="5"/>
    ` : ''}
    
    <!-- Текст -->
    <text x="100" y="35" font-family="Arial, sans-serif" font-size="16" fill="white" font-weight="bold">
        ${truncate(name, 20)}
    </text>
    <text x="100" y="60" font-family="Arial, sans-serif" font-size="14" fill="#EEE">
        ${truncate(artist, 20)}
    </text>
    <text x="100" y="85" font-family="Arial, sans-serif" font-size="12" fill="#DDD">
        ${nowPlaying ? '▶ Сейчас играет' : `⏱ ${time}`}
    </text>
</svg>
    `.trim();
}

function truncate(str, maxLength) {
    return str.length > maxLength ? str.substring(0, maxLength) + '...' : str;
}

async function main() {
    try {
        if (!fs.existsSync('../assets')) {
            fs.mkdirSync('../assets', { recursive: true });
        }
        
        const track = await getTrackInfo();
        const svg = generateSVG(track);
        fs.writeFileSync(OUTPUT_PATH, svg);
        console.log('SVG успешно обновлен!');
    } catch (error) {
        console.error('Фатальная ошибка:', error.message);
        // Создаем fallback SVG
        const fallbackSvg = generateSVG(null);
        fs.writeFileSync(OUTPUT_PATH, fallbackSvg);
    }
}

main();
