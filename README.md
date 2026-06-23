# Rental Owner

> A semantic property search platform built with Django, PostgreSQL, PGVector, and Sentence Transformers enabling natural language location search with lightning-fast HNSW vector indexing.

---

##  Quick Preview





---

## 🛠️ Tech Stack

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
git clone <your-repository-url>
cd my_project
```

---

### Step 2 — Configure Environment Assets

Create your local environment config file, or verify your rental data CSV is present:

```bash
# Option A: Copy the example env file and fill in your values
cp .env.example .env

# Option B: Verify your CSV data file is in the root folder
ls rentals.csv
```

---

### Step 3 — Build and Start Docker Containers

Build the environment and install all dependencies including AI/ML libraries (`pgvector`, `sentence-transformers`, `numpy`):

```bash
docker compose up -d --build
```

> ⚠️ **First-run note:** The initial build may take **5–10 minutes** — Docker downloads large ML models and libraries. Do **not** interrupt this process.

---

### Step 4 — Apply Database Migrations

Prepare the PostgreSQL database with spatial extensions and create all required tables:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

---

### Step 5 — Initialize the HNSW Vector Index

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

> 💡 **Why HNSW?** Hierarchical Navigable Small World indexing enables sub-millisecond approximate nearest-neighbour vector searches — even across millions of embeddings.

---

### Step 6 — Import Data & Generate AI Embeddings

Process your CSV, generate semantic vector embeddings for all locations, and populate the database:

```bash
docker compose exec web python manage.py import_properties rentals.csv
```

This command will:
1. Parse `rentals.csv` via Pandas
2. Create `Location` and `Property` records
3. Generate sentence embeddings for each location name
4. Store vectors in PGVector for semantic search

---

### Step 7 — Access the Application

Your app is live! Open your browser:

| Interface | URL |
|---|---|
| 🏠 Homepage Search | `http://localhost:8000/` |
| ⚙️ Django Admin Panel | `http://localhost:8000/admin/` |

---

## Future improvement

-  **Semantic location search** (understands context, not just keywords)
-  Combined **geo + semantic search** pipeline
-  **Location autocomplete API** powered by semantic search



## License

This project is for learning purpose assigned by W3 Engineers Ltd.