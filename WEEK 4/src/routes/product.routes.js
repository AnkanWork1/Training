import express from "express";
import * as productController from "../controllers/product.controller.js";

const router = express.Router();

router.get("/", productController.getProducts);
router.get("/:id", productController.getProductById);
router.delete("/:id", productController.softDeleteProduct);
router.patch("/:id/restore", productController.restoreProduct);

export default router;
