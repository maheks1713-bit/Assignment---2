require("dotenv").config();
const dns = require("dns");
const createApp = require("./app");
const connectDB = require("./config/db");

// Some hosts (e.g. Render) have unreliable IPv6 egress, which makes the TLS
// handshake to MongoDB Atlas fail with a misleading "tlsv1 alert internal
// error" instead of a clean connection error. Forcing IPv4 resolution first
// avoids that path entirely.
dns.setDefaultResultOrder("ipv4first");

console.log("[diagnostic] container boot time (UTC):", new Date().toISOString());
console.log("[diagnostic] node version:", process.version);

const PORT = process.env.PORT || 5000;

async function start() {
  if (!process.env.MONGODB_URI) {
    console.error("Missing MONGODB_URI in environment. Copy .env.example to .env and fill it in.");
    process.exit(1);
  }
  if (!process.env.JWT_SECRET) {
    console.error("Missing JWT_SECRET in environment. Copy .env.example to .env and fill it in.");
    process.exit(1);
  }

  await connectDB(process.env.MONGODB_URI);
  const app = createApp();
  app.listen(PORT, () => console.log(`CampusCart API listening on port ${PORT}`));
}

start();
