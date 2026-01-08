import express from "express";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import User from "../models/User.js";

const router = express.Router();

router.post("/register", async (req, res) => {
  const { username, key } = req.body;

  if (!username || !key)
    return res.json({ success: false, message: "Missing fields" });

  const existing = await User.findOne({ username });
  if (existing)
    return res.json({ success: false, message: "Username already exists" });

  const hashedKey = await bcrypt.hash(key, 10);

  const user = new User({ username, key: hashedKey });
  await user.save();

  res.json({ success: true, message: "User registered" });
});

router.post("/login", async (req, res) => {
  const { username, key } = req.body;

  const user = await User.findOne({ username });
  if (!user)
    return res.json({ success: false });

  const match = await bcrypt.compare(key, user.key);
  if (!match)
    return res.json({ success: false });

  const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, {
    expiresIn: "1d"
  });

  res.json({ success: true, token });
});

export default router;
