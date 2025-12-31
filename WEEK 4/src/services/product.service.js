import Product from "../models/product.model.js";
import { AppError } from "../utils/AppError.js";

export const getProducts = async (query) => {
  const { search, minPrice, maxPrice, tags, sort = "createdAt:desc", page = 1, limit = 10, includeDeleted } = query;

  const filters = {};

  if (!includeDeleted) filters.deletedAt = null;

  if (search) {
    filters.$or = [
      { name: { $regex: search, $options: "i" } },
      { description: { $regex: search, $options: "i" } },
    ];
  }

  if (minPrice || maxPrice) {
    filters.price = {};
    if (minPrice) filters.price.$gte = Number(minPrice);
    if (maxPrice) filters.price.$lte = Number(maxPrice);
  }

  if (tags) {
    filters.tags = { $all: tags.split(",") };
  }

  const [sortField, sortOrder] = sort.split(":");
  const sortObj = { [sortField]: sortOrder === "desc" ? -1 : 1 };

  const skip = (page - 1) * limit;

  return Product.find(filters).sort(sortObj).skip(Number(skip)).limit(Number(limit));
};

export const softDeleteProduct = async (id) => {
  const product = await Product.findById(id);
  if (!product) throw new AppError("Product not found", 404, "PRODUCT_NOT_FOUND");

  product.deletedAt = new Date();
  await product.save();
};
