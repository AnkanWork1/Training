import Order  from "../models/Order.js";

export const OrderRepository = {
  async create(data) {
    return Order.create(data);
  },

  async findByAccount(accountId, { limit = 10, cursor }) {
    const query = { accountId };

    if (cursor) {
      query._id = { $lt: cursor };
    }

    return Order.find(query)
      .sort({ _id: -1 })
      .limit(limit)
      .lean();
  }
};
