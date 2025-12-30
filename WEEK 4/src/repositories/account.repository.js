import  Account  from "../models/Account.js";

export const AccountRepository = {
  async create(data) {
    const account = new Account(data);
    return account.save();
  },

  async findById(id) {
    return Account.findById(id).lean();
  },

  async findPaginated({ limit = 10, cursor }) {
    const query = {};

    if (cursor) {
      query._id = { $lt: cursor }; // cursor-based pagination
    }

    return Account.find(query)
      .sort({ _id: -1 })
      .limit(limit)
      .lean();
  },

  async update(id, updates) {
    return Account.findByIdAndUpdate(id, updates, {
      new: true,
      runValidators: true
    }).lean();
  },

  async delete(id) {
    return Account.findByIdAndDelete(id);
  }
};
