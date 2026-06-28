/*
 * Local smoke test: spins up an in-memory MongoDB, starts the Express app,
 * and exercises the auth + listing endpoints with real HTTP requests.
 * Run with: npm run test:memory
 * This does NOT require MongoDB Atlas or any deployment - it's purely to
 * verify the implementation logic before you deploy and test with Postman.
 */
process.env.NODE_ENV = "test";
process.env.JWT_SECRET = "smoke-test-secret";
process.env.JWT_EXPIRES_IN = "1h";

const { MongoMemoryServer } = require("mongodb-memory-server");
const mongoose = require("mongoose");
const http = require("http");
const createApp = require("../app");

function request(server, method, path, { body, token } = {}) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const { port } = server.address();
    const req = http.request(
      {
        host: "127.0.0.1",
        port,
        path,
        method,
        headers: {
          "Content-Type": "application/json",
          ...(data ? { "Content-Length": Buffer.byteLength(data) } : {}),
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
      },
      (res) => {
        let raw = "";
        res.on("data", (chunk) => (raw += chunk));
        res.on("end", () => {
          let json = null;
          try {
            json = raw ? JSON.parse(raw) : null;
          } catch (e) {
            json = raw;
          }
          resolve({ status: res.statusCode, body: json });
        });
      }
    );
    req.on("error", reject);
    if (data) req.write(data);
    req.end();
  });
}

function assert(condition, message) {
  if (!condition) throw new Error(`ASSERTION FAILED: ${message}`);
  console.log(`  PASS: ${message}`);
}

async function main() {
  console.log("Starting in-memory MongoDB...");
  const mongod = await MongoMemoryServer.create();
  await mongoose.connect(mongod.getUri());

  const app = createApp();
  const server = http.createServer(app);
  await new Promise((resolve) => server.listen(0, resolve));
  console.log(`Test server listening on port ${server.address().port}\n`);

  console.log("1) Register a new student");
  let res = await request(server, "POST", "/api/auth/register", {
    body: { fullName: "Jane Smith", universityEmail: "j.smith@dal.ca", password: "Password123" },
  });
  assert(res.status === 201, `register returns 201 (got ${res.status}: ${JSON.stringify(res.body)})`);
  assert(res.body.token, "register response includes a JWT token");
  const token = res.body.token;

  console.log("\n2) Reject duplicate registration");
  res = await request(server, "POST", "/api/auth/register", {
    body: { fullName: "Jane Smith", universityEmail: "j.smith@dal.ca", password: "Password123" },
  });
  assert(res.status === 409, `duplicate register returns 409 (got ${res.status})`);

  console.log("\n3) Reject registration with invalid email / weak password");
  res = await request(server, "POST", "/api/auth/register", {
    body: { fullName: "Bad Input", universityEmail: "not-an-email", password: "123" },
  });
  assert(res.status === 400, `invalid input returns 400 (got ${res.status})`);

  console.log("\n4) Login with correct credentials");
  res = await request(server, "POST", "/api/auth/login", {
    body: { universityEmail: "j.smith@dal.ca", password: "Password123" },
  });
  assert(res.status === 200, `login returns 200 (got ${res.status})`);
  assert(res.body.token, "login response includes a JWT token");

  console.log("\n5) Login with wrong password");
  res = await request(server, "POST", "/api/auth/login", {
    body: { universityEmail: "j.smith@dal.ca", password: "WrongPassword" },
  });
  assert(res.status === 401, `wrong password returns 401 (got ${res.status})`);

  console.log("\n6) REQUIRED ENDPOINT: create a listing while authenticated");
  res = await request(server, "POST", "/api/listings", {
    token,
    body: {
      title: "Calculus: Early Transcendentals 8th Ed.",
      description: "Gently used, like new condition.",
      price: 45,
      category: "Textbooks",
      condition: "Like New",
    },
  });
  assert(res.status === 201, `create listing returns 201 (got ${res.status}: ${JSON.stringify(res.body)})`);
  const listingId = res.body.listing._id;

  console.log("\n7) Reject creating a listing without a token");
  res = await request(server, "POST", "/api/listings", {
    body: { title: "No auth", description: "x", price: 1, category: "Other", condition: "Fair" },
  });
  assert(res.status === 401, `unauthenticated create returns 401 (got ${res.status})`);

  console.log("\n8) Reject creating a listing with invalid body (NoSQL-injection-style payload)");
  res = await request(server, "POST", "/api/listings", {
    token,
    body: { title: { $gt: "" }, description: "x", price: -5, category: "NotACategory", condition: "Fair" },
  });
  assert(res.status === 400, `malformed/invalid payload returns 400 (got ${res.status})`);

  console.log("\n9) REQUIRED ENDPOINT: browse/search listings (public, no token)");
  res = await request(server, "GET", "/api/listings?category=Textbooks&sort=price_asc");
  assert(res.status === 200, `browse listings returns 200 (got ${res.status})`);
  assert(res.body.listings.length === 1, `browse returns the 1 seeded textbook listing (got ${res.body.listings.length})`);
  assert(res.body.pagination.total === 1, "pagination metadata present");

  console.log("\n10) Get single listing by id increments view count");
  res = await request(server, "GET", `/api/listings/${listingId}`);
  assert(res.status === 200, `get by id returns 200 (got ${res.status})`);
  assert(res.body.listing.views === 1, "view count incremented");

  console.log("\n11) Save the listing, then fetch saved listings");
  res = await request(server, "POST", `/api/saved/${listingId}`, { token });
  assert(res.status === 201, `save listing returns 201 (got ${res.status})`);
  res = await request(server, "GET", "/api/saved", { token });
  assert(res.status === 200 && res.body.saved.length === 1, "saved listings includes the saved item");

  console.log("\nAll smoke tests passed.");

  server.close();
  await mongoose.connection.close();
  await mongod.stop();
  process.exit(0);
}

main().catch((err) => {
  console.error("\nSMOKE TEST FAILED:", err);
  process.exit(1);
});
