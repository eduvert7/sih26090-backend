# SIH26090 — AI-Driven Market Linkage & Smart Cataloging Backend

Backend for a mobile application helping marginalized artisans catalog products using AI, connect directly with buyers, and overcome language/digital literacy barriers.

## Problem Statement

- Manual product cataloging is hard for artisans
- Lack of direct market access
- Language & digital literacy barriers
- Poor product presentation

## Features

| Feature | Description | Status |
|---|---|---|
| Snap & Catalog (AI Vision) | Upload a product photo → AI generates title, description, tags | ✅ |
| Auto-Storytelling | Same AI call generates a short artisan/craft story for the listing | ✅ |
| Auth | Signup/login via Supabase Auth | ✅ |
| Product Listings | Browse/fetch cataloged products | ✅ |
| Voice-First & Vernacular UI | Voice input transcribed and translated | 🚧 |
| Payment Gateway | Razorpay test-mode integration for demo | 🚧 |

## Tech Stack

- **Backend Framework:** Python, FastAPI
- **AI (Vision + Storytelling + Voice/Translation):** Gemini API (`google-genai`)
- **Database, Auth & Storage:** Supabase (Postgres)
- **Payments:** Razorpay (Test Mode)
- **Deployment:** Render / Railway

## Project Structure

```
sih-backend/
├── main.py              # App entrypoint, mounts all routers, CORS config
├── catalog_routes.py    # /catalog — AI vision cataloging + storytelling (Palak)
├── product_route.py     # /signup, /login, /products — auth & listings (Akshita)
├── voice_routes.py       # /voice — voice-to-text & translation (Ananya)
├── payment_routes.py     # /pay — Razorpay test mode (Ananya)
├── requirements.txt
├── .env                  # Not committed — see below
└── .gitignore
```

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/eduvert7/sih26090-backend.git
cd sih-backend
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file
This file is gitignored — create your own with:
```
GEMINI_API_KEY=your_gemini_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
RAZORPAY_KEY_ID=your_razorpay_test_key_id
RAZORPAY_KEY_SECRET=your_razorpay_test_key_secret
```

### 5. Run the server
```bash
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Database Schema (Supabase)

**Table: `products`**

| Column | Type |
|---|---|
| id | int8 (auto) |
| title | text |
| description | text |
| tags | text |
| story | text |
| image_url | text |
| created_at | timestamptz (auto) |

**Storage bucket:** `product-images` (public)

**Auth:** Supabase email/password provider

## API Endpoints

| Method | Endpoint | Description | Owner |
|---|---|---|---|
| POST | `/catalog` | Upload image → AI-generated listing | Palak |
| POST | `/signup` | Create a new user | Akshita |
| POST | `/login` | Log in, returns access token | Akshita |
| GET | `/products` | List all products | Akshita |
| GET | `/products/{id}` | Get a single product | Akshita |
| POST | `/voice` | Transcribe & translate voice input | Ananya |
| POST | `/pay` | Razorpay test-mode payment | Ananya |

## Team & Ownership

To minimize merge conflicts, each person owns a separate router file, all mounted in `main.py`:

- **Palak** — AI Vision Cataloging & Storytelling (`catalog_routes.py`)
- **Akshita** — Auth, Database & Product Listings (`product_route.py`)
- **Ananya** — Voice/Translation & Payments (`voice_routes.py`, `payment_routes.py`)

## Notes

- Row Level Security (RLS) is enabled on Supabase tables with basic read/insert policies for the demo.
- CORS is currently open (`allow_origins=["*"]`) for hackathon/demo purposes — tighten before any production use.
