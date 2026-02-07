# Claude Code Telegram Bot

Telegram 메시지를 Claude CLI로 전달하고 응답을 반환하는 봇입니다. 채팅별로 대화 기록을 유지합니다.

## 요구사항

- Python 3.10+
- [Claude CLI](https://github.com/anthropics/claude-code) 설치 및 PATH에 등록

## 설치

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
```

`.env` 파일을 열고 `TELEGRAM_BOT_TOKEN`을 설정하세요. [@BotFather](https://t.me/BotFather)에서 토큰을 발급받을 수 있습니다.

## 실행

```bash
python bot.py
```

## 사용법

- 봇에게 메시지를 보내면 Claude가 응답합니다
- `/start` - 시작 메시지
- `/reset` - 대화 기록 초기화

## 설정

`bot.py` 상단의 상수를 수정하여 조정할 수 있습니다:

| 상수 | 기본값 | 설명 |
|------|--------|------|
| `MAX_HISTORY` | 20 | 유지할 최대 대화 턴 수 |
| `MAX_HISTORY_CHARS` | 10000 | 히스토리 최대 문자 수 |

## 라이선스

MIT
