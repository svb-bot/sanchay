import { Router } from "express";
import {
    fetchPaymentCategories,
    addPaymentCategory,
    editPaymentCategory,
    removePaymentCategory,
    fetchPaymentCategoryById
} from "../controllers/paymentCategoryController.js";

const router = Router();

router.get("/", fetchPaymentCategories);
router.post("/", addPaymentCategory);
router.get("/:id", fetchPaymentCategoryById);
router.put("/:id", editPaymentCategory);
router.delete("/:id", removePaymentCategory);

export default router;