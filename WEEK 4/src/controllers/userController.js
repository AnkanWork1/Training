import User from "../models/User.js";
import { sanitizeObject } from "../utils/sanitize.js";

export const registerUser = async (req, res) => {
  try {
    // 🔐 sanitize incoming data
    const cleanBody = sanitizeObject(req.body);

    const user = await User.create(cleanBody);

    res.status(201).json({
      message: "User created",
      user
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
