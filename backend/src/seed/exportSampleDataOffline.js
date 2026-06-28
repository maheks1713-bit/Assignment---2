/*
 * Produces campuscart-sample-data.json using an in-memory MongoDB instance,
 * so a sample database export can be submitted even before MongoDB Atlas is set up.
 * Run with: node src/seed/exportSampleDataOffline.js
 * Once you have a real MongoDB Atlas cluster, prefer running `npm run seed` instead,
 * which writes the same file from your real, deployed database.
 */
const fs = require("fs");
const path = require("path");
const bcrypt = require("bcryptjs");
const mongoose = require("mongoose");
const { MongoMemoryServer } = require("mongodb-memory-server");
const User = require("../models/User");
const Listing = require("../models/Listing");
const SavedListing = require("../models/SavedListing");

async function run() {
  const mongod = await MongoMemoryServer.create();
  await mongoose.connect(mongod.getUri());

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
    _note: "Sample seed data for CampusCart (Assignment 2). All demo accounts use password: Password123",
    users: await User.find().lean(),
    listings: await Listing.find().lean(),
    savedListings: await SavedListing.find().lean(),
  };

  const outPath = path.join(__dirname, "..", "..", "campuscart-sample-data.json");
  fs.writeFileSync(outPath, JSON.stringify(exportData, null, 2));
  console.log(`Wrote sample data export to ${outPath}`);

  await mongoose.connection.close();
  await mongod.stop();
  process.exit(0);
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
