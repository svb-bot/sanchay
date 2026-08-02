import { Router } from "express";
import {
    addBillPaymentMode,
    fetchBillPaymentModes,
    fetchBillPaymentModeById,
    editBillPaymentMode,
    removeBillPaymentMode
} from "../controllers/billPaymentModeController.js";

const router = Router();

router.get("/", fetchBillPaymentModes);
router.post("/", addBillPaymentMode);
router.get("/:id", fetchBillPaymentModeById);
router.put("/:id", editBillPaymentMode);
router.delete("/:id", removeBillPaymentMode);

export default router;