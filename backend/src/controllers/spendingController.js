import {
    createSpending,
    getAllSpending
} from "../models/spendingModel.js";

export async function addSpending(req, res) {
    try {
        const result = await createSpending(req.body);

        res.status(201).json({
            success: true,
            payment_id: result.insertId
        });
    } catch (error) {
        console.error(error);

        res.status(500).json({
            success: false,
            message: error.message
        });
    }
}

export async function fetchSpending(req, res) {
    try {
        const rows = await getAllSpending();

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