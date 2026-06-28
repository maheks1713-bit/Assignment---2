const express = require("express");
const { body, param, query } = require("express-validator");
const validate = require("../middleware/validate");
const { requireAuth, requireRole } = require("../middleware/auth");
const {
  createListing,
  getListings,
  getListingById,
  updateListing,
  deleteListing,
} = require("../controllers/listingController");

const router = express.Router();

const CATEGORIES = ["Textbooks", "Electronics", "Furniture", "Accessories", "Other"];
const CONDITIONS = ["New", "Like New", "Good", "Fair"];

const listingBodyRules = [
  body("title").trim().notEmpty().withMessage("title is required").isLength({ max: 120 }),
  body("description").trim().notEmpty().withMessage("description is required").isLength({ max: 2000 }),
  body("price").isFloat({ min: 0 }).withMessage("price must be a number >= 0"),
  body("category").isIn(CATEGORIES).withMessage(`category must be one of: ${CATEGORIES.join(", ")}`),
  body("condition").isIn(CONDITIONS).withMessage(`condition must be one of: ${CONDITIONS.join(", ")}`),
  body("images").optional().isArray({ max: 6 }).withMessage("images must be an array of up to 6 URLs"),
];

// REQUIRED ENDPOINT #2: GET /api/listings — public browse/search/filter
router.get(
  "/",
  [
    query("page").optional().isInt({ min: 1 }),
    query("limit").optional().isInt({ min: 1, max: 50 }),
    query("minPrice").optional().isFloat({ min: 0 }),
    query("maxPrice").optional().isFloat({ min: 0 }),
  ],
  validate,
  getListings
);

router.get("/:id", [param("id").isMongoId().withMessage("Invalid listing id")], validate, getListingById);

// REQUIRED ENDPOINT #1: POST /api/listings — create listing (authenticated students only)
router.post("/", requireAuth, requireRole("student", "admin"), listingBodyRules, validate, createListing);

router.put(
  "/:id",
  requireAuth,
  [param("id").isMongoId().withMessage("Invalid listing id"), ...listingBodyRules.map((r) => r.optional())],
  validate,
  updateListing
);

router.delete("/:id", requireAuth, [param("id").isMongoId().withMessage("Invalid listing id")], validate, deleteListing);

module.exports = router;
