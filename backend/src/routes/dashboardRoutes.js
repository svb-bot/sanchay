import { Router } from "express"
import { fetchSpendingSummary, fetchIncomeSummary } from "../controllers/dashboardController.js"

const router = Router()

router.get("/spending-summary", fetchSpendingSummary)
router.get("/income-summary", fetchIncomeSummary)

export default router
