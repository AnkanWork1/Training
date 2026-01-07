import mongoose from "mongoose";

const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true
    },

    description: {
      type: String,
      trim: true
    },

    price: {
      type: Number,
      required: true,
      min: 0
    },

    tags: {
      type: [String],
      default: []
    },

    deletedAt: {
      type: Date,
      default: null,
      index: true
    }
  },
  { timestamps: true }
);

/**
 * ✅ GLOBAL SOFT DELETE FILTER
 * Automatically exclude soft-deleted docs
 */
productSchema.pre(/^find/, function () {
  // `this` is the mongoose query
  if (this.options && this.options.includeDeleted) {
    return;
  }

  this.where({ deletedAt: null });
});

const Product = mongoose.model("Product", productSchema);
export default Product;
