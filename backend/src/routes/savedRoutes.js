const express = require("express");
const { param } = require("express-validator");
const validate = require("../middleware/validate");
const { requireAuth } = require("../middleware/auth");
const { saveListing, getSavedListings, unsaveListing } = require("../controllers/savedController");

const router = express.Router();

router.get("/", requireAuth, getSavedListings);
router.post("/:id", requireAuth, [param("id").isMongoId()], validate, saveListing);
router.delete("/:id", requireAuth, [param("id").isMongoId()], validate, unsaveListing);

module.exports = router;
