const express = require("express");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
// Inside Docker Compose the backend is reachable by its service name "backend"
const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:5000";

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.urlencoded({ extended: true }));

// Show the form
app.get("/", (req, res) => {
  res.render("index", { error: null, form: {} });
});

// Receive the form and forward it to the Flask backend
app.post("/submit", async (req, res) => {
  const form = {
    name: req.body.name || "",
    email: req.body.email || "",
    message: req.body.message || "",
  };

  try {
    const response = await fetch(`${BACKEND_URL}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const result = await response.json();

    if (!response.ok || !result.success) {
      return res.render("index", { error: result.error || "Something went wrong.", form });
    }
    res.render("success", { result });
  } catch (err) {
    res.render("index", { error: `Could not reach backend: ${err.message}`, form });
  }
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Frontend running on port ${PORT}, backend at ${BACKEND_URL}`);
});
