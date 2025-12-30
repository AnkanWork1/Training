import { loadEnv } from "../config/env.js";
import { config } from "../config/index.js";
import { connectDB } from "../loaders/db.js";
import { AccountRepository } from "../repositories/account.repository.js";
import { OrderRepository } from "../repositories/order.repository.js";

loadEnv();
async function seed() {
    console.log(config);
  await connectDB(config().db.uri);

  const account = await AccountRepository.create({
    firstName: "Ankan",
    lastName: "Guha",
    email: "ankanguha@test.com",
    password: "password123"
  });

  console.log("Created account:", account.fullName);

  const order = await OrderRepository.create({
    accountId: account._id,
    amount: 2500
  });

  console.log("Created order:", order);
  process.exit(0);
}

seed();
console.log("🟣 seed.js running");
