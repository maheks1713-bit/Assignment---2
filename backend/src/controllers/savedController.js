const SavedListing = require("../models/SavedListing");
const Listing = require("../models/Listing");

// POST /api/listings/:id/save
async function saveListing(req, res) {
  const listing = await Listing.findById(req.params.id);
  if (!listing) {
    return res.status(404).json({ error: "NotFound", message: "Listing not found" });
  }

  try {
    const saved = await SavedListing.create({ user: req.user._id, listing: listing._id });
    return res.status(201).json({ saved });
  } catch (err) {
    if (err.code === 11000) {
      return res.status(409).json({ error: "Conflict", message: "Listing is already saved" });
    }
    throw err;
  }
}

// GET /api/saved
async function getSavedListings(req, res) {
  const saved = await SavedListing.find({ user: req.user._id }).populate({
    path: "listing",
    populate: { path: "seller", select: "fullName universityEmail" },
  });
  return res.status(200).json({ saved });
}

// DELETE /api/listings/:id/save
async function unsaveListing(req, res) {
  const result = await SavedListing.findOneAndDelete({ user: req.user._id, listing: req.params.id });
  if (!result) {
    return res.status(404).json({ error: "NotFound", message: "This listing is not in your saved list" });
  }
  return res.status(200).json({ message: "Listing removed from saved list" });
}

module.exports = { saveListing, getSavedListings, unsaveListing };
