import { getIncomeSummary } from "../models/incomeModel.js";
import { getSpendingSummary } from "../models/spendingModel.js";

export async function fetchSpendingSummary(req, res) {
    try {
        const rows = await getSpendingSummary(res.body);
        res.json({
            success: true,
            data: rows
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}

export async function fetchIncomeSummary(req, res) {
    try {
        const rows = await getIncomeSummary(res.body);
        res.json({
            success: true,
            data: rows
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}
