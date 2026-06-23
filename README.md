# Rental Owner

## Description
This project  built using Django, GeoDjango, PostGIS, and pgvector. It combines precise geographic location tracking with advanced AI-powered semantic search, allowing users to find properties based on both physical distance and conceptual meaning.The semantic search feature needs further enhancement.

##  Quick Preview
<img width="1920" height="1080" alt="Screenshot from 2026-06-23 16-34-24" src="https://github.com/user-attachments/assets/2dc7633d-314d-4969-a2d3-5a8e8b89a6d2" />
<img width="1920" height="1080" alt="Screenshot from 2026-06-23 15-27-43" src="https://github.com/user-attachments/assets/44121bdc-052f-475d-bb52-625e50be7012" />
<img width="1920" height="1080" alt="Screenshot from 2026-06-23 16-34-48" src="https://github.com/user-attachments/assets/3ad685be-e73d-46e1-b0f4-91b2f848a9e1" />
<img width="1920" height="1080" alt="Screenshot from 2026-06-23 16-34-57" src="https://github.com/user-attachments/assets/bac47d23-5789-49dd-adfb-84e890f85710" />
<img width="1920" height="1080" alt="Screenshot from 2026-06-23 16-35-16" src="https://github.com/user-attachments/assets/84a9e8b5-49ee-4280-b3c4-1657fca58f9f" />
<img width="1920" height="1080" alt="Screenshot from 2026-06-23 16-36-01" src="https://github.com/user-attachments/assets/65fcccbd-ac95-485f-aeca-8af40f038dff" />
<img width="1920" height="1080" alt="Screenshot from 2026-06-23 16-36-11" src="https://github.com/user-attachments/assets/70e6197e-2c87-423f-becb-4c6d56026134" />




---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Django 4.x (Python) |
| **Database** | PostgreSQL with PostGIS + PGVector |
| **AI / Embeddings** | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Vector Search** | PGVector + HNSW Indexing |
| **Data Processing** | Pandas (CSV ingestion) |
| **Containerization** | Docker + Docker Compose |
| **Admin Panel** | Django Admin (custom filters + image previews) |
| **Spatial Features** | PostGIS (geo queries + distance calculation) |

---

##  Features

### Day 1 
-  PostgreSQL (via Docker) with **PostGIS** spatial extension and **PGVector** for embeddings
-  Django + PostgreSQL full configuration
-  Database models — `Location`, `Property`, `PropertyImage`
-  CSV bulk importer using **Pandas** (`rentals.csv`)
-  Django Admin with **custom filters**, column sorting, and **inline image previews**

###  Day 2 — Search Interface & Property Pages
-  Homepage with location-based **search form**
-  **Location-based property search** using PostGIS spatial queries
-  Property listing page with **pagination**
-  Property detail page with **images** and **amenities**
-  **Distance from city center** displayed on each property detail page

###  Day 3 — AI Semantic Search
-  Integrated **Sentence Transformers** (`all-MiniLM-L6-v2`)
-  Generated **location name vector embeddings**
-  Stored embeddings as vectors in **PGVector**
-  **HNSW indexing** for millisecond-level vector lookups


---

## Distance Measurement (Location to property)


- Row 1 (The Pioneer): When the script reads your first Dhaka property (Beachfront Paradise Villa), no Dhaka location hub exists yet. So, it creates one and pins its coordinates to this exact property's coordinates from csv. Because the property pin and the hub pin are in the identical spot, the distance is 0.0000 meters.

- Rows 2, 3, 4... (The Followers): When the script reads subsequent Dhaka properties (Gulshan Luxury Penthouse, Banani Urban Studio, etc.), It skips creating a new location and links these properties back to that very first location hub coordinate anchor.
---

## Getting Started



###  Clone the Repository

```bash
git clone https://github.com/Parisa-Reza/Owner-Rental-Parisa-Reza
cd Owner-Rental-Parisa-Reza
```

---

### Configure Environment Assets

Create your local environment config file, or verify your rental data CSV is present:

```bash
# Option A: Copy the example env file and fill in your values
cp .env.example .env

# Option B: Verify your CSV data file is in the root folder
ls rentals.csv
```

---

### Build and Start Docker Containers

Build the environment and install all dependencies including AI/ML libraries (`pgvector`, `sentence-transformers`, `numpy`):

```bash
docker compose up -d --build
```

> **First-run note:** The initial build may take **15–20 minutes** — Docker downloads large ML models and libraries. Do **not** interrupt this process.

---

### Apply Database Migrations

Prepare the PostgreSQL database with spatial extensions and create all required tables:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

---

### Initialize the HNSW Vector Index

Open the Django shell:

```bash
docker compose exec web python manage.py shell
```

Then paste and run this script inside the shell:

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS location_embedding_idx
        ON property_app_location
        USING hnsw (embedding vector_cosine_ops);
    """)

exit()
```


---
###  Superuser creation


```bash
docker compose exec web python manage.py createsuperuser
```
---
###  Import Data & Generate AI Embeddings

Process your CSV, generate semantic vector embeddings for all locations, and populate the database:

```bash
docker compose exec web python manage.py import_properties rentals.csv
```


---

### Access the Application

Open your browser:

| Interface | URL |
|---|---|
| Homepage Search | `http://localhost:8000/` |
| Django Admin Panel | `http://localhost:8000/admin/` |

---

## Future improvement

- Enhance semantic search feature



## License

This project is for learning purpose assigned by W3 Engineers Ltd.
