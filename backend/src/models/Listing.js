const mongoose = require("mongoose");

const listingSchema = new mongoose.Schema(
  {
    title: { type: String, required: true, trim: true, maxlength: 120 },
    description: { type: String, required: true, trim: true, maxlength: 2000 },
    price: { type: Number, required: true, min: 0 },
    category: {
      type: String,
      required: true,
      enum: ["Textbooks", "Electronics", "Furniture", "Accessories", "Other"],
    },
    condition: {
      type: String,
      required: true,
      enum: ["New", "Like New", "Good", "Fair"],
    },
    images: { type: [String], default: [] },
    seller: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    status: { type: String, enum: ["active", "sold", "flagged", "removed"], default: "active" },
    views: { type: Number, default: 0 },
  },
  { timestamps: true }
);

listingSchema.index({ title: "text", description: "text" });

module.exports = mongoose.model("Listing", listingSchema);
