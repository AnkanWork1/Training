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

// GET /users
export const getUsers = async (req, res, next) => {
  try {
    const users = await User.find().lean();
    res.json(users);
  } catch (err) {
    next(err);
  }
};

// GET /users/:id
export const getUserById = async (req, res, next) => {
  try {
    const user = await User.findById(req.params.id).lean();

    if (!user) {
      return res.status(404).json({ message: "User not found" });
    }

    res.json(user);
  } catch (err) {
    next(err);
  }
};