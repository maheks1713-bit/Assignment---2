# -*- coding: utf-8 -*-
"""
Generates Assignment2_Report.docx for CSCI 5709 Assignment 2 (CampusCart).
Run: python build_report.py
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BLUE = RGBColor(0x2B, 0x5F, 0xD9)
DARK = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x55, 0x55, 0x55)
RED = RGBColor(0xB0, 0x00, 0x20)

doc = Document()

# ---------- base style ----------
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10.5)

def set_cell_shading(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def add_heading(text, level=1, color=BLUE, space_before=14, space_after=6):
    h = doc.add_heading(level=level)
    h.paragraph_format.space_before = Pt(space_before)
    h.paragraph_format.space_after = Pt(space_after)
    run = h.add_run(text)
    run.font.color.rgb = color
    return h

def add_para(text, bold=False, italic=False, size=10.5, color=DARK, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return p

def add_bullets(items, size=10.5):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        r = p.add_run(it)
        r.font.size = Pt(size)

def add_screenshot_placeholder(label):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(f"[ INSERT SCREENSHOT HERE: {label} ]")
    r.bold = True
    r.italic = True
    r.font.color.rgb = RED
    r.font.size = Pt(10)
    # light box border via simple bordered table cell trick
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    cell = table.cell(0, 0)
    cell.text = f"[ INSERT SCREENSHOT HERE: {label} ]"
    cell.paragraphs[0].runs[0].italic = True
    cell.paragraphs[0].runs[0].font.color.rgb = RED
    set_cell_shading(cell, "FFF5F5")
    doc.add_paragraph()

def endpoint_block(ep):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    r = p.add_run(f"{ep['method']}  {ep['path']}")
    r.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = BLUE
    if ep.get("required"):
        rr = p.add_run("   [REQUIRED ENDPOINT - IMPLEMENTED & DEPLOYED]")
        rr.bold = True
        rr.font.size = Pt(9)
        rr.font.color.rgb = RED

    add_para(ep["description"], space_after=4)

    meta = doc.add_paragraph()
    meta.add_run("Authentication: ").bold = True
    meta.add_run(ep.get("auth", "None (public endpoint)") + "    ")
    meta.add_run("Authorization: ").bold = True
    meta.add_run(ep.get("authz", "N/A"))
    meta.paragraph_format.space_after = Pt(4)

    if ep.get("params"):
        add_para("Request Parameters / Body:", bold=True, space_after=2)
        table = doc.add_table(rows=1, cols=4)
        table.style = "Light Grid Accent 1"
        hdr = table.rows[0].cells
        for i, h in enumerate(["Field", "Type", "Required?", "Notes"]):
            hdr[i].text = h
            hdr[i].paragraphs[0].runs[0].bold = True
        for field, ftype, req, notes in ep["params"]:
            row = table.add_row().cells
            row[0].text = field
            row[1].text = ftype
            row[2].text = req
            row[3].text = notes
        doc.add_paragraph()

    add_para(f"Success Response: {ep['success_code']}", bold=True, space_after=2)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(ep["success_body"])
    run.font.name = "Consolas"
    run.font.size = Pt(9)

    add_para("Error Responses:", bold=True, space_after=2)
    table = doc.add_table(rows=1, cols=3)
    table.style = "Light Grid Accent 1"
    hdr = table.rows[0].cells
    for i, h in enumerate(["Status Code", "Condition", "Error Message (JSON)"]):
        hdr[i].text = h
        hdr[i].paragraphs[0].runs[0].bold = True
    for code, cond, msg in ep["errors"]:
        row = table.add_row().cells
        row[0].text = code
        row[1].text = cond
        row[2].text = msg
    doc.add_paragraph()


# =====================================================================
# TITLE PAGE
# =====================================================================
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_before = Pt(140)
r = title.add_run("CSCI 5709: Advanced Web Services")
r.font.size = Pt(20)
r.bold = True

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run("Assignment 2 - RESTful API Design, Security, and Implementation")
r.font.size = Pt(15)
r.bold = True
r.font.color.rgb = BLUE

sub2 = doc.add_paragraph()
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub2.add_run("Project: CampusCart - A Campus Buy-and-Sell Marketplace")
r.font.size = Pt(13)

for line in [
    "Student: Mahek Dilipbhai Shah",
    "Banner ID: B01043202",
    "Group: Group 8",
    "Date: June 27, 2026",
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(line).font.size = Pt(11)

note = doc.add_paragraph()
note.alignment = WD_ALIGN_PARAGRAPH.CENTER
note.paragraph_format.space_before = Pt(40)
r = note.add_run(
    "This document was prepared individually and independently, per the assignment instructions, "
    "based on the core features defined in the Group 8 project proposal for CampusCart."
)
r.italic = True
r.font.size = Pt(9.5)
r.font.color.rgb = GREY

doc.add_page_break()

# =====================================================================
# 0. INTRODUCTION
# =====================================================================
add_heading("0. Introduction and Scope", level=1)
add_para(
    "CampusCart is a campus-only buy-and-sell marketplace for university students, as defined in the "
    "Group 8 project proposal. This report designs and documents the RESTful API for three of CampusCart's "
    "core features, defines the security-related endpoints needed to protect them, sketches the underlying "
    "data models, and describes a working implementation of two endpoints from one of the three features."
)
add_para("The three core features selected for this assignment are:", bold=True, space_after=2)
add_bullets([
    "Core Feature 2 - Product Listing Management (create, edit, delete, view listings)",
    "Core Feature 3 - Browse, Search & Filter (public discovery of listings)",
    "Core Feature 4 - Favorite / Saved Listings (bookmarking listings for later)",
])
add_para(
    "As instructed, user registration and login are documented separately under Section 2 "
    "(Security-Related Endpoints) rather than counted as core features."
)
add_para(
    "All endpoints below are prefixed with the API base path /api and assume JSON request/response bodies "
    "(Content-Type: application/json) unless otherwise noted."
)

doc.add_page_break()

# =====================================================================
# 1. CORE FEATURE ENDPOINTS
# =====================================================================
add_heading("1. Core Feature API Endpoints", level=1)

# ---------------- 1.1 Product Listing Management ----------------
add_heading("1.1 Core Feature 2 - Product Listing Management", level=2)
add_para(
    "Authenticated students can create, view, edit, and delete their own product listings. Each listing "
    "stores a title, description, price, category, condition, optional images, and a reference to the seller. "
    "This maps directly to the proposal's Core Feature 2."
)

listing_eps = [
    dict(
        method="POST", path="/api/listings", required=True,
        description="Create a new product listing. Only authenticated users with role 'student' or 'admin' may create listings.",
        auth="Required - Bearer JWT in Authorization header",
        authz="Any authenticated student (role-based, not ownership-based, since this creates a new resource)",
        params=[
            ("title", "String", "Yes", "1-120 characters"),
            ("description", "String", "Yes", "1-2000 characters"),
            ("price", "Number", "Yes", ">= 0"),
            ("category", "String (enum)", "Yes", "Textbooks | Electronics | Furniture | Accessories | Other"),
            ("condition", "String (enum)", "Yes", "New | Like New | Good | Fair"),
            ("images", "Array<String>", "No", "Up to 6 image URLs"),
        ],
        success_code="201 Created",
        success_body='{\n  "listing": {\n    "_id": "665f1...",\n    "title": "Calculus: Early Transcendentals 8th Ed.",\n    "description": "Gently used, like new condition.",\n    "price": 45,\n    "category": "Textbooks",\n    "condition": "Like New",\n    "images": [],\n    "seller": "665f0...",\n    "status": "active",\n    "views": 0,\n    "createdAt": "2026-06-27T19:34:42.232Z"\n  }\n}',
        errors=[
            ("400 Bad Request", "Missing/invalid field (e.g. blank title, negative price, invalid category)", '{"error":"ValidationError","message":"One or more fields are invalid","details":[{"field":"price","message":"price must be a number >= 0"}]}'),
            ("401 Unauthorized", "Missing or invalid JWT", '{"error":"Unauthorized","message":"Missing or malformed Authorization header. Expected: Bearer <token>"}'),
            ("403 Forbidden", "Account suspended by an admin", '{"error":"Forbidden","message":"This account has been suspended"}'),
        ],
    ),
    dict(
        method="GET", path="/api/listings/:id", required=False,
        description="Retrieve a single listing by id, including seller's public profile fields. Increments the listing's view counter (supports Seller Dashboard view metrics).",
        auth="Not required (public)",
        authz="N/A - read-only public resource",
        params=[("id", "ObjectId (path param)", "Yes", "Must be a valid 24-character Mongo ObjectId")],
        success_code="200 OK",
        success_body='{\n  "listing": {\n    "_id": "665f1...",\n    "title": "Calculus: Early Transcendentals 8th Ed.",\n    "price": 45,\n    "views": 12,\n    "seller": { "fullName": "Jane Smith", "universityEmail": "j.smith@dal.ca" }\n  }\n}',
        errors=[
            ("400 Bad Request", "id is not a valid ObjectId", '{"error":"ValidationError","message":"One or more fields are invalid","details":[{"field":"id","message":"Invalid listing id"}]}'),
            ("404 Not Found", "No listing exists with that id", '{"error":"NotFound","message":"Listing not found"}'),
        ],
    ),
    dict(
        method="PUT", path="/api/listings/:id", required=False,
        description="Edit an existing listing. Only the original seller (or an admin) may edit it. Demonstrates ownership-based access control (broken-access-control mitigation).",
        auth="Required - Bearer JWT",
        authz="Owner of the listing OR admin role",
        params=[
            ("title", "String", "No", "1-120 characters"),
            ("description", "String", "No", "1-2000 characters"),
            ("price", "Number", "No", ">= 0"),
            ("category", "String (enum)", "No", "See Core Feature 2 categories"),
            ("condition", "String (enum)", "No", "New | Like New | Good | Fair"),
            ("status", "String (enum)", "No", "active | sold | flagged | removed"),
        ],
        success_code="200 OK",
        success_body='{\n  "listing": { "_id": "665f1...", "title": "Updated title", "price": 40, "status": "sold" }\n}',
        errors=[
            ("401 Unauthorized", "Missing/invalid JWT", '{"error":"Unauthorized","message":"Invalid JWT"}'),
            ("403 Forbidden", "Authenticated user does not own this listing", '{"error":"Forbidden","message":"You can only edit your own listings"}'),
            ("404 Not Found", "Listing id does not exist", '{"error":"NotFound","message":"Listing not found"}'),
        ],
    ),
    dict(
        method="DELETE", path="/api/listings/:id", required=False,
        description="Permanently delete a listing. Only the original seller (or an admin) may delete it.",
        auth="Required - Bearer JWT",
        authz="Owner of the listing OR admin role",
        params=[("id", "ObjectId (path param)", "Yes", "")],
        success_code="200 OK",
        success_body='{ "message": "Listing deleted successfully" }',
        errors=[
            ("401 Unauthorized", "Missing/invalid JWT", '{"error":"Unauthorized","message":"Invalid JWT"}'),
            ("403 Forbidden", "Authenticated user does not own this listing", '{"error":"Forbidden","message":"You can only delete your own listings"}'),
            ("404 Not Found", "Listing id does not exist", '{"error":"NotFound","message":"Listing not found"}'),
        ],
    ),
]
for ep in listing_eps:
    endpoint_block(ep)

# ---------------- 1.2 Browse Search Filter ----------------
add_heading("1.2 Core Feature 3 - Browse, Search & Filter", level=2)
add_para(
    "All visitors, including unauthenticated ones, can browse listings on the main marketplace page, search by "
    "keyword, filter by category/condition/price, sort, and page through results."
)

browse_eps = [
    dict(
        method="GET", path="/api/listings", required=True,
        description="Browse, search, filter, sort, and paginate active listings. This is the primary endpoint behind the marketplace home page.",
        auth="Not required (public)",
        authz="N/A - read-only public resource; results are always limited to status='active' listings",
        params=[
            ("q", "String (query)", "No", "Free-text search across title & description (MongoDB text index)"),
            ("category", "String (query)", "No", "Textbooks | Electronics | Furniture | Accessories | Other"),
            ("condition", "String (query)", "No", "New | Like New | Good | Fair"),
            ("minPrice / maxPrice", "Number (query)", "No", ">= 0"),
            ("sort", "String (query)", "No", "newest (default) | oldest | price_asc | price_desc"),
            ("page", "Integer (query)", "No", "Default 1"),
            ("limit", "Integer (query)", "No", "Default 12, max 50"),
        ],
        success_code="200 OK",
        success_body='{\n  "listings": [ { "_id": "665f1...", "title": "Calculus...", "price": 45, "category": "Textbooks" } ],\n  "pagination": { "page": 1, "limit": 12, "total": 6, "totalPages": 1 }\n}',
        errors=[
            ("400 Bad Request", "Invalid category/condition value, or non-numeric page/limit/minPrice/maxPrice", '{"error":"ValidationError","message":"category must be one of: Textbooks, Electronics, Furniture, Accessories, Other"}'),
        ],
    ),
    dict(
        method="GET", path="/api/listings/categories", required=False,
        description="Returns the static list of valid categories and conditions so the front end can render filter dropdowns without hardcoding enum values.",
        auth="Not required (public)",
        authz="N/A",
        params=[],
        success_code="200 OK",
        success_body='{\n  "categories": ["Textbooks","Electronics","Furniture","Accessories","Other"],\n  "conditions": ["New","Like New","Good","Fair"]\n}',
        errors=[("500 Internal Server Error", "Unexpected server failure", '{"error":"InternalServerError","message":"Something went wrong on our end"}')],
    ),
]
for ep in browse_eps:
    endpoint_block(ep)
add_para(
    "Note: Browse/Search/Filter reuses the GET /api/listings endpoint documented above with query parameters, "
    "rather than duplicating it under a separate route - this avoids redundant endpoints for what is fundamentally "
    "the same resource collection with different query filters, which is consistent with REST conventions."
)

# ---------------- 1.3 Saved Listings ----------------
add_heading("1.3 Core Feature 4 - Favorite / Saved Listings", level=2)
add_para(
    "Logged-in students can bookmark listings to a personal saved list, view that list, and remove items from it."
)

saved_eps = [
    dict(
        method="POST", path="/api/saved/:id", required=False,
        description="Save (bookmark) a listing for the current user.",
        auth="Required - Bearer JWT",
        authz="Any authenticated user; uniqueness is enforced per (user, listing) pair",
        params=[("id", "ObjectId (path param)", "Yes", "Id of the listing to save")],
        success_code="201 Created",
        success_body='{ "saved": { "_id": "665f2...", "user": "665f0...", "listing": "665f1..." } }',
        errors=[
            ("401 Unauthorized", "Missing/invalid JWT", '{"error":"Unauthorized","message":"Invalid JWT"}'),
            ("404 Not Found", "Listing id does not exist", '{"error":"NotFound","message":"Listing not found"}'),
            ("409 Conflict", "Listing already saved by this user", '{"error":"Conflict","message":"Listing is already saved"}'),
        ],
    ),
    dict(
        method="GET", path="/api/saved", required=False,
        description="Retrieve the current user's saved listings, with the full listing (and seller) details populated.",
        auth="Required - Bearer JWT",
        authz="Returns only the authenticated user's own saved items (enforced via req.user._id, not a client-supplied id)",
        params=[],
        success_code="200 OK",
        success_body='{ "saved": [ { "_id": "665f2...", "listing": { "title": "Calculus...", "price": 45, "status": "active" } } ] }',
        errors=[("401 Unauthorized", "Missing/invalid JWT", '{"error":"Unauthorized","message":"Invalid JWT"}')],
    ),
    dict(
        method="DELETE", path="/api/saved/:id", required=False,
        description="Remove a listing from the current user's saved list.",
        auth="Required - Bearer JWT",
        authz="Only removes the saved-listing row owned by the authenticated user",
        params=[("id", "ObjectId (path param)", "Yes", "Id of the listing to unsave")],
        success_code="200 OK",
        success_body='{ "message": "Listing removed from saved list" }',
        errors=[
            ("401 Unauthorized", "Missing/invalid JWT", '{"error":"Unauthorized","message":"Invalid JWT"}'),
            ("404 Not Found", "Listing was not in the user's saved list", '{"error":"NotFound","message":"This listing is not in your saved list"}'),
        ],
    ),
]
for ep in saved_eps:
    endpoint_block(ep)

doc.add_page_break()

# =====================================================================
# 2. SECURITY-RELATED ENDPOINTS
# =====================================================================
add_heading("2. Security-Related Endpoints", level=1)
add_para(
    "This section documents endpoints dedicated exclusively to authentication, authorization, and data "
    "validation, as required by the assignment. These are intentionally separate from the three core "
    "features above, since the assignment specifies that login and registration are not core features."
)

add_heading("2.1 Authentication", level=2)
auth_eps = [
    dict(
        method="POST", path="/api/auth/register", required=False,
        description="Register a new student account. Restricted to university email addresses to preserve CampusCart's trust model.",
        auth="Not required (public)",
        authz="N/A - always creates a 'student' role account; role cannot be supplied by the client (see Section 2.4 - mass assignment mitigation)",
        params=[
            ("fullName", "String", "Yes", "1-100 characters"),
            ("universityEmail", "String", "Yes", "Valid email format; must end in a university domain (e.g. .ca/.edu)"),
            ("studentId", "String", "No", "Up to 20 characters"),
            ("password", "String", "Yes", "Minimum 8 characters; hashed with bcrypt (cost factor 12) before storage"),
        ],
        success_code="201 Created",
        success_body='{\n  "user": { "id": "665f0...", "fullName": "Jane Smith", "universityEmail": "j.smith@dal.ca", "role": "student" },\n  "token": "eyJhbGciOiJIUzI1NiIs..."\n}',
        errors=[
            ("400 Bad Request", "Invalid email format, non-university email, or password < 8 characters", '{"error":"ValidationError","message":"One or more fields are invalid","details":[{"field":"password","message":"Password must be at least 8 characters long"}]}'),
            ("409 Conflict", "An account with this email already exists", '{"error":"Conflict","message":"An account with this email already exists"}'),
            ("429 Too Many Requests", "Rate limit exceeded (20 requests / 15 min / IP)", '{"error":"TooManyRequests","message":"Too many attempts, please try again later"}'),
        ],
    ),
    dict(
        method="POST", path="/api/auth/login", required=False,
        description="Authenticate with university email + password and receive a signed JWT access token.",
        auth="Not required (public)",
        authz="N/A",
        params=[
            ("universityEmail", "String", "Yes", ""),
            ("password", "String", "Yes", ""),
        ],
        success_code="200 OK",
        success_body='{\n  "user": { "id": "665f0...", "fullName": "Jane Smith", "role": "student" },\n  "token": "eyJhbGciOiJIUzI1NiIs..."\n}',
        errors=[
            ("400 Bad Request", "Missing email or password", '{"error":"ValidationError","message":"One or more fields are invalid"}'),
            ("401 Unauthorized", "Email not found or password incorrect (identical message for both, to avoid leaking which emails are registered)", '{"error":"InvalidCredentials","message":"Email or password is incorrect"}'),
            ("403 Forbidden", "Account has been suspended by an admin", '{"error":"Forbidden","message":"This account has been suspended. Contact an administrator."}'),
            ("429 Too Many Requests", "Rate limit exceeded - mitigates credential-stuffing / brute force", '{"error":"TooManyRequests","message":"Too many attempts, please try again later"}'),
        ],
    ),
    dict(
        method="GET", path="/api/auth/me", required=False,
        description="Return the profile of the currently authenticated user, resolved from the JWT (never trusts a client-supplied user id).",
        auth="Required - Bearer JWT",
        authz="Self only",
        params=[],
        success_code="200 OK",
        success_body='{ "user": { "id": "665f0...", "fullName": "Jane Smith", "role": "student", "status": "active" } }',
        errors=[("401 Unauthorized", "Missing, invalid, or expired JWT", '{"error":"TokenExpired","message":"JWT has expired, please log in again"}')],
    ),
    dict(
        method="POST", path="/api/auth/forgot-password", required=False,
        description="(Planned supporting endpoint - see note below) Issues a short-lived, single-use password reset token and emails a reset link to the user's university address.",
        auth="Not required (public)",
        authz="N/A",
        params=[("universityEmail", "String", "Yes", "")],
        success_code="200 OK",
        success_body='{ "message": "If that email exists, a reset link has been sent." }',
        errors=[("400 Bad Request", "Invalid email format", '{"error":"ValidationError","message":"One or more fields are invalid"}')],
    ),
    dict(
        method="POST", path="/api/auth/reset-password", required=False,
        description="(Planned supporting endpoint) Consumes a reset token and sets a new password; the token is single-use and expires after 30 minutes.",
        auth="Not required (the resetToken itself acts as a one-time credential)",
        authz="N/A",
        params=[
            ("resetToken", "String", "Yes", "Raw token from the emailed link; only its bcrypt hash is stored server-side"),
            ("newPassword", "String", "Yes", "Minimum 8 characters"),
        ],
        success_code="200 OK",
        success_body='{ "message": "Password updated successfully" }',
        errors=[
            ("400 Bad Request", "Weak password", '{"error":"ValidationError","message":"Password must be at least 8 characters long"}'),
            ("401 Unauthorized", "Token invalid, already used, or expired", '{"error":"InvalidToken","message":"This reset link is invalid or has expired"}'),
        ],
    ),
]
for ep in auth_eps:
    endpoint_block(ep)
add_para(
    "Note on scope: /api/auth/register, /api/auth/login, and /api/auth/me are fully implemented in the source "
    "code submitted with this assignment (see Section 4). /api/auth/forgot-password and /api/auth/reset-password "
    "are documented to the same level of rigor (including the PasswordResetToken entity in Section 3) as a planned "
    "extension, since the assignment scope for live implementation is limited to two endpoints from one core feature.",
    italic=True, size=9.5, color=GREY,
)

add_heading("2.2 Authorization", level=2)
add_para(
    "CampusCart uses two complementary authorization mechanisms layered on top of authentication:"
)
add_bullets([
    "Role-Based Access Control (RBAC): every JWT encodes the user's role (student or admin). The requireRole(...) "
    "middleware rejects requests from a role that is not permitted to call that route - for example, only "
    "student/admin roles may create a listing in the first place, and a hypothetical future 'banned' role would "
    "be rejected entirely at the requireAuth stage.",
    "Resource-ownership Access Control List (ACL): for actions on an existing resource (editing/deleting a listing, "
    "managing a saved-list entry), the API does not rely on role alone. It loads the resource, compares its "
    "seller/user field against req.user._id (taken from the verified JWT, never from the request body or URL), "
    "and only allows the action if the requester owns the resource or is an admin. This directly mitigates the "
    "OWASP 'Broken Access Control' risk of a user editing or deleting someone else's data by guessing an id.",
])
admin_eps = [
    dict(
        method="GET", path="/api/admin/listings", required=False,
        description="(Documented - Admin Dashboard core feature, not one of the 3 selected features, but included here as it is a security-relevant, role-gated endpoint) List all listings, including flagged/removed ones, for moderation.",
        auth="Required - Bearer JWT",
        authz="role=admin only",
        params=[("status", "String (query)", "No", "Filter by active | sold | flagged | removed")],
        success_code="200 OK",
        success_body='{ "listings": [ { "_id": "665f1...", "status": "flagged" } ] }',
        errors=[("403 Forbidden", "Authenticated but not an admin", '{"error":"Forbidden","message":"Requires one of the following roles: admin"}')],
    ),
    dict(
        method="PATCH", path="/api/admin/users/:id/status", required=False,
        description="(Documented) Suspend, warn, or reactivate a user account, e.g. after a policy violation.",
        auth="Required - Bearer JWT",
        authz="role=admin only",
        params=[("status", "String (enum)", "Yes", "active | warned | suspended")],
        success_code="200 OK",
        success_body='{ "user": { "id": "665f0...", "status": "suspended" } }',
        errors=[
            ("403 Forbidden", "Not an admin", '{"error":"Forbidden","message":"Requires one of the following roles: admin"}'),
            ("404 Not Found", "User id does not exist", '{"error":"NotFound","message":"User not found"}'),
        ],
    ),
]
for ep in admin_eps:
    endpoint_block(ep)

add_heading("2.3 Data Validation Strategy", level=2)
add_para("Every write endpoint validates input at two layers before it ever reaches the database:")
add_bullets([
    "Layer 1 - express-validator at the route level: checks types, lengths, enum membership, email format, and "
    "numeric ranges, and rejects the request with 400 Bad Request and a field-level error list before the "
    "controller runs any business logic.",
    "Layer 2 - Mongoose schema validation at the model level: enforces required fields, enum values, and types "
    "again at the data layer, so the database can never persist an invalid document even if a future endpoint "
    "forgets to call the validator middleware.",
])

add_heading("2.4 Mitigating Security Risks Covered in Class", level=2)
risk_table_data = [
    ("Injection (NoSQL injection)", "Mongoose's query builder parameterizes all queries, so user input is never concatenated into a query string. The express-mongo-sanitize middleware additionally strips any keys starting with '$' or containing '.' from req.body/req.query/req.params, so an attacker cannot send {\"universityEmail\": {\"$gt\": \"\"}} to bypass a login check or filter."),
    ("Broken Access Control", "Ownership checks (Section 2.2) ensure a JWT only grants access to the holder's own resources; RBAC middleware separately gates admin-only routes. Mongo ObjectIds are validated with isMongoId() so a malformed id cannot be used to probe internal behaviour."),
    ("Broken Authentication / credential stuffing", "Passwords are hashed with bcrypt (cost factor 12, salted automatically) - plaintext passwords are never stored or logged. Login and register are rate-limited (20 requests / 15 minutes / IP) via express-rate-limit. JWTs expire after 1 hour, limiting the blast radius of a stolen token."),
    ("Mass assignment", "Controllers whitelist exactly which fields can be set from the request body (e.g. role is hard-coded to 'student' on register and can never be supplied by the client; updateListing only copies a fixed allow-list of fields), rather than blindly spreading req.body into a Mongoose document."),
    ("Sensitive data exposure", "passwordHash is excluded from every API response via .select('-passwordHash') and is never included in the JSON serialization of a User. Helmet sets secure HTTP headers (X-Content-Type-Options, no X-Powered-By, etc.)."),
    ("Cross-Origin misuse", "CORS is restricted to an explicit allow-list of origins (the deployed frontend URL) via the CORS_ORIGIN environment variable, rather than reflecting any origin."),
]
table = doc.add_table(rows=1, cols=2)
table.style = "Light Grid Accent 1"
hdr = table.rows[0].cells
hdr[0].text = "Risk"
hdr[1].text = "Mitigation in CampusCart's API"
for c in hdr:
    c.paragraphs[0].runs[0].bold = True
for risk, mitigation in risk_table_data:
    row = table.add_row().cells
    row[0].text = risk
    row[0].paragraphs[0].runs[0].bold = True
    row[1].text = mitigation
doc.add_paragraph()

doc.add_page_break()

# =====================================================================
# 3. DATA INTEGRATION STRATEGY
# =====================================================================
add_heading("3. Data Integration Strategy", level=1)
add_para(
    "CampusCart persists data in MongoDB (MongoDB Atlas in production) using Mongoose schemas. The diagram "
    "below sketches the four collections needed to support the three core features documented in Section 1 "
    "plus the security entities from Section 2."
)

doc.add_picture("erd_diagram.png", width=Inches(6.6))
last_p = doc.paragraphs[-1]
last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap = doc.add_paragraph()
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap.add_run("Figure 1. CampusCart Entity Relationship Diagram")
r.italic = True
r.font.size = Pt(9.5)
r.font.color.rgb = GREY

add_heading("3.1 Entity Definitions", level=2)

def entity_table(name, rows):
    add_para(name, bold=True, size=11, space_after=2)
    table = doc.add_table(rows=1, cols=4)
    table.style = "Light Grid Accent 1"
    hdr = table.rows[0].cells
    for i, h in enumerate(["Field", "Type", "Required?", "Notes"]):
        hdr[i].text = h
        hdr[i].paragraphs[0].runs[0].bold = True
    for field, ftype, req, notes in rows:
        row = table.add_row().cells
        row[0].text = field
        row[1].text = ftype
        row[2].text = req
        row[3].text = notes
    doc.add_paragraph()

entity_table("User", [
    ("_id", "ObjectId (PK)", "Auto", "MongoDB-generated primary key"),
    ("fullName", "String", "Required", "Max 100 characters"),
    ("universityEmail", "String", "Required, unique", "Validated email format; must be a university domain"),
    ("studentId", "String", "Optional", "Self-reported student id"),
    ("passwordHash", "String", "Required", "bcrypt hash; never returned in API responses"),
    ("role", "Enum", "Required", "student (default) | admin"),
    ("status", "Enum", "Required", "active (default) | warned | suspended"),
    ("createdAt / updatedAt", "Date", "Auto", "Mongoose timestamps"),
])

entity_table("Listing", [
    ("_id", "ObjectId (PK)", "Auto", ""),
    ("title", "String", "Required", "Max 120 characters"),
    ("description", "String", "Required", "Max 2000 characters"),
    ("price", "Number", "Required", ">= 0"),
    ("category", "Enum", "Required", "Textbooks | Electronics | Furniture | Accessories | Other"),
    ("condition", "Enum", "Required", "New | Like New | Good | Fair"),
    ("images", "Array<String>", "Optional", "Up to 6 URLs"),
    ("seller", "ObjectId (FK -> User)", "Required", "Owner of the listing"),
    ("status", "Enum", "Required", "active (default) | sold | flagged | removed"),
    ("views", "Number", "Auto", "Default 0; incremented on GET /api/listings/:id"),
    ("createdAt / updatedAt", "Date", "Auto", ""),
])

entity_table("SavedListing", [
    ("_id", "ObjectId (PK)", "Auto", ""),
    ("user", "ObjectId (FK -> User)", "Required", "Who saved the listing"),
    ("listing", "ObjectId (FK -> Listing)", "Required", "What was saved"),
    ("createdAt", "Date", "Auto", "Compound unique index on (user, listing) prevents duplicate saves"),
])

entity_table("PasswordResetToken", [
    ("_id", "ObjectId (PK)", "Auto", ""),
    ("user", "ObjectId (FK -> User)", "Required", ""),
    ("tokenHash", "String", "Required", "bcrypt hash of the emailed token; raw token is never stored"),
    ("expiresAt", "Date", "Required", "30 minutes after creation"),
    ("used", "Boolean", "Required", "Default false; set true after a successful reset (single-use)"),
    ("createdAt", "Date", "Auto", ""),
])

add_heading("3.2 CRUD Operations Mapping", level=2)
add_para(
    "The table below maps each entity to the CRUD (and related) operations performed against it, and the "
    "exact API endpoint the client calls to trigger that operation."
)

crud_rows = [
    ("User", "Create", "POST /api/auth/register", "Public"),
    ("User", "Read (self)", "GET /api/auth/me", "Owner"),
    ("User", "Update (status)", "PATCH /api/admin/users/:id/status", "Admin"),
    ("Listing", "Create", "POST /api/listings", "Authenticated student/admin"),
    ("Listing", "Read (one)", "GET /api/listings/:id", "Public"),
    ("Listing", "Read (many / search / filter / sort / paginate)", "GET /api/listings", "Public"),
    ("Listing", "Update", "PUT /api/listings/:id", "Owner or admin"),
    ("Listing", "Delete", "DELETE /api/listings/:id", "Owner or admin"),
    ("Listing", "Moderate (read all incl. flagged)", "GET /api/admin/listings", "Admin"),
    ("SavedListing", "Create", "POST /api/saved/:id", "Authenticated user"),
    ("SavedListing", "Read (own list)", "GET /api/saved", "Owner"),
    ("SavedListing", "Delete", "DELETE /api/saved/:id", "Owner"),
    ("PasswordResetToken", "Create", "POST /api/auth/forgot-password", "Public"),
    ("PasswordResetToken", "Consume / Update (used=true)", "POST /api/auth/reset-password", "Holder of raw token"),
]
table = doc.add_table(rows=1, cols=4)
table.style = "Light Grid Accent 1"
hdr = table.rows[0].cells
for i, h in enumerate(["Entity", "Operation", "Endpoint", "Who can perform it"]):
    hdr[i].text = h
    hdr[i].paragraphs[0].runs[0].bold = True
for entity_name, op, endpoint, who in crud_rows:
    row = table.add_row().cells
    row[0].text = entity_name
    row[1].text = op
    row[2].text = endpoint
    row[3].text = who
doc.add_paragraph()

doc.add_page_break()

# =====================================================================
# 4. IMPLEMENTATION AND DEPLOYMENT
# =====================================================================
add_heading("4. Implementation and Deployment", level=1)
add_para(
    "Two endpoints from Core Feature 2 (Product Listing Management) were implemented end-to-end and deployed "
    "live, with the supporting registration/login endpoints needed to obtain a JWT and complete the workflow:"
)
add_bullets([
    "POST /api/listings - create a new product listing (requires authentication)",
    "GET /api/listings - browse/search/filter/sort/paginate listings (public)",
    "Supporting endpoints enabling the full workflow: POST /api/auth/register, POST /api/auth/login",
])

add_heading("4.1 Technology Stack", level=2)
add_bullets([
    "Runtime/Framework: Node.js + Express.js",
    "Database: MongoDB Atlas (cloud-hosted), accessed via Mongoose",
    "Authentication: JSON Web Tokens (jsonwebtoken), bcryptjs for password hashing",
    "Validation/Security middleware: express-validator, express-mongo-sanitize, helmet, cors, express-rate-limit",
    "Hosting (backend): Render (Node web service, free tier, auto-deploys from Git)",
])

add_heading("4.2 Live Endpoint URLs", level=2)
add_para("[ TODO - fill in after deploying to Render/Heroku/AWS ]", bold=True, color=RED)
table = doc.add_table(rows=1, cols=3)
table.style = "Light Grid Accent 1"
hdr = table.rows[0].cells
for i, h in enumerate(["Endpoint", "Method", "Live URL"]):
    hdr[i].text = h
    hdr[i].paragraphs[0].runs[0].bold = True
for ep, method in [("Health check", "GET"), ("Register", "POST"), ("Login", "POST"), ("Create Listing", "POST"), ("Browse Listings", "GET")]:
    row = table.add_row().cells
    row[0].text = ep
    row[1].text = method
    row[2].text = "https://<your-app-name>.onrender.com/api/..."
doc.add_paragraph()

add_heading("4.3 Source Code", level=2)
add_para("GitHub repository: [ TODO - paste your repo URL here, or note that a zip file is attached on Brightspace ]", bold=True, color=RED)
add_para(
    "The backend source code is provided in the /backend directory of this submission, containing the Express "
    "app (src/app.js, src/server.js), Mongoose models (src/models/), JWT/RBAC middleware (src/middleware/auth.js), "
    "input-validation middleware (src/middleware/validate.js), route/controller pairs for auth, listings, and "
    "saved listings, a seed script (src/seed/seed.js), and an automated smoke test that exercises every endpoint "
    "against an in-memory MongoDB instance (src/seed/memoryServerSmokeTest.js, runnable via `npm run test:memory`)."
)

add_heading("4.4 Database Source Files", level=2)
add_para(
    "campuscart-sample-data.json (included with this submission) contains a full export of the seeded "
    "User, Listing, and SavedListing collections, produced by running `npm run seed` against the database. "
    "This satisfies the requirement to provide the source files for the database with data in it."
)

add_heading("4.5 Postman Evidence", level=2)
add_para(
    "A ready-to-import Postman collection (backend/postman/CampusCart.postman_collection.json) is included. "
    "Import it, set the collection variable baseUrl to the deployed Render URL, and run the requests in order "
    "(01 through 11) to reproduce every screenshot listed below."
)

screenshot_list = [
    "01 - Register (success) - 201 response showing the created user and JWT",
    "02 - Register (error: duplicate email) - 409 Conflict response",
    "03 - Register (error: invalid email / weak password) - 400 validation error response",
    "04 - Login (authentication failure: wrong password) - 401 response",
    "05 - Login (authentication success) - 200 response with JWT",
    "06 - Create Listing [REQUIRED ENDPOINT] (success, persists data) - 201 response with the created listing",
    "07 - Create Listing (authentication failure: no token) - 401 response",
    "08 - Create Listing (error: invalid body) - 400 validation error response",
    "09 - Browse Listings [REQUIRED ENDPOINT] (public, filter+sort) - 200 response showing the listing created in step 6, proving persistence",
    "10 - Get Listing By Id - 200 response showing views incremented",
    "11 - Get Listing By Id (error: not found) - 404 response",
    "12 - MongoDB Atlas dashboard (or Compass) showing the persisted 'listings' collection with the document created via Postman",
]
add_para("Required screenshots (annotate each with the step name before pasting):", bold=True, space_after=4)
for label in screenshot_list:
    add_screenshot_placeholder(label)

doc.add_page_break()

# =====================================================================
# 5. REFERENCES
# =====================================================================
add_heading("5. References", level=1)
refs = [
    "OWASP Foundation. (2021). OWASP Top 10:2021. https://owasp.org/Top10/",
    "Fielding, R. T. (2000). Architectural Styles and the Design of Network-based Software Architectures (REST). University of California, Irvine.",
    "MongoDB, Inc. (2024). Mongoose Documentation. https://mongoosejs.com/docs/",
    "Express.js. (2024). Express API Reference. https://expressjs.com/en/4x/api.html",
    "jwt.io. (2024). Introduction to JSON Web Tokens. https://jwt.io/introduction",
    "Group 8. (2026). CampusCart Project Proposal. Dalhousie University, CSCI 5709.",
]
for r_ in refs:
    add_bullets([r_])

doc.save("Assignment2_Report.docx")
print("FINAL report saved as Assignment2_Report.docx")
