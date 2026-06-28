require("dotenv").config();
const fs = require("fs");
const path = require("path");
const bcrypt = require("bcryptjs");
const mongoose = require("mongoose");
const connectDB = require("../config/db");
const User = require("../models/User");
const Listing = require("../models/Listing");
const SavedListing = require("../models/SavedListing");

async function run() {
  await connectDB(process.env.MONGODB_URI);

  await Promise.all([User.deleteMany({}), Listing.deleteMany({}), SavedListing.deleteMany({})]);

  const passwordHash = await bcrypt.hash("Password123", 12);

  const jane = await User.create({
    fullName: "Jane Smith",
    universityEmail: "j.smith@dal.ca",
    studentId: "B01234567",
    passwordHash,
    role: "student",
  });

  const maya = await User.create({
    fullName: "Maya Patel",
    universityEmail: "maya.patel@dal.ca",
    studentId: "B07654321",
    passwordHash,
    role: "student",
  });

  const admin = await User.create({
    fullName: "Admin User",
    universityEmail: "admin@dal.ca",
    passwordHash,
    role: "admin",
  });

  const listings = await Listing.insertMany([
    {
      title: "Calculus: Early Transcendentals 8th Ed.",
      description: "Gently used copy, spine intact, no missing pages, minimal highlighting. Perfect for MATH 1000/2001.",
      price: 45,
      category: "Textbooks",
      condition: "Like New",
      seller: jane._id,
    },
    {
      title: "HP 15in Laptop - Core i5, 8GB RAM",
      description: "Reliable laptop for note-taking and assignments. Light wear on the lid, works perfectly.",
      price: 320,
      category: "Electronics",
      condition: "Good",
      seller: jane._id,
    },
    {
      title: "Ergonomic Desk Chair - Black",
      description: "Comfortable desk chair, adjustable height, great for long study sessions.",
      price: 60,
      category: "Furniture",
      condition: "Like New",
      seller: maya._id,
    },
  ]);

  await SavedListing.create({ user: maya._id, listing: listings[0]._id });

  const exportData = {
    users: await User.find().lean(),
    listings: await Listing.find().lean(),
    savedListings: await SavedListing.find().lean(),
  };

  const outPath = path.join(__dirname, "..", "..", "campuscart-sample-data.json");
  fs.writeFileSync(outPath, JSON.stringify(exportData, null, 2));
  console.log(`Seeded database and wrote sample data export to ${outPath}`);

  await mongoose.connection.close();
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
