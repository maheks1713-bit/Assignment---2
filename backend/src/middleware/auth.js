const jwt = require("jsonwebtoken");
const User = require("../models/User");

async function requireAuth(req, res, next) {
  const header = req.headers.authorization || "";
  const token = header.startsWith("Bearer ") ? header.slice(7) : null;

  if (!token) {
    return res.status(401).json({ error: "Unauthorized", message: "Missing or malformed Authorization header. Expected: Bearer <token>" });
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET);
    const user = await User.findById(payload.sub).select("-passwordHash");
    if (!user) {
      return res.status(401).json({ error: "Unauthorized", message: "User belonging to this token no longer exists" });
    }
    if (user.status === "suspended") {
      return res.status(403).json({ error: "Forbidden", message: "This account has been suspended" });
    }
    req.user = user;
    next();
  } catch (err) {
    if (err.name === "TokenExpiredError") {
      return res.status(401).json({ error: "TokenExpired", message: "JWT has expired, please log in again" });
    }
    return res.status(401).json({ error: "Unauthorized", message: "Invalid JWT" });
  }
}

function requireRole(...roles) {
  return (req, res, next) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ error: "Forbidden", message: `Requires one of the following roles: ${roles.join(", ")}` });
    }
    next();
  };
}

module.exports = { requireAuth, requireRole };
