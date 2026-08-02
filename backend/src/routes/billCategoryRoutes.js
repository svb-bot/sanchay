import { Router } from "express";
import {
    fetchBillCategories,
    addBillCategory,
    fetchBillCategoryById,
    editBillCategory,
    removeBillCategory
} from "../controllers/billCategoryController.js";

const router = Router();

router.get("/", fetchBillCategories);
router.post("/", addBillCategory);
router.get("/:id", fetchBillCategoryById);
router.put("/:id", editBillCategory);
router.delete("/:id", removeBillCategory);

export default router;