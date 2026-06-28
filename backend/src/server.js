require("dotenv").config();
const createApp = require("./app");
const connectDB = require("./config/db");

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
