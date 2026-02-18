import express from "express";
import { validateBody } from "../middlewares/validate.js";
import { registerUser, getUsers, getUserById } from "../controllers/userController.js";
import { userSchema } from "../validators/userValidator.js";

const router = express.Router();

router.post("/register", validateBody(userSchema), registerUser);
router.get("/", getUsers);
router.get("/:id", getUserById);
export default router;
