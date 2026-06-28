# CampusCart Backend (Assignment 2)

Node.js + Express + MongoDB API implementing the **Product Listing** core feature
(`POST /api/listings`, `GET /api/listings`) plus the supporting auth endpoints
(`POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`) needed to
exercise the full workflow. Also includes the full CRUD for listings and the
Saved Listings feature.

## 1. Run locally

```bash
cd backend
npm install
cp .env.example .env   # then fill in MONGODB_URI and JWT_SECRET
npm run dev            # starts on http://localhost:5000
```

Verify everything works without needing MongoDB Atlas yet:

```bash
npm run test:memory    # spins up an in-memory Mongo and runs 14 end-to-end checks
```

Seed sample data (requires a real `MONGODB_URI` in `.env`):

```bash
npm run seed
```

This wipes and repopulates the `users`/`listings`/`savedListings` collections and
writes `backend/campuscart-sample-data.json` — the database export file required
by the assignment. (A version of this file generated from an in-memory database
is already included so you have something to submit even before Atlas is set up;
re-run `npm run seed` against your real Atlas cluster once it's live so the
export reflects your actual deployed data.)

Demo accounts created by the seed script (password for all: `Password123`):
- `j.smith@dal.ca` — student
- `maya.patel@dal.ca` — student
- `admin@dal.ca` — admin

## 2. Set up MongoDB Atlas (required before deploying)

1. Create a free account/cluster at https://www.mongodb.com/atlas
2. Database Access → add a user with a strong password
3. Network Access → add `0.0.0.0/0` (allow access from anywhere) so Render can connect
4. Get the connection string ("Drivers" view) and paste it into `MONGODB_URI`
   in your `.env` (and later into Render's environment variables)

## 3. Deploy to Render (free tier)

1. Push this repo to GitHub
2. On https://render.com → New → Web Service → connect your GitHub repo
3. Root directory: `backend`
4. Build command: `npm install`
5. Start command: `npm start`
6. Add environment variables in the Render dashboard:
   - `MONGODB_URI` = your Atlas connection string
   - `JWT_SECRET` = a long random string
   - `JWT_EXPIRES_IN` = `1h`
   - `CORS_ORIGIN` = your deployed frontend URL (or `*` while testing)
7. Deploy. Render gives you a public URL like `https://campuscart-api.onrender.com`
8. Sanity check: open `https://<your-app>.onrender.com/api/health` in a browser —
   should return `{"status":"ok",...}`

## 4. Test with Postman and capture the required screenshots

1. Import `postman/CampusCart.postman_collection.json` into Postman
2. Set the collection variable `baseUrl` to your Render URL
3. Run requests `01` through `11` in order (top to bottom) — the collection
   auto-saves the JWT and created listing id between requests via a test script
4. Screenshot each response (request + response body + status code visible),
   matching the list in Section 4.5 of `Assignment2_Report.docx`
5. Open MongoDB Atlas → Browse Collections (or Compass) and screenshot the
   `listings` collection showing the document you just created via Postman —
   this is your proof of persistence

## 5. What's already verified

`npm run test:memory` exercises, against a real (in-memory) MongoDB:
register success/duplicate/invalid input, login success/wrong-password,
create-listing success/no-auth/invalid-body, browse with filters, get-by-id
view-count increment, and save/get saved listings — 14/14 passing.
