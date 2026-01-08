import mongoose from "mongoose";

const UserSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  key: { type: String, required: true }
});

export default mongoose.model("User", UserSchema);
