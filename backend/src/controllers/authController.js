const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const User = require("../models/User");

function signToken(user) {
  return jwt.sign({ sub: user._id.toString(), role: user.role }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN || "1h",
  });
}

function toPublicUser(user) {
  return {
    id: user._id,
    fullName: user.fullName,
    universityEmail: user.universityEmail,
    role: user.role,
    status: user.status,
    createdAt: user.createdAt,
  };
}

// POST /api/auth/register
async function register(req, res) {
  const { fullName, universityEmail, studentId, password } = req.body;

  const existing = await User.findOne({ universityEmail: universityEmail.toLowerCase() });
  if (existing) {
    return res.status(409).json({ error: "Conflict", message: "An account with this email already exists" });
  }

  const passwordHash = await bcrypt.hash(password, 12);
  const user = await User.create({
    fullName,
    universityEmail: universityEmail.toLowerCase(),
    studentId: studentId || null,
    passwordHash,
    role: "student",
  });

  const token = signToken(user);
  return res.status(201).json({ user: toPublicUser(user), token });
}

// POST /api/auth/login
async function login(req, res) {
  const { universityEmail, password } = req.body;

  const user = await User.findOne({ universityEmail: universityEmail.toLowerCase() });
  if (!user) {
    return res.status(401).json({ error: "InvalidCredentials", message: "Email or password is incorrect" });
  }

  const isMatch = await bcrypt.compare(password, user.passwordHash);
  if (!isMatch) {
    return res.status(401).json({ error: "InvalidCredentials", message: "Email or password is incorrect" });
  }

  if (user.status === "suspended") {
    return res.status(403).json({ error: "Forbidden", message: "This account has been suspended. Contact an administrator." });
  }

  const token = signToken(user);
  return res.status(200).json({ user: toPublicUser(user), token });
}

// GET /api/auth/me
async function me(req, res) {
  return res.status(200).json({ user: toPublicUser(req.user) });
}

module.exports = { register, login, me };
