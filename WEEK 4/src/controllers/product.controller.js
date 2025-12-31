import * as productService from "../services/product.service.js";
import { AppError } from "../utils/AppError.js";

export const getProducts = async (req, res, next) => {
  try {
    const products = await productService.getProducts(req.query);
    res.json({ success: true, data: products });
  } catch (err) {
    next(err);
  }
};

export const softDeleteProduct = async (req, res, next) => {
  try {
    await productService.softDeleteProduct(req.params.id);
    res.json({ success: true, message: "Product soft deleted" });
  } catch (err) {
    next(err);
  }
};
