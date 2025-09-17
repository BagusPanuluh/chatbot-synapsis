# Synapsis Chatbot — Customer Support

Chatbot customer support untuk challenge **Jr. AI Engineer — PT Synapsis Sinergi Digital**.  
Dibangun dengan **FastAPI + SQLite + Ollama (LLM)**.

---

## Fitur
- Menjawab pertanyaan terkait pesanan:
  - "Dimana pesanan saya 1001?" → detail status, ekspedisi, ETA.
  - "Apa ekspedisi pesanan saya 1001?" → hanya ekspedisi.
  - "Bagaimana status pesanan saya 1001?" → hanya status.
  - "Estimasi pesanan saya 1001 kapan sampai?" → ETA **+3 hari** dari database.
- Memberikan informasi produk:
  - "Apa kelebihan produk LaptopA?"
- Menjawab pertanyaan umum via LLM.
- Menyimpan riwayat percakapan ke SQLite.
- API berbasis **FastAPI** dengan Swagger UI.

---

## Requirements
- [Docker](https://www.docker.com/)  
- Internet (untuk pull model LLM pertama kali)

---

## Struktur Project
```
chatbot-synapsis/
├─ app/
│  ├─ main.py
│  ├─ db.py
│  ├─ tools.py
│  ├─ ollama_client.py
├─ models.sql
├─ requirements.txt
├─ Dockerfile
└─ README.md
```

---

## Cara Menjalankan dengan Docker

### 1. Jalankan Ollama (LLM)
```
docker run -d --name ollama -p 11434:11434 -v ollama_data:/root/.ollama ollama/ollama:latest
```

Lalu masuk ke dalam container untuk download model:
```
docker exec -it ollama bash
ollama pull llama3.2:3b
exit
```

> Model hanya perlu didownload sekali.  

---

### 2. Build image chatbot
Dari folder project (`chatbot-synapsis`):
```
docker build -t synapsis-chatbot .
```

---

### 3. Jalankan chatbot
- **Windows PowerShell**
  ```
  docker run -d --name chatbot -p 8000:8000 -v ${PWD}/chatbot.db:/app/chatbot.db --env OLLAMA_URL=http://ollama:11434 --env OLLAMA_MODEL=llama3.2:3b --link ollama:ollama synapsis-chatbot
  ```

- **Linux/Mac**
  ```
  docker run -d --name chatbot -p 8000:8000 -v $(pwd)/chatbot.db:/app/chatbot.db --env OLLAMA_URL=http://ollama:11434 --env OLLAMA_MODEL=llama3.2:3b --link ollama:ollama synapsis-chatbot
  ```

---

### 4. Cek apakah berjalan
```
docker ps
```

Harus terlihat container `chatbot` di port `8000`.  
Cek log:
```
docker logs chatbot
```

Kalau sukses, akan muncul:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### 5. Tes API
- Root API → [http://localhost:8000/](http://localhost:8000/)  
  Balik JSON:
  ```
  {"status":"ok","info":"Synapsis Chatbot API"}
  ```

- Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)

- Contoh query dengan curl:
  ```
  curl -Method POST http://localhost:8000/chat -Headers @{"Content-Type"="application/json"} -Body '{"user_id":"u123","message":"Estimasi pesanan saya 1001 kapan sampai?"}'
  ```
- Contoh running dengan swagger:
  ```
  http://localhost:8000/docs

  - Klik "Try it Out"
  - Isi bagian "user_id" dengan "u123" dan bagian "message" dengan contoh pertanyaan. Misal:
        {
        "user_id": "u123",
        "message": "Estimasi pesanan 1001",
        "metadata": {
            "additionalProp1": {}
        }
        }
  - Klik execute
  - Output akan keluar pada bagian response 
  ```


---

## Stop service
Hentikan dan hapus container:
```
docker stop chatbot ollama
docker rm chatbot ollama
```

---

## Catatan
- Database SQLite (`chatbot.db`) otomatis dibuat saat pertama kali jalan.
- Data contoh:
  - Order `1001` → user `u123`, status `Shipped`, ekspedisi `JNE`, ETA `2025-09-18`.
  - Produk: `LaptopA`, `SmartphoneX`, `HeadsetZ`.
- ETA akan ditambah **+3 hari** saat dijawab chatbot.
- Contoh pertanyaan:
  - "Berikan informasi mengenai garansi"
  - "Berikan daftar produk yang tersedia"
  - "Kapan estimasi pesanan 1001 sampai?"
  - "Apa status pesanan 1001?"
  - "Apa ekspedisi pesanan 1001"