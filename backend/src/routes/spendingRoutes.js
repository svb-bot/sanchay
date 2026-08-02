import { Router } from "express";
import {
    addSpending,
    fetchSpending
} from "../controllers/spendingController.js";

const router = Router();

router.get("/", fetchSpending);
router.post("/", addSpending);

export default router;