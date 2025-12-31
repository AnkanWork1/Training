import express from "express";
import { getProducts, softDeleteProduct } from "../controllers/product.controller.js";

const router = express.Router();

router.get("/", getProducts);
router.delete("/:id", softDeleteProduct);

export default router;
