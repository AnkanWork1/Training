// src/routes/product.routes.js
import express from "express";
import {
  getProducts,
  getProductById,
  softDeleteProduct,
  restoreProduct
} from "../controllers/product.controller.js";

const router = express.Router();

router.get("/", getProducts);
router.get("/:id", getProductById);
router.delete("/:id", softDeleteProduct);
router.patch("/:id/restore", restoreProduct);

export default router;
