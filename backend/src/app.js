import express from "express"
import cors from "cors"
import incomeRoutes from "./routes/incomeRoutes.js"
import spendingRoutes from "./routes/spendingRoutes.js"
import paymentCategoryRoutes from "./routes/paymentCategoryRoutes.js"
import paymentModeRoutes from "./routes/paymentModeRoutes.js"
import billCategoryRoutes from "./routes/billCategoryRoutes.js"
import billPaymentModeRoutes from "./routes/billPaymentModeRoutes.js"
import dashboardRoutes from "./routes/dashboardRoutes.js"

const app = express()

app.use(cors())
app.use(express.json())

app.use("/api/income", incomeRoutes)
app.use("/api/spending", spendingRoutes)
app.use("/api/payment-category", paymentCategoryRoutes)
app.use("/api/payment-mode", paymentModeRoutes)
app.use("/api/bill-category", billCategoryRoutes)
app.use("/api/bill-payment-mode", billPaymentModeRoutes)
app.use("/api/dashboard", dashboardRoutes)
app.get("/api/health", (req, res) => {
    res.json({ status: "ok" })
})
app.get("/api/routes", (req, res) => {
    const routes = [
        "/api/income",
        "/api/spending",
        "/api/payment-category",
        "/api/payment-mode",
        "/api/bill-category",
        "/api/bill-payment-mode"
    ]
    res.json(routes)
})

export default app;