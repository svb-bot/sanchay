import { Router } from "express";
import {
    addPaymentMode,
    fetchPaymentModes,
    fetchPaymentModeById,
    editPaymentMode,
    removePaymentMode
} from "../controllers/paymentModeController.js";

const router = Router();

router.get("/", fetchPaymentModes);
router.post("/", addPaymentMode);
router.get("/:id", fetchPaymentModeById);
router.put("/:id", editPaymentMode);
router.delete("/:id", removePaymentMode);

export default router;