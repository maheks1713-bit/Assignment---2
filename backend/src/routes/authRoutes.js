const express = require("express");
const rateLimit = require("express-rate-limit");
const { body } = require("express-validator");
const validate = require("../middleware/validate");
const { requireAuth } = require("../middleware/auth");
const { register, login, me } = require("../controllers/authController");

const router = express.Router();

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 20,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: "TooManyRequests", message: "Too many attempts, please try again later" },
});

router.post(
  "/register",
  authLimiter,
  [
    body("fullName").trim().notEmpty().withMessage("fullName is required").isLength({ max: 100 }),
    body("universityEmail")
      .trim()
      .isEmail()
      .withMessage("A valid university email is required")
      .matches(/\.(edu|ca|ac\.[a-z]{2})$/i)
      .withMessage("Please use your university email address"),
    body("password")
      .isLength({ min: 8 })
      .withMessage("Password must be at least 8 characters long"),
    body("studentId").optional().trim().isLength({ max: 20 }),
  ],
  validate,
  register
);

router.post(
  "/login",
  authLimiter,
  [
    body("universityEmail").trim().isEmail().withMessage("A valid email is required"),
    body("password").notEmpty().withMessage("Password is required"),
  ],
  validate,
  login
);

router.get("/me", requireAuth, me);

module.exports = router;
