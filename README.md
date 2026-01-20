# 🎬 Pipeline Data Streaming Real-Time - Movies Analytics

Pipeline streaming real-time untuk menganalisis data dari Netflix, Amazon Prime, dan Disney+ menggunakan Apache Kafka, Spark Streaming, PostgreSQL, dan Power BI.


example : https://drive.google.com/drive/folders/1NJFG7emT7nTEz-iLEV9Pl51wExyBsKOz?usp=sharing

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Spark](https://img.shields.io/badge/spark-3.5.6-orange.svg)
![Kafka](https://img.shields.io/badge/kafka-7.5.0-black.svg)

## 📋 Daftar Isi

- [Gambaran Umum](#gambaran-umum)
- [Arsitektur](#arsitektur)
- [Teknologi](#teknologi)
- [Struktur Proyek](#struktur-proyek)
- [Instalasi](#instalasi)
- [Cara Menjalankan](#cara-menjalankan)
- [Transformasi Data](#transformasi-data)
- [Power BI](#power-bi)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Gambaran Umum

Project ini membangun **pipeline streaming data real-time** yang mengumpulkan, memproses, dan menganalisis data film dan serial TV dari 3 platform streaming terbesar:

- 🔴 **Netflix** (~8,800 judul)
- 🔵 **Amazon Prime** (~9,600 judul)
- ⭐ **Disney+** (~1,400 judul)

### Tujuan Proyek

1. ✅ Membangun pipeline streaming end-to-end
2. ✅ Pemrosesan data secara real-time
3. ✅ Dashboard analitik interaktif
4. ✅ Deployment siap produksi dengan Docker

### Hasil Akhir

- Dashboard Power BI interaktif
- Real-time insights dari streaming data
- Analisis perbandingan antar platform
- Visualisasi kategori dan distribusi geografis

---

## 🏗️ Arsitektur

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Netflix   │ │ Amazon Prime│ │   Disney+   │
│   CSV File  │ │   CSV File  │ │   CSV File  │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        ▼
                 ┌─────────────┐
                 │   Producer  │
                 │   (Python)  │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │    Kafka    │
                 │    Topic    │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │    Spark    │
                 │  Streaming  │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │ PostgreSQL  │
                 │  Database   │
                 └──────┬──────┘
                        │
                        ▼
                 ┌─────────────┐
                 │  Power BI   │
                 │  Dashboard  │
                 └─────────────┘
```

---

## 🛠️ Teknologi

| Komponen | Teknologi | Versi | Fungsi |
|----------|-----------|-------|--------|
| **Message Broker** | Apache Kafka | 7.5.0 | Streaming pesan real-time |
| **Stream Processing** | Apache Spark | 3.5.6 | Pemrosesan & transformasi |
| **Database** | PostgreSQL | 15 | Penyimpanan data |
| **Visualization** | Power BI Desktop | - | Dashboard analitik |
| **Containerization** | Docker Compose | - | Orkestrasi container |
| **Programming** | Python | 3.11 | Development |
| **Notebook** | Jupyter | - | Testing & debugging |

### Docker Containers

Pipeline ini menggunakan **8 Docker containers**:

1. **Zookeeper** - Koordinasi Kafka
2. **Kafka** - Message broker
3. **Kafka UI** - Monitoring Kafka (port 8080)
4. **PostgreSQL** - Database (port 5432)
5. **Spark Master** - Cluster manager (port 8081)
6. **Spark Worker 1** - Processing node (port 8082)
7. **Spark Worker 2** - Processing node (port 8083)
8. **Producer** - Data ingestion service

---

## 📁 Struktur Proyek

```
streaming-data-pipeline/
│
├── consumer/
│   ├── kafka_spark_consumer.py    # Consumer untuk production (Docker)
│   └── requirements.txt            # Dependencies Python
│
├── producer/
│   ├── movies_producer.py          # Producer untuk kirim data ke Kafka
│   ├── requirements.txt            # Dependencies Python
│   └── Dockerfile                  # Container image untuk producer
│
├── dataset/
│   ├── netflix_titles.csv          # Data Netflix
│   ├── amazon_prime_titles.csv     # Data Amazon Prime
│   └── disney_plus_titles.csv      # Data Disney+
│
├── jars/
│   └── postgresql-42.2.20.jar      # JDBC driver PostgreSQL
│
├── spark-output/
│   ├── bronze/                     # Raw data (Parquet)
│   ├── silver/                     # Cleaned data (Parquet)
│   └── gold/                       # Aggregated data (unused)
│
├── Dockerfile                      # Image untuk Spark containers
├── docker-compose.yaml             # Orkestrasi semua services
├── init-db.sql                     # Database schema
├── Makefile                        # Helper commands
├── SparkNotebook.ipynb             # Testing notebook (local)
├── README.md                       # Dokumentasi (file ini)
└── QUICK-REFERENCE.md              # Quick reference guide
```

---

## 🚀 Instalasi

### Prerequisites

Pastikan sudah terinstall:

- ✅ **Docker Desktop** (minimum 8GB RAM)
- ✅ **Docker Compose** (included in Docker Desktop)
- ✅ **Git** (untuk clone repository)
- ✅ **10GB disk space**

Optional (untuk testing):
- ✅ **Python 3.11**
- ✅ **Jupyter Notebook**
- ✅ **Power BI Desktop**

### Langkah Instalasi

1. **Clone Repository**

```bash
git clone https://github.com/yourusername/streaming-data-pipeline.git
cd streaming-data-pipeline
```

2. **Siapkan Direktori**

```bash
mkdir
