const Listing = require("../models/Listing");

const CATEGORIES = ["Textbooks", "Electronics", "Furniture", "Accessories", "Other"];
const CONDITIONS = ["New", "Like New", "Good", "Fair"];

// POST /api/listings  (REQUIRED ENDPOINT #1 — create a listing)
async function createListing(req, res) {
  const { title, description, price, category, condition, images } = req.body;

  const listing = await Listing.create({
    title,
    description,
    price,
    category,
    condition,
    images: Array.isArray(images) ? images.slice(0, 6) : [],
    seller: req.user._id,
  });

  return res.status(201).json({ listing });
}

// GET /api/listings  (REQUIRED ENDPOINT #2 — browse/search/filter listings)
async function getListings(req, res) {
  const { q, category, condition, minPrice, maxPrice, sort, page = 1, limit = 12 } = req.query;

  const filter = { status: "active" };

  if (category) {
    if (!CATEGORIES.includes(category)) {
      return res.status(400).json({ error: "ValidationError", message: `category must be one of: ${CATEGORIES.join(", ")}` });
    }
    filter.category = category;
  }

  if (condition) {
    if (!CONDITIONS.includes(condition)) {
      return res.status(400).json({ error: "ValidationError", message: `condition must be one of: ${CONDITIONS.join(", ")}` });
    }
    filter.condition = condition;
  }

  if (minPrice || maxPrice) {
    filter.price = {};
    if (minPrice) filter.price.$gte = Number(minPrice);
    if (maxPrice) filter.price.$lte = Number(maxPrice);
  }

  if (q) {
    filter.$text = { $search: String(q) };
  }

  const sortMap = {
    newest: { createdAt: -1 },
    oldest: { createdAt: 1 },
    price_asc: { price: 1 },
    price_desc: { price: -1 },
  };
  const sortBy = sortMap[sort] || sortMap.newest;

  const pageNum = Math.max(1, parseInt(page, 10) || 1);
  const limitNum = Math.min(50, Math.max(1, parseInt(limit, 10) || 12));

  const [listings, total] = await Promise.all([
    Listing.find(filter)
      .sort(sortBy)
      .skip((pageNum - 1) * limitNum)
      .limit(limitNum)
      .populate("seller", "fullName universityEmail"),
    Listing.countDocuments(filter),
  ]);

  return res.status(200).json({
    listings,
    pagination: { page: pageNum, limit: limitNum, total, totalPages: Math.ceil(total / limitNum) },
  });
}

// GET /api/listings/:id
async function getListingById(req, res) {
  const listing = await Listing.findById(req.params.id).populate("seller", "fullName universityEmail");
  if (!listing) {
    return res.status(404).json({ error: "NotFound", message: "Listing not found" });
  }
  listing.views += 1;
  await listing.save();
  return res.status(200).json({ listing });
}

// PUT /api/listings/:id
async function updateListing(req, res) {
  const listing = await Listing.findById(req.params.id);
  if (!listing) {
    return res.status(404).json({ error: "NotFound", message: "Listing not found" });
  }
  if (listing.seller.toString() !== req.user._id.toString() && req.user.role !== "admin") {
    return res.status(403).json({ error: "Forbidden", message: "You can only edit your own listings" });
  }

  const allowedFields = ["title", "description", "price", "category", "condition", "images", "status"];
  for (const field of allowedFields) {
    if (req.body[field] !== undefined) listing[field] = req.body[field];
  }
  await listing.save();
  return res.status(200).json({ listing });
}

// DELETE /api/listings/:id
async function deleteListing(req, res) {
  const listing = await Listing.findById(req.params.id);
  if (!listing) {
    return res.status(404).json({ error: "NotFound", message: "Listing not found" });
  }
  if (listing.seller.toString() !== req.user._id.toString() && req.user.role !== "admin") {
    return res.status(403).json({ error: "Forbidden", message: "You can only delete your own listings" });
  }
  await listing.deleteOne();
  return res.status(200).json({ message: "Listing deleted successfully" });
}

module.exports = { createListing, getListings, getListingById, updateListing, deleteListing };
