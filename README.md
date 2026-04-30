# VKMusic-readme
Показывайте сейчас играющую музыку на ВКонтакте прямо в README профиля!

[![Badge](https://img.shields.io/github/issues/IsNotAcceptable/VKMusic-readme?style=for-the-badge)](https://github.com/IsNotAcceptable/VKMusic-readme/issues)
[![Badge](https://img.shields.io/github/forks/IsNotAcceptable/VKMusic-readme?style=for-the-badge)](https://github.com/IsNotAcceptable/VKMusic-readme/network)
[![Badge](https://img.shields.io/github/stars/IsNotACceptable/VKMusic-readme?style=for-the-badge)](https://github.com/IsNotAcceptable/VKMusic-readme/stargazers)
<!-- vkmusic-start -->

![Now Playing](./music-card.svg?v=1777587096)

<!-- vkmusic-end -->

## 📋 Требования

- Поставить звездочку на этот репозиторий, да это обязательно
- Активный аккаунт Last.fm или ВКонтакте
- GitHub аккаунт с репозиторием

## ⚙️ Инструкция по настройке

### 1️⃣ Получение токенов и ключей

#### VK Token (обязателен)
1. Перейдите на [vkhost](https://vkhost.github.io/)
2. Выбрать Kate Mobile
3. Подтвердить вход
4. Скопируйте токен после `access_token=` до символа `&`

#### Last.fm API (опционально)
1. Перейдите на [last.fm/api](https://www.last.fm/api)
2. Кликните **Get an API Account**
3. Зарегистрируйтесь/авторизуйтесь
4. Создайте **API Application**
5. Скопируйте ваше **API Key** и **Username** (ваш логин Last.fm)

### 2️⃣ Добавление GitHub Secrets

Перейдите в **Settings → Secrets and variables → Actions** вашего репозитория и добавьте следующие секреты:

| Переменная | Значение | Обязательно? | Откуда взять |
|-----------|---------|--------|-----------|
| `VK_TOKEN` | Service Access Token от ВКонтакте | ✅ Да | vk.com/dev → Настройки приложения |
| `LASTFM_API_KEY` | API Key от Last.fm | ⚠️ Опционально | last.fm/api → API Account |
| `LASTFM_USERNAME` | Ваш username Last.fm | ⚠️ Опционально* | Ваш логин Last.fm |

*Если вы используете Last.fm, нужны оба параметра для получения информации о текущем треке

### 3️⃣ Бэйджик трека

Изначально этот README будет иметь:
```markdown
<!-- vkmusic-start -->

![Now Playing](./music-card.svg?v=1777225217)

<!-- vkmusic-end -->
```
В остальных указываете ссылку на raw SVG-файл
```
https://raw.githubusercontent.com/ВАШ-НИКНЕЙМ/НАЗВАНИЕ-РЕПОЗИТОРИЯ/master/music-card.svg
```

## 🚀 Как это работает
1. Автоматическое обновление каждые 5 минут благодаря GitHub Actions
2. Получает информацию о текущем треке из VK, обложку трека с Last.fm
3. Генерирует красивую SVG карточку с обложкой альбома
4. Обновляет README автоматически
5. Загружает изменения в репозиторий
