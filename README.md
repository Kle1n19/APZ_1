# LAB 4
## Запустити три екземпляра logging-service (локально їх можна запустити на різних портах), відповідно мають запуститись також три екземпляра Hazelcast

Запускаємо три екземпляра за допомогою наступних команд:
```
uvicorn logging_service:app --host 127.0.0.1 --port 8001  
uvicorn logging_service:app --host 127.0.0.1 --port 8002
uvicorn logging_service:app --host 127.0.0.1 --port 8003
```
Node's сворюються атоматично при запуску багатьох екземплярів logging_service.
## Запустити два екземпляри messages-service (локально їх можна запустити на різних портах)
Запустити можна за допомогою наступних команд:
```
uvicorn messages_service:app --host 127.0.0.1 --port 8004
uvicorn messages_service:app --host 127.0.0.1 --port 8005
```

## Через HTTP POST записати 10 повідомлень msg1-msg10 через facade-service
Я використав наступну команду:
```
for i in {0..10}; do
  curl -X POST http://127.0.0.1:8000/send \
       -H "Content-Type: application/json" \
       -d "{\"msg\": \"msg$i\"}"
done

```
## Показати які повідомлення отримав кожен з екземплярів logging-service (це має бути видно у логах сервісу)
!["Akmnthyfnbdybq ntrcn"](/images/image1.png)
## Показати які повідомлення отримав кожен з екземплярів messages-service (це має бути видно у логах сервісу)
!["Akmnthyfnbdybq ntrcn"](/images/image3.png)
!["Akmnthyfnbdybq ntrcn"](/images/image4.png)
Також от що я відобразив на `facade_service`:
!["Akmnthyfnbdybq ntrcn"](/images/image2.png)
## Декілька разів викликати HTTP GET на facade-service та отримати об'єднані дві множини повідомлень - це мають бути повідомлення з logging-service та messages-service
!["Akmnthyfnbdybq ntrcn"](/images/image6.png)
# Перевірка відмовостійкості черги повідомлень
Після проведених тестів не відбулось втрат повідомлень з чергий в при повному відключенню `messages_service` повідомлення зберігаються в черзі й вичитуються потім:
!["Akmnthyfnbdybq ntrcn"](/images/image7.png)
`messages_service`:
!["Akmnthyfnbdybq ntrcn"](/images/image8.png)