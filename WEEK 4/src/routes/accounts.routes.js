import express from "express";
import {
  createAccount,
  getAccountById,
  getAccounts,
  updateAccount,
  deleteAccount
} from "../controllers/account.controller.js";

const router = express.Router();

router.post("/", createAccount);
router.get("/", getAccounts);
router.get("/:id", getAccountById);
router.patch("/:id", updateAccount);
router.delete("/:id", deleteAccount);

export default router;
