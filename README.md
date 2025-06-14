<div align="center">
  <img src="https://img.icons8.com/?size=50&id=EAOurVhu2y8d&format=png" width="100" align="center">
  <h1>VKMusic-readme</h1>
  
[![Badge](https://img.shields.io/github/issues/IsNotAcceptable/VKMusic-readme?style=for-the-badge)](https://github.com/IsNotAcceptable/VKMusic-readme/issues)
[![Badge](https://img.shields.io/github/forks/IsNotAcceptable/VKMusic-readme?style=for-the-badge)](https://github.com/IsNotAcceptable/VKMusic-readme/network)
[![Badge](https://img.shields.io/github/stars/IsNotAcceptable/VKMusic-readme?style=for-the-badge)](https://github.com/IsNotAcceptable/VKMusic-readme/stargazers)
</div>
<p align="center">
  Динамичный и работающий в режиме реального времени виджет VK Музыка для ваших файлов markdown, который синхронизируется с песней, которую вы сейчас слушаете. Если вы сейчас не слушаете песню, он покажет одну из ваших последних песен! Не стесняйтесь просить о помощи или делать любые запросы на извлечение, проблемы или предложения.
</p>

## Виджет

<div>
  <img src="https://raw.githubusercontent.com/IsNotAcceptable/VKMusic-readme/main/assets/lastfm_widget.svg?t=0" width="400">

</div>

## Установка/Использование
> [!NOTE]
> Нужен аккаунт в [last.fm](https://www.last.fm/) для интеграции

#### 0. Отметьте этот репозиторий звездой
- Да, обязательно.

#### 1. Итеграция
- Вам нужно подключить ВК Музыку с last.fm.

#### 2. Создания API
- Заходим на [Dev last.fm](https://www.last.fm/api).
  - Создаем приложение:
    - Ваша почта, название, описание, и ссылку на ваш Github account.
  - Получам API ключ.
 
#### 3. Настройка репозитория
- Делаем форк.
- Делаем Secrets:
  - LASTFM_API_KEY и API ключ last.fm.
  - LASTFM_USERNAME и ваш ник в last.fm.
- В ./scripts/lastfm_widget.js в bgColor можете поменять цвет по вашему усмотрению.

#### 4. Использование в README файл
- В своем файле вставляете:
  ```html
  <img src="https://raw.githubusercontent.com/ВАШ_НИКНЕЙМ/ВАШ_РЕПОЗИТОРИЙ/main/assets/lastfm_widget.svg" width="400">
  ```

<h6 align="right">
  IsNotAcceptable
</h6>
