import * as productService from "../services/product.service.js";

export const getProducts = async (req, res, next) => {
  try {
    const products = await productService.getProducts(req.query);
    res.json({ success: true, data: products });
  } catch (err) {
    next(err);
  }
};

export const getProductById = async (req, res, next) => {
  try {
    const product = await productService.getProductById(req.params.id);
    res.json({ success: true, data: product });
  } catch (err) {
    next(err);
  }
};

export const softDeleteProduct = async (req, res, next) => {
  try {
    const result = await productService.softDeleteProduct(req.params.id);
    res.json(result);
  } catch (err) {
    next(err);
  }
};

export const restoreProduct = async (req, res, next) => {
  try {
    const result = await productService.restoreProduct(req.params.id);
    res.json(result);
  } catch (err) {
    next(err);
  }
};
