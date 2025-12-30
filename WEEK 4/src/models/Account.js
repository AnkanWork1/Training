import mongoose from "mongoose";

const accountSchema = new mongoose.Schema(
  {
    firstName: {
      type: String,
      required: true,
      trim: true,
    },
    lastName: {
      type: String,
      required: true,
      trim: true,
    },
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      trim: true,
      match: /.+\@.+\..+/, // validation
    },
    password: {
      type: String,
      required: true,
      minlength: 8,
    },
    status: {
      type: String,
      enum: ["ACTIVE", "BLOCKED"],
      default: "ACTIVE",
    },
  },
  {
    timestamps: true, // createdAt, updatedAt
  }
);

/* ---------- VIRTUAL FIELD ---------- */
accountSchema.virtual("fullName").get(function () {
  return `${this.firstName} ${this.lastName}`;
});

/* ---------- INDEX ---------- */
accountSchema.index({ status: 1, createdAt: -1 });

/* ---------- PRE-SAVE HOOK ---------- */
// Using regular function with next callback for synchronous preprocessing
accountSchema.pre("save", function () {
  // Ensure email is always lowercase
  this.email = this.email.toLowerCase();
  // If you need async code later, convert this to async and remove next()
});

// Create and export model
const Account = mongoose.model("Account", accountSchema);
export default Account;
