import express from "express";
import { validateBody } from "../middlewares/validate.js";
import { registerUser } from "../controllers/userController.js";
import { userSchema } from "../validators/userValidator.js";

const router = express.Router();

router.post("/register", validateBody(userSchema), registerUser);

export default router;
