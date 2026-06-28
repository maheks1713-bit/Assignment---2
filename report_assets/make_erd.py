import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D

fig, ax = plt.subplots(figsize=(14, 9.5))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10.2)
ax.axis("off")

HEADER_BLUE = "#2B5FD9"
BODY_FILL = "#F4F7FF"
BORDER = "#1F3C8C"
PK_COLOR = "#B00020"
FK_COLOR = "#0B6E4F"


def entity(ax, x, y, w, h, title, fields):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                          linewidth=1.4, edgecolor=BORDER, facecolor=BODY_FILL, zorder=2)
    ax.add_patch(box)
    header_h = 0.45
    header = FancyBboxPatch((x, y + h - header_h), w, header_h,
                             boxstyle="round,pad=0.0,rounding_size=0.06",
                             linewidth=1.4, edgecolor=BORDER, facecolor=HEADER_BLUE, zorder=3)
    ax.add_patch(header)
    ax.text(x + w / 2, y + h - header_h / 2, title, ha="center", va="center",
            fontsize=12, fontweight="bold", color="white", zorder=4)

    line_h = (h - header_h) / max(len(fields), 1)
    for i, (fname, ftype, marker) in enumerate(fields):
        fy = y + h - header_h - (i + 0.5) * line_h
        color = PK_COLOR if marker == "PK" else (FK_COLOR if marker == "FK" else "#222222")
        label = f"{marker + '  ' if marker else ''}{fname}"
        ax.text(x + 0.15, fy, label, ha="left", va="center", fontsize=8.8, color=color, zorder=4)
        ax.text(x + w - 0.15, fy, ftype, ha="right", va="center", fontsize=7.8, color="#555555",
                style="italic", zorder=4)
    return dict(x=x, y=y, w=w, h=h)


def hedge(ax, box_left_right_pair, y, label, m1, m2):
    (x1, x2) = box_left_right_pair
    ax.add_line(Line2D([x1, x2], [y, y], color="#555555", linewidth=1.3, zorder=1))
    ax.text(x1 + 0.18, y + 0.15, m1, fontsize=9, color="#333333", fontweight="bold", ha="center", va="center")
    ax.text(x2 - 0.18, y + 0.15, m2, fontsize=9, color="#333333", fontweight="bold", ha="center", va="center")
    ax.text((x1 + x2) / 2, y + 0.28, label, fontsize=8.5, color="#1F3C8C", style="italic",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))


def vedge(ax, x, top_y, bottom_y, label, m_top, m_bottom):
    ax.add_line(Line2D([x, x], [top_y, bottom_y], color="#555555", linewidth=1.3, zorder=1))
    ax.text(x - 0.25, top_y - 0.2, m_top, fontsize=9, color="#333333", fontweight="bold", ha="center", va="center")
    ax.text(x - 0.25, bottom_y + 0.2, m_bottom, fontsize=9, color="#333333", fontweight="bold", ha="center", va="center")
    ax.text(x + 0.35, (top_y + bottom_y) / 2, label, fontsize=8.5, color="#1F3C8C", style="italic",
            ha="left", va="center", rotation=90, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))


# ---- Entities ----
user = entity(ax, 0.5, 6.1, 3.2, 2.8, "User", [
    ("_id", "ObjectId", "PK"),
    ("fullName", "String, req.", ""),
    ("universityEmail", "String, req., unique", ""),
    ("studentId", "String, opt.", ""),
    ("passwordHash", "String, req.", ""),
    ("role", "Enum[student,admin]", ""),
    ("status", "Enum[active,warned,suspended]", ""),
    ("createdAt / updatedAt", "Date", ""),
])

listing = entity(ax, 4.4, 6.1, 4.0, 2.8, "Listing", [
    ("_id", "ObjectId", "PK"),
    ("title", "String, req.", ""),
    ("description", "String, req.", ""),
    ("price", "Number, req., >=0", ""),
    ("category", "Enum, req.", ""),
    ("condition", "Enum, req.", ""),
    ("images", "[String], opt.", ""),
    ("seller", "ObjectId -> User", "FK"),
    ("status", "Enum, default active", ""),
    ("views", "Number, default 0", ""),
])

saved = entity(ax, 9.7, 6.5, 3.6, 2.0, "SavedListing", [
    ("_id", "ObjectId", "PK"),
    ("user", "ObjectId -> User", "FK"),
    ("listing", "ObjectId -> Listing", "FK"),
    ("createdAt", "Date", ""),
])

reset = entity(ax, 0.5, 1.0, 3.6, 2.4, "PasswordResetToken", [
    ("_id", "ObjectId", "PK"),
    ("user", "ObjectId -> User", "FK"),
    ("tokenHash", "String, req.", ""),
    ("expiresAt", "Date, req.", ""),
    ("used", "Boolean, default false", ""),
    ("createdAt", "Date", ""),
])

# ---- Relationships ----
hedge(ax, (user["x"] + user["w"], listing["x"]), 7.5, "lists", "1", "N")
hedge(ax, (listing["x"] + listing["w"], saved["x"]), 7.5, "is saved as", "1", "N")
vedge(ax, user["x"] + 1.6, user["y"], reset["y"] + reset["h"], "requests reset for", "1", "N")

ax.text(7, 9.85, "CampusCart - Entity Relationship Diagram", fontsize=15, fontweight="bold", ha="center")
ax.text(7, 9.45, "Core Feature 2 (Product Listing) + Core Feature 4 (Saved Listings) + Security entities",
        fontsize=10, ha="center", color="#444444")
ax.text(7, 9.15, "PK = Primary Key   |   FK = Foreign Key   |   Lines show 1 -> N cardinality",
        fontsize=8.8, ha="center", color="#666666", style="italic")

plt.tight_layout()
plt.savefig("erd_diagram.png", dpi=200, bbox_inches="tight")
print("Saved erd_diagram.png")
