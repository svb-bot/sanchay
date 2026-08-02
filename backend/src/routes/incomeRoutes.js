import { Router } from "express";
import {
    addIncome,
    fetchIncome
} from "../controllers/incomeController.js";

const router = Router();

router.get("/", fetchIncome);
router.post("/", addIncome);

export default router;