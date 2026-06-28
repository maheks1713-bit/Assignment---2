const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const morgan = require("morgan");
const mongoSanitize = require("express-mongo-sanitize");

const authRoutes = require("./routes/authRoutes");
const listingRoutes = require("./routes/listingRoutes");
const savedRoutes = require("./routes/savedRoutes");

function createApp() {
  const app = express();

  app.use(helmet());
  const corsOrigin = process.env.CORS_ORIGIN || "*";
  app.use(
    cors({
      origin: corsOrigin === "*" ? "*" : corsOrigin.split(","),
    })
  );
  app.use(express.json({ limit: "1mb" }));
  app.use(mongoSanitize());
  if (process.env.NODE_ENV !== "test") {
    app.use(morgan("dev"));
  }

  app.get("/api/health", (req, res) => res.status(200).json({ status: "ok", time: new Date().toISOString() }));

  app.use("/api/auth", authRoutes);
  app.use("/api/listings", listingRoutes);
  app.use("/api/saved", savedRoutes);

  app.use((req, res) => {
    res.status(404).json({ error: "NotFound", message: `Route ${req.method} ${req.originalUrl} does not exist` });
  });

  app.use((err, req, res, next) => {
    console.error(err);
    if (err.name === "CastError") {
      return res.status(400).json({ error: "BadRequest", message: "Invalid identifier supplied" });
    }
    res.status(err.status || 500).json({ error: "InternalServerError", message: "Something went wrong on our end" });
  });

  return app;
}

module.exports = createApp;
