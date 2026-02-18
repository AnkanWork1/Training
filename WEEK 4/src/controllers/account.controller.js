import { AccountRepository } from "../repositories/account.repository.js";

export const createAccount = async (req, res, next) => {
  try {
    const account = await AccountRepository.create(req.body);
    res.status(201).json(account);
  } catch (err) {
    next(err);
  }
};

export const getAccountById = async (req, res, next) => {
  try {
    const account = await AccountRepository.findById(req.params.id);

    if (!account) {
      return res.status(404).json({ message: "Account not found" });
    }

    res.json(account);
  } catch (err) {
    next(err);
  }
};

export const getAccounts = async (req, res, next) => {
  try {
    const limit = req.query.limit ? Number(req.query.limit) : 10;
    const cursor = req.query.cursor;

    const accounts = await AccountRepository.findPaginated({
      limit,
      cursor
    });

    res.json(accounts);
  } catch (err) {
    next(err);
  }
};

export const updateAccount = async (req, res, next) => {
  try {
    const account = await AccountRepository.update(
      req.params.id,
      req.body
    );

    if (!account) {
      return res.status(404).json({ message: "Account not found" });
    }

    res.json(account);
  } catch (err) {
    next(err);
  }
};

export const deleteAccount = async (req, res, next) => {
  try {
    const account = await AccountRepository.delete(req.params.id);

    if (!account) {
      return res.status(404).json({ message: "Account not found" });
    }

    res.json({ message: "Account deleted" });
  } catch (err) {
    next(err);
  }
};
