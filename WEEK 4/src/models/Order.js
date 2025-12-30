import mongoose from "mongoose";

const orderSchema = new mongoose.Schema(
  {
    accountId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Account",
      required: true,
      index: true
    },

    amount: {
      type: Number,
      required: true,
      min: 0
    },

    status: {
      type: String,
      enum: ["PENDING", "COMPLETED", "CANCELLED"],
      default: "PENDING"
    }
  },
  {
    timestamps: true
  }
);

/* Compound index for order history */
orderSchema.index({ accountId: 1, createdAt: -1 });

const Order = mongoose.model("Order", orderSchema);
export default Order;