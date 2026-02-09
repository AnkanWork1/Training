// src/services/product.service.js
import Product from "../models/product.model.js";
import { AppError } from "../utils/AppError.js";
import mongoose from "mongoose";

const productService = {
  getProducts: async (query) => {
    const { search, minPrice, maxPrice, tags, sort = "createdAt:desc", page = 1, limit = 10, includeDeleted } = query;
    const filters = {};

    if (search) {
      filters.$or = [
        { name: { $regex: search, $options: "i" } },
        { description: { $regex: search, $options: "i" } }
      ];
    }

    if (minPrice || maxPrice) {
      filters.price = {};
      if (minPrice) filters.price.$gte = Number(minPrice);
      if (maxPrice) filters.price.$lte = Number(maxPrice);
    }

    if (tags) filters.tags = { $all: tags.split(",") };

    const [sortField, sortOrder] = sort.split(":");
    const sortObj = { [sortField]: sortOrder === "desc" ? -1 : 1 };

    const skip = (page - 1) * limit;
    const includeDeletedBool = includeDeleted === "true";

    const products = await Product.find(filters)
      .setOptions({ includeDeleted: includeDeletedBool })
      .sort(sortObj)
      .skip(Number(skip))
      .limit(Number(limit));

    return products;
  },

  getProductById: async (id) => {
    if (!mongoose.Types.ObjectId.isValid(id)) return { message: "Invalid product ID" };
    const product = await Product.findOne({ _id: id });
    if (!product) return { message: "Product not found -> was softDeleted" };
    return product;
  },

  softDeleteProduct: async (id) => {
    if (!mongoose.Types.ObjectId.isValid(id)) return { message: "Invalid product ID" };
    const product = await Product.findOne({ _id: id });
    if (!product) return { message: "Product not found or already deleted" };
    product.deletedAt = new Date();
    await product.save();
    return { success: true, message: "Product deleted successfully" };
  },

  restoreProduct: async (id) => {
    const product = await Product.findOne({ _id: id }).setOptions({ includeDeleted: true });
    if (!product) throw new AppError("Product not found", 404);
    product.deletedAt = null;
    await product.save();
    return { success: true, message: "Product restored successfully" };
  }
};

export default productService;
